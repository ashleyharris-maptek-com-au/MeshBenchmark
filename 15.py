prompt = """
You are playing tetris(tm), and are cursed to only get the L-shaped tetrimino for all time.

The L shaped piece initially arrives in this orientation (and indent representing grid position):

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

Blocks spawn at position 0,0, the top left of the grid. The grid is PARAM_A cells wide and 64 cells high.

When a row is filled, it is removed from the grid, and all blocks above it are shifted down by one row.

Position blocks by moving them left and right, and rotating them in clockwise 90 degree increments, for as long as possible. 
When you get bored, run out of token limits, mistakenly truncate your output, or make too many mistakes, 
the game will end and your score will be tallied. You solution must remove at least PARAM_B rows to pass.
"""

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

def gradeAnswer(answer : dict, subPassIndex : int):
    widths = [10, 16, 20, 40]
    required = [10, 15, 20, 30]
    if subPassIndex < 0 or subPassIndex >= len(widths):
        return 0
    W = widths[subPassIndex]
    H = 64
    target = required[subPassIndex]

    moves = answer.get("moves") if isinstance(answer, dict) else None
    if not isinstance(moves, list):
        return 0

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

        for dx, dy in shape:
            x = px + dx
            y = py + dy
            if 0 <= y < H:
                grid[y][x] = 1

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

    if target <= 0:
        return 0
    score = cleared / float(target)
    if score > 1:
        score = 1
    if score < 0:
        score = 0
    return score
