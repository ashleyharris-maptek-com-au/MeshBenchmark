
prompt = """

Here is an GRIDSIZExGRIDSIZE grid representing a space partition:

GRIDDETAILS

0, 0 is the top left, x is horizontal, y is vertical.

Using the formula:

let cell = 

   # if ax^3 + bx^2 + cx + d + ey^3 + fy^2 + gy + h > 0
   . if ax^3 + bx^2 + cx + d + ey^3 + fy^2 + gy + h <= 0

(where a, b, c, d, e, f, g, and h are possibly complex numbers).

return values of a,b,c,d,e,f,g, and h such that the formula when evaluated at all grid cells returns output matching the grid above,
if you believe no solution is possible, approximate the grid as best as possible and return a best-fit result.
"""

grids = [
"""
###.....
##......
##......
###.....
####....
#####...
#######.
########
""",
"""
########....
######......
####........
###.........
###.........
##..........
##..........
#...........
............
............
............
............
""",
"""
........................
........................
........................
........................
........................
........................
........................
........................
........................
.....###................
....######..............
....########............
....##########..........
....###########.........
.....############.......
......###########.......
........#######.........
..........###...........
...........#............
........................
........................
........................
........................
........................
""",
"""
........
........
...##...
..####..
.######.
.##..##.
##....##
#......#
"""
]

structure = {
  "type": "object",
  "properties": {
    "a": {
      "type": "object",
      "properties": {
        "real": { "type": "number" },
        "imaginary": { "type": "number" }
      },
      "propertyOrdering": [ "real", "imaginary" ],
      "required": [ "real" ]
    },
    "b": {
      "type": "object",
      "properties": {
        "real": { "type": "number" },
        "imaginary": { "type": "number" }
      },
      "propertyOrdering": [ "real", "imaginary" ],
      "required": [ "real" ]
    },
    "c": {
      "type": "object",
      "properties": {
        "real": { "type": "number" },
        "imaginary": { "type": "number" }
      },
      "propertyOrdering": [ "real", "imaginary" ],
      "required": [ "real" ]
    },
    "d": {
      "type": "object",
      "properties": {
        "real": { "type": "number" },
        "imaginary": { "type": "number" }
      },
      "propertyOrdering": [ "real", "imaginary" ],
      "required": [ "real" ]
    },
    "e": {
      "type": "object",
      "properties": {
        "real": { "type": "number" },
        "imaginary": { "type": "number" }
      },
      "propertyOrdering": [ "real", "imaginary" ],
      "required": [ "real" ]
    },
    "f": {
      "type": "object",
      "properties": {
        "real": { "type": "number" },
        "imaginary": { "type": "number" }
      },
      "propertyOrdering": [ "real", "imaginary" ],
      "required": [ "real" ]
    },
    "g": {
      "type": "object",
      "properties": {
        "real": { "type": "number" },
        "imaginary": { "type": "number" }
      },
      "propertyOrdering": [ "real", "imaginary" ],
      "required": [ "real" ]
    },
    "h": {
      "type": "object",
      "properties": {
        "real": { "type": "number" },
        "imaginary": { "type": "number" }
      },
      "propertyOrdering": [ "real", "imaginary" ],
      "required": [ "real" ]
    }
  },
  "propertyOrdering": [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h"
  ]
}


def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("GRIDSIZE", "8").replace("GRIDDETAILS", grids[0])
    if index == 1: return prompt.replace("GRIDSIZE", "12").replace("GRIDDETAILS", grids[1])
    if index == 2: return prompt.replace("GRIDSIZE", "24").replace("GRIDDETAILS", grids[2])
    if index == 3: return prompt.replace("GRIDSIZE", "8").replace("GRIDDETAILS", grids[3])
    raise StopIteration


def gradeAnswer(answer : str, subPass : int):
    a = complex(answer["a"]["real"], answer["a"]["imaginary"])
    b = complex(answer["b"]["real"], answer["b"]["imaginary"])
    c = complex(answer["c"]["real"], answer["c"]["imaginary"])
    d = complex(answer["d"]["real"], answer["d"]["imaginary"])
    e = complex(answer["e"]["real"], answer["e"]["imaginary"])
    f = complex(answer["f"]["real"], answer["f"]["imaginary"])
    g = complex(answer["g"]["real"], answer["g"]["imaginary"])
    h = complex(answer["h"]["real"], answer["h"]["imaginary"])
    
    gridSize = 8 if subPass == 0 else 12 if subPass == 1 else 24 if subPass == 2 else 8
    
    grid = grids[subPass].splitlines()
    score = 0

    for y in range(gridSize):
        for x in range(gridSize):
            p = a * x**3 + b * x**2 + c * x + d + e * y**3 + f * y**2 + g * y + h
            if p > 0:
                if grid[y][x] == "#":
                    score += 1
            else:
                if grid[y][x] == ".":
                    score += 1
                    
    return score / (gridSize * gridSize)
