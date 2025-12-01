import math

title = "Tetrahedron Shadow Coverage"

prompt = """
Here is the points and faces of a regular tetrahedron with all sides equal 1, resting on the Z=0 plane and with an edge along the X=0 plane:

polyhedron(
    points = [
        [0, 0, 0],                               // 0
        [1, 0, 0],                               // 1
        [0.5, sqrt(3)/2, 0],                     // 2
        [0.5, sqrt(3)/6, sqrt(2/3)]              // 3 (apex)
    ],
    faces = [
        [0, 2, 1],   // base (oriented outward)
        [0, 1, 3],
        [1, 2, 3],
        [2, 0, 3]
    ],
    convexity = 4
);

We define a 7-part rigid transform of (x,y,z,q0,q1,q2,q3), where q0,q1,q2,q3 is a normalised quaternion, and x, y, z are the translation.
Rotation is defined around the 0,0,0 point (Which is NOT THE CENTRE), and is performed before translation.

We create a scene with mulitple tetrahedra, each with a different transform. Return the transforms of such a scene
such that a shadow projected vertically (onto the Z=0 plane) fully covers PARAM, centered at the origin.

Score will be deducted for any shadow outside of the square, for reduntant tetrahedra, or non-normalised quaternions.
"""

structure = {
    "type": "object",
    "properties": {
      "tetrahedrons": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "x": {
              "type": "number"
            },
            "y": {
              "type": "number"
            },
            "z": {
              "type": "number"
            },
            "q0": {
              "type": "number"
            },
            "q1": {
              "type": "number"
            },
            "q2": {
              "type": "number"
            },
            "q3": {
              "type": "number"
            }
          },
          "required": [
            "x",
            "y",
            "z",
            "q0",
            "q1",
            "q2",
            "q3"
          ],
          "additionalProperties": False
        }
      }
    },
    "required": [
      "tetrahedrons"
    ],
    "additionalProperties": False
}

subpassParamSummary = [
    "Cover a square of side length 4. \n\n(Note that the shadow has been linearly extruded to a height of 1 to simplify volume comparison)",
    "Cover a circle of diameter 4",
    "Cover a square of side length 6, with a hole in the centre of side length 2"
]

def prepareSubpassPrompt(index: int) -> str:
    if index == 0: return prompt.replace("PARAM", "a square of side length 4")
    if index == 1: return prompt.replace("PARAM", "a circle of diameter 4")
    if index == 2: return prompt.replace("PARAM", "a square of side length 6, with a hole in the centre of side length 2")
    raise StopIteration

referenceScad = """
module reference(){
    translate([0,0,0.5]) cube([4,4,1], center=true);
}
"""

def prepareSubpassReferenceScad(index: int) -> str:
    if index == 0: return """
module reference(){
    translate([0,0,0.5]) cube([4,4,1], center=true);
}
"""
    if index == 1: return """
module reference(){
    translate([0,0,0.5]) cylinder(r=2, h=1, center=true, $fn=100);
}
"""
    if index == 2: return """
module reference(){
  difference() {
    translate([0,0,0.5]) cube([6,6,1], center=true);
    translate([0,0,0.5]) cube([2,2,2], center=true);
  }
}
"""

def quaternionToPitchRollYawInDegrees(q0, q1, q2, q3):
    return [math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2))), 
            math.degrees(math.asin(2 * (q0 * q2 - q1 * q3))), 
            math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))]

scadModules = """
module tetrahedron(){
    polyhedron(
        points = [
            [0, 0, 0],                               // 0
            [1, 0, 0],                               // 1
            [0.5, sqrt(3)/2, 0],                     // 2
            [0.5, sqrt(3)/6, sqrt(2/3)]              // 3 (apex)
        ],
        faces = [
            [0, 2, 1],   // base (oriented outward)
            [0, 1, 3],
            [1, 2, 3],
            [2, 0, 3]
        ],
        convexity = 4
    );
  
}
"""

def resultToScad(result):
    scad = "module result(){ " 
    scad += "linear_extrude(height=1){ projection() { minkowski(){cube(0.001); union() { "
    for transform in result["tetrahedrons"]:
        scad += "translate([" + str(transform["x"]) + "," + \
            str(transform["y"]) + "," + str(transform["z"]) + "]) rotate(" + \
            str(quaternionToPitchRollYawInDegrees(transform["q0"], transform["q1"], transform["q2"], transform["q3"])) + ") tetrahedron();\n"
    return scad + "}}}}}\n\n"
