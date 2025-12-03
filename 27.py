import random

title = "Jewel swap"
prompt = """

You are given a 2D grid, laid out like so:

GRID

A represents Amethysist
B represents Blue Sapphire
C represents Cubic Zirconia
D represents Diamond
E represents Emerald

Your job is to swap jewels in the grid, when 3 jewels are in a line, horizontally, vertically, 
they are removed from the grid, go into your pocket, and the jewels above them fall down, leaving empty
space at the top of the game board. Falling jewels may match with neighbours, leading to future profits.

0,0 is the bottom left grid cell and indices increase up and to the right.

The goal is to remove as many jewels as possible and get the highest payout.

You may make up to 1000 moves.

"""

def makeGrid(size : list[int]):
  while True:
    grid = []
    for i in range(size[0]):
        row = []
        for j in range(size[1]):
            row.append(random.choice("ABCDE"))
        grid.append(row)

    if processGrid(grid)[0] == 0:
      return grid

def processGrid(grid : list[list[str]]) -> tuple[int, list[list[str]]]:
    # Look for any vertical or horizontal lines of 3 or more jewels
    # If found, remove them, count the jewels removed, repeat the search, and 
    # return the count removed and the new grid.
    # If no matches are found, return the original grid and 0
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    total_removed = 0
    
    while True:
        # Find all cells to remove
        to_remove = set()
        
        # Check horizontal matches
        for r in range(rows):
            run_start = 0
            for c in range(1, cols + 1):
                if c < cols and grid[r][c] == grid[r][run_start] and grid[r][c] != ' ':
                    continue
                # End of run
                run_length = c - run_start
                if run_length >= 3 and grid[r][run_start] != ' ':
                    for i in range(run_start, c):
                        to_remove.add((r, i))
                run_start = c
        
        # Check vertical matches
        for c in range(cols):
            run_start = 0
            for r in range(1, rows + 1):
                if r < rows and grid[r][c] == grid[run_start][c] and grid[r][c] != ' ':
                    continue
                # End of run
                run_length = r - run_start
                if run_length >= 3 and grid[run_start][c] != ' ':
                    for i in range(run_start, r):
                        to_remove.add((i, c))
                run_start = r
        
        if not to_remove:
            break
        
        total_removed += len(to_remove)
        
        # Remove matched jewels
        for r, c in to_remove:
            grid[r][c] = ' '
        
        # Gravity: make jewels fall down (row 0 is bottom)
        for c in range(cols):
            # Collect non-empty cells from bottom to top
            column = [grid[r][c] for r in range(rows) if grid[r][c] != ' ']
            # Fill from bottom, pad top with empty
            for r in range(rows):
                if r < len(column):
                    grid[r][c] = column[r]
                else:
                    grid[r][c] = ' '
    
    return total_removed, grid

structure = {
    "type" : "object",
    "properties" : {
        "moves" : { "type" : "array", "items" : { 
            "type" : "object", 
            "properties" : 
              {"cellX" : { "type" : "integer" },
               "cellY" : { "type" : "integer" },
               "direction" : { "type" : "string", "enum" : [ "up", "down", "left", "right" ] }
              },
              "additionalProperties" : False,
              "required" : [ "cellX", "cellY", "direction" ]
        }}
    },
    "additionalProperties" : False,
    "required" : [ "grid", "removed" ]
}

promptChangeSummary = "Progressively larger grids."

gridSize = [[32,8],[48,12],[56,16],[64,24],[72,32]]

grids = []
solvedGrids = []

for size in gridSize:
    grids.append(makeGrid(size))
    solvedGrids.append(None)

def prepareSubpassPrompt(index):
    if index < 5: return prompt.replace("GRID", grids[index])
    raise StopIteration

def gradeAnswer(answer, subPass, aiEngineName):
    grid = grids[subPass].copy()
    
    score = 0
    maxScore = gridSize[subPass][0] * gridSize[subPass][1] - 10

    for move in answer.get("moves", []):
        pos = (move.get("cellX"), move.get("cellY"))
        if pos[0] < 0 or pos[0] >= gridSize[subPass][0] or pos[1] < 0 or pos[1] >= gridSize[subPass][1]:
            solvedGrids[subpass] = grid.copy()
            return 0, "Out of bounds move start position" + str(move)
        
        pos2 = list(pos)
        if move.get("direction") == "up":
            pos2[1] += 1
        elif move.get("direction") == "down":
            pos2[1] -= 1
        elif move.get("direction") == "left":
            pos2[0] -= 1
        elif move.get("direction") == "right":
            pos2[0] += 1
        
        if pos[0] < 0 or pos[0] >= gridSize[subPass][0] or pos[1] < 0 or pos[1] >= gridSize[subPass][1]:
            solvedGrids[subPass] = grid.copy()
            return 0, "Out of bounds move end position" + str(move)
        
        value = grid[pos[1]][pos[0]]
        value2 = grid[pos2[1]][pos2[0]]
        if value == ' ' or value2 == ' ':
            solvedGrids[subPass] = grid.copy()
            return 0, "Invalid move, can't swap air" + str(move)
        if value == value2:
            solvedGrids[subPass] = grid.copy()
            return 0, "Invalid move, same jewels" + str(move)
        
        grid[pos[1]][pos[0]] = value2
        grid[pos2[1]][pos2[0]] = value
        
        removed, grid = processGrid(grid)
        score += removed
    
    solvedGrids[subPass] = grid.copy()
    return min(1, score / maxScore), "Made " + str(score) + " moves"


def resultToNiceReport(result, subPassIndex, aiEngineName : str):
    region_colours = {" " : [1,1,1]}
    
    # Use the grid from the grade answer pass, so we don't have to redo the entire game.
    grid = solvedGrids[subPassIndex]
    
    out = "<span style='font-family: monospace;"
    out += "font-size:10px; line-height:10px"
    out += "'>"
    
    for y in range(10, size):
        for x in range(len(grid[y])):
            cell = grid[y][x]
            if cell not in region_colours:
                region_colours[cell] = [10 * random.randint(0, 25), 10 * random.randint(0, 25), 10 * random.randint(0, 25)]
            out += f"<span style='background-color: rgb({region_colours[cell][0]}, {region_colours[cell][1]}, {region_colours[cell][2]});'>"
            out += "#" if cell else "&nbsp;"
            out += "</span>"
        out += "<br>"

    out += "</span>"
    return out

