title = "Lay out pipe to make a H shape."

prompt = """
You are given 5 rigid lengths of pipe, each 5 meters long and 10cm in diameter. 

One pipe is fixed with its center at the origin (0,0) and a rotation of 0, meaning its length is along the x-axis, and it
spans from -2.5,-0.05 to 2.5, 0.05.

Arrange the remaining 4 pipes on a 2D plane such that the the pipes resemble a "H" shape 10m high when viewed from above.

Pipes can not intersect each other, and should only touch at their ends.

Return a 5 element array of where each of the pipes are located:
"""

structure = {
  "type": "object",
  "properties": {
    "reasoning": {
      "type": "string"
    },
    "pipes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "xCentre": {
            "type": "number"
          },
          "yCentre": {
            "type": "number"
          },
          "rotationDegrees": {
            "type": "number"
          }
        },
        "propertyOrdering": [
          "xCentre",
          "yCentre",
          "rotationDegrees"
        ],
        "required": [
          "xCentre",
          "yCentre",
          "rotationDegrees"
        ],
        "additionalProperties": False,
      }
    }
  },
  "propertyOrdering": [
    "reasoning",
    "pipes"
  ],
  "required": [
    "reasoning",
    "pipes"
  ],
  "additionalProperties": False,
}

referenceScad = """
module reference()
{
  color("red") cube([5,0.1,.1], center=true);
  translate([2.55,0,0]) cube([0.1,10,.1], center=true);
  translate([-2.55,0,0]) cube([0.1,10,.1], center=true);
}
"""

def resultToScad(result):
  scad = "module result(){ union(){"
  for pipe in result["pipes"]:
    scad += "translate([" + str(pipe["xCentre"]) + "," + \
      str(pipe["yCentre"]) + "]) rotate([0,0," + \
      str(pipe["rotationDegrees"]) + "]) cube([5,0.1,.1], center=true);\n"

  return scad + "}}"

subpassParamSummary =[ 
  "Note that we're defining pipes by their centroid. " +
  " And a 5m long pipe at the origin TOUCHES x = +/- 2.5m, so a 10cm wide pipe perpindicular to it needs an additional 5cm of space."]
