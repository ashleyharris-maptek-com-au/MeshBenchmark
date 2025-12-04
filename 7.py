import VolumeComparison as vc
import concurrent.futures
import threading


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
The path must visit at least 20% of all cells.
No single elevation can occupy more than 20% of the grid.
"""

suffix = \
"""
Your output must be ONLY the maze's heightmap, nothing else.
Your output must be PARAM_A rows long, and every row must be PARAM_A characters long.
The maze must be your only output - Extra text above or below the maze itself corrupt your work.
"""

subpassParamSummary = [
    "Cover a 5x5 grid with A at level 5 and B at level 0, requiring at least 2 jumps",
    "Cover a 10x10 grid with A at level 0 and B at level 9, requiring at least 4 jumps",
    "Cover a 15x15 grid with A at level 5 and B at level 5, requiring at least 6 jumps",
    "Cover a 20x20 grid with A at level 5 and B at level 5, requiring at least 8 jumps",
    "Cover a 25x25 grid with A at level 5 and B at level 5, requiring at least 10 jumps",
    "Cover a 30x30 grid with A at level 5 and B at level 0, requiring at least 12 jumps"
]

structure = None # We just take a string here.

def prepareSubpassPrompt(index):
    if index == 0: return prompt + "Create a maze of size 5x5 that has A at level 5 and B at level 0, and at least 2 jumps." + suffix.replace("PARAM_A","5")
    if index == 1: return prompt + "Create a maze of size 10x10 that has A at level 0 and B at level 9, and at least 4 jumps." + suffix.replace("PARAM_A","10")
    if index == 2: return prompt + "Create a maze of size 15x15 that has A at level 5 and B at level 5, and at least 6 jumps." + suffix.replace("PARAM_A","15")
    if index == 3: return prompt + "Create a maze of size 20x20 that has A at level 5 and B at level 5, and at least 8 jumps." + suffix.replace("PARAM_A","20")
    if index == 4: return prompt + "Create a maze of size 25x25 that has A at level 5 and B at level 5, and at least 10 jumps." + suffix.replace("PARAM_A","25")
    if index == 5: return prompt + "Create a maze of size 30x30 that has A at level 5 and B at level 0, and at least 12 jumps." + suffix.replace("PARAM_A","30")
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
    elif subPass == 3:
        bHeight = 5
    elif subPass == 4:
        bHeight = 5
    elif subPass == 5:
        bHeight = 0

    rows = result.split('\n')
    scad_content = "union() {\n"
    a_pos = None
    b_pos = None
    for j, row in enumerate(rows):
        for i, char in enumerate(row):
            if char in '123456789':
                scad_content += f'    translate([{j}, {i}, {int(char)/2}]) cube([1, 1, {char}], center=true);\n'
            elif char == 'A':
                scad_content += f'    translate([{j}, {i}, {aHeight-0.5}]) color([1, 0, 0]) cube([1, 1, 1], center=true);\n'
                a_pos = (j, i)
            elif char == 'B':
                scad_content += f'    translate([{j}, {i}, {bHeight-0.5}]) color([0, 0, 1]) cube([1, 1, 1], center=true);\n'
                b_pos = (j, i)
    scad_content += "}\n"
    
    print("Drawing 3D maze of size " + str(len(rows)) + "x" + str(len(rows[0])))

    import os
    os.makedirs("results", exist_ok=True)
    output_path = "results/7_Visualization_" + aiEngineName + "_" + str(len(rows)) + ".png"
    
    # Calculate camera: position above A, looking toward B
    grid_size = len(rows)
    center_x = grid_size / 2
    center_y = grid_size / 2
    if a_pos and b_pos:
        # Direction from A to B
        dx = b_pos[0] - a_pos[0]
        dy = b_pos[1] - a_pos[1]
        # Camera offset: behind A (opposite to A->B direction), elevated
        cam_x = a_pos[0] - dx * 1.5
        cam_y = a_pos[1] - dy * 1.5
        cam_z = grid_size * 1.2  # Above looking down
        camera_arg = f"--camera={cam_x},{cam_y},{cam_z},{center_x},{center_y},0,{grid_size * 2}"
    else:
        camera_arg = f"--camera={grid_size},{grid_size},{grid_size},0,0,0,{grid_size * 2}"
    
    vc.render_scadText_to_png(scad_content, output_path, camera_arg)
    print(f"Saved visualization to {output_path}")

    return f'<img src="{os.path.basename(output_path)}" alt="3D Maze Visualization" style="max-width: 100%;">'


def gradeAnswer(answer : str, subPass : int, aiEngineName : str):
    answer = answer.strip()
    if answer.count("A") != 1 or answer.count("B") != 1:
        return 0, "Maze must have exactly one A and one B"
    
    rows = answer.split("\n")
    if subPass == 0 and len(rows) != 5:
        return 0, "Maze must have exactly 5 rows"
    if subPass == 1 and len(rows) != 10:
        return 0, "Maze must have exactly 10 rows"
    if subPass == 2 and len(rows) != 15:
        return 0, "Maze must have exactly 15 rows"
    if subPass == 3 and len(rows) != 20:
        return 0, "Maze must have exactly 20 rows"
    if subPass == 4 and len(rows) != 25:
        return 0, "Maze must have exactly 25 rows"
    if subPass == 5 and len(rows) != 30:
        return 0, "Maze must have exactly 30 rows"
    
    if subPass == 0 and len(rows[0]) != 5:
        return 0, "Maze must have exactly 5 columns"
    if subPass == 1 and len(rows[0]) != 10:
        return 0, "Maze must have exactly 10 columns"
    if subPass == 2 and len(rows[0]) != 15:
        return 0, "Maze must have exactly 15 columns"
    if subPass == 3 and len(rows[0]) != 20:
        return 0, "Maze must have exactly 20 columns"
    if subPass == 4 and len(rows[0]) != 25:
        return 0, "Maze must have exactly 25 columns"
    if subPass == 5 and len(rows[0]) != 30:
        return 0, "Maze must have exactly 30 columns"
    
    for row in rows:
        if len(row) != len(rows[0]):
            return 0, "Maze must have all rows the same width"
    
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
                else:
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
                elif subPass == 3:
                    height_map[(i, j)] = 5
                elif subPass == 4:
                    height_map[(i, j)] = 5
                elif subPass == 5:
                    height_map[(i, j)] = 0
                else:
                    height_map[(i, j)] = 5
            elif char.isdigit():
                height_map[(i, j)] = int(char)
            else:
                return 0, f"Invalid character in maze: {char}"
            grid_row.append(char)
        grid.append(grid_row)
    

    # Check that no elevation occupies more than 20% of the grid
    elevation_counts = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            height = height_map.get((i, j))
            if height is not None:
                elevation_counts[height] = elevation_counts.get(height, 0) + 1
    
    total_cells = len(grid) * len(grid[0])
    for height, count in elevation_counts.items():
        if count / total_cells > 0.2:
            return 0, f"Elevation {height} occupies more than 20% of the grid"
    
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
    
    # Find all paths using DFS with timeout protection
    all_paths = []
    stop_flag = threading.Event()

    def dfs(current, target, visited, path, jump_count):
        if stop_flag.is_set():
            return
        if current == target:
            all_paths.append((path[:], jump_count))
            return
        
        for neighbor, is_jump in get_neighbors(current):
            if stop_flag.is_set():
                return
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, target, visited, path, jump_count + (1 if is_jump else 0))
                path.pop()
                visited.remove(neighbor)
    
    def run_dfs():
        visited = {a_pos}
        dfs(a_pos, b_pos, visited, [a_pos], 0)
    
    # Run DFS with a 60-second timeout
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(run_dfs)
        try:
            future.result(timeout=60)
        except concurrent.futures.TimeoutError:
            stop_flag.set()
            return 0, "Grading timed out (maze too complex or infinite loop detected)"
    
    # Check that exactly one path exists
    if len(all_paths) == 0:
        return 0, "No valid path from A to B"
    
    if len(all_paths) > 1:
        return 0, f"Multiple paths exist ({len(all_paths)} paths found). Maze must have only one solution."
    
    # Check minimum number of jumps
    path, jump_count = all_paths[0]
    required_jumps = [2, 4, 6, 8, 10, 12][subPass]
    
    # Check that path visits at least 20% of cells
    visited_cells = set(path)
    total_cells = len(grid) * len(grid[0])
    visited_percentage = len(visited_cells) / total_cells
    if visited_percentage < 0.2:
        return 0, f"Path visits only {visited_percentage:.2%} of cells (required: 20%)"

    if jump_count < required_jumps:
        return 0, f"Path has {jump_count} jumps, but at least {required_jumps} are required"
    
    return 1, f"Valid maze with {jump_count} jumps (required: {required_jumps})"

if __name__ == "__main__":
    resultToNiceReport("""
000000000B
0000000099
0000000090
0000000090
0000078086
0000202260
0000572400
0000060640
0000000640
A123450530
""".strip(), 1, "Placebo")