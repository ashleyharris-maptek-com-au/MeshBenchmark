import VolumeComparison as vc
import os
title = "Hide and seek behind a building"

promptChangeSummary = "Varying crowd size and building dimensions"

subpassParamSummary = [
    "4 people, 2m building",
    "20 people, 4m building",
    "40 people, 6m building", 
    "80 people, 8m building",
    "150 people, 10m building",
    "200 people, 7m building",
]

prompt = """
You have a building at the origin, axis aligned, PARAM_B meters wide and deep, and 10 meters tall.

A sniper is located at (100,100,20) and is looking at the building.

Position a crowd of PARAM_A people (represented by a 0.5*0.5*2m axis aligned bounding box resting on the z=0 plane) 
in such a way that:
- the sniper can not see any of them due to the building blocking their line of sight.
- the people must be positioned entirely on the ground (z=0).
- the people must not overlap with the building or each other.
- nobody is more than 30 meters away from the building's center.
"""

structure = {
    "type": "object",
    "properties": {
        "people": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "xy": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    }
                },
                "propertyOrdering": [
                    "xy"
                ],
                "required": [
                    "xy"
                ],
                "additionalProperties": False,
            }
        }
    },
    "additionalProperties": False,
    "propertyOrdering": [
        "people"
    ],
    "required": [
        "people"
    ]
}

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "4").replace("PARAM_B", "2")
    if index == 1: return prompt.replace("PARAM_A", "20").replace("PARAM_B", "4")
    if index == 2: return prompt.replace("PARAM_A", "40").replace("PARAM_B", "6")
    if index == 3: return prompt.replace("PARAM_A", "80").replace("PARAM_B", "8")
    if index == 4: return prompt.replace("PARAM_A", "150").replace("PARAM_B", "10")
    if index == 5: return prompt.replace("PARAM_A", "200").replace("PARAM_B", "7")
    raise StopIteration

def resultToImage(result, subPass, aiEngineName : str, fromAbove : bool = False):
    buildingWidth = 2  # Default width for subpass 0
    if subPass == 1:
        buildingWidth = 4
    elif subPass == 2:
        buildingWidth = 6
    elif subPass == 3:
        buildingWidth = 8
    elif subPass == 4:
        buildingWidth = 10
    elif subPass == 5:
        buildingWidth = 7

    openScadData = f"translate([0, 0, 5]) color([0,1,0,0.9]) cube([{buildingWidth}, {buildingWidth}, 10], center=true);\n"

    for person in result["people"]:
        x, y = person["xy"]
        openScadData += f"translate([{x}, {y}, 1]) color([1,0,0]) cube([0.5, 0.5, 2], center=true);\n"

    output_path = f"results/13_Visualization_{aiEngineName}_subpass{subPass}_{fromAbove}.png"
    vc.render_scadText_to_png(openScadData, output_path, "--camera=100,100,20,0,0,2" if not fromAbove else "--camera=-10,-10,200,0,0,20")
    print(f"Saved visualization to {output_path}")
    return output_path

def gradeAnswer(result, subPass, aiEngineName : str):
    buildingWidth = 2  # Default width for subpass 0
    if subPass == 1:
        buildingWidth = 4
    elif subPass == 2:
        buildingWidth = 6
    elif subPass == 3:
        buildingWidth = 8
    elif subPass == 4:
        buildingWidth = 10
    elif subPass == 5:
        buildingWidth = 7

    expectedPopulationSize = [4, 20, 40, 80, 150, 200][subPass]
    actualPopulationSize = len(result.get("people", []))
    if actualPopulationSize != expectedPopulationSize:
        return 0.0, f"Expected {expectedPopulationSize} people, got {actualPopulationSize}"

    for person in result["people"]:
        x, y = person["xy"]
        distance_from_center = (x**2 + y**2)**0.5
        if distance_from_center > 30:
            return 0, f"Person at ({x}, {y}) is too far from center: {distance_from_center}"

    # Check for overlaps between people
    for i, person1 in enumerate(result["people"]):
        x1, y1 = person1["xy"]
        for j, person2 in enumerate(result["people"][i+1:], i+1):
            x2, y2 = person2["xy"]
            distance_between = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            if distance_between < 0.5:  # People overlap
                return 0, f"Overlap detected between person {i} and person {j}"

    # Check for intersection people and the building
    building_half_width = buildingWidth / 2
    for person in result["people"]:
        x, y = person["xy"]
        if (abs(x) <= building_half_width + 0.25) and (abs(y) <= building_half_width + 0.25):
            return 0, f"Person at ({x}, {y}) intersects with building"

    path = resultToImage(result, subPass, aiEngineName)

    import PIL.Image
    img = PIL.Image.open(path)

    # search for any red pixels (people)
    pixels = img.load()
    score = 1.0
    visible_pixels = 0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            if r > g and r > b and g < 50 and b < 50:  # Red pixel
                score -= 0.005
                visible_pixels += 1

    final_score = max(0.0, score)
    if visible_pixels > 0:
        return final_score, f"{visible_pixels} red pixels visible (people partially visible to sniper)"
    return final_score, f"All {actualPopulationSize} people hidden from sniper"

def resultToNiceReport(result, subPass, aiEngineName : str):
    path = resultToImage(result, subPass, aiEngineName)
    path2 = resultToImage(result, subPass, aiEngineName, True)
    return \
        "<img src='" + os.path.basename(path) + "' alt='Subpass " + str(subPass) + " visualization' style='max-width: 100%;' />" + \
        "<img src='" + os.path.basename(path2) + "' alt='Subpass " + str(subPass) + " visualization from above' style='max-width: 100%;' />"
