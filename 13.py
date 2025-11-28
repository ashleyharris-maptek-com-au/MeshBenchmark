import VolumeComparison as vc
import os
title = "Hide and seek behind a building"

promptChangeSummary = "Varying crowd size and building dimensions"

subpassParamSummary = [
    "4 people, 5m building",
    "20 people, 10m building",
    "40 people, 15m building", 
    "80 people, 17m building",
    "150 people, 20m building"
]

prompt = """
You have a building at the origin, axis aligned, PARAM_B meters wide and deep, and 30 meters tall.

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
                ]
            }
        }
    },
    "propertyOrdering": [
        "people"
    ]
}

def prepareSubpassPrompt(index):
    if index == 0: return prompt.replace("PARAM_A", "4").replace("PARAM_B", "5")
    if index == 1: return prompt.replace("PARAM_A", "20").replace("PARAM_B", "10")
    if index == 2: return prompt.replace("PARAM_A", "40").replace("PARAM_B", "15")
    if index == 3: return prompt.replace("PARAM_A", "80").replace("PARAM_B", "17")
    if index == 4: return prompt.replace("PARAM_A", "150").replace("PARAM_B", "20")
    raise StopIteration

def resultToImage(result, subPass, aiEngineName : str):
    buildingWidth = 5  # Default width for subpass 0
    if subPass == 1:
        buildingWidth = 10
    elif subPass == 2:
        buildingWidth = 15
    elif subPass == 3:
        buildingWidth = 17
    elif subPass == 4:
        buildingWidth = 20

    openScadData = f"translate([0, 0, 15]) color([0,1,0]) cube([{buildingWidth}, {buildingWidth}, 30], center=true);\n"

    for person in result["people"]:
        x, y = person["xy"]
        openScadData += f"translate([{x}, {y}, 1]) color([1,0,0]) cube([0.5, 0.5, 2], center=true);\n"

    output_path = f"results/13_Visualization_{aiEngineName}_subpass{subPass}.png"
    vc.render_scadText_to_png(openScadData, output_path, "--camera=100,100,20,0,0,20")
    print(f"Saved visualization to {output_path}")
    return output_path

def gradeAnswer(result, subPass, aiEngineName : str):
    buildingWidth = 5  # Default width for subpass 0
    if subPass == 1:
        buildingWidth = 10
    elif subPass == 2:
        buildingWidth = 15
    elif subPass == 3:
        buildingWidth = 17
    elif subPass == 4:
        buildingWidth = 20

    expectedPopulationSize = [4, 20, 40, 80, 150][subPass]
    actualPopulationSize = len(result.get("people", []))
    if actualPopulationSize != expectedPopulationSize:
        print(f"Expected {expectedPopulationSize} people, got {actualPopulationSize}")
        return 0.0

    for person in result["people"]:
        x, y = person["xy"]
        distance_from_center = (x**2 + y**2)**0.5
        if distance_from_center > 30:
            print(f"Person at ({x}, {y}) is too far from center: {distance_from_center}")
            return 0  # Person is too far from building center

    # Check for overlaps between people
    for i, person1 in enumerate(result["people"]):
        x1, y1 = person1["xy"]
        for j, person2 in enumerate(result["people"][i+1:], i+1):
            x2, y2 = person2["xy"]
            distance_between = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            if distance_between < 0.5:  # People overlap
                print(f"Overlap detected between person {i} and person {j}")
                return 0

    # Check for intersection people and the building
    building_half_width = buildingWidth / 2
    for person in result["people"]:
        x, y = person["xy"]
        if (abs(x) <= building_half_width + 0.25) and (abs(y) <= building_half_width + 0.25):
            print(f"Person at ({x}, {y}) intersects with building")
            return 0  # Person intersects with building

    path = resultToImage(result, subPass, aiEngineName)

    import PIL.Image
    img = PIL.Image.open(path)

    # search for any red pixels (people)
    pixels = img.load()
    score = 1.0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            if r > g and r > b and g < 50 and b < 50:  # Red pixel
                score -= 0.005

    return max(0.0, score)  # Ensure non-negative score

def resultToNiceReport(result, subPass, aiEngineName : str):
    path = resultToImage(result, subPass, aiEngineName)
    return f"<img src='{os.path.basename(path)}' alt='Subpass {subPass} visualization' style='max-width: 100%;' />"
