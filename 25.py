import random
from scipy.spatial import Delaunay
import numpy as np

title = "2D Delaunay Triangulation"

prompt = """
You are given a set of points in 2D space. Triangulate the points using Delaunay Triangulation and return the triangles in order.
"""

structure = {
    "type" : "object",
    "properties" : {
        "reasoning" : { "type" : "string"},
        "triangles" : { "type" : "array", "items" : { "type" : "array", "items" : { "type" : "integer"} } }
    },
    "additionalProperties": False,
    "propertyOrdering": [
        "reasoning",
        "triangles"
    ],
    "required": [
        "reasoning",
        "triangles"
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

def referenceDelaunay(pts):
    """Compute reference Delaunay triangulation using scipy"""
    if len(pts) < 3:
        return []
    
    pts_array = np.array(pts)
    tri = Delaunay(pts_array)
    
    # Convert to list of sorted triangles for comparison
    triangles = []
    for simplex in tri.simplices:
        triangle = sorted(simplex.tolist())
        triangles.append(triangle)
    
    triangles.sort()
    return triangles

def gradeAnswer(result, subPass, aiEngineName):
    triangles = result.get("triangles", [])
    
    if not isinstance(triangles, list):
        return 0, "triangles must be a list"
    
    # Get the points for this subpass
    count = pointsCount[subPass]
    pts = points[:count]
    
    # Sort each individual triangle (breaks winding order but enables comparison)
    ai_triangles = []
    for tri in triangles:
        if isinstance(tri, list) and len(tri) == 3:
            ai_triangles.append(sorted(tri))
        else:
            return 0, f"Invalid triangle format: {tri}"
    
    # Sort the list of triangles
    ai_triangles.sort()
    
    # Compute reference Delaunay triangulation
    ref_triangles = referenceDelaunay(pts)

    # Compare
    if ai_triangles == ref_triangles:
        return 1, f"Perfect match! {len(ref_triangles)} triangles"
    
    # Partial scoring: count matching triangles
    ai_set = set(tuple(t) for t in ai_triangles)
    ref_set = set(tuple(t) for t in ref_triangles)
    
    correct = len(ai_set & ref_set)
    total = len(ref_set)
    extra = len(ai_set - ref_set)
    missing = len(ref_set - ai_set)
    
    score = correct / total if total > 0 else 0
    
    return score, f"Matched {correct}/{total} triangles. Extra: {extra}, Missing: {missing}"

def resultToNiceReport(result, subPassIndex, aiEngineName : str):
    triangles = result.get("triangles", [])
    scad_content = ""
    
    for a,b,c in triangles:
        #generate a random colour for each triangle:
        r = random.random()
        g = random.random()
        b = random.random()

        scad_content += "color([" + str(r) + "," + str(g) + "," + str(b) + "]) hull(){\n"
        scad_content += f"    translate([{points[a][0]},{points[a][1]}]) sphere(0.01);\n"
        scad_content += f"    translate([{points[b][0]},{points[b][1]}]) sphere(0.01);\n"
        scad_content += f"    translate([{points[c][0]},{points[c][1]}]) sphere(0.01);\n"
        scad_content += "}\n"
    
    scad_content += f"translate([0,0,-0.01]) color([0.1,0.1,0.1]) cube([{squareSize},{squareSize},0.01]);"

    import os
    os.makedirs("results", exist_ok=True)
    output_path = "results/25_Visualization_" + aiEngineName + "_" + str(squareSize) + ".png"
    vc.render_scadText_to_png(scad_content, output_path)
    print(f"Saved visualization to {output_path}")

    return f'<img src="{os.path.basename(output_path)}" alt="Pipe Loop Visualization" style="max-width: 100%;">'