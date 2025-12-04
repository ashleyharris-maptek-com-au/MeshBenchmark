skip = True

title = "Cage match. Can LLMs design interlocking parts for 3D printing?"

prompt = """

I would like you to generate a cage of internal size 350 x 350 x 700 mm. 

The cage should feature an all-around grid of 10mm thick bars, each with a square cross section. No thinner, no thicker.

The gap between bars should be between 5cm and 10cm, and uniform all over the model.

The cage needs to be split into parts that can be 3D printed on a 3D printer, with a build area
of 400x400x100mm.

The cage assembly should be held together by 4 x M6 threaded rods threaded through the middle
of the 4 vertical corner bars. You do not need to carve a female thread or nut slots into your parts,
but should ensure that a rod fits with adequete clearence into every hole. Use no additional connectors.

Generate all .stl files that are needed for this project. They should be:
- valid STL files
- ready to slice
- print without supports.
- orientated such that they fit within the build volume
- sitting on z=0 plane.
- not going to fall over during printing.

For each part, include a rigid transform matrix that shows where the part sits in 3D space when assembled, in
your assembled 3D space, the cage sits on the z=0 plane and centred in x & y around 0,0.
Take care to get this projection right as it will be used to test whether the parts fit together correctly. 

"""

structure = {
    "type": "object",
    "properties": {
        "reasoning" : {"type": "string"},
        "parts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "stl": {
                        "type": "string",
                        "description": "The STL file for this part to be sent to the slicer. First word is typically 'solid' and last line starts with 'endsolid'."
                    },
                    "transform": {
                        "type": "array",
                        "items": {
                            "type": "number",
                            "description": "The 4x4 transform matrix for this part. Must be a rigid transform (no scale or skew)."
                        }
                    }
                },
                "required": ["stl", "transform"],
                "additionalProperties": False,
                "propertyOrdering": ["stl", "transform"]
            }
        }
    },
    "required": ["parts","reasoning"],
    "propertyOrdering": ["reasoning", "parts"],
    "additionalProperties": False
}