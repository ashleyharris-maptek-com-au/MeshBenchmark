
import itertools,random

title = "2D convex hull, identify points on the hull."

prompt = """
You are given a set of points in 2D space. Identify all points that are on the convex hull of the set
and return them in order.
"""

structure = {
    "type" : "object",
    "properties" : {
        "reasoning" : { "type" : "string"},
        "hull" : { "type" : "array", "items" : { "type" : "integer"} }
    },
    "additionalProperties": False,
    "propertyOrdering": [
        "reasoning",
        "hull"
    ],
    "required": [
        "reasoning",
        "hull"
    ]
}

points = []
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
  scad = "module result(){difference(){union(){"

  for i,j in itertools.pairwise(result["hull"]):
    scad += "hull(){"
    scad += "translate([" + str(points[i][0]) + "," + str(points[i][1]) + "]) circle(1);\n"
    scad += "translate([" + str(points[j][0]) + "," + str(points[j][1]) + "]) circle(1);\n"
    scad += "};\n"

  scad += "};\nhull(){"
  for i in result["hull"]:
    scad += "translate([" + str(points[i][0]) + "," + str(points[i][1]) + "]) circle(0.001);\n"

  scad += "};\n" + "}}\n\n"

  return scad

def prepareSubpassReferenceScad(index):
  scad = "module reference(){ difference() {hull(){"
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