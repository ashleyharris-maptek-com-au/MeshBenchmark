prompt = """
You have a SIZE*SIZE grid of unit squares, with cell coordinates (x, y) where 1 ≤ x ≤ SIZE, 1 ≤ y ≤ SIZE.

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
        ]
      }
    }
  },
  "propertyOrdering": [
    "steps"
  ]
}


def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("SIZE", "4").replace("SQUARED", "16").replace("TWIST", "")
    if index == 1: return prompt.replace("SIZE", "8").replace("SQUARED", "64").replace("TWIST", "")
    if index == 2: return prompt.replace("SIZE", "12").replace("SQUARED", "144").replace("TWIST", "")
    if index == 3: return prompt.replace("SIZE", "16").replace("SQUARED", "256").replace("TWIST", "")
    if index == 4: return prompt.replace("SIZE", "16").replace("SQUARED", "254").replace("TWIST", 
        "Cells 3,3 and 3,4 have been removed from the grid and must be skipped.")


    raise StopIteration


def gradeAnswer(answer : dict, subPass : int):
    if subPass == 0 and len(answer["steps"]) != 16:
        return 0
    if subPass == 1 and len(answer["steps"]) != 64:
        return 0
    if subPass == 2 and len(answer["steps"]) != 144:
        return 0
    if subPass == 3 and len(answer["steps"]) != 256:
        return 0
    if subPass == 4 and len(answer["steps"]) != 254:
        return 0

    size = 4 if subPass == 0 else 8 if subPass == 1 else 12 if subPass == 2 else 16

    # since the path is supposed to be a loop, we start at the end to check that the start
    # and end are adjacent.
    location = answer["steps"][-1]["xy"]

    visited = set()

    for step in answer["steps"]:

        if step["xy"][0] <= 0 or step["xy"][0] > size or step["xy"][1] <= 0 or step["xy"][1] > size:
            print("Out of bounds!")
            return 0
        
        if subPass == 4 and (step["xy"][0] == 3 and step["xy"][1] == 3 or step["xy"][0] == 3 and step["xy"][1] == 4):
            print("You forgot to skip cell 3,3 or 3,4!")
            return 0

        # check that the step is side-adjacent to the previous step
        xDiff = abs(step["xy"][0] - location[0])
        yDiff = abs(step["xy"][1] - location[1])
        if xDiff + yDiff != 1:
            print("didn't step side-adjacent" + str(step["xy"]) + " from " + str(location))
            return 0
        location = step["xy"]
        if location in visited:
            print("visited " + str(location) + " more than once!")
            return 0
        visited.add(location)

    return 1

