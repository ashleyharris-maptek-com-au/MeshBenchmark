title = "Build a Lego(tm) hemispherical shell"

prompt = """
You have an unlimited number of lego(tm) bricks, each of individual size 31.8mm * 15.8mm * 11.4mm but when assembled they are 
32mm * 16mm * 9.6mm due to interlocking studs and voids.

Assemble the bricks such that they resemble a 3D hemispherical shell, with inner radius PARAM_Acm and outer radius PARAM_Bcm, 
the centre of the hemisphere is at the origin (0,0,0).

Since it's impossible to create a perfect curve, the best score is one which is closer to the ideal curve, with
scoring being calculated based on the volume difference between the ideal curve and the actual brick structure. 
The structure needs to be buildable in 3D, so bricks can not overlap or be floating in mid air. A great answer does not 
contain any holes or missing bricks.

Return a list of the bricks (location in xyz mm relative to the origin and rotation in degrees). 
You may also provide your reasoning in a seperate field, but it is not graded.
"""

structure = {
  "type": "object",
  "properties": {
    "reasoning": {
      "type": "string"
    },
    "bricks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Centroid": {
            "type": "array",
            "items": {
              "type": "number"
            }
          },
          "RotationDegrees": {
            "type": "number"
          }
        },
        "propertyOrdering": [
          "Centroid",
          "RotationDegrees"
        ],
        "required": [
          "Centroid",
          "RotationDegrees"
        ],
        "additionalProperties": False
      }
    }
  },
  "propertyOrdering": [
    "reasoning",
    "bricks"
  ],
  "required": [
    "reasoning",
    "bricks"
  ],
  "additionalProperties": False
}

referenceScad = """
$fn=30;

module reference()
{
    difference()
    {
        sphere(PARAM_B * 10);
        sphere(PARAM_A * 10);
        translate([0,0,-500]) cube([1000,1000,1000], center=true);
    }
}
"""

promptChangeSummary = "Inner and outer radius parameters increase progressively across subpasses"

subpassParamSummary = [
  "4cm inner, 7cm outer. ~120 bricks", 
  "8cm inner, 11cm outer. ~300 bricks", 
  "15cm inner, 17cm outer ~400 bricks"]

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "4").replace("PARAM_B", "7")
    if index == 1: return prompt.replace("PARAM_A", "8").replace("PARAM_B", "11")
    if index == 2: return prompt.replace("PARAM_A", "15").replace("PARAM_B", "17")
    raise StopIteration


def prepareSubpassReferenceScad(index):
    if index == 0: return referenceScad.replace("PARAM_A", "4").replace("PARAM_B", "7")
    if index == 1: return referenceScad.replace("PARAM_A", "8").replace("PARAM_B", "11")
    if index == 2: return referenceScad.replace("PARAM_A", "15").replace("PARAM_B", "17")
    raise StopIteration

def resultToScad(result):
  scad = "union() {"
  for brick in result["bricks"]:
    scad += "translate([" + str(brick["Centroid"][0]) + "," + \
      str(brick["Centroid"][1]) + "," + str(brick["Centroid"][2]) + "]) rotate([0,0," + \
      str(brick["RotationDegrees"]) + "]) cube([32,16,9.6], center=true);\n"

  return "module result(){ " + scad + "}}\n\n"

def volumeValidateDelta(result, resultVolume, referenceVolume, intersectionVolume, differenceVolume):
    brickCount = len(result["bricks"])
    expectedBrickCount = referenceVolume / 9.6 / 16 / 32

    delta = abs(brickCount - expectedBrickCount)
    
    if delta < 2:
        return 0.0
    
    print("50% penalty due to bricks overlapping: " + str(delta))
    print("Structure has " + str(brickCount) + \
        " bricks, but the union of the bricks created a volume of " + str(resultVolume) + " mm^3," +\
             " the expected volume is " + str(expectedBrickCount * 9.6 * 16 * 32))
    return -0.5


def postProcessScore(score):
  # Packing efficincy of rectangle prism in sphere is about 75%. I couldn't find an exact figure
  # but it's close enough for this test.
  return min(1,score / 0.75)