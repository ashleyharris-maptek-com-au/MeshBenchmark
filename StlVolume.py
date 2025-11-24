import struct
import sys
import math
import warnings
import os
from typing import List, Tuple, Dict, Optional, Iterable


Vec3 = Tuple[float, float, float]
Tri = Tuple[Vec3, Vec3, Vec3]


def calculate_stl_volume(path: str, *, tolerance: Optional[float] = None) -> float:
    if not os.path.exists(path): return 0.0

    tris = _load_stl(path)
    if not tris:
        return 0.0
    min_v, max_v = _bounds(tris)
    diag = math.sqrt(
        (max_v[0] - min_v[0]) ** 2 + (max_v[1] - min_v[1]) ** 2 + (max_v[2] - min_v[2]) ** 2
    )
    if diag == 0.0:
        return 0.0
    if tolerance is None:
        tol = max(diag * 1e-9, 1e-12)
    else:
        tol = max(float(tolerance), 0.0)
    tris = _filter_degenerate(tris, diag)
    if not tris:
        return 0.0
    verts, faces = _dedup_vertices(tris, tol)
    if not faces:
        return 0.0
    (
        components,
        flips,
        edge_counts_per_comp,
        nonmanifold_edge_counts_per_comp,
        orient_conflicts,
    ) = _orient_faces_and_components(faces, len(verts))
    comp_ids = sorted(components.keys())
    comps = []
    for comp_id in comp_ids:
        comp_faces = components[comp_id]
        edges = edge_counts_per_comp.get(comp_id, {})
        nonmf = nonmanifold_edge_counts_per_comp.get(comp_id, 0)
        boundary_edges = sum(1 for n in edges.values() if n == 1)
        if boundary_edges > 0:
            warnings.warn(
                f"Component {comp_id}: mesh is not watertight; result is a best-effort estimate.",
                RuntimeWarning,
            )
        if nonmf > 0:
            warnings.warn(
                f"Component {comp_id}: non-manifold edges detected ({nonmf}); result may be unreliable.",
                RuntimeWarning,
            )
        if orient_conflicts.get(comp_id, 0) > 0:
            warnings.warn(
                f"Component {comp_id}: orientation conflicts detected ({orient_conflicts[comp_id]}).",
                RuntimeWarning,
            )
        vol_abs = abs(_component_volume(comp_faces, flips, faces, verts))
        bbox = _component_bbox(comp_faces, faces, verts)
        tris_comp = _component_triangles(comp_faces, faces, verts)
        comps.append(
            {
                "id": comp_id,
                "faces": comp_faces,
                "volume": vol_abs,
                "bbox": bbox,
                "tris": tris_comp,
                "closed": boundary_edges == 0,
            }
        )
    eps = max(diag * 1e-9, 1e-12)
    depths: Dict[int, int] = {c["id"]: 0 for c in comps}
    interior_points: Dict[int, Optional[Vec3]] = {}
    for c in comps:
        interior_points[c["id"]] = _choose_interior_point(c["tris"], c["bbox"], eps)
    for i in comps:
        pi = interior_points.get(i["id"]) if i["closed"] else None
        if pi is None:
            continue
        cnt = 0
        for j in comps:
            if j["id"] == i["id"]:
                continue
            if not j["closed"]:
                continue
            if not _bbox_contains(j["bbox"], i["bbox"], eps * 10.0):
                continue
            if _point_in_mesh(pi, j["tris"], eps):
                cnt += 1
        depths[i["id"]] = cnt
    total_volume = 0.0
    for c in comps:
        depth = depths.get(c["id"], 0)
        sign = -1.0 if (depth % 2 == 1) else 1.0
        total_volume += sign * c["volume"]
    if total_volume < 0:
        total_volume = -total_volume
    return float(total_volume)


def _bounds(tris: List[Tri]) -> Tuple[Vec3, Vec3]:
    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = float("-inf")
    for a, b, c in tris:
        for x, y, z in (a, b, c):
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if z < min_z:
                min_z = z
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            if z > max_z:
                max_z = z
    return (min_x, min_y, min_z), (max_x, max_y, max_z)


def _filter_degenerate(tris: List[Tri], diag: float) -> List[Tri]:
    thr = (1e-12 * diag * diag) if diag > 0 else 1e-24
    out: List[Tri] = []
    dropped = 0
    for a, b, c in tris:
        ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        ac = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
        cx = ab[1] * ac[2] - ab[2] * ac[1]
        cy = ab[2] * ac[0] - ab[0] * ac[2]
        cz = ab[0] * ac[1] - ab[1] * ac[0]
        area2 = cx * cx + cy * cy + cz * cz
        if area2 <= thr:
            dropped += 1
            continue
        out.append((a, b, c))
    if dropped:
        warnings.warn(
            f"Dropped {dropped} degenerate triangles during parsing.", RuntimeWarning
        )
    return out


def _quantize(v: Vec3, tol: float) -> Tuple[int, int, int]:
    inv = 1.0 / tol if tol > 0 else 1e12
    return (int(round(v[0] * inv)), int(round(v[1] * inv)), int(round(v[2] * inv)))


def _dedup_vertices(tris: List[Tri], tol: float) -> Tuple[List[Vec3], List[Tuple[int, int, int]]]:
    index: Dict[Tuple[int, int, int], int] = {}
    verts: List[Vec3] = []
    faces: List[Tuple[int, int, int]] = []
    for a, b, c in tris:
        qa = _quantize(a, tol)
        qb = _quantize(b, tol)
        qc = _quantize(c, tol)
        ia = index.get(qa)
        if ia is None:
            ia = len(verts)
            index[qa] = ia
            verts.append(a)
        ib = index.get(qb)
        if ib is None:
            ib = len(verts)
            index[qb] = ib
            verts.append(b)
        ic = index.get(qc)
        if ic is None:
            ic = len(verts)
            index[qc] = ic
            verts.append(c)
        if ia == ib or ib == ic or ic == ia:
            continue
        faces.append((ia, ib, ic))
    return verts, faces


def _edges_of_face(face: Tuple[int, int, int]) -> List[Tuple[Tuple[int, int], int]]:
    a, b, c = face
    out: List[Tuple[Tuple[int, int], int]] = []
    for u, v in ((a, b), (b, c), (c, a)):
        if u <= v:
            out.append(((u, v), +1))
        else:
            out.append(((v, u), -1))
    return out


def _orient_faces_and_components(
    faces: List[Tuple[int, int, int]], nverts: int
) -> Tuple[
    Dict[int, List[int]],
    List[bool],
    Dict[int, Dict[Tuple[int, int], int]],
    Dict[int, int],
    Dict[int, int],
]:
    edge_to_faces: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
    for fi, f in enumerate(faces):
        for e, d in _edges_of_face(f):
            edge_to_faces.setdefault(e, []).append((fi, d))
    adj: List[List[Tuple[int, int, int]]] = [[] for _ in faces]
    for e, lst in edge_to_faces.items():
        for i in range(len(lst)):
            fi, d1 = lst[i]
            for j in range(i + 1, len(lst)):
                fj, d2 = lst[j]
                adj[fi].append((fj, d1, d2))
                adj[fj].append((fi, d2, d1))
    visited = [False] * len(faces)
    flips = [False] * len(faces)
    components: Dict[int, List[int]] = {}
    edge_counts_per_comp: Dict[int, Dict[Tuple[int, int], int]] = {}
    nonmanifold_edge_counts_per_comp: Dict[int, int] = {}
    orient_conflicts: Dict[int, int] = {}
    comp_id = 0
    for start in range(len(faces)):
        if visited[start]:
            continue
        queue = [start]
        visited[start] = True
        components[comp_id] = []
        edge_counts_per_comp[comp_id] = {}
        nonmanifold_edge_counts_per_comp[comp_id] = 0
        orient_conflicts[comp_id] = 0
        while queue:
            cur = queue.pop()
            components[comp_id].append(cur)
            for e, d in _edges_of_face(faces[cur]):
                edge_counts_per_comp[comp_id][e] = edge_counts_per_comp[comp_id].get(e, 0) + 1
                if len(edge_to_faces[e]) > 2:
                    nonmanifold_edge_counts_per_comp[comp_id] += 1
            for nb, d1, d2 in adj[cur]:
                expected_flip = flips[cur] if d1 != d2 else (not flips[cur])
                if not visited[nb]:
                    visited[nb] = True
                    flips[nb] = expected_flip
                    queue.append(nb)
                else:
                    if flips[nb] != expected_flip:
                        orient_conflicts[comp_id] += 1
        comp_id += 1
    return (
        components,
        flips,
        edge_counts_per_comp,
        nonmanifold_edge_counts_per_comp,
        orient_conflicts,
    )


def _component_volume(
    comp_faces: List[int], flips: List[bool], faces: List[Tuple[int, int, int]], verts: List[Vec3]
) -> float:
    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = float("-inf")
    for fi in comp_faces:
        a, b, c = faces[fi]
        for idx in (a, b, c):
            x, y, z = verts[idx]
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if z < min_z:
                min_z = z
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            if z > max_z:
                max_z = z
    cx = 0.5 * (min_x + max_x)
    cy = 0.5 * (min_y + max_y)
    cz = 0.5 * (min_z + max_z)
    vol = 0.0
    for fi in comp_faces:
        ia, ib, ic = faces[fi]
        if flips[fi]:
            ib, ic = ic, ib
        a = (verts[ia][0] - cx, verts[ia][1] - cy, verts[ia][2] - cz)
        b = (verts[ib][0] - cx, verts[ib][1] - cy, verts[ib][2] - cz)
        c = (verts[ic][0] - cx, verts[ic][1] - cy, verts[ic][2] - cz)
        cxp = b[1] * c[2] - b[2] * c[1]
        cyp = b[2] * c[0] - b[0] * c[2]
        czp = b[0] * c[1] - b[1] * c[0]
        vol += (a[0] * cxp + a[1] * cyp + a[2] * czp) / 6.0
    return vol


def _component_bbox(
    comp_faces: List[int], faces: List[Tuple[int, int, int]], verts: List[Vec3]
) -> Tuple[Vec3, Vec3]:
    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = float("-inf")
    for fi in comp_faces:
        a, b, c = faces[fi]
        for idx in (a, b, c):
            x, y, z = verts[idx]
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if z < min_z:
                min_z = z
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            if z > max_z:
                max_z = z
    return (min_x, min_y, min_z), (max_x, max_y, max_z)


def _component_triangles(
    comp_faces: List[int], faces: List[Tuple[int, int, int]], verts: List[Vec3]
) -> List[Tri]:
    out: List[Tri] = []
    for fi in comp_faces:
        ia, ib, ic = faces[fi]
        out.append((verts[ia], verts[ib], verts[ic]))
    return out


def _bbox_contains(a: Tuple[Vec3, Vec3], b: Tuple[Vec3, Vec3], margin: float) -> bool:
    (ax0, ay0, az0), (ax1, ay1, az1) = a
    (bx0, by0, bz0), (bx1, by1, bz1) = b
    return (
        ax0 - margin <= bx0 <= bx1 <= ax1 + margin
        and ay0 - margin <= by0 <= by1 <= ay1 + margin
        and az0 - margin <= bz0 <= bz1 <= az1 + margin
    )


def _choose_interior_point(
    tris: List[Tri], bbox: Tuple[Vec3, Vec3], eps: float
) -> Optional[Vec3]:
    (mx0, my0, mz0), (mx1, my1, mz1) = bbox
    dx = mx1 - mx0
    dy = my1 - my0
    dz = mz1 - mz0
    diag = math.sqrt(dx * dx + dy * dy + dz * dz)
    if diag <= 0:
        return None
    cx = mx0 + 0.5 * dx
    cy = my0 + 0.5 * dy
    cz = mz0 + 0.5 * dz
    cands: List[Vec3] = []
    cands.append((cx, cy, cz))
    if tris:
        sx = sy = sz = 0.0
        for a, b, c in tris:
            sx += (a[0] + b[0] + c[0]) / 3.0
            sy += (a[1] + b[1] + c[1]) / 3.0
            sz += (a[2] + b[2] + c[2]) / 3.0
        n = float(len(tris))
        cands.append((sx / n, sy / n, sz / n))
    for p in cands:
        if _point_in_mesh(p, tris, eps):
            return p
    step = max(diag * 1e-6, eps * 10.0)
    limit = min(10, len(tris))
    for k in range(limit):
        a, b, c = tris[k]
        ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        ac = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
        nx = ab[1] * ac[2] - ab[2] * ac[1]
        ny = ab[2] * ac[0] - ab[0] * ac[2]
        nz = ab[0] * ac[1] - ab[1] * ac[0]
        nn = math.sqrt(nx * nx + ny * ny + nz * nz)
        if nn <= eps:
            continue
        nx /= nn
        ny /= nn
        nz /= nn
        cc = ((a[0] + b[0] + c[0]) / 3.0, (a[1] + b[1] + c[1]) / 3.0, (a[2] + b[2] + c[2]) / 3.0)
        for sgn in (1.0, -1.0):
            p = (cc[0] + sgn * nx * step, cc[1] + sgn * ny * step, cc[2] + sgn * nz * step)
            if _point_in_mesh(p, tris, eps):
                return p
    return None


def _point_in_mesh(p: Vec3, tris: List[Tri], eps: float) -> bool:
    if not tris:
        return False
    px = p[0] + eps * 0.173
    py = p[1] + eps * 0.349
    pz = p[2] + eps * 0.937
    o = (px, py, pz)
    dirs = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    votes = []
    for d in dirs:
        cnt = 0
        for a, b, c in tris:
            t = _ray_triangle_intersect(o, d, a, b, c, eps)
            if t is not None and t > eps:
                cnt += 1
        votes.append(cnt % 2 == 1)
    truthy = sum(1 for v in votes if v)
    return truthy >= 2


def _ray_triangle_intersect(
    o: Vec3, d: Vec3, a: Vec3, b: Vec3, c: Vec3, eps: float
) -> Optional[float]:
    e1 = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    e2 = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    px = d[1] * e2[2] - d[2] * e2[1]
    py = d[2] * e2[0] - d[0] * e2[2]
    pz = d[0] * e2[1] - d[1] * e2[0]
    det = e1[0] * px + e1[1] * py + e1[2] * pz
    if -eps < det < eps:
        return None
    inv_det = 1.0 / det
    tx = o[0] - a[0]
    ty = o[1] - a[1]
    tz = o[2] - a[2]
    u = (tx * px + ty * py + tz * pz) * inv_det
    if u < -eps or u > 1.0 + eps:
        return None
    qx = ty * e1[2] - tz * e1[1]
    qy = tz * e1[0] - tx * e1[2]
    qz = tx * e1[1] - ty * e1[0]
    v = (d[0] * qx + d[1] * qy + d[2] * qz) * inv_det
    if v < -eps or u + v > 1.0 + eps:
        return None
    t = (e2[0] * qx + e2[1] * qy + e2[2] * qz) * inv_det
    if t <= eps:
        return None
    return t


def _load_stl(path: str) -> List[Tri]:
    try:
        size = _file_size(path)
    except Exception:
        size = None
    if size is not None and size >= 84:
        with open(path, "rb") as f:
            header = f.read(80)
            n_bytes = f.read(4)
            if len(n_bytes) == 4:
                n = struct.unpack("<I", n_bytes)[0]
                expected = 84 + 50 * n
                if expected == size:
                    return _parse_binary_stl(path, n)
    try:
        return _parse_ascii_stl(path)
    except Exception:
        return _parse_binary_streaming(path)


def _file_size(path: str) -> Optional[int]:
    try:
        import os

        return os.path.getsize(path)
    except Exception:
        return None


def _parse_binary_stl(path: str, n: int) -> List[Tri]:
    tris: List[Tri] = []
    with open(path, "rb") as f:
        f.read(84)
        for _ in range(n):
            data = f.read(50)
            if len(data) < 50:
                break
            vals = struct.unpack("<12fH", data)
            nx, ny, nz = vals[0], vals[1], vals[2]
            ax, ay, az = vals[3], vals[4], vals[5]
            bx, by, bz = vals[6], vals[7], vals[8]
            cx, cy, cz = vals[9], vals[10], vals[11]
            v1x, v1y, v1z = (bx - ax, by - ay, bz - az)
            v2x, v2y, v2z = (cx - ax, cy - ay, cz - az)
            crx = v1y * v2z - v1z * v2y
            cry = v1z * v2x - v1x * v2z
            crz = v1x * v2y - v1y * v2x
            dot = crx * nx + cry * ny + crz * nz
            if dot < 0.0:
                tris.append(((ax, ay, az), (cx, cy, cz), (bx, by, bz)))
            else:
                tris.append(((ax, ay, az), (bx, by, bz), (cx, cy, cz)))
    return tris


def _parse_binary_streaming(path: str) -> List[Tri]:
    tris: List[Tri] = []
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 84:
        return tris
    n = struct.unpack("<I", data[80:84])[0]
    pos = 84
    for _ in range(n):
        if pos + 50 > len(data):
            break
        chunk = data[pos : pos + 50]
        vals = struct.unpack("<12fH", chunk)
        nx, ny, nz = vals[0], vals[1], vals[2]
        ax, ay, az = vals[3], vals[4], vals[5]
        bx, by, bz = vals[6], vals[7], vals[8]
        cx, cy, cz = vals[9], vals[10], vals[11]
        v1x, v1y, v1z = (bx - ax, by - ay, bz - az)
        v2x, v2y, v2z = (cx - ax, cy - ay, cz - az)
        crx = v1y * v2z - v1z * v2y
        cry = v1z * v2x - v1x * v2z
        crz = v1x * v2y - v1y * v2x
        dot = crx * nx + cry * ny + crz * nz
        if dot < 0.0:
            tris.append(((ax, ay, az), (cx, cy, cz), (bx, by, bz)))
        else:
            tris.append(((ax, ay, az), (bx, by, bz), (cx, cy, cz)))
        pos += 50
    return tris


def _parse_ascii_stl(path: str) -> List[Tri]:
    tris: List[Tri] = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f
        verts: List[Vec3] = []
        collected = False
        cur_n: Optional[Vec3] = None
        for line in lines:
            s = line.strip()
            if not s:
                continue
            if s.startswith("vertex"):
                parts = s.split()
                if len(parts) >= 4:
                    try:
                        x = float(parts[1])
                        y = float(parts[2])
                        z = float(parts[3])
                        verts.append((x, y, z))
                    except ValueError:
                        continue
            elif s.startswith("endloop"):
                if not collected and len(verts) >= 3:
                    a, b, c = verts[-3], verts[-2], verts[-1]
                    if cur_n is not None:
                        v1 = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
                        v2 = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
                        crx = v1[1] * v2[2] - v1[2] * v2[1]
                        cry = v1[2] * v2[0] - v1[0] * v2[2]
                        crz = v1[0] * v2[1] - v1[1] * v2[0]
                        dot = crx * cur_n[0] + cry * cur_n[1] + crz * cur_n[2]
                        if dot < 0.0:
                            b, c = c, b
                    tris.append((a, b, c))
                    collected = True
            elif s.startswith("facet"):
                verts.clear()
                collected = False
                cur_n = None
                parts = s.split()
                if len(parts) >= 5 and parts[0] == "facet" and parts[1] == "normal":
                    try:
                        cur_n = (float(parts[2]), float(parts[3]), float(parts[4]))
                    except Exception:
                        cur_n = None
    if not tris:
        with open(path, "rb") as fb:
            data = fb.read(84)
            if data[:5].lower() == b"solid":
                warnings.warn("STL appears ASCII but no facets parsed; attempting binary.", RuntimeWarning)
        return _parse_binary_streaming(path)
    return tris


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stl_volume.py <path-to-stl> [tolerance]")
        sys.exit(1)
    p = sys.argv[1]
    tol = None
    if len(sys.argv) >= 3:
        try:
            tol = float(sys.argv[2])
        except Exception:
            tol = None
    vol = calculate_stl_volume(p, tolerance=tol)
    print(f"{vol}")
