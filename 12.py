import VolumeComparison as vc
import itertools
import math

title = "Fit a loop into a square that's perimeter is smaller than the total length"

prompt = """
You have PARAM_A 1m lengths of pipe, and an square area of side length PARAM_B to play with.

Lay the pipe out to form a closed loop, using all the pipe, and returning to the starting point.

You can not cross existing pipe, you can not re-use vertices, and you can not cross the boundary of the area. You do not need to 
stick to axis aligned paths.

Return the loop as a list of the pipe endpoints. Note that N pipes requires N+1 verticies to describe a path, but since the 
first and last vertices are the same, you only need to return N points.
"""

subpassParamSummary = [
    "3 pipes in 1x1. This is a trivial equalateral triangle.", 
    "16 pipes in 3x3", 
    "30 pipes in 4x4", 
    "60 pipes in 10x10", 
    "150 pipes in 20x20", 
    "600 pipes in 40x40"
]

promptChangeSummary = "Increasing pipe length and square size."

structure = {
    "type": "object",
    "properties": {
        "points": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "number"
                    },
                    "y": {
                        "type": "number"
                    }
                },
                "propertyOrdering": [
                    "x",
                    "y"
                ],
                "additionalProperties": False,
                "required": [
                    "x",
                    "y"
                ]
            }
        }
    },
    "propertyOrdering": [
        "points"
    ],
    "additionalProperties": False,
    "required": [
        "points"
    ]
}

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "3").replace("PARAM_B", "1")
    if index == 1: return prompt.replace("PARAM_A", "16").replace("PARAM_B", "3")
    if index == 2: return prompt.replace("PARAM_A", "30").replace("PARAM_B", "4")
    if index == 3: return prompt.replace("PARAM_A", "60").replace("PARAM_B", "10")
    if index == 4: return prompt.replace("PARAM_A", "150").replace("PARAM_B", "20")
    if index == 5: return prompt.replace("PARAM_A", "600").replace("PARAM_B", "40")
    raise StopIteration

def gradeAnswer(answer: dict, subPassIndex: int, aiEngineName: str):
    # Get parameters for this subpass
    pipe_counts = [3, 16, 30, 60, 150, 600]
    boundary_sizes = [2, 3, 4, 10, 20, 40]
    
    if subPassIndex < 0 or subPassIndex >= len(pipe_counts):
        return 0, "Invalid subPassIndex"
    
    expected_pipes = pipe_counts[subPassIndex]
    boundary = boundary_sizes[subPassIndex]
    tolerance = 0.05  # 5% tolerance for distance checking
    
    # Extract points from answer
    points = answer.get("points") if isinstance(answer, dict) else None
    if not isinstance(points, list):
        return 0, "Answer must contain a 'points' array"
    
    # Parse points
    parsed_points = []
    for pt in points:
        if not isinstance(pt, dict):
            continue
        try:
            x = float(pt.get('x', 0))
            y = float(pt.get('y', 0))
            parsed_points.append((x, y))
        except (TypeError, ValueError):
            continue
    
    # Check correct number of points (N pipes in a closed loop = N vertices)
    if len(parsed_points) != expected_pipes:
        return 0, f"Expected {expected_pipes} points (for {expected_pipes} pipe segments in closed loop), got {len(parsed_points)}"
    
    # Check all points are within bounds [0, boundary]
    for i, (x, y) in enumerate(parsed_points):
        if x < 0 or x > boundary or y < 0 or y > boundary:
            return 0, f"Point {i} ({x}, {y}) is outside boundary [0, {boundary}]"
    
    # Check all consecutive segments are 1 unit long (within tolerance)
    for i in range(len(parsed_points) - 1):
        x1, y1 = parsed_points[i]
        x2, y2 = parsed_points[i + 1]
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if abs(dist - 1.0) > tolerance:
            return 0, f"Segment {i} from ({x1}, {y1}) to ({x2}, {y2}) has length {dist:.4f}, expected 1.0 ± {tolerance}"
    
    # Check that it forms a loop (first and last points are 1 unit apart)
    x1, y1 = parsed_points[-1]
    x2, y2 = parsed_points[0]
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    if abs(dist - 1.0) > tolerance:
        return 0, f"Loop does not close: distance from last point to first is {dist:.4f}, expected 1.0 ± {tolerance}"
    
    # Helper function to check if two line segments intersect
    def segments_intersect(p1, p2, p3, p4):
        """Check if line segment p1-p2 intersects with p3-p4 (excluding shared endpoints)"""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        
        # Check if segments share an endpoint (adjacent segments)
        eps = 1e-9
        if (abs(x1 - x3) < eps and abs(y1 - y3) < eps) or \
           (abs(x1 - x4) < eps and abs(y1 - y4) < eps) or \
           (abs(x2 - x3) < eps and abs(y2 - y3) < eps) or \
           (abs(x2 - x4) < eps and abs(y2 - y4) < eps):
            return False
        
        # Calculate cross products to determine intersection
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        
        # Segments intersect if endpoints are on opposite sides of each other
        return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)
    
    # Build list of segments (including the closing segment)
    segments = []
    for i in range(len(parsed_points)):
        p1 = parsed_points[i]
        p2 = parsed_points[(i + 1) % len(parsed_points)]
        segments.append((p1, p2))
    
    # Check for crossing segments
    for i in range(len(segments)):
        for j in range(i + 2, len(segments)):
            # Don't check adjacent segments (they share endpoints)
            # Also skip checking last segment with first segment (adjacent in loop)
            if i == 0 and j == len(segments) - 1:
                continue
            
            if segments_intersect(segments[i][0], segments[i][1], segments[j][0], segments[j][1]):
                return 0, f"Segment {i} crosses segment {j}"
    
    # Check for backtracking (consecutive segments that are nearly opposite in direction)
    for i in range(len(segments)):
        p0 = segments[i][0]
        p1 = segments[i][1]
        p2 = segments[(i + 1) % len(segments)][1]
        
        # Vector from p0 to p1
        v1x, v1y = p1[0] - p0[0], p1[1] - p0[1]
        # Vector from p1 to p2
        v2x, v2y = p2[0] - p1[0], p2[1] - p1[1]
        
        # Normalize vectors
        len1 = math.sqrt(v1x**2 + v1y**2)
        len2 = math.sqrt(v2x**2 + v2y**2)
        if len1 > 0 and len2 > 0:
            v1x, v1y = v1x / len1, v1y / len1
            v2x, v2y = v2x / len2, v2y / len2
            
            # Dot product close to -1 means vectors are opposite (backtracking)
            dot = v1x * v2x + v1y * v2y
            if dot < -0.99:  # Allow some tolerance for near-backtracking
                return 0, f"Segment {i} backtracks on segment {(i + 1) % len(segments)}"
    
    return 1, f"Valid loop with {len(parsed_points)} points, all within bounds and 1 unit apart"


def resultToNiceReport(result : dict, subPass, aiEngineName : str):

    # Get the square size from the subpass parameters
    boundary_sizes = [1, 3, 4, 10, 20, 40]
    squareSize = boundary_sizes[subPass] if subPass < len(boundary_sizes) else 10

    scad_content = ""
    
    result['points'].append(result['points'][0])

    for a,b in itertools.pairwise(result['points']):
      if round(math.sqrt((b['x'] - a['x'])**2 + (b['y'] - a['y'])**2)) == 1:
        scad_content += "hull(){\n"
        scad_content += f"    translate([{a['x']}, {a['y']}]) sphere(0.01);\n"
        scad_content += f"    translate([{b['x']}, {b['y']}]) sphere(0.01);\n"
        scad_content += "}\n"
    
    scad_content += f"translate([0,0,-0.01]) color([0.1,0.1,0.1]) cube([{squareSize},{squareSize},0.01]);"

    import os
    os.makedirs("results", exist_ok=True)
    output_path = "results/12_Visualization_" + aiEngineName + "_" + str(squareSize) + ".png"
    vc.render_scadText_to_png(scad_content, output_path)
    print(f"Saved visualization to {output_path}")

    return f'<img src="{os.path.basename(output_path)}" alt="Pipe Loop Visualization" style="max-width: 100%;">'
