prompt = """
Do you remember the snake game on Nokia phones? This is hyper-snake!

You are a snake in a PARAM_AD space grid of size PARAM_B. You can move to any adjacent cell in the grid, along any of the
available PARAM_A dimensions, but you can not move to a cell which you have visited before, nor can you move "diagonally",
that is, you can not move in more than one dimension at a time.

The game ends when you run out of space to move, when you hit the boundary, or when you run into yourself.

Return the path of the snake as a list of cells, the first element of which is PARAM_C, and going for as long as you can.
"""

structure = {
    "type": "object",
    "properties": {
        "path": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "number"
                }
            }
        }
    },
    "propertyOrdering": [
        "path"
    ]
}

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "3").replace("PARAM_B", "(4,4,4)").replace("PARAM_C", "[0, 0,0]")
    if index == 1: return prompt.replace("PARAM_A", "4").replace("PARAM_B", "(5,5,5,5)").replace("PARAM_C", "[0, 0,0,0]")
    if index == 2: return prompt.replace("PARAM_A", "5").replace("PARAM_B", "(4,4,4,4,4)").replace("PARAM_C", "[0, 0,0,0,0]")
    if index == 3: return prompt.replace("PARAM_A", "6").replace("PARAM_B", "(3,3,3,3,3,3)").replace("PARAM_C", "[0, 0,0,0,0,0]")
    raise StopIteration
