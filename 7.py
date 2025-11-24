prompt = """

Here is a 2D platform maze, in which A is located at height 5, and B is located at height 0:

A555
2B20
3015
4555

The character can move:
- 1 cell horizontally or vertically, so long as the height is within 1 unit.
- Can jump 2 cells horizontally or vertically, so long as:
  - source and destination heights are the same
  - the height of the cell between the source and destination is lower than the source height (no jumping through walls!)

In this case, the character:
- starts at A, which is at level 5
- walks flat for a bit, 
- jumps over a casym of height 0 to another level 5 block.
- walks flat for a bit
- descends until level 2, then jumps over B to level 2,
- and then continues down to level 0, reaching B.

The maze must use only 0-9, A & B to represent height, and must only have one solution.
A & B must appear in the grid once each.
"""

structure = None # We just take a string here.

def prepareSubpassPrompt(index):
    if index == 0: return prompt + "Create a maze of size 5x5 that has A at level 5 and B at level 0, and at least 2 jumps."
    if index == 1: return prompt + "Create a maze of size 10x10 that has A at level 0 and B at level 9, and at least 4 jumps."
    if index == 2: return prompt + "Create a maze of size 15x15 that has A at level 5 and B at level 5, and at least 6 jumps."
    raise StopIteration


def gradeAnswer(answer : str, subPass : int):
    answer = answer.strip()
    if answer.count("A") != 1 or answer.count("B") != 1:
        print("Maze must have exactly one A and one B")
        return 0
    
    rows = answer.split("\n")
    if subPass == 0 and len(rows) != 5:
        print("Maze must have exactly 5 rows")
        return 0
    if subPass == 1 and len(rows) != 10:
        print("Maze must have exactly 10 rows")
        return 0
    if subPass == 2 and len(rows) != 15:
        print("Maze must have exactly 15 rows")
        return 0
    
    if subPass == 0 and len(rows[0]) != 5:
        print("Maze must have exactly 5 columns")
        return 0
    if subPass == 1 and len(rows[0]) != 10:
        print("Maze must have exactly 10 columns")
        return 0
    if subPass == 2 and len(rows[0]) != 15:
        print("Maze must have exactly 15 columns")
        return 0

    for row in rows:
        if len(row) != len(rows[0]):
            print("Maze must have all rows the same width")
            return 0
    


    
    
