import re

title = "Fit a curve to partition 2D ascii patterns via cubic polynomials"

prompt = """

Here is an GRIDSIZExGRIDSIZE grid representing a space partition:

GRIDDETAILS

0, 0 is the top left, x is horizontal, y is vertical. Coordinates are in integers.

Using the formula:

let cell = 

   # if f(x,y) > 0
   . if f(x,y) <= 0

where f(x,y) is a polynomial of whatever degree you need to solve this. You can include cross terms like x*y, x**2*y, x*y**2, etc.

Return the formula as python function f(x,y) that uses ONLY:
- arithmetic operations (+, -, *, /)
- powers (**) 
- parentheses for grouping
- integer coordinates x, y
- the words "def" and "return"

Do not use type annotations, casts, conditionals, branches or comments or anything else.

You can use the following example as a template:

def f(x, y):
    return x**2 + 3*y**2 - 4*x*y - 145

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
""".strip(),
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
""".strip(),
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
""".strip(),
"""
........
........
...##...
..####..
.######.
.##..##.
##....##
#......#
""".strip()
]

structure = None


def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("GRIDSIZE", "8").replace("GRIDDETAILS", grids[0])
    if index == 1: return prompt.replace("GRIDSIZE", "12").replace("GRIDDETAILS", grids[1])
    if index == 2: return prompt.replace("GRIDSIZE", "24").replace("GRIDDETAILS", grids[2])
    if index == 3: return prompt.replace("GRIDSIZE", "8").replace("GRIDDETAILS", grids[3])
    raise StopIteration


subpassParamSummary = ["<pre>" + g + "</pre>" for g in grids]

def gradeAnswer(answer : str, subPass : int, aiEngineName : str):
    validPass = answer
    validPass = validPass.replace("def", "").strip()
    validPass = validPass.replace("f", "").strip()
    validPass = validPass.replace("return", "").strip()
    validPass = validPass.replace("x", "").strip()
    validPass = validPass.replace("y", "").strip()
    
    if re.search(r'[A-Za-z]', validPass):
        print(f"Invalid characters in answer: {answer}. It contained \"{validPass}\". Score is 0")
        return 0.0
    
    gridSize = 8 if subPass == 0 else 12 if subPass == 1 else 24 if subPass == 2 else 8
    
    g = {}
    exec(answer.strip(), globals=g)
    
    f = g["f"]

    grid = grids[subPass].splitlines()
    score = 0

    print(f"Grid size: {gridSize}")
    print(grid)

    for y in range(gridSize):
        for x in range(gridSize):
            try:
                p = f(x, y)  # use the evaluated function
                if p > 0:
                    if grid[y][x] == "#":
                        score += 1
                else:
                    if grid[y][x] == ".":
                        score += 1
            except Exception as e:
                print(f"Error evaluating f({x}, {y}): {e}")
                continue
                    
    return score / (gridSize * gridSize)

def resultToNiceReport(answer: str, subPass: int, aiEngineName: str):
  gridSize = 8 if subPass == 0 else 12 if subPass == 1 else 24 if subPass == 2 else 8
  gridRow = " " * gridSize
  grid = [gridRow] * gridSize
  
  g = {}
  exec(answer.strip(), globals=g)

  f = g["f"]

  for y in range(gridSize):
      for x in range(gridSize):
          grid[y] = grid[y][:x] + ("#" if f(x, y) > 0 else ".") + grid[y][x+1:]

  return f"<td>{answer.replace('\n','<br/>')}</td><td><pre>{'<br/>'.join(grid)}</pre></td>"