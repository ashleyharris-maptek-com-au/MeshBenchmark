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

Do not use type annotations, casts, conditionals, branches, additional variables, comments or anything else.

You can use the following example as a template:

def f(x, y):
    return x**2 + 3*y**2 - 4*x*y - 145

DO NOT OUTPUT ANYTHING ELSE THAN THE FUNCTION.
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

structure = {
    "type" : "object",
    "properties" : {
        "reasoning" : { "type" : "string"},
        "function" : { "type" : "string"}
    },
    "additionalProperties": False,
    "propertyOrdering": [
        "reasoning",
        "function"
    ],
    "required": [
        "reasoning",
        "function"
    ]
}


def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("GRIDSIZE", "8").replace("GRIDDETAILS", grids[0])
    if index == 1: return prompt.replace("GRIDSIZE", "12").replace("GRIDDETAILS", grids[1])
    if index == 2: return prompt.replace("GRIDSIZE", "24").replace("GRIDDETAILS", grids[2])
    if index == 3: return prompt.replace("GRIDSIZE", "8").replace("GRIDDETAILS", grids[3])
    raise StopIteration


subpassParamSummary = ["<pre>" + g + "</pre>" for g in grids]

def gradeAnswer(answer : dict, subPass : int, aiEngineName : str):
    answer = answer["function"]
    validPass = answer
    validPass = validPass.replace("def", "").strip()
    validPass = validPass.replace("f", "").strip()
    validPass = validPass.replace("return", "").strip()
    validPass = validPass.replace("x", "").strip()
    validPass = validPass.replace("y", "").strip()
    
    if re.search(r'[A-Za-z]', validPass):
        return 0.0, f"Invalid characters in answer: {answer}. It contained \"{validPass}\". Score is 0"
    
    gridSize = 8 if subPass == 0 else 12 if subPass == 1 else 24 if subPass == 2 else 8
    
    g = {}
    try:
        exec(answer.strip(), g)
    except Exception as e:
        return 0.0, f"Error evaluating AI-generated python function: {e}"
    
    f = g["f"]

    grid = grids[subPass].splitlines()
    score = 0
    errors = []

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
                errors.append(f"Error evaluating f({x}, {y}): {e}")
                continue
    
    final_score = score / (gridSize * gridSize)
    reasoning = f"Grid size: {gridSize}, matched {score}/{gridSize*gridSize} cells"
    if errors:
        reasoning += f"\n{len(errors)} evaluation errors occurred"
    return final_score, reasoning

def resultToNiceReport(answer: dict, subPass: int, aiEngineName: str):
  answer = answer["function"]
  gridSize = 8 if subPass == 0 else 12 if subPass == 1 else 24 if subPass == 2 else 8
  gridRow = " " * gridSize
  grid = [gridRow] * gridSize
  
  g = {}
  try:
    exec(answer.strip(), g)
  except Exception as e:
    return f"<td>{answer.replace('\n','<br/>')}</td><td>Error evaluating AI-generated python function: {e}</td>"

  f = g["f"]

  for y in range(gridSize):
      for x in range(gridSize):
          grid[y] = grid[y][:x] + ("#" if f(x, y) > 0 else ".") + grid[y][x+1:]

  return f"<td style='font-size: 8px'><div style='max-width:800px'>{answer.replace('\n','<br/>')}</div></td><td><pre>{'<br/>'.join(grid)}</pre></td>"