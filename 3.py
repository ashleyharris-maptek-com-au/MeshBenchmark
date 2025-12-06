title = "CSG Union of Rectangular Prism and Cube"

prompt = """

You can output polyhedrons in a json format. This is a simple cube, every face has 4 vertices, and there are 6 faces:

{
"polyhedron":
  {
    "vertex":[{"xyz":[-1.0,-1.0,-1.0]},{"xyz":[1.0,-1.0,-1.0]},{"xyz":[1.0,1.0,-1.0]},{"xyz":[-1.0,1.0,-1.0]},{"xyz":[-1.0,-1.0,1.0]},{"xyz":[1.0,-1.0,1.0]},{"xyz":[1.0,1.0,1.0]},{"xyz":[-1.0,1.0,1.0]}],
    "faces":[{"vertex":[3,2,1,0]},{"vertex":[4,5,6,7]},{"vertex":[0,1,5,4]},{"vertex":[7,6,2,3]},{"vertex":[3,0,4,7]},{"vertex":[1,2,6,5]}}]
  }
}

Now you've learnt the format, use it to solve the following problem:

You are given a solid rectangular prism of size 10cm * 20cm * 30cm, translated such that it's centre of mass is at PARAMcm, 5cm, 5cm.

You are also given a solid cube with single side dimension 15cm, translated such that it's centre of mass is at -PARAMcm, -5cm, -5cm.

Return a polyhedron that is the union of the two solid objects. 
- Ensure faces have normals encoded in a consistent direction.
- Ensure no geometry occurs inside the polyhedron, and no faces cross through it.
- Note that some faces may have more than 4 vertices.
- Your output should have no degenerate faces or redundant vertices. 
- The task is a failure if the output is not watertight.
"""

structure = {
  "type": "object",
  "properties": {
    "polyhedron": {
      "type": "object",
      "properties": {
        "vertex": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "xyz": {
                "type": "array",
                "items": {
                  "type": "number"
                }
              }
            },
            "propertyOrdering": [
              "xyz"
            ],
            "additionalProperties": False,
            "required": [
              "xyz"
            ]
          }
        },
        "faces": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "vertex": {
                "type": "array",
                "items": {
                  "type": "integer"
                }
              }
            },
            "propertyOrdering": [
              "vertex"
            ],
            "additionalProperties": False,
            "required": [
              "vertex"
            ]
          }
        }
      },
      "propertyOrdering": [
        "vertex",
        "faces"
      ],
      "additionalProperties": False,
      "required": [
        "vertex",
        "faces"
      ]
    }
  },
  "propertyOrdering": [
    "polyhedron"
  ],
  "additionalProperties": False,
  "required": [
    "polyhedron"
  ]
}

referenceScad = """
module reference()
{
    translate([PARAM,5,5]) cube([10,20,30], center=true);
    translate([-PARAM,-5,-5]) cube([15,15,15], center=true);
}
"""

promptChangeSummary = "Cube and rectangle move further apart in x."

subpassParamSummary = [
  "10cm apart in X ", 
  "20cm apart in X ",
  "30cm apart in X ",
  "5cm apart in X "]

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM", "5")
    if index == 1: return prompt.replace("PARAM", "10")
    if index == 2: return prompt.replace("PARAM", "15")
    if index == 3: return prompt.replace("PARAM", "2.5")
    raise StopIteration

def prepareSubpassReferenceScad(index):
    if index == 0: return referenceScad.replace("PARAM", "5")
    if index == 1: return referenceScad.replace("PARAM", "10")
    if index == 2: return referenceScad.replace("PARAM", "15")
    if index == 3: return referenceScad.replace("PARAM", "2.5")
    raise StopIteration

def resultToScad(result):
    scad = """
polyhedron(
      points=[
"""
    for vertex in result["polyhedron"]["vertex"]:
        scad += "    [" + str(vertex["xyz"][0]) + "," + str(vertex["xyz"][1]) + "," + str(vertex["xyz"][2]) + "],\n"
    scad += "    ],\n"
    scad += "    faces=[\n"
    for face in result["polyhedron"]["faces"]:
        scad += "    [" + ",".join(map(str, face["vertex"])) + "],\n"
    scad += "    ]\n"
    scad += ");\n"
    return "module result(){ " + scad + " }"

