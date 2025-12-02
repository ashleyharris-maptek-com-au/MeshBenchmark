import os
import VolumeComparison as vc

title = "Painting a 3D scene in ASCII, with lighting."

subpassParamSummary = ["16x16", "32x32", "64x64", "128x128", "256x256"]

promptChangeSummary = "Higher and higher resolution ASCII art."

prompt = """
You are a painter, you have a canvas of size PARAM_A * PARAM_A pixels.

You are painting a scene from the north east, at a 45 degree angle looking down. You are using an orthographic projection.

The scene contains 5 axis aligned cubes, each with a side length of 1 unit. The cubes bottom-centres are placed at the vertices of a 
regular pentagram of side length 5 units, centred at the origin, aligned so it's 'pointing' positive y, 
and is centred in the middle of your painting.

Your painting is zoomed such that the outer edges of the cubes touch the edges of the canvas.

Return the canvas as a string, with:
- # representing a surface facing up (the top plane of a cube)
- " representing a surface facing east or west.
- ' representing a surface facing north or south.
- (space) representing unpainted pixels, the ground, sky, pentagram or anything else.
"""

structure = {
    "type" : "object",
    "properties" : {
        "reasoning" : { "type" : "string"},
        "painting" : { "type" : "string"}
    },
    "additionalProperties": False,
    "propertyOrdering": [
        "reasoning",
        "painting"
    ],
    "required": [
        "reasoning",
        "painting"
    ]
}

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "16")
    if index == 1: return prompt.replace("PARAM_A", "32")
    if index == 2: return prompt.replace("PARAM_A", "64")
    if index == 3: return prompt.replace("PARAM_A", "128")
    if index == 4: return prompt.replace("PARAM_A", "256")
    raise StopIteration

def generateReferencePicture(aiEngineName : str):
    os.makedirs("results", exist_ok=True)
    # For now, we'll create a simple placeholder scad_content
    scad_content = """
    
    for (i = [0:4]) {
        union() {
            // Draw each cube as a 3D object
            translate([5 * sin(i * 72), 5 * cos(i * 72), 0.5]) cube([1, 1, 1],center=true);
        }
    }

     """
    output_path = "results/10_" + aiEngineName + "_Visualization.png"
    vc.render_scadText_to_png(scad_content, output_path, "--camera=100,100,100,0,0,0")
    print(f"Saved visualization to {output_path}")

#generateReferencePicture()

def generateReferenceAscii(gridSize : int, aiEngineName : str):
    from PIL import Image
    import numpy as np
    
    if not os.path.exists("results/10_" + aiEngineName + "_Visualization.png"):
        generateReferencePicture(aiEngineName)
    
    # Load the PNG file
    img = Image.open("results/10_" + aiEngineName + "_Visualization.png")
    img_array = np.array(img.convert("RGB"))
    
    # Find bounding box by removing black edges
    # Identify non-black pixels (where any RGB channel > threshold)
    non_black = np.any(img_array > 10, axis=2)
    rows = np.any(non_black, axis=1)
    cols = np.any(non_black, axis=0)
    
    if not rows.any() or not cols.any():
        # Image is all black
        return " " * (gridSize * (gridSize + 1))
    
    row_min, row_max = np.where(rows)[0][[0, -1]]
    col_min, col_max = np.where(cols)[0][[0, -1]]
    
    # Crop to non-black region
    cropped = img_array[row_min:row_max+1, col_min:col_max+1]
    
    # Resize to gridSize x gridSize
    cropped_img = Image.fromarray(cropped)
    resized_img = cropped_img.resize((gridSize, gridSize), Image.Resampling.NEAREST)
    resized_array = np.array(resized_img)
    
    # Find unique colors
    pixels = resized_array.reshape(-1, 3)
    unique_colors = np.unique(pixels, axis=0)
    
    # Map colors to characters
    # We need to identify which color corresponds to which face type
    # Typically: brightest = top (#), medium shades = sides (" and '), darkest = background (space)
    color_brightness = {tuple(color): np.sum(color) for color in unique_colors}
    sorted_colors = sorted(color_brightness.items(), key=lambda x: x[1], reverse=True)
    
    # Assign characters based on brightness (top is brightest, sides are medium, background is darkest)
    char_map = {}
    if len(sorted_colors) >= 4:
        char_map[sorted_colors[0][0]] = '#'  # Brightest - top face
        char_map[sorted_colors[1][0]] = '"'  # Second - east/west face
        char_map[sorted_colors[2][0]] = "'"  # Third - north/south face
        for i in range(3, len(sorted_colors)):
            char_map[sorted_colors[i][0]] = ' '  # Rest - background
    elif len(sorted_colors) == 3:
        char_map[sorted_colors[0][0]] = '#'
        char_map[sorted_colors[1][0]] = '"'
        char_map[sorted_colors[2][0]] = ' '
    elif len(sorted_colors) == 2:
        char_map[sorted_colors[0][0]] = '#'
        char_map[sorted_colors[1][0]] = ' '
    else:
        char_map[sorted_colors[0][0]] = ' '
    
    # Generate ASCII art
    ascii_lines = []
    for row in resized_array:
        line = ''.join(char_map.get(tuple(pixel), ' ') for pixel in row)
        ascii_lines.append(line)
    
    return '\n'.join(ascii_lines)

def gradeAnswer(answer: dict, subPass: int, aiEngineName: str):
    # Get the reference ASCII for the given subpass
    gridSize = 16 if subPass == 0 else 32 if subPass == 1 else 64 if subPass == 2 else 128 if subPass == 3 else 256
    reference = generateReferenceAscii(gridSize, aiEngineName)
    
    answer_lines = answer["painting"].strip().split('\n')
    reference_lines = reference.strip().split('\n')
    
    if len(answer_lines) != len(reference_lines):
        return 0.0, f"Line count mismatch: got {len(answer_lines)}, expected {len(reference_lines)}"
    
    correct = 0
    total = 0
    
    for a_line, r_line in zip(answer_lines, reference_lines):
        a_line = a_line.ljust(gridSize, ' ')
        r_line = r_line.ljust(gridSize, ' ')
        for a_char, r_char in zip(a_line, r_line):
            if a_char == r_char:
                correct += 1
            total += 1
    
    score = correct / total if total > 0 else 0.0
    return score, f"Matched {correct}/{total} characters ({score*100:.1f}%)"

def resultToNiceReport(answer: dict, subPass: int, aiEngineName: str):
    if subPass < 2:
      html = "<div style='font:monospace;font-size:12px;line-height:12px;'>"
    elif subPass < 4:
      html = "<div style='font:monospace;font-size:4px;line-height:4px;'>"
    else:
      html = "<div style='font:monospace;font-size:1px;line-height:1px;'>"


    # Get the reference ASCII for the given subpass
    gridSize = 16 if subPass == 0 else 32 if subPass == 1 else 64 if subPass == 2 else 128 if subPass == 3 else 256
    reference = generateReferenceAscii(gridSize, aiEngineName)    
    
    answer_lines = answer["painting"].lstrip("\n").rstrip().split('\n')
    reference_lines = reference.lstrip("\n").rstrip().split('\n')
    
    if len(answer_lines) != len(reference_lines):
        html += "<td><pre style='font:monospace;font-size:4px;line-height:4px;'>" + "\n".join(answer_lines) + "</pre>"
        html += f"</td><td>Answer has {len(answer_lines)} lines, reference has {len(reference_lines)} lines.</td>"
        return html
    
    for a_line, r_line in zip(answer_lines, reference_lines):
        a_line = a_line.ljust(gridSize, ' ')
        r_line = r_line.ljust(gridSize, ' ')
        for a_char, r_char in zip(a_line, r_line):
            if a_char == r_char:
                html += f"<span style='color:green;width:1ch;display:inline-block'>{a_char}</span>"
            elif r_char == ' ':
                html += f"<span style='color:red;width:1ch;display:inline-block'>{a_char}</span>"
            elif a_char == ' ':
                html += f"<span style='color:red;width:1ch;display:inline-block'>{r_char}</span>"
            else:
                html += f"<span style='color:orange;width:1ch;display:inline-block'>{a_char}</span>"
        html += "<br>"
    
    html += "</div>"
    return html

