import VolumeComparison as vc


title = "3D maze - solution requires jumping over gaps"

prompt = """

Here is a heightmap platform maze, in which A is located at height 5, and B is located at height 0. 
The maze represents a 3D space where movement is constrained by height differences. 
Characters can only move to adjacent cells if the height difference is at most 1, or jump over gaps.

A555
2B20
3015
4555

The character can move:
- 1 cell horizontally or vertically, so long as the height is within 1 unit.
- Can jump 2 cells horizontally or vertically, so long as:
  - source and destination heights are the same
  - the height of the cell between the source and destination is lower than the source height (jump over gaps, not through walls!)

In this case, the character:
- starts at A, which is at level 5
- walks flat for a bit, 
- jumps over a gap of height 0 to another level 5 block.
- walks flat for a bit
- descends until level 2, then jumps over B to level 2,
- and then continues down to level 0, reaching B.

The maze must use only 0-9, A & B to represent height, and must only have one solution.
A & B must appear in the grid once each.
"""

subpassParamSummary = [
    "Cover a 5x5 grid with A at level 5 and B at level 0, requiring at least 2 jumps",
    "Cover a 10x10 grid with A at level 0 and B at level 9, requiring at least 4 jumps",
    "Cover a 15x15 grid with A at level 5 and B at level 5, requiring at least 6 jumps"
]

structure = None # We just take a string here.

def prepareSubpassPrompt(index):
    if index == 0: return prompt + "Create a maze of size 5x5 that has A at level 5 and B at level 0, and at least 2 jumps."
    if index == 1: return prompt + "Create a maze of size 10x10 that has A at level 0 and B at level 9, and at least 4 jumps."
    if index == 2: return prompt + "Create a maze of size 15x15 that has A at level 5 and B at level 5, and at least 6 jumps."
    raise StopIteration

def resultToNiceReport(result, subPass, aiEngineName):
    aHeight = 5
    if subPass == 1:
        aHeight = 0
    elif subPass == 2:
        aHeight = 5
        
    bHeight = 0
    if subPass == 1:
        bHeight = 9
    elif subPass == 2:
        bHeight = 5

    rows = result.split('\n')
    scad_content = "union() {\n"
    for j, row in enumerate(rows):
        for i, char in enumerate(row):
            if char in '123456789':
                scad_content += f'    translate([{j}, {i}, {int(char)/2}]) cube([1, 1, {char}], center=true);\n'
            elif char == 'A':
                scad_content += f'    translate([{j}, {i}, {aHeight-0.5}]) color([1, 0, 0]) cube([1, 1, 1], center=true);\n'
            elif char == 'B':
                scad_content += f'    translate([{j}, {i}, {bHeight-0.5}]) color([0, 0, 1]) cube([1, 1, 1], center=true);\n'
    scad_content += "}\n"
    
    import os
    os.makedirs("results", exist_ok=True)
    output_path = "results/7_Visualization_" + aiEngineName + "_" + str(len(rows)) + ".png"
    vc.render_scadText_to_png(scad_content, output_path)
    print(f"Saved visualization to {output_path}")

    return f'<img src="{os.path.basename(output_path)}" alt="3D Maze Visualization" style="max-width: 100%;">'


def gradeAnswer(answer : str, subPass : int, aiEngineName : str):
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
    
    # Parse the maze and find A and B positions
    grid = []
    a_pos = None
    b_pos = None
    height_map = {}
    
    for i, row in enumerate(rows):
        grid_row = []
        for j, char in enumerate(row):
            if char == 'A':
                a_pos = (i, j)
                # A's height depends on subPass
                if subPass == 0:
                    height_map[(i, j)] = 5
                elif subPass == 1:
                    height_map[(i, j)] = 0
                elif subPass == 2:
                    height_map[(i, j)] = 5
            elif char == 'B':
                b_pos = (i, j)
                # B's height depends on subPass
                if subPass == 0:
                    height_map[(i, j)] = 0
                elif subPass == 1:
                    height_map[(i, j)] = 9
                elif subPass == 2:
                    height_map[(i, j)] = 5
            elif char.isdigit():
                height_map[(i, j)] = int(char)
            else:
                print(f"Invalid character in maze: {char}")
                return 0
            grid_row.append(char)
        grid.append(grid_row)
    
    # Find all valid paths from A to B using DFS
    def get_height(pos):
        return height_map.get(pos, None)
    
    def get_neighbors(pos):
        """Get all valid moves from current position"""
        i, j = pos
        current_height = get_height(pos)
        neighbors = []
        
        # 4 directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for di, dj in directions:
            # Try 1-cell move (walk)
            ni, nj = i + di, j + dj
            if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                next_height = get_height((ni, nj))
                if next_height is not None and abs(current_height - next_height) <= 1:
                    neighbors.append(((ni, nj), False))  # (position, is_jump)
            
            # Try 2-cell move (jump)
            ni2, nj2 = i + 2*di, j + 2*dj
            if 0 <= ni2 < len(grid) and 0 <= nj2 < len(grid[0]):
                dest_height = get_height((ni2, nj2))
                middle_height = get_height((ni, nj))
                
                # Jump rules: same height at source and dest, middle is lower
                if (dest_height is not None and middle_height is not None and
                    current_height == dest_height and middle_height < current_height):
                    neighbors.append(((ni2, nj2), True))  # (position, is_jump)
        
        return neighbors
    
    # Find all paths using DFS
    all_paths = []
    
    def dfs(current, target, visited, path, jump_count):
        if current == target:
            all_paths.append((path[:], jump_count))
            return
        
        for neighbor, is_jump in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, target, visited, path, jump_count + (1 if is_jump else 0))
                path.pop()
                visited.remove(neighbor)
    
    visited = {a_pos}
    dfs(a_pos, b_pos, visited, [a_pos], 0)
    
    # Check that exactly one path exists
    if len(all_paths) == 0:
        print("No valid path from A to B")
        return 0
    
    if len(all_paths) > 1:
        print(f"Multiple paths exist ({len(all_paths)} paths found). Maze must have only one solution.")
        return 0
    
    # Check minimum number of jumps
    path, jump_count = all_paths[0]
    required_jumps = [2, 4, 6][subPass]
    
    if jump_count < required_jumps:
        print(f"Path has {jump_count} jumps, but at least {required_jumps} are required")
        return 0
    
    return 1
