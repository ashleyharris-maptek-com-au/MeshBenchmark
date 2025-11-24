prompt = """
You have a building at the origin, axis aligned, PARAM_B meters wide and deep, and 30 meters tall.

A sniper is located at (100,100,20) and is looking at the building.

Position a crowd of PARAM_A people (represented by a 0.5*0.5*2m axis aligned bounding box resting on the z=0 plane) in such a way that
the sniper can not see any of them due to the building blocking their line of site.
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
    if index == 0: return prompt.replace("PARAM_A", "20").replace("PARAM_B", "10")
    if index == 1: return prompt.replace("PARAM_A", "40").replace("PARAM_B", "15")
    if index == 2: return prompt.replace("PARAM_A", "80").replace("PARAM_B", "20")
    if index == 3: return prompt.replace("PARAM_A", "150").replace("PARAM_B", "25")
    raise StopIteration
