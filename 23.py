import numpy as np
import VolumeComparison as vc

title = "Fluid simulation"
prompt = """
You are given a 3D voxel world, of dimensions PARAM_A * PARAM_A * 8 voxels,
currently filled with dirt uniformly flat and solid at the layers z = [0,1,2]

Rainfall occurs at the top centre of the world, and follows the following rules:
- If air is below water, the water falls (z = z - 1)
- If water has ground or water below it, it "flood fills" out looking for any air voxels 
  at the z level below it, and moves to the nearest one.
- If water touches the sides or bottom of the world, it falls off and is lost forever.
- If water can't find a reachable air voxel to walk to, it remains there as a pool of water.

Rainfall currently all runs off the edge of the map, meaning earthworks are required to achieve
your goals. After your earthworks complete, there will be 1000s of voxels worth of rainfall
before your world is graded.

Add dirt or air voxels to the world in order to accomplish your task:

Ensure that; after the rains end,
"""

subpassParamSummary = [
    "there is a lake of at least 36 voxels in surface area.",
    "there are 3 unconnected bodies of water each at least 2x2",
    "there is a lake of at least 2 voxels at z > 5",
    "there is an underground lake of at least 10 voxels in volume, that isn't visible from above",
    "there are 3 lakes on 3 different z levels",
    "there is a lake at least 6 voxels deep"
]

structure = {
  "type": "object",
  "properties": {
    "reasoning" : { "type" : "string"},
    "voxels": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "xyz": {
            "type": "array",
            "items": {
              "type": "number"
            },
          },
          "material": {
            "type" : "string",
            "enum" : ["Air", "Dirt"]
          }
        },
        "propertyOrdering": [
          "xyz",
          "material"
        ],
        "additionalProperties": False,
        "required": [
          "xyz",
          "material"
        ]
      }
    }
  },
  "propertyOrdering": [
    "reasoning",
    "voxels"
  ],
  "additionalProperties": False,
  "required": [
    "reasoning",
    "voxels"
  ]
}

def getWorldSize(subPass):
    sizes = [16, 24, 32, 40, 48, 56]
    return sizes[subPass] if subPass < len(sizes) else 56

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "16") + subpassParamSummary[index]
    if index == 1: return prompt.replace("PARAM_A", "24") + subpassParamSummary[index]
    if index == 2: return prompt.replace("PARAM_A", "32") + subpassParamSummary[index]
    if index == 3: return prompt.replace("PARAM_A", "40") + subpassParamSummary[index]
    if index == 4: return prompt.replace("PARAM_A", "48") + subpassParamSummary[index]
    if index == 5: return prompt.replace("PARAM_A", "56") + subpassParamSummary[index]
    raise StopIteration

LastVoxelWorld = [None] * 6

def gradeAnswer(answer: dict, subPass: int, aiEngineName: str):
    global LastVoxelWorld
    import numpy as np
    from collections import deque
    
    voxels = answer.get("voxels", [])
    if not isinstance(voxels, list):
        return 0, "voxels must be a list"
    
    WORLD_SIZE = getWorldSize(subPass)
    WORLD_HEIGHT = 8
    
    # 0 = air, 1 = dirt, 2 = water
    world = np.zeros((WORLD_SIZE, WORLD_SIZE, WORLD_HEIGHT), dtype=np.uint8)

    # Fill z=0,1,2 with dirt initially
    world[:, :, 0] = 1
    world[:, :, 1] = 1
    world[:, :, 2] = 1

    # Apply AI's earthworks
    for v in voxels:
        xyz = v.get("xyz", [0, 0, 0])
        if len(xyz) < 3:
            continue
        x, y, z = int(xyz[0]), int(xyz[1]), int(xyz[2])
        if x < 0 or x >= WORLD_SIZE or y < 0 or y >= WORLD_SIZE or z < 0 or z >= WORLD_HEIGHT:
            continue  # Skip invalid coordinates
        material = v.get("material", "Air")
        if material == "Dirt":
            world[x, y, z] = 1
        elif material == "Air":
            world[x, y, z] = 0

    # Simulate rainfall - spawn water at top centre
    centre = WORLD_SIZE // 2
    RAIN_AMOUNT = 1000
    
    def is_edge(x, y, z):
        """Check if position is at world edge (water escapes)"""
        return x == 0 or x == WORLD_SIZE - 1 or y == 0 or y == WORLD_SIZE - 1 or z == 0
    
    def simulate_water_drop():
        """Simulate a single water drop from the top centre"""
        x, y, z = centre, centre, WORLD_HEIGHT - 1
        
        while True:
            # Check if at edge - water escapes
            if is_edge(x, y, z):
                return  # Water lost
            
            # Check what's below
            below = world[x, y, z - 1]
            
            if below == 0:  # Air below - fall down
                z -= 1
                continue
            
            # Ground or water below - try to flood fill to find a drop point
            # BFS to find nearest air cell at z-1 that we can reach via walkable cells at current z
            visited = set()
            queue = deque([(x, y, 0)])  # (x, y, distance)
            visited.add((x, y))
            
            best_drop = None
            best_dist = float('inf')
            touches_edge = False
            
            while queue:
                cx, cy, dist = queue.popleft()
                
                # Check if this cell touches edge at current z level
                if cx == 0 or cx == WORLD_SIZE - 1 or cy == 0 or cy == WORLD_SIZE - 1:
                    touches_edge = True
                    continue
                
                # Check if we can drop down from here
                if world[cx, cy, z - 1] == 0:  # Air below
                    if dist < best_dist:
                        best_dist = dist
                        best_drop = (cx, cy)
                
                # Expand to neighbors (can walk through air or water at same z level)
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < WORLD_SIZE and 0 <= ny < WORLD_SIZE:
                        if (nx, ny) not in visited:
                            # Can move through air or water at this z level
                            if world[nx, ny, z] != 1:  # Not dirt
                                visited.add((nx, ny))
                                queue.append((nx, ny, dist + 1))
            
            if best_drop:
                # Move to the drop point and fall
                x, y = best_drop
                z -= 1
                continue

            if touches_edge:
                return  # Water escapes off the edge
            
            # No escape, no drop point - water settles in basin
            # Find any unfilled air cell in the reachable region at this z level
            for (cx, cy) in visited:
                if world[cx, cy, z] == 0:  # Air cell we can fill
                    world[cx, cy, z] = 2
                    return
            
            # All cells at this level are filled, try to rise
            # Check if there's air above any visited cell
            for (cx, cy) in visited:
                if z + 1 < WORLD_HEIGHT and world[cx, cy, z + 1] == 0:
                    # Water can rise here
                    world[cx, cy, z + 1] = 2
                    return
            
            # Basin completely full or blocked
            return
    
    # Run the rain simulation
    for _ in range(RAIN_AMOUNT):
        simulate_water_drop()
    
    LastVoxelWorld[subPass] = world.copy()
    
    # Helper: find connected components of water in 3D
    def find_water_bodies():
        visited = np.zeros_like(world, dtype=bool)
        bodies = []
        
        for x in range(WORLD_SIZE):
            for y in range(WORLD_SIZE):
                for z in range(WORLD_HEIGHT):
                    if world[x, y, z] == 2 and not visited[x, y, z]:
                        # BFS to find connected water body
                        body = []
                        queue = deque([(x, y, z)])
                        visited[x, y, z] = True
                        while queue:
                            cx, cy, cz = queue.popleft()
                            body.append((cx, cy, cz))
                            for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                                nx, ny, nz = cx+dx, cy+dy, cz+dz
                                if 0 <= nx < WORLD_SIZE and 0 <= ny < WORLD_SIZE and 0 <= nz < WORLD_HEIGHT:
                                    if world[nx, ny, nz] == 2 and not visited[nx, ny, nz]:
                                        visited[nx, ny, nz] = True
                                        queue.append((nx, ny, nz))
                        bodies.append(body)
        return bodies
    
    # Helper: get surface area (unique x,y positions) of a water body
    def surface_area(body):
        return len(set((x, y) for x, y, z in body))
    
    # Helper: check if body spans at least 2x2 in surface
    def is_at_least_2x2(body):
        xs = set(x for x, y, z in body)
        ys = set(y for x, y, z in body)
        return len(xs) >= 2 and len(ys) >= 2
    
    # Helper: check if water voxel is underground (has dirt above it at some level)
    def is_underground(x, y, z):
        for zz in range(z + 1, WORLD_HEIGHT):
            if world[x, y, zz] == 1:  # Dirt above
                return True
        return False
    
    if subPass == 0:
        # Search for a lake of at least 36 voxels in surface area
        bodies = find_water_bodies()
        max_surface = max((surface_area(b) for b in bodies), default=0)
        if max_surface >= 36:
            return 1, f"Lake with surface area {max_surface} >= 36"
        return max_surface / 36, f"Largest lake surface area: {max_surface}/36"
    
    elif subPass == 1:
        # Search for 3 unconnected bodies of water each at least 2x2
        bodies = find_water_bodies()
        qualifying = [b for b in bodies if is_at_least_2x2(b)]
        count = len(qualifying)
        if count >= 3:
            return 1, f"Found {count} bodies of water each at least 2x2"
        return count / 3, f"Found {count}/3 qualifying water bodies"
    
    elif subPass == 2:
        # Search for a lake of at least 2 voxels at z > 5
        high_water = np.sum((world[:, :, 6:] == 2))
        if high_water >= 2:
            return 1, f"Found {high_water} water voxels at z > 5"
        return high_water / 2, f"Found {high_water}/2 high water voxels"
    
    elif subPass == 3:
        # Search for underground lake of at least 10 voxels, not visible from above
        underground_count = 0
        for x in range(WORLD_SIZE):
            for y in range(WORLD_SIZE):
                for z in range(WORLD_HEIGHT):
                    if world[x, y, z] == 2 and is_underground(x, y, z):
                        underground_count += 1
        if underground_count >= 10:
            return 1, f"Found {underground_count} underground water voxels"
        return underground_count / 10, f"Found {underground_count}/10 underground water voxels"
    
    elif subPass == 4:
        # Search for 3 lakes on 3 different z levels
        z_levels_with_water = set()
        for z in range(WORLD_HEIGHT):
            if np.any(world[:, :, z] == 2):
                z_levels_with_water.add(z)
        count = len(z_levels_with_water)
        if count >= 3:
            return 1, f"Water on {count} different z levels"
        return count / 3, f"Water on {count}/3 z levels"
    
    elif subPass == 5:
        # Search for a lake at least 6 voxels deep
        max_depth = 0
        for x in range(WORLD_SIZE):
            for y in range(WORLD_SIZE):
                # Find continuous water column depth at this x,y
                depth = 0
                for z in range(WORLD_HEIGHT):
                    if world[x, y, z] == 2:
                        depth += 1
                        max_depth = max(max_depth, depth)
                    else:
                        depth = 0
        if max_depth >= 6:
            return 1, f"Found water column {max_depth} deep"
        return max_depth / 6, f"Deepest water column: {max_depth}/6"
    
    return 0, "Unknown subpass"

def resultToNiceReport(result, subPass, aiEngineName):
    global LastVoxelWorld
    import numpy as np
    from collections import deque
    WORLD_SIZE = getWorldSize(subPass)
    WORLD_HEIGHT = 8
    
    voxels = LastVoxelWorld[subPass]
    scad_content = "union() {\n"

    for x in range(WORLD_SIZE):
        for y in range(WORLD_SIZE):
            for z in range(WORLD_HEIGHT):
                if voxels[x, y, z] == 2:
                    scad_content += f'    translate([{x}, {y}, {z}]) color("blue") cube([0.9, 0.9, 0.9],center=true);\n'
                elif voxels[x, y, z] == 1:
                    scad_content += f'    translate([{x}, {y}, {z}]) color("brown") cube([1, 1, 1],center=true);\n'

    scad_content += "}\n"
    
    import os
    os.makedirs("results", exist_ok=True)
    output_path = "results/23_Visualization_" + aiEngineName + "_" + str(len(voxels)) + ".png"
    vc.render_scadText_to_png(scad_content, output_path)
    print(f"Saved visualization to {output_path}")

    return f'<img src="{os.path.basename(output_path)}" alt="Voxel Grid Visualization" style="max-width: 100%;">'

if __name__ == "__main__":
    gradeAnswer({
    "voxels": [
        {
            "xyz": [4, 4, 2],
            "material": "Air"
        }
    ]
    }, 0, "Test")

    resultToNiceReport("", 0, "Test")