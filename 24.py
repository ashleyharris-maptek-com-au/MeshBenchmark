
import itertools,random

title = "2D convex hull, identify points on the hull."

prompt = """
You are given a set of points in 2D space. A rubber band is stretch around the entire scene,
and let snap. Return a list of all the points the rubber band touches.


"""

structure = {
    "type" : "object",
    "properties" : {
        "reasoning" : { "type" : "string"},
        "pointSequence" : { "type" : "array", "items" : { "type" : "integer"} }
    },
    "additionalProperties": False,
    "propertyOrdering": [
        "reasoning",
        "pointSequence"
    ],
    "required": [
        "reasoning",
        "pointSequence"
    ]
}

points = []
random.seed(42)
for i in range(1024):
    points.append((random.randint(0, 100), random.randint(0, 100)))

pointsCount = [16, 32, 64, 128, 512, 1024]

referenceScad = ""

def prepareSubpassPrompt(index):
    def pointString(count):
        return "\n".join([f"{i}: ({x}, {y})" for i, (x, y) in enumerate(points[:count])])

    if index >= len(pointsCount):
        raise StopIteration
    
    return prompt + "\n\n" + pointString(pointsCount[index])

def resultToScad(result):
  scad = "module result(){linear_extrude(1) difference(){union(){"

  for i,j in itertools.pairwise(result["pointSequence"]):
    scad += "hull(){"
    scad += "translate([" + str(points[i][0]) + "," + str(points[i][1]) + "]) circle(1);\n"
    scad += "translate([" + str(points[j][0]) + "," + str(points[j][1]) + "]) circle(1);\n"
    scad += "};\n"

  if len(result["pointSequence"]) > 1:
    scad += "hull(){"
    scad += "translate([" + str(points[-1][0]) + "," + str(points[-1][1]) + "]) circle(1);\n"
    scad += "translate([" + str(points[0][0]) + "," + str(points[0][1]) + "]) circle(1);\n"
    scad += "};\n"

  scad += "};\nhull(){"
  for i in result["pointSequence"]:
    scad += "translate([" + str(points[i][0]) + "," + str(points[i][1]) + "]) circle(0.001);\n"

  scad += "};\n" + "}}\n\n"

  return scad

def prepareSubpassReferenceScad(index):
  scad = "module reference(){ linear_extrude(1) difference() {hull(){"
  for i in range(pointsCount[index]):
    scad += "translate([" + str(points[i][0]) + "," + str(points[i][1]) + "]) circle(1);\n"

  scad += "};\nhull(){"
  for i in range(pointsCount[index]):
    scad += "translate([" + str(points[i][0]) + "," + str(points[i][1]) + "]) circle(0.001);\n"

  scad += "};\n" + "}}\n\n"

  return scad

if __name__ == "__main__":
    print(prepareSubpassReferenceScad(2))
    print(prepareSubpassReferenceScad(1))