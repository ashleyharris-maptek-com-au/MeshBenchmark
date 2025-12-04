title = "Subdivided binary tree walk."

prompt = """
You are given a list of dimensions, these represent a series of recursive subdivisions of a 0,0,0->1,1,1 unit cube.

Eg [Z,Z,Z,X] means:
- the cube has 16 rectangular prism leaf nodes, 
- Each of size [1/2, 1, 1/8]. 
- Nodes are identified by their path through the tree. 0 represents the minimum split, 1 represents the maximum split.
- "" is the root node. "0" is the z= [0,0.5] half of the cube. "00" is the z= [0,0.25] quarter of the cube. etc.

"""

structure = {
    "type" : "object",
    "properties" : {
        "reasoning" : { "type" : "string"},
        "nodes" : { "type" : "array", "items" : { "type" : "string"} }
    },
    "additionalProperties": False,
    "propertyOrdering": [
        "reasoning",
        "nodes"
    ],
    "required": [
        "reasoning",
        "nodes"
    ]
}

import random
import os
import VolumeComparison as vc

trees = ["Z", "X", "Y", "Z", "X", "Y", "Z", "X", "Y", "Z", "X", "Y", "Z", "X", "Y", "Z"]
tasks = [
    "List all landlocked nodes. That is nodes that don't touch the edge of the unit cube.",
    "List all nodes that touch on an edge, but not a face, to the node 000111",
    "List all nodes that touch a vertex, but not an edge or a face, to the node 001101",
    "List all nodes that touch a face to the node 10101",
    "List all nodes that touch a face to one of the 8 corner nodes"
]

def getNodeBounds(path, treeDepth):
    """Get the [xmin,xmax], [ymin,ymax], [zmin,zmax] bounds for a node path."""
    bounds = {'X': [0.0, 1.0], 'Y': [0.0, 1.0], 'Z': [0.0, 1.0]}
    
    for i, bit in enumerate(path):
        if i >= treeDepth:
            break
        axis = trees[i]
        mid = (bounds[axis][0] + bounds[axis][1]) / 2
        if bit == '0':
            bounds[axis][1] = mid
        else:
            bounds[axis][0] = mid
    
    return bounds

def getAllLeafNodes(treeDepth):
    """Generate all leaf node paths for a given tree depth."""
    if treeDepth == 0:
        return [""]
    nodes = []
    for i in range(2 ** treeDepth):
        path = bin(i)[2:].zfill(treeDepth)
        nodes.append(path)
    return nodes

def touchesCubeEdge(bounds, eps=1e-9):
    """Check if bounds touch x=0, x=1, y=0, y=1, z=0, or z=1."""
    for axis in ['X', 'Y', 'Z']:
        if bounds[axis][0] <= eps or bounds[axis][1] >= 1.0 - eps:
            return True
    return False

def getSharedDimensions(bounds1, bounds2, eps=1e-9):
    """
    Returns (face_touch, edge_touch, vertex_touch).
    - face_touch: share a face (2D overlap + 1 axis touching)
    - edge_touch: share an edge (1D overlap + 2 axes touching) but not a face
    - vertex_touch: share only a vertex (0D overlap + 3 axes touching)
    """
    overlaps = 0  # dimensions with interior overlap
    touches = 0   # dimensions that touch at boundary
    
    for axis in ['X', 'Y', 'Z']:
        min1, max1 = bounds1[axis]
        min2, max2 = bounds2[axis]
        
        # Check for interior overlap
        overlap_min = max(min1, min2)
        overlap_max = min(max1, max2)
        
        if overlap_max - overlap_min > eps:
            overlaps += 1
        elif abs(max1 - min2) < eps or abs(max2 - min1) < eps:
            touches += 1
        else:
            # No contact at all
            return False, False, False
    
    face_touch = (overlaps == 2 and touches == 1)
    edge_touch = (overlaps == 1 and touches == 2)
    vertex_touch = (overlaps == 0 and touches == 3)
    
    return face_touch, edge_touch, vertex_touch

def getCornerNodes(treeDepth):
    """Get the 8 corner nodes (nodes touching 3 faces of the unit cube)."""
    corners = []
    for node in getAllLeafNodes(treeDepth):
        bounds = getNodeBounds(node, treeDepth)
        touching_faces = 0
        for axis in ['X', 'Y', 'Z']:
            if bounds[axis][0] < 1e-9 or bounds[axis][1] > 1.0 - 1e-9:
                touching_faces += 1
        if touching_faces == 3:
            corners.append(node)
    return corners

def prepareSubpassPrompt(index):
    if index == 5: raise StopIteration
    treeDepth = 8 + 2 * index
    treeSpec = "\n".join([f"{i}: {trees[i]}" for i in range(treeDepth)])
    return prompt + "\n\nTree structure:\n" + treeSpec + "\n\nTask: " + tasks[min(index, len(tasks)-1)]

def gradeAnswer(result, subPass, aiEngineName):
    treeDepth = 8 + 2 * subPass
    givenNodes = set(result.get("nodes", []))
    
    if not givenNodes:
        return 0, "No nodes provided"
    
    # Compute the correct answer based on subpass
    correctNodes = set()
    
    if subPass == 0:
        # Landlocked nodes: don't touch cube boundary
        for node in getAllLeafNodes(treeDepth):
            bounds = getNodeBounds(node, treeDepth)
            if not touchesCubeEdge(bounds):
                correctNodes.add(node)
    
    elif subPass == 1:
        # Nodes that touch edge (but not face) to 000111
        targetBounds = getNodeBounds("000111", treeDepth)
        for node in getAllLeafNodes(treeDepth):
            if node == "000111":
                continue
            bounds = getNodeBounds(node, treeDepth)
            face, edge, vertex = getSharedDimensions(targetBounds, bounds)
            if edge and not face:
                correctNodes.add(node)
    
    elif subPass == 2:
        # Nodes that touch vertex (but not edge or face) to 001101
        targetBounds = getNodeBounds("001101", treeDepth)
        for node in getAllLeafNodes(treeDepth):
            if node == "001101":
                continue
            bounds = getNodeBounds(node, treeDepth)
            face, edge, vertex = getSharedDimensions(targetBounds, bounds)
            if vertex and not edge and not face:
                correctNodes.add(node)
    
    elif subPass == 3:
        # Nodes that touch face to 10101
        targetBounds = getNodeBounds("10101", treeDepth)
        for node in getAllLeafNodes(treeDepth):
            if node == "10101":
                continue
            bounds = getNodeBounds(node, treeDepth)
            face, edge, vertex = getSharedDimensions(targetBounds, bounds)
            if face:
                correctNodes.add(node)
    
    elif subPass == 4:
        # Nodes that touch face to one of the 8 corner nodes
        cornerNodes = getCornerNodes(treeDepth)
        for node in getAllLeafNodes(treeDepth):
            if node in cornerNodes:
                continue
            bounds = getNodeBounds(node, treeDepth)
            for corner in cornerNodes:
                cornerBounds = getNodeBounds(corner, treeDepth)
                face, edge, vertex = getSharedDimensions(cornerBounds, bounds)
                if face:
                    correctNodes.add(node)
                    break
    
    # Score: intersection over union
    intersection = len(givenNodes & correctNodes)
    union = len(givenNodes | correctNodes)
    extra = len(givenNodes - correctNodes)
    missing = len(correctNodes - givenNodes)
    
    if union == 0:
        return 0, "No valid nodes to compare"
    
    score = intersection / union
    return score, f"""
    Matched {intersection}/{len(correctNodes)} correct nodes. <br>
    Nodes wrongly included: {extra}.<br>
    Nodes incorrectly excldued: {missing}
    """

def resultToNiceReport(result, subPassIndex, aiEngineName: str):
    treeDepth = 8 + 2 * subPassIndex
    nodes = result.get("nodes", [])
    
    if not nodes:
        return "No nodes to visualize"
    
    openScadData = ""
    
    for node in nodes:
        bounds = getNodeBounds(node, treeDepth)
        
        xmin, xmax = bounds['X']
        ymin, ymax = bounds['Y']
        zmin, zmax = bounds['Z']
        
        pos = [(xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2]
        span = [xmax - xmin, ymax - ymin, zmax - zmin]
        
        randomColour = [random.random(), random.random(), random.random()]
        openScadData += f"translate([{pos[0]}, {pos[1]}, {pos[2]}]) color({randomColour}) cube([{span[0]*0.95}, {span[1]*0.95}, {span[2]*0.95}], center=true);\n"
    
    # Add wireframe unit cube for reference
    openScadData += "color([0.3,0.3,0.3,0.3]) difference() { cube([1,1,1]); translate([0.01,0.01,0.01]) cube([0.98,0.98,0.98]); }\n"
    
    output_path = f"results/26_Visualization_{aiEngineName}_subpass{subPassIndex}.png"
    vc.render_scadText_to_png(openScadData, output_path)
    print(f"Saved visualization to {output_path}")
    return "<img src=\"" + os.path.basename(output_path) + "\" />"