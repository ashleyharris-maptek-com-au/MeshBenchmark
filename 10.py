prompt = """
You are a painter, you have a canvas of size PARAM_A * PARAM_A pixels.

You are painting a scene from the north east, at a 45 degree angle looking down. You are using an orthographic projection.

The scene contains 5 axis aligned cubes, each with a side length of 1 unit. The cubes bottom-centres are placed at the vertices of a 
regular pentagram of side length 5 units, centred at the origin, which is centred in the middle of your painting.

Your painting is zoomed such that the edges of the cubes touch the edges of the canvas.

Return the canvas as a string, with # representing painted pixels, and (space) representing unpainted pixels.
"""

structure = None # We just take a string here.

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "32")
    if index == 1: return prompt.replace("PARAM_A", "64")
    if index == 2: return prompt.replace("PARAM_A", "128")
    if index == 3: return prompt.replace("PARAM_A", "256")
    raise StopIteration

