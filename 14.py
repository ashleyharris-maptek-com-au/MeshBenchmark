import random

title = "Grid Partitioning with Off-Axis Lines"

promptChangeSummary = "Bigger grids with more regions"

def createGrid(index):
    random.seed(index)
    cells = []
    size = index * index * 10 + 10
    for i in range(size): # 10, 20, 50, 130
        cells.append(list("." * size))

    for i in range(index * index * 3 + 3):
      while True:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        if cells[row][col] == ".":
            cells[row][col] = chr(ord('A') + i % 26)
            break

    return "\n".join([''.join(row) for row in cells])

structure = {
    "type": "object",
    "properties": {
        "lines": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number"
                    },
                    "b": {
                        "type": "number"
                    }
                },
                "propertyOrdering": [
                    "a",
                    "b"
                ],
                "additionalProperties": False,
                "required": [
                    "a",
                    "b"
                ]
            }
        }
    },
    "propertyOrdering": [
        "lines"
    ],
    "additionalProperties": False,
    "required": [
        "lines"
    ]
}

def prepareSubpassPrompt(index):
    prompt = "You are given the following grid of cells:"

    if index == 4: 
        raise StopIteration

    prompt += "\n" + createGrid(index)

    prompt += """
Partition this space such that each cell contains exactly one of the letters.
Use lines of the form ax+b =0 to partition the space. The topleft of the grid is (0,0) and cell cooridinates are integers.
Return the lines as a list of (a,b) tuples.

You can create a horizontal line by setting a=0 and b to the y coordinate of the line. Giving an equation of the form y=b.
You can create a vertical line by setting a to +/- infinity and b to the x coordinate of the line, which although not mathematically 
rigerous, is a common convention in computer graphics. Giving an "equation" that simplifies to the form x=b.
"""

    return prompt

subpassParamSummary = [
    "<br><pre>" + createGrid(0).replace("\n","<br>") + "</pre>",
    "<br><pre>" + createGrid(1).replace("\n","<br>") + "</pre>",
    "<br><pre style='font-size:10px'>" + createGrid(2).replace("\n","<br>") + "</pre>",
    "<br><pre style='font-size:7px'>" + createGrid(3).replace("\n","<br>") + "</pre>"]

def gradeAnswer(answer : dict, subPassIndex : int, aiEngineName : str):
    # Get the lines from the answer
    lines = answer.get("lines") if isinstance(answer, dict) else None
    if not isinstance(lines, list):
        return 0, "Answer must contain a 'lines' array"
    
    # Create and parse the grid
    grid_str = createGrid(subPassIndex)
    grid = [list(row) for row in grid_str.split('\n')]
    size = len(grid)
    
    # Extract line equations (y = ax + b)
    equations = []
    for line in lines:
        if not isinstance(line, dict):
            continue
        try:
            a = float(line.get('a', 0))
            b = float(line.get('b', 0))
            equations.append((a, b))
        except (TypeError, ValueError):
            continue
    
    # For each cell with a letter, determine its region ID based on which side of each line it's on
    def get_region_id(x, y):
        # Region ID is a tuple of booleans indicating which side of each line the point is on
        region = []
        for a, b in equations:
            # Line equation: y = ax + b
            # Point is above line if y > ax + b
            if a == float('inf'):
                above = x > b
            elif a == float('-inf'):
                above = x < b
            else:
                above = y > a * x + b
            region.append(above)
        return tuple(region)
    
    # Collect all letters in each region
    from collections import defaultdict
    region_letters = defaultdict(set)
    
    for y in range(size):
        for x in range(size):
            cell = grid[y][x]
            if cell != '.':
                region_id = get_region_id(x, y)
                region_letters[region_id].add(cell)
    
    # Check if each region contains only one unique letter
    total_regions = len(region_letters)
    if total_regions == 0:
        return 0, "No regions found"
    
    correct_regions = sum(1 for letters in region_letters.values() if len(letters) == 1)
    
    # Return the fraction of regions that are correctly partitioned
    score = correct_regions / total_regions
    return score, f"{correct_regions}/{total_regions} regions correctly partitioned using {len(equations)} lines"

def resultToNiceReport(answer, subPassIndex, aiEngineName : str):
    grid_str = createGrid(subPassIndex)
    grid = [list(row) for row in grid_str.split('\n')]
    size = len(grid)

    # Extract line equations (y = ax + b)
    equations = []
    for line in answer.get('lines', []):
        if not isinstance(line, dict):
            continue
        try:
            a = float(line.get('a', 0))
            b = float(line.get('b', 0))
            equations.append((a, b))
        except (TypeError, ValueError):
            continue
    
    # For each cell with a letter, determine its region ID based on which side of each line it's on
    def get_region_id(x, y):
        # Region ID is a tuple of booleans indicating which side of each line the point is on
        region = []
        for a, b in equations:
            # Line equation: y = ax + b
            # Point is above line if y > ax + b
            if a == float('inf'):
                above = x > b
            elif a == float('-inf'):
                above = x < b
            else:
                above = y > a * x + b
            region.append(above)
        return tuple(region)
    
    # Collect all letters in each region
    from collections import defaultdict
    region_colours = {}
    
    out = "<span style='font-family: monospace;'>"
    for y in range(size):
        for x in range(size):
            cell = grid[y][x]
            id = get_region_id(x, y)
            if id not in region_colours:
                region_colours[id] = [10 * random.randint(0, 25), 10 * random.randint(0, 25), 10 * random.randint(0, 25)]
            out += f"<span style='background-color: rgb({region_colours[id][0]}, {region_colours[id][1]}, {region_colours[id][2]});'>"
            out += cell
            out += "</span>"
        out += "<br>"

    out += "</span>"
    return out


