import itertools

prompt = """
Position PARAM_A voxels in a cubic grid of PARAM_B voxels per side, such that the orthographic projection to all 3 planes is 
solid (no holes in the projection), and there are no trivial symmetries (rotations or reflections that leave the shape unchanged).


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
            "type": "number"
          }
        },
        "propertyOrdering": [
          "xyz"
        ],
        "required": [
          "xyz"
        ]
      }
    }
  },
  "propertyOrdering": [
    "voxels"
  ]
}

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "50").replace("PARAM_B", "6")
    if index == 1: return prompt.replace("PARAM_A", "100").replace("PARAM_B", "8")
    if index == 2: return prompt.replace("PARAM_A", "200").replace("PARAM_B", "12")
    raise StopIteration

def gradeAnswer(answer: dict, subPass: int):
    sizes = [6, 8, 12]
    counts = [50, 100, 200]
    if subPass < 0 or subPass >= len(sizes):
        print("Invalid subPass")
        return 0
    N = sizes[subPass]
    expected = counts[subPass]
    vox = answer.get("voxels")
    if not isinstance(vox, list):
        print("voxels must be a list")
        return 0

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
            print("Invalid voxel entry:", it)
            return 0
        pts.append(p)

    if len(pts) != expected:
        print("Incorrect voxel count", len(pts), "expected", expected)
        return 0
    S = set(pts)
    if len(S) != expected:
        print("Duplicate voxel coordinates detected")
        return 0

    xy = {(x, y) for (x, y, z) in S}
    xz = {(x, z) for (x, y, z) in S}
    yz = {(y, z) for (x, y, z) in S}
    if len(xy) != N * N:
        print("XY projection has holes or gaps")
        return 0
    if len(xz) != N * N:
        print("XZ projection has holes or gaps")
        return 0
    if len(yz) != N * N:
        print("YZ projection has holes or gaps")
        return 0

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
                print("Shape has a trivial symmetry (rotation/reflection)")
                return 0

    return 1
        
