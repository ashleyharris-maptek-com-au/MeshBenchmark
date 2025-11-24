prompt = """
You are given 5 rigid lengths of pipe, each 5 meters long and 10cm in diameter. 

One pipe is fixed with it's center at the origin (0,0) and a rotation of 0, meaning it's length is along the x-axis, and it
spans from -2.5,-0.05 to 2.5, 0.05.

Arrange the remaining 4 pipes on a 2D plane such that the the pipes resemble a "H" shape when viewed from above.

Return a 5 element array of where each of the pipes are located:
"""

structure = {
  "type": "object",
  "properties": {
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
        ]
      }
    }
  },
  "propertyOrdering": [
    "pipes"
  ]
}

referenceScad = """
module reference()
{
  cube([5,0.1,.1], center=true);
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

gemini3Answer = [{
        "pipes": [
            {
                "xCentre":0,
                "yCentre": 0,
                "rotationDegrees": 0
            },
            {
                "xCentre": -2.55,
                "yCentre": 2.5,
                "rotationDegrees": 90
            },
            {
                "xCentre": 2.55,
                "yCentre": 2.5,
                "rotationDegrees": 90
            },
            {
                "xCentre": -2.55,
                "yCentre": -2.5,
                "rotationDegrees": 90
            },
            {
                "xCentre": 2.55,
                "yCentre": -2.5,
                "rotationDegrees": 90
            }
        ]
    }]