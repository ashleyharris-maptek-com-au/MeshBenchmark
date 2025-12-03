import math,itertools
import VolumeComparison as vc

title = "Rollercoaster Track planner"

prompt = """

You are given a 3D space of dimensions {PARAM_A} * {PARAM_A} * {PARAM_A} meters, and have to build a rollercoaster track that
meets the following requirements:

- Starts at altitude Z = {PARAM_B} meters
- Minimum track length: {PARAM_C}
- Must exceed a speed of at least: {PARAM_D}
- Must not exceed a speed of 40m/s
- Once up to speed, must not drop below a speed of 5m/s
- Must finish at altitude Z = 0 meters
- Must not use any acceleration other than Earth's gravity.
- Must not exceed 5G acceleration when turning.

{PARAM_E}

Track segments are represented by a list of points, where each point is a list of [x, y, z] coordinates.

Track layout must follow these rules:
- No segment longer than 1.8m.
- No segment shorter than 90cm
- The angle between 2 segments must not exceed 10 degrees.
- When crossing existing track, a vertical clearence of 3m minimum is required.
- All track segments must be within 0,0,0 -> {PARAM_A},{PARAM_A},{PARAM_A}

You do not need to consider support positions at this stage of the planning.

Assume frictionless vacuum for all track segments except loops. 
A full loop results in a halving of speed.

Return the track as a list of points, where each point is a list of [x, y, z] coordinates.

"""

PARAM_A = [10, 15, 20, 50, 100, 300]
PARAM_B = [5, 9, 19, 48, 95, 250]
PARAM_C = [12, 100, 200, 500, 1000, 3000]
PARAM_D = [5, 8, 12, 15, 20, 25]
PARAM_E = [
    "", 
    "",
    "Must include at least 1 turn of at least 2 G acceleration.", 
    "Any track below z = 5 must avoid x,y=25,25 by a 10m margin", 
    "Must include at least 1 loop", 
    "Must include at least 3 loops"]

structure = {
    "type": "object",
    "properties": {
        "trackPoints": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "number"
                },
                "description": "XYZ position of a track point"
            }
        }
    },
    "propertyOrdering": [
        "trackPoints"
    ],
    "required": [
        "trackPoints"
    ],
    "additionalProperties": False
}

subpassParamSummary = [
    "Very basic. 10m cube. 5m start altitude. 12m length. 5m/s speed min. ",
    "15m cube, start at 9m, 100m length. 5m/s min speed. Must exceed 8m/s at least once.", 
    "20m cube, start at 19m, 200m length. 2G turn.", 
    "50m cube, start at 48m, 500m length. Avoid centre cylinder at ground.", 
    "100m cube, start at 95m, 1000m length. Must include a loop.", 
    "300m cube, start at 250m, 3000m length. Must include 3 loops."]

def prepareSubpassPrompt(index: int) -> str:
    if index == 0: return prompt.format(PARAM_A=PARAM_A[0], PARAM_B=PARAM_B[0], PARAM_C=PARAM_C[0], PARAM_D=PARAM_D[0], PARAM_E=PARAM_E[0])
    if index == 1: return prompt.format(PARAM_A=PARAM_A[1], PARAM_B=PARAM_B[1], PARAM_C=PARAM_C[1], PARAM_D=PARAM_D[1], PARAM_E=PARAM_E[1])
    if index == 2: return prompt.format(PARAM_A=PARAM_A[2], PARAM_B=PARAM_B[2], PARAM_C=PARAM_C[2], PARAM_D=PARAM_D[2], PARAM_E=PARAM_E[2])
    if index == 3: return prompt.format(PARAM_A=PARAM_A[3], PARAM_B=PARAM_B[3], PARAM_C=PARAM_C[3], PARAM_D=PARAM_D[3], PARAM_E=PARAM_E[3])
    if index == 4: return prompt.format(PARAM_A=PARAM_A[4], PARAM_B=PARAM_B[4], PARAM_C=PARAM_C[4], PARAM_D=PARAM_D[4], PARAM_E=PARAM_E[4])
    if index == 5: return prompt.format(PARAM_A=PARAM_A[5], PARAM_B=PARAM_B[5], PARAM_C=PARAM_C[5], PARAM_D=PARAM_D[5], PARAM_E=PARAM_E[5])
    raise StopIteration

def gradeAnswer(answer: dict, subPass: int, aiEngineName: str):
    G = 9.81  # Earth gravity m/s²
    MAX_SPEED = 40.0
    MIN_SPEED_ONCE_MOVING = 5.0
    MAX_G_FORCE = 5.0
    MIN_SEGMENT_LEN = 0.9
    MAX_SEGMENT_LEN = 1.8
    MAX_ANGLE_DEG = 10.0
    CROSSING_CLEARANCE = 3.0
    
    maxSize = PARAM_A[subPass]
    startAltitude = PARAM_B[subPass]
    minLength = PARAM_C[subPass]
    minSpeed = PARAM_D[subPass]
    minLoopCount = 1 if subPass == 3 else 3 if subPass == 4 else 0
    require2GTurn = (subPass == 1)
    avoidCentre = (subPass == 2)
    
    trackPoints = answer.get("trackPoints", [])
    
    if len(trackPoints) < 2:
        return 0, "Track must have at least 2 points"
    
    # Parse points
    points = []
    for i, pt in enumerate(trackPoints):
        if not isinstance(pt, (list, tuple)) or len(pt) < 3:
            return 0, f"Point {i} is invalid: {pt}"
        try:
            points.append((float(pt[0]), float(pt[1]), float(pt[2])))
        except (TypeError, ValueError):
            return 0, f"Point {i} has non-numeric coordinates: {pt}"
    
    errors = []
    warnings = []
    
    # Check start altitude
    if abs(points[0][2] - startAltitude) > 0.5:
        errors.append(f"Start altitude {points[0][2]:.2f}m != required {startAltitude}m")
    
    # Check end altitude
    if abs(points[-1][2]) > 0.5:
        errors.append(f"End altitude {points[-1][2]:.2f}m != required 0m")
    
    # Validate bounds
    for i, (x, y, z) in enumerate(points):
        if x < 0 or x > maxSize or y < 0 or y > maxSize or z < 0 or z > maxSize:
            errors.append(f"Point {i} ({x:.1f},{y:.1f},{z:.1f}) out of bounds [0,{maxSize}]")
            if len(errors) > 5:
                errors.append("...more bound errors")
                break
    
    # Calculate segments and validate geometry
    segments = []
    total_length = 0.0
    
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        dx, dy, dz = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
        seg_len = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        if seg_len < 0.001:
            errors.append(f"Segment {i} has zero length")
            continue
            
        segments.append((dx, dy, dz, seg_len))
        total_length += seg_len
        
        if seg_len < MIN_SEGMENT_LEN:
            errors.append(f"Segment {i} too short: {seg_len:.2f}m < {MIN_SEGMENT_LEN}m")
        if seg_len > MAX_SEGMENT_LEN:
            errors.append(f"Segment {i} too long: {seg_len:.2f}m > {MAX_SEGMENT_LEN}m")
    
    # Check angles between consecutive segments
    for i in range(len(segments) - 1):
        d1 = segments[i]
        d2 = segments[i + 1]
        len1, len2 = d1[3], d2[3]
        if len1 > 0 and len2 > 0:
            dot = (d1[0]*d2[0] + d1[1]*d2[1] + d1[2]*d2[2]) / (len1 * len2)
            dot = max(-1, min(1, dot))  # Clamp for numerical stability
            angle_deg = math.degrees(math.acos(dot))
            if angle_deg > MAX_ANGLE_DEG:
                errors.append(f"Angle at point {i+1}: {angle_deg:.1f}° > {MAX_ANGLE_DEG}°")
    
    # Check track length
    if total_length < minLength - 0.1:
        errors.append(f"Track length {total_length:.1f}m < required {minLength}m")
    
    # Check for track crossings (simplified: check all segment pairs for XY proximity with Z clearance)
    for i in range(len(points)):
        for j in range(i + 3, len(points)):  # Skip adjacent segments
            p1, p2 = points[i], points[j]
            xy_dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
            z_diff = abs(p1[2] - p2[2])
            if xy_dist < 1.0 and z_diff < CROSSING_CLEARANCE:
                errors.append(f"Crossing violation: points {i} and {j} too close (XY:{xy_dist:.1f}m, Z:{z_diff:.1f}m)")
                break
    
    # Subpass 2: Avoid centre cylinder when z < 5
    if avoidCentre:
        for i, (x, y, z) in enumerate(points):
            if z < 5:
                dist_from_centre = math.sqrt((x - 25)**2 + (y - 25)**2)
                if dist_from_centre < 10:
                    errors.append(f"Point {i} at z={z:.1f}m violates 10m margin from (25,25)")
    
    # Physics simulation
    speed = 0.0
    max_speed_reached = 0.0
    has_been_up_to_speed = False
    max_g_force_reached = 0.0
    has_2g_turn = False
    loop_count = 0
    cumulative_vertical_angle = 0.0
    prev_vertical_direction = None
    
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        dz = p2[2] - p1[2]
        seg_len = segments[i][3] if i < len(segments) else 0
        
        if seg_len < 0.001:
            continue
        
        # Energy conservation: v² = v₀² + 2g*Δh (Δh is drop, so negative dz)
        # v² = v₀² - 2g*dz
        v_squared = speed * speed - 2 * G * dz
        
        if v_squared < 0:
            errors.append(f"Physics violation at segment {i}: insufficient energy to climb (speed={speed:.1f}m/s, climb={dz:.1f}m)")
            v_squared = 0
        
        speed = math.sqrt(v_squared)
        max_speed_reached = max(max_speed_reached, speed)
        
        # Check speed limits
        if speed > MAX_SPEED:
            errors.append(f"Speed {speed:.1f}m/s exceeds max {MAX_SPEED}m/s at segment {i}")
        
        if speed >= minSpeed:
            has_been_up_to_speed = True
        
        if has_been_up_to_speed and speed < MIN_SPEED_ONCE_MOVING:
            errors.append(f"Speed dropped to {speed:.1f}m/s < {MIN_SPEED_ONCE_MOVING}m/s after reaching speed, at segment {i}")
        
        # Calculate centripetal acceleration (turning G-force)
        if i < len(segments) - 1 and speed > 0.1:
            d1 = segments[i]
            d2 = segments[i + 1]
            len1, len2 = d1[3], d2[3]
            
            if len1 > 0 and len2 > 0:
                # Direction change
                dir1 = (d1[0]/len1, d1[1]/len1, d1[2]/len1)
                dir2 = (d2[0]/len2, d2[1]/len2, d2[2]/len2)
                
                # Angle between directions
                dot = dir1[0]*dir2[0] + dir1[1]*dir2[1] + dir1[2]*dir2[2]
                dot = max(-1, min(1, dot))
                angle_rad = math.acos(dot)
                
                # Approximate radius of curvature: r ≈ segment_length / angle
                if angle_rad > 0.001:
                    avg_seg_len = (len1 + len2) / 2
                    radius = avg_seg_len / angle_rad
                    
                    # Centripetal acceleration: a = v²/r
                    centripetal_accel = (speed * speed) / radius
                    g_force = centripetal_accel / G
                    max_g_force_reached = max(max_g_force_reached, g_force)
                    
                    if g_force >= 2.0:
                        has_2g_turn = True
                    
                    if g_force > MAX_G_FORCE:
                        errors.append(f"G-force {g_force:.1f}G exceeds {MAX_G_FORCE}G at segment {i}")
                
                # Track vertical direction for loop detection
                vertical_angle = math.degrees(math.asin(max(-1, min(1, dir2[2]))))
                if prev_vertical_direction is not None:
                    angle_change = vertical_angle - prev_vertical_direction
                    cumulative_vertical_angle += angle_change
                    
                    # A complete loop is ~360° of vertical rotation
                    if abs(cumulative_vertical_angle) >= 360:
                        loop_count += 1

                        # Halve the speed. We allow the carriage to drop below 5m/s for this section.
                        speed /= 2
                        has_been_up_to_speed = False

                        cumulative_vertical_angle = cumulative_vertical_angle % 360
                
                prev_vertical_direction = vertical_angle
    
    # Check minimum speed reached
    if max_speed_reached < minSpeed:
        errors.append(f"Max speed {max_speed_reached:.1f}m/s < required {minSpeed}m/s")
    
    # Check 2G turn requirement (subpass 1)
    if require2GTurn and not has_2g_turn:
        errors.append(f"No 2G turn found (max G-force: {max_g_force_reached:.1f}G)")
    
    # Check loop requirements (subpass 3, 4)
    if minLoopCount > 0 and loop_count < minLoopCount:
        errors.append(f"Only {loop_count} loops detected, need {minLoopCount}")
    
    # Build reasoning
    reasoning = f"Track: {len(points)} points, {total_length:.1f}m length\n"
    reasoning += f"Max speed: {max_speed_reached:.1f}m/s\nMax cornering G-force: {max_g_force_reached:.1f}G\n"
    if loop_count > 0:
        reasoning += f"Loops detected: {loop_count}\n"
    
    if errors:
        # Cap errors shown
        if len(errors) > 10:
            shown_errors = errors[:10] + [f"...and {len(errors)-10} more errors"]
        else:
            shown_errors = errors
        reasoning += "ERRORS:\n- " + "\n- ".join(shown_errors)
        return 0, reasoning
    
    # Score based on track quality
    score = 1.0
    reasoning += "All requirements met!"
    
    return score, reasoning


def resultToNiceReport(answer, subPass, aiEngineName):
    scadOutput = ""
    for a,b in itertools.pairwise(answer["trackPoints"]):
        xMid = (a[0] + b[0])/2
        yMid = (a[1] + b[1])/2
        zMid = (a[2] + b[2])/2

        scadOutput += f"""
hull() {{
    translate([{a[0]* 0.9 + xMid*0.1}, {a[1]* 0.9 + yMid*0.1}, {a[2]* 0.9 + zMid*0.1}]) cube([0.4, 0.4, 0.1], center=true);
    translate([{b[0]* 0.9 + xMid*0.1}, {b[1]* 0.9 + yMid*0.1}, {b[2]* 0.9 + zMid*0.1}]) cube([0.4, 0.4, 0.1], center=true);
}}

"""

    import os
    os.makedirs("results", exist_ok=True)
    output_path = "results/21_Visualization_" + aiEngineName + "_" + str(len(answer["trackPoints"])) + ".png"
    vc.render_scadText_to_png(scadOutput, output_path)
    print(f"Saved visualization to {output_path}")

    return f"""
<a href="{os.path.basename(output_path).replace(".png", "temp.scad")}" download>
<img src="{os.path.basename(output_path)}" alt="Rollercoaster Visualization" style="max-width: 100%;">
</a>
"""
