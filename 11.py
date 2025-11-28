title = "Hyper-snake Challenge"

promptChangeSummary = "Dimensions increase from 3D to 6D"
subpassParamSummary = ["3D grid 4x4x4", "4D grid 5x5x5x5", "5D grid 4x4x4x4x4", "6D grid 3x3x3x3x3x3"]

prompt = """
Do you remember the snake game, where you have to direct a snake around a 2D space to avoid hitting itself? This is hyper-snake!

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
        "type": "object",
        "properties": {
          "pos": {
            "type": "array",
            "items": {
              "type": "integer"
            }
          }
        },
        "propertyOrdering": [
          "pos"
        ]
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

def gradeAnswer(answer : dict, subPassIndex : int, aiEngineName : str):
    # Define test parameters based on subPassIndex
    if subPassIndex == 0:
        dimensions = 3
        grid_size = (4, 4, 4)
        start_pos = [0, 0, 0]
    elif subPassIndex == 1:
        dimensions = 4
        grid_size = (5, 5, 5, 5)
        start_pos = [0, 0, 0, 0]
    elif subPassIndex == 2:
        dimensions = 5
        grid_size = (4, 4, 4, 4, 4)
        start_pos = [0, 0, 0, 0, 0]
    elif subPassIndex == 3:
        dimensions = 6
        grid_size = (3, 3, 3, 3, 3, 3)
        start_pos = [0, 0, 0, 0, 0, 0]
    else:
        return 0
    
    # Extract path from answer
    if "path" not in answer:
        return 0
    
    path = answer["path"]
    
    # Path must have at least one position
    if not path or len(path) == 0:
        return 0
    
    # Check first position matches start
    if len(path[0]["pos"]) != dimensions:
        return 0
    
    if list(path[0]["pos"]) != start_pos:
        return 0
    
    # Track visited cells to detect repeats
    visited = set()
    visited.add(tuple(path[0]["pos"]))
    
    # Validate each move
    for i in range(1, len(path)):
        curr_pos = path[i]["pos"]
        prev_pos = path[i-1]["pos"]
        
        # Check dimensionality
        if len(curr_pos) != dimensions:
            return 0
        
        # Count how many dimensions changed
        changes = []
        for dim in range(dimensions):
            if curr_pos[dim] != prev_pos[dim]:
                changes.append((dim, curr_pos[dim] - prev_pos[dim]))
        
        # Must change exactly one dimension
        if len(changes) != 1:
            return 0
        
        # Must be a single cell move (+1 or -1)
        dim, delta = changes[0]
        if abs(delta) != 1:
            return 0
        
        # Check bounds
        for dim in range(dimensions):
            if curr_pos[dim] < 0 or curr_pos[dim] >= grid_size[dim]:
                return 0
        
        # Check for repeats
        pos_tuple = tuple(curr_pos)
        if pos_tuple in visited:
            return 0
        
        visited.add(pos_tuple)
    
    # Score is the fraction of cells occupied
    total_cells = 1
    for size in grid_size:  
        total_cells *= size
    
    return len(path) / total_cells

def resultToNiceReport(answer, subPassIndex, aiEngineName):
    # Calculate total cells for the current subpass
    if subPassIndex == 0:
        total_cells = 4 * 4 * 4
    elif subPassIndex == 1:
        total_cells = 5 * 5 * 5 * 5
    elif subPassIndex == 2:
        total_cells = 4 * 4 * 4 * 4 * 4
    elif subPassIndex == 3:
        total_cells = 3 * 3 * 3 * 3 * 3 * 3
    else:
        total_cells = 0
    
    return f"Visited {len(answer['path'])} cells out of {total_cells} total cells."