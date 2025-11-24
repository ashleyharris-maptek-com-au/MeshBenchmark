import random


def createGrid(index):
    random.seed(index)
    cells = []
    size = index * index * 10 + 10
    for i in range(size): # 10, 20, 50, 130
        cells.append("." * size)

    for i in range(size * 5):
        cells[random.randint(0, size - 1)][random.randint(0, size - 1)] = chr(ord('A') + i)

    return "\n".join(cells)



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

