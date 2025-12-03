title = "Subdivided binary tree walk."

skip = True

prompt = """
You are given a list of dimensions, these represent a series of recursive subdivisions of a 0,0,0->1,1,1 unit cube.

Eg [Z,Z,Z,X] means:
- the cube has 16 rectangular prism leaf nodes, 
- Each of size [1/2, 1, 1/8]. 
- Nodes are identified by their path through the tree. 0 represents the minimum split, 1 represents the maximum split.
- "" is the root node. "0" is the z= [0,0.5] half of the cube. "00" is the z= [0,0.25] quarter of the cube. etc.

"""

trees = ["Z", "X", "Y", "Z", "X", "Y", "Z", "X", "Y", "Z", "X", "Y", "Z", "X", "Y", "Z"]
tasks = [
    "List all landlocked nodes. That is nodes that don't touch the edge of the unit cube."
    "List all nodes that touch on a edge, but not a face, to the node ",
    "List all nodes that touch a vertex, but not an edge or a face, to the node ",
    "List all nodes that touch a face to the node",
]

def gradeAnswer(result, subPass, aiEngineName):
    return 0, ""