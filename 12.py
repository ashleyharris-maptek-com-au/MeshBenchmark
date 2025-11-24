prompt = """
You have PARAM_A 1m lengths of pipe, and an square area of side length PARAM_B to play with.

Lay the pipe out to form a closed loop, using all the pipe, and returning to the starting point.

You can not cross yourself, and you can not cross the boundary of the area. You do not need to 
stick to axis aligned paths.

Return the loop as a list of the pipe endpoints.
"""

structure = None # We just take a string here.

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "16").replace("PARAM_B", "3")
    if index == 1: return prompt.replace("PARAM_A", "30").replace("PARAM_B", "4")
    if index == 2: return prompt.replace("PARAM_A", "60").replace("PARAM_B", "10")
    if index == 3: return prompt.replace("PARAM_A", "150").replace("PARAM_B", "20")
    raise StopIteration

    