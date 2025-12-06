import itertools
import VolumeComparison as vc

title="Hamiltonian Path on Grid"

prompt = """
You have a SIZE*SIZE grid of unit squares, with cell coordinates (x, y) where 1 <= x <= SIZE, 1 <= y <= SIZE.

TWIST

Draw a single closed path that:
- Moves from cell to cell using only side-adjacent moves.
- Visits every cell exactly once.
- Returns to its starting cell (so the path is a loop).
- The last cell in your list must be side-adjacent to the first.

Answer format:
Give an ordered list of the SQUARED cell coordinates for the loop, starting anywhere, for example:

1,1
1,2
1,3
...
2,1
"""

structure = {
  "type": "object",
  "properties": {
    "steps": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "xy": {
            "type": "array",
            "items": {
              "type": "number"
            }
          }
        },
        "propertyOrdering": [
          "xy"
        ],
        "additionalProperties": False,
        "required": [
          "xy"
        ]
      }
    }
  },
  "propertyOrdering": [
    "steps"
  ],
  "additionalProperties": False,
  "required": [
    "steps"
  ]
}

subpassParamSummary = ["4x4 grid", "8x8 grid", "12x12 grid", "16x16 grid", "16x16 grid with cells (3,3) and (3,4) removed", "16x16 grid with no odd numbered cells"]
promptChangeSummary = "Grid size increases across subpasses, with a missing chunk in the final subpass"


def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("SIZE", "4").replace("SQUARED", "16").replace("TWIST", "")
    if index == 1: return prompt.replace("SIZE", "8").replace("SQUARED", "64").replace("TWIST", "")
    if index == 2: return prompt.replace("SIZE", "12").replace("SQUARED", "144").replace("TWIST", "")
    if index == 3: return prompt.replace("SIZE", "16").replace("SQUARED", "256").replace("TWIST", "")
    if index == 4: return prompt.replace("SIZE", "16").replace("SQUARED", "254").replace("TWIST", 
        "Cells 3,3 and 3,4 have been removed from the grid and must be skipped.")
    if index == 5: return prompt.replace("SIZE", "16").replace("SQUARED", "256").replace("TWIST", 
        "No cells with both coordinates being odd can be visited.")
    raise StopIteration


def gradeAnswer(answer : dict, subPass : int, aiEngineName : str):
    expected_steps = [16, 64, 144, 256, 254, 256 - 64]
    if subPass < len(expected_steps) and len(answer["steps"]) != expected_steps[subPass]:
        return 0, f"Expected {expected_steps[subPass]} steps, got {len(answer['steps'])}"

    size = 4 if subPass == 0 else 8 if subPass == 1 else 12 if subPass == 2 else 16

    # since the path is supposed to be a loop, we start at the end to check that the start
    # and end are adjacent.
    location = answer["steps"][-1]["xy"]

    visited = set()

    for step in answer["steps"]:

        if step["xy"][0] <= 0 or step["xy"][0] > size or step["xy"][1] <= 0 or step["xy"][1] > size:
            return 0, "Out of bounds!"
        
        if subPass == 4 and (step["xy"][0] == 3 and step["xy"][1] == 3 or step["xy"][0] == 3 and step["xy"][1] == 4):
            return 0, "You forgot to skip cell 3,3 or 3,4!"

        if subPass == 5 and (step["xy"][0] % 2 == 1 and step["xy"][1] % 2 == 1):
            return 0, f"You visited an odd numbered cell {step['xy']}!"

        # check that the step is side-adjacent to the previous step
        xDiff = abs(step["xy"][0] - location[0])
        yDiff = abs(step["xy"][1] - location[1])
        if xDiff + yDiff != 1:
            return 0, f"didn't step side-adjacent {step['xy']} from {location}"
        location = tuple(step["xy"])
        if location in visited:
            return 0, f"visited {location} more than once!"
        visited.add(location)

    return 1, f"Valid Hamiltonian path with {len(answer['steps'])} steps"

def resultToNiceReport(answer, subPass, aiEngineName):
    scadOutput = ""
    for a,b in itertools.pairwise(answer["steps"]):
        xMid = (a['xy'][0] + b['xy'][0])/2
        yMid = (a['xy'][1] + b['xy'][1])/2

        scadOutput += f"""
hull() {{
    translate([{a['xy'][0]* 0.9 + xMid*0.1}, {a['xy'][1]* 0.9 + yMid*0.1}, 0]) cube([0.01, 0.01, 0.01], center=true);
    translate([{b['xy'][0]* 0.9 + xMid*0.1}, {b['xy'][1]* 0.9 + yMid*0.1}, 0]) cube([0.01, 0.01, 0.01], center=true);
}}

"""

    for i,a in enumerate(answer["steps"]):
        scadOutput += f"""
translate([{a['xy'][0]}, {a['xy'][1]}, 0]) linear_extrude(0.01) text("{i}",size=0.15, halign="center", valign="center");
"""

    import os
    os.makedirs("results", exist_ok=True)
    output_path = "results/9_Visualization_" + aiEngineName + "_" + str(len(answer["steps"])) + ".png"
    vc.render_scadText_to_png(scadOutput, output_path)
    print(f"Saved visualization to {output_path}")

    return f'<img src="{os.path.basename(output_path)}" alt="Hamiltonian Path Visualization" style="max-width: 100%;">'