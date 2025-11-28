import random

title = "Tetris™ but with only the L-Piece"

prompt = """
You are playing Tetris™, and are cursed to only get the L-shaped tetrimino for all time.

The L shaped piece initially arrives in this orientation (with indent representing grid position):

###
#

It can be rotated in 90 degree increments clockwise, and moved left and right. The centre of rotation is the corner of the L.

Two units of movement to the right looks like this (noting indent):

  ###
  #

Three units of movement to the right and a 90 degree rotation looks like this (noting indent):

  ##
   #
   #

2 units of movement to the right, and a 180 degree rotation looks like this (noting indent):

  #
###

Blocks spawn at position 0,0, the top left of the grid. The grid is PARAM_A cells wide and 30 cells high.

When a row is filled, it is removed from the grid, and all blocks above it are shifted down by one row.

Position blocks by moving them left and right, and rotating them in clockwise 90 degree increments for as long as possible. 
When you get bored, run out of token limits, mistakenly truncate your output, or make too many mistakes, 
the game will end and your score will be tallied. You solution must remove at least PARAM_B rows to pass.
"""

promptChangeSummary = "Increasing grid size and row target"

subpassParamSummary = [
    "10x30 grid, remove 10 rows. <br> Apparently this matches the original 1980s game.",
    "16x30 grid, remove 15 rows", 
    "20x30 grid, remove 20 rows",
    "40x30 grid, remove 30 rows"
]

structure = {
  "type": "object",
  "properties": {
    "moves": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "translationCount": {
            "type": "number"
          },
          "rotationCount": {
            "type": "number"
          }
        },
        "propertyOrdering": [
          "translationCount",
          "rotationCount"
        ]
      }
    }
  },
  "propertyOrdering": [
    "moves"
  ]
}


def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "10").replace("PARAM_B", "10")
    if index == 1: return prompt.replace("PARAM_A", "16").replace("PARAM_B", "15")
    if index == 2: return prompt.replace("PARAM_A", "20").replace("PARAM_B", "20")
    if index == 3: return prompt.replace("PARAM_A", "40").replace("PARAM_B", "30")
    raise StopIteration

remainsOfLastRun = None

def gradeAnswer(answer : dict, subPassIndex : int, aiEngineName : str):
    global remainsOfLastRun
    remainsOfLastRun = None
    widths = [10, 16, 20, 40]
    required = [10, 15, 20, 30]
    if subPassIndex < 0 or subPassIndex >= len(widths):
        return 0
    W = widths[subPassIndex]
    H = 30
    target = required[subPassIndex]

    moves = answer.get("moves") if isinstance(answer, dict) else None
    if not isinstance(moves, list):
        return 0

    # Ensure that we end with a pile of blocks up, as if a player walks away,
    # as tetris has no good ending.
    for _ in range(20):
        moves.append({"translationCount": random.randint(0,W), "rotationCount": random.randint(0, 3)})

    shapes = [
        [(0, 0), (1, 0), (2, 0), (0, 1)],
        [(0, 0), (-1, 0), (0, 1), (0, 2)],
        [(0, 0), (-1, 0), (-2, 0), (0, -1)],
        [(0, 0), (1, 0), (0, -1), (0, -2)],
    ]

    grid = [[0] * W for _ in range(H)]
    cleared = 0

    def collides(px, py, shape):
        for dx, dy in shape:
            x = px + dx
            y = py + dy
            if x < 0 or x >= W:
                return True
            if y >= H:
                return True
            if y >= 0 and grid[y][x]:
                return True
        return False

    for mv in moves:
        if not isinstance(mv, dict):
            continue
        try:
            t = int(round(float(mv.get("translationCount", 0))))
        except Exception:
            t = 0
        try:
            r = int(round(float(mv.get("rotationCount", 0))))
        except Exception:
            r = 0
        r %= 4
        shape = shapes[r]

        min_dx = min(d for d, _ in shape)
        max_dx = max(d for d, _ in shape)
        low = -min_dx
        high = W - 1 - max_dx
        px = t
        if px < low:
            px = low
        if px > high:
            px = high
        py = 0

        if collides(px, py, shape):
            break
        while not collides(px, py + 1, shape):
            py += 1

        blockNo = random.randint(0, 48)

        for dx, dy in shape:
            x = px + dx
            y = py + dy
            if 0 <= y < H:
                grid[y][x] = blockNo

        new_rows = []
        removed = 0
        for y in range(H):
            row = grid[y]
            if all(row):
                removed += 1
            else:
                new_rows.append(row)
        if removed:
            grid = [[0] * W for _ in range(removed)] + new_rows
            cleared += removed

    # Store the grid state for potential use in reporting
    remainsOfLastRun = grid

    if target <= 0:
        return 0
    score = cleared / float(target)
    if score > 1:
        score = 1
    if score < 0:
        score = 0
    return score

def resultToNiceReport(result, subPassIndex, aiEngineName : str):
    region_colours = {0 : [0,0,0]}
    
    # Use the grid from the last run
    grid = remainsOfLastRun
    size = len(grid)
    
    out = "<span style='font-family: monospace;"
    
    if size < 20: out += "font-size:20px; line-height:20px"
    else: out += "font-size:10px; line-height:10px"

    out += "'>"
    
    for y in range(size):
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

