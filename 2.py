prompt = """
You have an unlimited number of lego(tm) bricks, each of individual size 31.8mm * 15.8mm * 11.4mm but when assembled they are 
32mm * 16mm * 9.6mm due to interlocking studs and voids.

Assemble the bricks such that they resemble a 3D hemispherical shell, with inner radius PARAM_Acm and outer radius PARAM_Bcm, 
the centre of the hemisphere is at the origin (0,0,0).

Since it's impossible to create a perfect curve, a better result is one which is closer to the ideal curve, with
scoring being calculated based on the volume difference between the ideal curve and the actual brick structure. 
The structure needs to be buildable in 3D, so bricks can not overlap or be floating in mid air.

Return a list of the bricks (location in xyz/mm relative to the origin and rotation in degrees).
"""

structure = {
  "type": "object",
  "properties": {
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
        ]
      }
    }
  },
  "propertyOrdering": [
    "bricks"
  ]
}

referenceScad = """
$fn=100;

module reference()
{
    difference()
    {
        sphere(PARAM_Bcm);
        sphere(PARAM_Acm);
        translate([0,0,-500]) cube([1000,1000,1000], center=true);
    }
}
"""

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "4").replace("PARAM_B", "7")
    if index == 1: return prompt.replace("PARAM_A", "8").replace("PARAM_B", "12")
    if index == 2: return prompt.replace("PARAM_A", "15").replace("PARAM_B", "17")
    raise StopIteration


def prepareSubpassReferenceScad(index):
    if index == 0: return referenceScad.replace("PARAM_A", "4").replace("PARAM_B", "7")
    if index == 1: return referenceScad.replace("PARAM_A", "8").replace("PARAM_B", "12")
    if index == 2: return referenceScad.replace("PARAM_A", "15").replace("PARAM_B", "17")
    raise StopIteration

def resultToScad(result):
  scad = "union() {"
  for brick in result["bricks"]:
    scad += "translate([" + str(brick["Centroid"][0]) + "," + \
      str(brick["Centroid"][1]) + "," + str(brick["Centroid"][2]) + "]) rotate([0,0," + \
      str(brick["RotationDegrees"]) + "]) cube([32,16,9.6], center=true);\n"

  return "module result(){ " + scad + " }"

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

gemini3Answer = [
    {},
    {
        "bricks": [
            { "Centroid": [ 96, 0, 4.8 ], "RotationDegrees": 0 },
    { "Centroid": [ -96, 0, 4.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 0, 96, 4.8 ], "RotationDegrees": 90 },
    { "Centroid": [ 0, -96, 4.8 ], "RotationDegrees": 90 },
    { "Centroid": [ 64, 64, 4.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 64, -64, 4.8 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, 64, 4.8 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, -64, 4.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 80, 32, 4.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 80, -32, 4.8 ], "RotationDegrees": 0 },
    { "Centroid": [ -80, 32, 4.8 ], "RotationDegrees": 0 },
    { "Centroid": [ -80, -32, 4.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 32, 80, 4.8 ], "RotationDegrees": 90 },
    { "Centroid": [ 32, -80, 4.8 ], "RotationDegrees": 90 },
    { "Centroid": [ -32, 80, 4.8 ], "RotationDegrees": 90 },
    { "Centroid": [ -32, -80, 4.8 ], "RotationDegrees": 90 },
    { "Centroid": [ 96, 16, 14.4 ], "RotationDegrees": 0 },
    { "Centroid": [ -96, 16, 14.4 ], "RotationDegrees": 0 },
    { "Centroid": [ 96, -16, 14.4 ], "RotationDegrees": 0 },
    { "Centroid": [ -96, -16, 14.4 ], "RotationDegrees": 0 },
    { "Centroid": [ 16, 96, 14.4 ], "RotationDegrees": 90 },
    { "Centroid": [ 16, -96, 14.4 ], "RotationDegrees": 90 },
    { "Centroid": [ -16, 96, 14.4 ], "RotationDegrees": 90 },
    { "Centroid": [ -16, -96, 14.4 ], "RotationDegrees": 90 },
    { "Centroid": [ 64, 48, 14.4 ], "RotationDegrees": 0 },
    { "Centroid": [ 64, -48, 14.4 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, 48, 14.4 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, -48, 14.4 ], "RotationDegrees": 0 },
    { "Centroid": [ 48, 64, 14.4 ], "RotationDegrees": 90 },
    { "Centroid": [ 48, -64, 14.4 ], "RotationDegrees": 90 },
    { "Centroid": [ -48, 64, 14.4 ], "RotationDegrees": 90 },
    { "Centroid": [ -48, -64, 14.4 ], "RotationDegrees": 90 },
    { "Centroid": [ 96, 0, 24.0 ], "RotationDegrees": 0 },
    { "Centroid": [ -96, 0, 24.0 ], "RotationDegrees": 0 },
    { "Centroid": [ 0, 96, 24.0 ], "RotationDegrees": 90 },
    { "Centroid": [ 0, -96, 24.0 ], "RotationDegrees": 90 },
    { "Centroid": [ 80, 48, 24.0 ], "RotationDegrees": 0 },
    { "Centroid": [ 80, -48, 24.0 ], "RotationDegrees": 0 },
    { "Centroid": [ -80, 48, 24.0 ], "RotationDegrees": 0 },
    { "Centroid": [ -80, -48, 24.0 ], "RotationDegrees": 0 },
    { "Centroid": [ 48, 80, 24.0 ], "RotationDegrees": 90 },
    { "Centroid": [ 48, -80, 24.0 ], "RotationDegrees": 90 },
    { "Centroid": [ -48, 80, 24.0 ], "RotationDegrees": 90 },
    { "Centroid": [ -48, -80, 24.0 ], "RotationDegrees": 90 },
    { "Centroid": [ 88, 24, 33.6 ], "RotationDegrees": 0 },
    { "Centroid": [ -88, 24, 33.6 ], "RotationDegrees": 0 },
    { "Centroid": [ 88, -24, 33.6 ], "RotationDegrees": 0 },
    { "Centroid": [ -88, -24, 33.6 ], "RotationDegrees": 0 },
    { "Centroid": [ 24, 88, 33.6 ], "RotationDegrees": 90 },
    { "Centroid": [ 24, -88, 33.6 ], "RotationDegrees": 90 },
    { "Centroid": [ -24, 88, 33.6 ], "RotationDegrees": 90 },
    { "Centroid": [ -24, -88, 33.6 ], "RotationDegrees": 90 },
    { "Centroid": [ 64, 64, 33.6 ], "RotationDegrees": 0 },
    { "Centroid": [ 64, -64, 33.6 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, 64, 33.6 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, -64, 33.6 ], "RotationDegrees": 0 },
    { "Centroid": [ 80, 0, 43.2 ], "RotationDegrees": 0 },
    { "Centroid": [ -80, 0, 43.2 ], "RotationDegrees": 0 },
    { "Centroid": [ 0, 80, 43.2 ], "RotationDegrees": 90 },
    { "Centroid": [ 0, -80, 43.2 ], "RotationDegrees": 90 },
    { "Centroid": [ 64, 48, 43.2 ], "RotationDegrees": 0 },
    { "Centroid": [ 64, -48, 43.2 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, 48, 43.2 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, -48, 43.2 ], "RotationDegrees": 0 },
    { "Centroid": [ 48, 64, 43.2 ], "RotationDegrees": 90 },
    { "Centroid": [ 48, -64, 43.2 ], "RotationDegrees": 90 },
    { "Centroid": [ -48, 64, 43.2 ], "RotationDegrees": 90 },
    { "Centroid": [ -48, -64, 43.2 ], "RotationDegrees": 90 },
    { "Centroid": [ 88, 16, 52.8 ], "RotationDegrees": 0 },
    { "Centroid": [ -88, 16, 52.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 88, -16, 52.8 ], "RotationDegrees": 0 },
    { "Centroid": [ -88, -16, 52.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 16, 88, 52.8 ], "RotationDegrees": 90 },
    { "Centroid": [ 16, -88, 52.8 ], "RotationDegrees": 90 },
    { "Centroid": [ -16, 88, 52.8 ], "RotationDegrees": 90 },
    { "Centroid": [ -16, -88, 52.8 ], "RotationDegrees": 90 },
    { "Centroid": [ 56, 56, 52.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 56, -56, 52.8 ], "RotationDegrees": 0 },
    { "Centroid": [ -56, 56, 52.8 ], "RotationDegrees": 0 },
    { "Centroid": [ -56, -56, 52.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 80, 32, 62.4 ], "RotationDegrees": 0 },
    { "Centroid": [ 80, -32, 62.4 ], "RotationDegrees": 0 },
    { "Centroid": [ -80, 32, 62.4 ], "RotationDegrees": 0 },
    { "Centroid": [ -80, -32, 62.4 ], "RotationDegrees": 0 },
    { "Centroid": [ 32, 80, 62.4 ], "RotationDegrees": 90 },
    { "Centroid": [ 32, -80, 62.4 ], "RotationDegrees": 90 },
    { "Centroid": [ -32, 80, 62.4 ], "RotationDegrees": 90 },
    { "Centroid": [ -32, -80, 62.4 ], "RotationDegrees": 90 },
    { "Centroid": [ 64, 0, 62.4 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, 0, 62.4 ], "RotationDegrees": 0 },
    { "Centroid": [ 0, 64, 62.4 ], "RotationDegrees": 90 },
    { "Centroid": [ 0, -64, 62.4 ], "RotationDegrees": 90 },
    { "Centroid": [ 64, 32, 72.0 ], "RotationDegrees": 0 },
    { "Centroid": [ 64, -32, 72.0 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, 32, 72.0 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, -32, 72.0 ], "RotationDegrees": 0 },
    { "Centroid": [ 32, 64, 72.0 ], "RotationDegrees": 90 },
    { "Centroid": [ 32, -64, 72.0 ], "RotationDegrees": 90 },
    { "Centroid": [ -32, 64, 72.0 ], "RotationDegrees": 90 },
    { "Centroid": [ -32, -64, 72.0 ], "RotationDegrees": 90 },
    { "Centroid": [ 80, 0, 72.0 ], "RotationDegrees": 0 },
    { "Centroid": [ -80, 0, 72.0 ], "RotationDegrees": 0 },
    { "Centroid": [ 0, 80, 72.0 ], "RotationDegrees": 90 },
    { "Centroid": [ 0, -80, 72.0 ], "RotationDegrees": 90 },
    { "Centroid": [ 0, 0, 81.6 ], "RotationDegrees": 0 },
    { "Centroid": [ 32, 0, 81.6 ], "RotationDegrees": 0 },
    { "Centroid": [ -32, 0, 81.6 ], "RotationDegrees": 0 },
    { "Centroid": [ 0, 32, 81.6 ], "RotationDegrees": 90 },
    { "Centroid": [ 0, -32, 81.6 ], "RotationDegrees": 90 },
    { "Centroid": [ 48, 48, 81.6 ], "RotationDegrees": 0 },
    { "Centroid": [ 48, -48, 81.6 ], "RotationDegrees": 0 },
    { "Centroid": [ -48, 48, 81.6 ], "RotationDegrees": 0 },
    { "Centroid": [ -48, -48, 81.6 ], "RotationDegrees": 0 },
    { "Centroid": [ 64, 16, 81.6 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, 16, 81.6 ], "RotationDegrees": 0 },
    { "Centroid": [ 64, -16, 81.6 ], "RotationDegrees": 0 },
    { "Centroid": [ -64, -16, 81.6 ], "RotationDegrees": 0 },
    { "Centroid": [ 16, 64, 81.6 ], "RotationDegrees": 90 },
    { "Centroid": [ 16, -64, 81.6 ], "RotationDegrees": 90 },
    { "Centroid": [ -16, 64, 81.6 ], "RotationDegrees": 90 },
    { "Centroid": [ -16, -64, 81.6 ], "RotationDegrees": 90 },
    { "Centroid": [ 0, 0, 91.2 ], "RotationDegrees": 0 },
    { "Centroid": [ 32, 16, 91.2 ], "RotationDegrees": 0 },
    { "Centroid": [ 32, -16, 91.2 ], "RotationDegrees": 0 },
    { "Centroid": [ -32, 16, 91.2 ], "RotationDegrees": 0 },
    { "Centroid": [ -32, -16, 91.2 ], "RotationDegrees": 0 },
    { "Centroid": [ 16, 32, 91.2 ], "RotationDegrees": 90 },
    { "Centroid": [ 16, -32, 91.2 ], "RotationDegrees": 90 },
    { "Centroid": [ -16, 32, 91.2 ], "RotationDegrees": 90 },
    { "Centroid": [ -16, -32, 91.2 ], "RotationDegrees": 90 },
    { "Centroid": [ 48, 0, 91.2 ], "RotationDegrees": 0 },
    { "Centroid": [ -48, 0, 91.2 ], "RotationDegrees": 0 },
    { "Centroid": [ 0, 48, 91.2 ], "RotationDegrees": 90 },
    { "Centroid": [ 0, -48, 91.2 ], "RotationDegrees": 90 },
    { "Centroid": [ 0, 0, 100.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 32, 0, 100.8 ], "RotationDegrees": 0 },
    { "Centroid": [ -32, 0, 100.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 0, 32, 100.8 ], "RotationDegrees": 90 },
    { "Centroid": [ 0, -32, 100.8 ], "RotationDegrees": 90 },
    { "Centroid": [ 16, 16, 100.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 16, -16, 100.8 ], "RotationDegrees": 0 },
    { "Centroid": [ -16, 16, 100.8 ], "RotationDegrees": 0 },
    { "Centroid": [ -16, -16, 100.8 ], "RotationDegrees": 0 },
    { "Centroid": [ 0, 0, 110.4 ], "RotationDegrees": 0 },
    { "Centroid": [ 16, 0, 110.4 ], "RotationDegrees": 90 },
    { "Centroid": [ -16, 0, 110.4 ], "RotationDegrees": 90 },
    { "Centroid": [ 0, 16, 110.4 ], "RotationDegrees": 0 },
    { "Centroid": [ 0, -16, 110.4 ], "RotationDegrees": 0 }
  ]
},
    {}
]