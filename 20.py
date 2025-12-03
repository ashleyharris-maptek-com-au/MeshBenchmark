import sys, base64, io
from PIL import Image
import numpy as np
import re

title = "Can you trace a rough map of Australia with under 1kb of data?"

prompt = """
Create a < CODE_SIZE snippet of python code that exports a function 'f', taking 2 parameters (x and y),
that when executed returns a parametric THING_TO_RETURN.

f(x,y) > 0 represents "inside".
f(x,y) <= 0 represents "outside".
Use a mercartor projection to project from spherical to 2D.
Scale the 2D shape such that it fits within a normalised 0,0 -> 1,1
+y is north. +x is east.
Comments are a waste of bytes, do not use them.
Coding standards & best practices are not enforced. Go nuts.
Will be executed in PYTHON_VERSION

Your python code can not import any modules of it's own, but it does have the following imports
prepended, and not included in the CODE_SIZE character limit.

PREFIX
""".replace("PYTHON_VERSION", str(sys.version_info) )

PREFIX = """
import math, numpy, scipy, cmath, decimal, fractions, random, statistics, itertools
"""

subpassParamSummary = [
    "Max data size 1024 bytes. Note the reference image is 512x512 pixels and ~4kb compressed PNG.",
    "Max data size 2048 bytes. Note the reference image is 512x512 pixels and ~4kb compressed PNG.",
    "Max data size 4096 bytes. Note the reference image is 512x512 pixels and ~4kb compressed PNG.",
]

structure = {
    "type" : "object",
    "properties" : {
        "reasoningAndDiscussion" : { "type" : "string"},
        "minifiedCode" : { "type" : "string"}
    },
    "additionalProperties": False,
    "propertyOrdering": [
        "reasoningAndDiscussion",
        "minifiedCode"
    ],
    "required": [
        "reasoningAndDiscussion",
        "minifiedCode"
    ]
}

mapOfAustralia = "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"

def prepareSubpassPrompt(index):
    if index == 0:
        return (prompt
          .replace("THING_TO_RETURN", "shape representing Australia's land mass, including at least Tasmania")
          .replace("PREFIX", PREFIX)
          .replace("CODE_SIZE", "1024 bytes"))

    if index == 1:
        return (prompt
          .replace("THING_TO_RETURN", "shape representing Australia's land mass, including at least Tasmania")
          .replace("PREFIX", PREFIX)
          .replace("CODE_SIZE", "2048 bytes"))

    if index == 2:
        return (prompt
          .replace("THING_TO_RETURN", "shape representing Australia's land mass, including at least Tasmania")
          .replace("PREFIX", PREFIX)
          .replace("CODE_SIZE", "4096 bytes"))

    raise StopIteration
                
def loadReferenceImage():
    # decode the mapOfAustralia
    decoded = base64.b64decode(mapOfAustralia)
    image = Image.open(io.BytesIO(decoded)).resize([512,512], Image.Resampling.NEAREST)
                
    return image

def getReferenceImage(subPass, aiEngineName : str):
    ref = loadReferenceImage()

    output_path = f"results/20_VisualizationReference_{aiEngineName}_subpass{subPass}.png"
    ref.save(output_path)
    return output_path

def pythonCodeToImage(code : str, size : int = 512):
    code = PREFIX + "\n\n" + code
    g = {}
    exec(code, g)
    f = g["f"]
    
    image = Image.new("L", (size, size), (255))
    
    for x in range(size):
        for y in range(size):
            if f(x / size, y / size) > 0:
                image.putpixel((x, y), 0)

    return image

def safeToRun(str : str):
    for banned in [
        "import", "from", "exec", "eval", "compile", "open", "os", "subprocess", "sys", 
        "builtins", "file", "modules"]:
        if re.search(r"\b" + banned + r"\b", str):
            return False
    return True

def gradeAnswer(result : dict, subPass : int, aiEngineName : str):
    answer = result["minifiedCode"]
    if subPass == 0 and len(answer) > 1024:
        return 0, f"Code too long: {len(answer)} bytes (max 1024)"
    if subPass == 1 and len(answer) > 2048:
        return 0, f"Code too long: {len(answer)} bytes (max 2048)"
    if subPass == 2 and len(answer) > 4096:
        return 0, f"Code too long: {len(answer)} bytes (max 4096)"

    if not safeToRun(answer):
        return 0, "Banned word found"

    size = 512

    ref = loadReferenceImage()
    try:
        test = pythonCodeToImage(answer, size)
    except Exception as e:
        return 0, f"Error executing code: {e}"
        
    correct = 0

    for x in range(size):
        for y in range(size):
            if ref.getpixel((x, y)) == test.getpixel((x, y)):
                correct += 1

    raw_accuracy = correct / (size * size)
    score = raw_accuracy ** 10
    return score, f"Matched {correct}/{size*size} pixels ({raw_accuracy*100:.1f}% accuracy, score: {score:.4f})"

def resultToImage(result, subPass, aiEngineName : str):
    if not safeToRun(result["minifiedCode"]):
        return "Error: Banned word found - not executing."

    try:
        test = pythonCodeToImage(result["minifiedCode"],512)
    except Exception as e:
        return f"Error executing code: {e}"
    ref = loadReferenceImage()
    for x in range(512):
        for y in range(512):
            if ref.getpixel((x, y)) != test.getpixel((x, y)):
                if ref.getpixel((x, y))  > test.getpixel((x, y)):
                    test.putpixel((x, y), 50)
                else:
                    test.putpixel((x, y), 200)

    output_path = f"results/20_Visualization_{aiEngineName}_subpass{subPass}.png"
    test.save(output_path)
    return output_path

if __name__ == "__main__":
    resultToImage({
    "minifiedCode": "def f(x,y):c1x=0.8694444444;c1y=0.580951;r1x=0.08;r1y=0.14;c2x=0.9069444444;c2y=0.6248;r2x=0.04;r2y=0.06;c3x=0.8194444444;c3y=0.58735;r3x=0.05;r3y=0.07;d1=((x-c1x)**2)/(r1x*r1x)+((y-c1y)**2)/(r1y*r1y);d2=((x-c2x)**2)/(r2x*r2x)+((y-c2y)**2)/(r2y*r2y);d3=((x-c3x)**2)/(r3x*r3x)+((y-c3y)**2)/(r3y*r3y);m=d1;if d2<m:m=d2;if d3<m:m=d3;return 1.0-m"
},
0, "Placebo")