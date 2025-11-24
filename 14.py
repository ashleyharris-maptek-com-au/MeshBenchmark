import random


def createGrid(index):
    random.seed(index)
    cells = []
    size = index * index * 10 + 10
    for i in range(size): # 10, 20, 50, 130
        cells.append(list("." * size))

    for i in range(size * 5):
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        cells[row][col] = chr(ord('A') + i % 26)

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
                ]
            }
        }
    },
    "propertyOrdering": [
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
"""

    return prompt

def gradeAnswer(answer : dict, subPassIndex : int):
    # Get the lines from the answer
    lines = answer.get("lines") if isinstance(answer, dict) else None
    if not isinstance(lines, list):
        return 0
    
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
        return 0
    
    correct_regions = sum(1 for letters in region_letters.values() if len(letters) == 1)
    
    # Return the fraction of regions that are correctly partitioned
    score = correct_regions / total_regions
    return score