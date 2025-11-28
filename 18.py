title = "Pyamid construction - more bricks than token limits"

prompt = """
A pharoh is building a pyramyd to rest on top of his tomb and protect him for the afterlife. 
He has an army of 100,000 men who are honour bound to assist him in the project.

Pyramids must face north, which is +y, and is centred over the future tomb.

Pharoh has PARAM_A cut large stones, each a 50cm side-length cube.
Each stone needs 10 men to move.

When placed on top of other stones, each stone must have all 4 base
corners sitting in the middle of another stone. Any other arrangements will result in collapse. 
The pyramid does not have any internal voids for this reason.

The final facade will be done with wedges of marble, and the local stonemason requires precise plans to cut 
marble such that each external large stone is covered and the resulting pyamid is smooth.

Generate an OpenSCAD plan showing the tallest pyramid the pharoh can build with his budget
of stone. This plan must be precisely detailed enough for a stonemason to prepare the thousands of 
wedges of marble for the facade.
"""

def prepareSubpassPrompt(index):
  if index == 0: return prompt.replace("PARAM_A", "20,000")
  if index == 1: return prompt.replace("PARAM_A", "150,000")
  if index == 2: return prompt.replace("PARAM_A", "600,000")
  if index == 3: return prompt.replace("PARAM_A", "2,500,000")
  raise StopIteration

structure = None

promptChangeSummary = """
Hundreds of thousands of stones, then millions. 
The AI needs to merge adjacent stones and work with merged
layers in order to solve this.
"""

subpassParamSummary = [
  "20,000 stones (~20m high)",
  "150,000 stones (~39m high)",
  "600,000 stones",
  "2,500,000 stones (~100m high / ~200 layers)"
]

referenceScad = ""

def prepareSubpassReferenceScad(index):
  stoneCount = 20000 if index == 0 else 150000 if index == 1 else 600000 if index == 2 else 2500000
  scad = ""
  level = 0
  while True:
    level += 1
    stones = level * level
    if stones < stoneCount:
        scad += f"translate([0,0,-{level * 0.5}])  cube([{level},{level}, 0.5], center=true);\n"
        stoneCount -= stones
    else: break

  scad = f"translate([0,0,{level * 0.5}])" + "{\n" + scad + "}\n"

  return "module reference()\n{\n" + scad + "\n}\n"


def resultToScad(result):
  if "```" in result:
    result = result.split("```")[1]
    result = result.partition("\n")[2] # Drop the first line as it might be "```openscad"

  return "module result(){ union(){" + result + "}}"
