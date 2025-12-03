title = "Maze generation - ASCII Art"

prompt = """
Generate a PARAM_A * PARAM_A ASCII art maze.

The maze must use the following characters:
# - Wall
. - Correct solution path
A - Start
B - End
  - Untaken path (space)

The maze must be solvable, there must be only one solution, the annotated path must not have any loops or branches, and shortest path
from A to B must cover at least 10% of the maze area. The path threw the maze can only be 1 cell wide, and solvable with
only horizontal or vertical moves.

The maze must be 'watertight', that is have walls touching the border of the grid all around, A and B must be within the maze.

Return the maze as a string, with newlines between rows. 
Every row and column of your output must be PARAM_A characters long, and your output must be PARAM_A rows long.
Outputting anything else than the maze will obviously result in a score of 0. 
"""

structure = {
    "type" : "object",
    "properties" : {
        "reasoning" : { "type" : "string"},
        "maze" : { "type" : "string"}
    },
    "additionalProperties": False,
    "propertyOrdering": [
        "reasoning",
        "maze"
    ],
    "required": [
        "reasoning",
        "maze"
    ]
}

subpassParamSummary = [
    "16x16 maze",
    "32x32 maze",
    "64x64 maze",
    "128x128 maze"
]

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "16")
    if index == 1: return prompt.replace("PARAM_A", "32")
    if index == 2: return prompt.replace("PARAM_A", "64")
    if index == 3: return prompt.replace("PARAM_A", "128")
    raise StopIteration

def gradeAnswer(answer : dict,subPass : int, aiEngineName : str):
    answer = answer["maze"].strip()
    if answer.count("A") != 1 or answer.count("B") != 1:
        return 0, "Maze must have exactly one A and one B"

    spaces = answer.count(" ")
    stepCount = answer.count(".") + 2 # +2 for A and B
    walls = answer.count("#")
    
    reasoning = f"Maze has {spaces} spaces, {stepCount} steps, and {walls} walls"

    if stepCount < spaces * 0.1:
        return 0, reasoning + "\nMaze must have at least 10% of the maze area as steps"

    rows = answer.split("\n")
    cells = []
    for row in rows:
        cells.append(list(row))

    expectedRows = 16 if subPass == 0 else 32 if subPass == 1 else 64 if subPass == 2 else 128
    expectedColumns = expectedRows

    # Check that all rows are the same width:
    for row in cells:
        if len(row) != expectedColumns:
            return 0, reasoning + f"\nMaze must have {expectedColumns} columns, this has {len(row)}"

    width = expectedColumns
    height = expectedRows

    if height != len(cells):
        return 0, reasoning + f"\nMaze must have {expectedRows} rows, this has {len(cells)}"

    location = None
    for y in range(len(cells)):
        for x in range(len(cells[y])):
            if cells[y][x] == "A":
                location = (x, y)
                break
        if location is not None:
            break

    timeout = width * height

    # Use flood fill to walk from A to B, marking each cell as visited by changing . to o
    stack = [location]
    while len(stack) > 0:
        x, y = stack.pop()
        if cells[y][x] == "B":
            break
        if cells[y][x] == "#":
            continue
        if cells[y][x] == "o":
            continue
        if cells[y][x] == " ": # Don't step off the path
            continue
        cells[y][x] = "o"
        if x > 0: stack.append((x - 1, y))
        if x < width - 1: stack.append((x + 1, y))
        if y > 0: stack.append((x, y - 1))
        if y < height - 1: stack.append((x, y + 1))
        timeout -= 1
        if timeout == 0:
            return 0, reasoning + "\nMaze is not solvable"

    # if there are any . left, the maze has loops
    for row in cells:
        for cell in row:
            if cell == ".":
                return 0, reasoning + "\nMaze has loops"

    return 1, reasoning + "\nMaze is valid"

def resultToNiceReport(result, subPass, aiEngineName : str):

    if len(result["maze"].strip()) == 0:
        return "Empty maze"
    
    charMap = {}
    for c in result["maze"]:
        if c not in charMap:
            charMap[c] = len(charMap)

    charMap.pop("\n", None)
    charMap.pop(" ", None)
    charMap.pop("#", None)
    charMap.pop(".", None)
    charMap.pop("A", None)
    charMap.pop("B", None)

    if charMap:
        return "Unknown characters in maze:\n" + str(charMap.keys())

    grid = result["maze"].strip().split("\n")
    
    out = "<span style='font-family: monospace;"
    
    if subPass < 2: out += "font-size:32px; line-height:32px"
    else: out += "font-size:10px; line-height:10px"
    out += "'>"
    
    expectedRows = 16 if subPass == 0 else 32 if subPass == 1 else 64 if subPass == 2 else 128
    expectedColumns = expectedRows

    overflowWarningShown = False

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            cell = grid[y][x]
            if x > expectedColumns:
                if not overflowWarningShown:
                    out += "<span style='color: red;'>... (overflow hidden)</span>"
                    overflowWarningShown = True
                else:
                    out += "<span style='color: red;'>...</span>"
                break
            if cell == "A":
                out += "<span style='color: red;'>A</span>"
            elif cell == "B":
                out += "<span style='color: green;'>B</span>"
            elif cell == "#":
                out += "<span style='color: black;'>#</span>"
            elif cell == ".":
                out += "<span style='color: blue;'>.</span>"
            elif cell == " ":
                out += "<span style='color: white;'> </span>"
            else:
                out += cell
        out += "<br>"

    out += "</span>"
    return out

if __name__ == "__main__":
    print(resultToNiceReport(
        {"maze": 
        "################\n#A.....#########\n######.########\n######.###...###\n######.###.#.###\n######.###.#.###\n##.....###.#.###\n##.#######.#.###\n##.#######.#.###\n##.#######.#.###\n##.........#.###\n############.###\n###B.........###\n################\n################\n################"}, 0, "Test"))