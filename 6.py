import itertools
import VolumeComparison as vc


title = "Voxel Grid Projection - shadow coverage and no symmetries"

prompt = """
Position PARAM_A voxels in a cubic grid of PARAM_B voxels per side, such that the orthographic projection to all 3 planes is 
solid (no holes in the projection), and there are no trivial symmetries (rotations or reflections that leave the shape unchanged).

0,0,0 is the bottom left grid cell and indices increase up and to the right.
"""

structure = {
  "type": "object",
  "properties": {
    "voxels": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "xyz": {
            "type": "array",
            "items": {
              "type": "number"
            }
          }
        },
        "propertyOrdering": [
          "xyz"
        ],
        "additionalProperties": False,
        "required": [
          "xyz"
        ]
      }
    }
  },
  "propertyOrdering": [
    "voxels"
  ],
  "additionalProperties": False,
  "required": [
    "voxels"
  ]
}

subpassParamSummary = [
    "Cover a 6x6x6 grid with 50 voxels",
    "Cover a 8x8x8 grid with 100 voxels", 
    "Cover a 12x12x12 grid with 200 voxels",
    "Cover a 16x16x16 grid with 400 voxels",
    "Cover a 24x24x24 grid with 1000 voxels",
    "Cover a 24x24x24 grid with 500 voxels, and sum of coordinates (x + y + z) has no 7 in it.",
]

promptChangeSummary = "Progressively larger grids with more voxels across subpasses"

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "50").replace("PARAM_B", "6")
    if index == 1: return prompt.replace("PARAM_A", "100").replace("PARAM_B", "8")
    if index == 2: return prompt.replace("PARAM_A", "200").replace("PARAM_B", "12")
    if index == 3: return prompt.replace("PARAM_A", "400").replace("PARAM_B", "16")
    if index == 4: return prompt.replace("PARAM_A", "1000").replace("PARAM_B", "24")
    if index == 5: return prompt.replace("PARAM_A", "500").replace("PARAM_B", "20") + "\nEnsure no voxels coordinate sum (x + y + z) has a 7 in it."
    raise StopIteration

def resultToNiceReport(result, subPass, aiEngineName):
    # Convert the result to a nice HTML report format

    voxels = result.get("voxels", [])
    scad_content = "union() {\n"
    for v in voxels:
        xyz = v.get("xyz", [0, 0, 0])
        x, y, z = xyz[0], xyz[1], xyz[2]
        scad_content += f'    translate([{x}, {y}, {z}]) cube([1, 1, 1]);\n'
    scad_content += "}\n"
    
    import os
    os.makedirs("results", exist_ok=True)
    output_path = "results/6_Visualization_" + aiEngineName + "_" + str(len(voxels)) + ".png"
    vc.render_scadText_to_png(scad_content, output_path)
    print(f"Saved visualization to {output_path}")

    return f'<img src="{os.path.basename(output_path)}" alt="Voxel Grid Visualization" style="max-width: 100%;">'

def gradeAnswer(answer: dict, subPass: int, aiEngineName: str):
    sizes = [6, 8, 12, 16, 24, 24]
    counts = [50, 100, 200, 400, 1000, 500]
    if subPass < 0 or subPass >= len(sizes):
        return 0, "Invalid subPass"
    N = sizes[subPass]
    expected = counts[subPass]
    vox = answer.get("voxels")
    if not isinstance(vox, list):
        return 0, "voxels must be a list"

    def to_int_coord(v):
        if abs(v - round(v)) > 1e-9:
            return None
        iv = int(round(v))
        if iv < 0 or iv >= N:
            return None
        return iv

    def parse_item(it):
        if isinstance(it, dict):
            if "xyz" in it:
                xyz = it["xyz"]
                if isinstance(xyz, (list, tuple)) and len(xyz) == 3:
                    xi, yi, zi = to_int_coord(float(xyz[0])), to_int_coord(float(xyz[1])), to_int_coord(float(xyz[2]))
                    if None in (xi, yi, zi):
                        return None
                    return (xi, yi, zi)
                if isinstance(xyz, (int, float)):
                    idx = int(round(float(xyz)))
                    if idx < 0 or idx >= N * N * N:
                        return None
                    x = idx % N
                    y = (idx // N) % N
                    z = idx // (N * N)
                    return (x, y, z)
                if isinstance(xyz, str):
                    try:
                        parts = [p.strip() for p in xyz.split(',')]
                        if len(parts) != 3:
                            return None
                        xi, yi, zi = to_int_coord(float(parts[0])), to_int_coord(float(parts[1])), to_int_coord(float(parts[2]))
                        if None in (xi, yi, zi):
                            return None
                        return (xi, yi, zi)
                    except Exception:
                        return None
            if all(k in it for k in ("x", "y", "z")):
                xi, yi, zi = to_int_coord(float(it["x"])), to_int_coord(float(it["y"])), to_int_coord(float(it["z"]))
                if None in (xi, yi, zi):
                    return None
                return (xi, yi, zi)
        if isinstance(it, (list, tuple)) and len(it) == 3:
            xi, yi, zi = to_int_coord(float(it[0])), to_int_coord(float(it[1])), to_int_coord(float(it[2]))
            if None in (xi, yi, zi):
                return None
            return (xi, yi, zi)
        if isinstance(it, (int, float)):
            idx = int(round(float(it)))
            if idx < 0 or idx >= N * N * N:
                return None
            x = idx % N
            y = (idx // N) % N
            z = idx // (N * N)
            return (x, y, z)
        if isinstance(it, str):
            try:
                parts = [p.strip() for p in it.split(',')]
                if len(parts) != 3:
                    return None
                xi, yi, zi = to_int_coord(float(parts[0])), to_int_coord(float(parts[1])), to_int_coord(float(parts[2]))
                if None in (xi, yi, zi):
                    return None
                return (xi, yi, zi)
            except Exception:
                return None
        return None

    pts = []
    for it in vox:
        p = parse_item(it)
        if p is None:
            return 0, f"Invalid voxel entry: {it}"

        if subPass == 5 and "7" in str(p[0] + p[1] + p[2]):
            return 0, f"Voxel {p} has a coordinate sum {p[0] + p[1] + p[2]} with a 7 in it"
        pts.append(p)

    if len(pts) != expected:
        return 0, f"Incorrect voxel count {len(pts)}, expected {expected}"
    S = set(pts)
    if len(S) != expected:
        for i in range(len(pts)):
            if pts[i] in pts[i+1:]:
                return 0, "Duplicate voxel coordinates detected. Voxel " + str(pts[i]) + " is repeated."

    xy = {(x, y) for (x, y, z) in S}
    xz = {(x, z) for (x, y, z) in S}
    yz = {(y, z) for (x, y, z) in S}
    if len(xy) != N * N:
        return 0, "XY projection has holes or gaps"
    if len(xz) != N * N:
        return 0, "XZ projection has holes or gaps"
    if len(yz) != N * N:
        return 0, "YZ projection has holes or gaps"

    def make_transform(perm, signs):
        def t(p):
            coords = [p[0], p[1], p[2]]
            out = []
            for i in range(3):
                v = coords[perm[i]]
                if signs[i] < 0:
                    v = (N - 1) - v
                out.append(v)
            return (out[0], out[1], out[2])
        return t

    for perm in itertools.permutations((0, 1, 2), 3):
        for signs in itertools.product((-1, 1), repeat=3):
            if perm == (0, 1, 2) and signs == (1, 1, 1):
                continue
            t = make_transform(perm, signs)
            T = {t(p) for p in S}
            if T == S:
                return 0, "Shape has a trivial symmetry (rotation/reflection)"

    return 1, f"Valid voxel configuration with {len(pts)} voxels, all projections solid, no symmetries"
        
