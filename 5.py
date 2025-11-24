prompt = """
Generate a PARAM_A * PARAM_A ASCII art maze.

The maze must use the following characters:
# - Wall
. - Correct solution Path
A - Start
B - End
  - Untaken path (space)

The maze must be solvable, there must be only one solution, the annotated path must not have any loops or branches, and shortest path
from A to B must cover at least 10% of the maze area. The path threw the maze can only be 1 cell wide, and solvable with
only horizontal or vertical moves.

Return the maze as a string, with newlines between rows.
"""

structure = None # We just take a string here.

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "16")
    if index == 1: return prompt.replace("PARAM_A", "32")
    if index == 2: return prompt.replace("PARAM_A", "64")
    if index == 3: return prompt.replace("PARAM_A", "128")
    raise StopIteration

def gradeAnswer(answer : str,subPass : int):
    answer = answer.strip()
    if answer.count("A") != 1 or answer.count("B") != 1:
        print("Maze must have exactly one A and one B")
        return 0
    
    spaces = answer.count(" ")
    stepCount = answer.count(".") + 2 # +2 for A and B
    walls = answer.count("#")
    
    print("Maze has " + str(spaces) + " spaces, " + str(stepCount) + " steps, and " + str(walls) + " walls")

    if stepCount < spaces * 0.1:
        print("Maze must have at least 10% of the maze area as steps")
        return 0

    rows = answer.split("\n")
    cells = []
    for row in rows:
        cells.append(list(row))

    # Check that all rows are the same width:
    for row in cells:
        if len(row) != len(cells[0]):
            print("Maze must have all rows the same width")
            return 0

    width = len(cells[0])
    height = len(cells)

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
            print("Maze is not solvable")
            return 0

    # if there are any . left, the maze has loops
    for row in cells:
        for cell in row:
            if cell == ".":
                print("Maze has loops")
                return 0

    return 1

    
gemini3Answer = [
    """
################
#A..#...#.....##
###.#.#.#.###.##
# #...#.#.# #.##
# #####.#.# #.##
#.....#...#...##
#.###.#####.####
#..B#...#...# ##
#######.#.### ##
#.......#.....##
#.###########.##
#.....#.......##
# ###.#.########
#   #...      ##
################
################

    """,
    """
    """,
    "",
    ""
]
