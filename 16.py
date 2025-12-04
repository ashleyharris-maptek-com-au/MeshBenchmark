from collections import defaultdict
import VolumeComparison as vc
import os
import random

title = "Pack rectangular prisms"

prompt = """
You are given the following rectangular prisms:

PRISM_LIST

and have to pack them as efficiently as possible into the smallest volume possible.
You can rotate the prisms as you see fit, return a list of min/max xyz coordinates.
"""

structure = {
  "type": "object",
  "properties": {
    "boxes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "XyzMin": {
            "type": "array",
            "items": {
              "type": "integer"
            }
          },
          "XyzMax": {
            "type": "array",
            "items": {
              "type": "integer"
            }
          }
        },
        "propertyOrdering": [
          "XyzMin",
          "XyzMax"
        ],
        "required": [
          "XyzMin",
          "XyzMax"
        ],
        "additionalProperties": False
      }
    }
  },
  "propertyOrdering": [
    "boxes"
  ],
  "required": [
    "boxes"
  ],
  "additionalProperties": False
}

prismList = [
        [7, 5, 3, 2],
        [11, 7, 5, 3],
        [13, 11, 7, 5],
        [17, 13, 11, 7],
        [19, 17, 13, 11],
        [23, 19, 17, 13],
]

def preparePrismListString(index):
    return "\n".join([
        str(a) + " prisms of " + str(b) + "x" + str(c) + "x" + str(d) for a,b,c,d in  prismList[0:index +1]])

def prepareSubpassPrompt(index):
    if index == 6 : raise StopIteration
    return prompt.replace("PRISM_LIST",preparePrismListString(index))

promptChangeSummary = "Adds additional prisms for each run"

subpassParamSummary =   [
    preparePrismListString(0).replace("\n","<br>"),
    preparePrismListString(1).replace("\n","<br>"),
    preparePrismListString(2).replace("\n","<br>"),
    preparePrismListString(3).replace("\n","<br>"),
    preparePrismListString(4).replace("\n","<br>"),
    preparePrismListString(5).replace("\n","<br>"),
    ]

def gradeAnswer(answer, subPass, aiEngineName):
    # calcualte the expected volume from the prismList and subpass
    expectedVolume = sum([a*b*c*d for a,b,c,d in prismList[0:subPass + 1]])

    # calculate the volume of all the boxes in the answer
    answerVolume = 0
    for box in answer["boxes"]:
      volume = (box["XyzMax"][0] - box["XyzMin"][0]) * (box["XyzMax"][1] - box["XyzMin"][1]) * (box["XyzMax"][2] - box["XyzMin"][2])
      answerVolume += volume

    reasoning = f"Answer volume: {answerVolume}, Expected volume: {expectedVolume}"
    if answerVolume != expectedVolume:
      return 0, reasoning + f"\nVolume mismatch: expected {expectedVolume}, got {answerVolume}"

    # count the number of boxes of each size
    boxCountBySize = defaultdict(int)
    for box in answer["boxes"]:
      span = [box["XyzMax"][0] - box["XyzMin"][0], box["XyzMax"][1] - box["XyzMin"][1], box["XyzMax"][2] - box["XyzMin"][2]]
      span.sort(reverse=True)
      boxCountBySize[tuple(span)] += 1

    # check to make sure that the number of boxes of each size is correct
    for boxCount, x,y,z in prismList[0:subPass + 1]:
        if boxCountBySize[(x,y,z)] != boxCount:
          return 0, reasoning + f"\nBox count mismatch for {x}x{y}x{z}: expected {boxCount}, got {boxCountBySize[(x,y,z)]}"

    # check to see if any boxes overlap
    for box in answer["boxes"]:
      for otherBox in answer["boxes"]:
        if box != otherBox:
          if box["XyzMin"][0] < otherBox["XyzMax"][0] and box["XyzMax"][0] > otherBox["XyzMin"][0] and box["XyzMin"][1] < otherBox["XyzMax"][1] and box["XyzMax"][1] > otherBox["XyzMin"][1] and box["XyzMin"][2] < otherBox["XyzMax"][2] and box["XyzMax"][2] > otherBox["XyzMin"][2]:
            return 0, reasoning + "\nBox overlap detected"

    # check to see if all coordinates are positive
    for box in answer["boxes"]:
      if box["XyzMin"][0] < 0 or box["XyzMin"][1] < 0 or box["XyzMin"][2] < 0:
        return 0, reasoning + "\nBox with negative coordinates detected"

    maxPoint = [0,0,0]
    for box in answer["boxes"]:
      maxPoint[0] = max(maxPoint[0], box["XyzMax"][0])
      maxPoint[1] = max(maxPoint[1], box["XyzMax"][1])
      maxPoint[2] = max(maxPoint[2], box["XyzMax"][2])

    enclosingVolume = maxPoint[0] * maxPoint[1] * maxPoint[2]
    score = answerVolume / enclosingVolume
    return score, reasoning + f"\nPacking efficiency: {score*100:.1f}% (enclosing volume: {enclosingVolume})"

def resultToNiceReport(result, subPass, aiEngineName : str):

    openScadData = ""

    for box in result["boxes"]:
      span = [box["XyzMax"][0] - box["XyzMin"][0], box["XyzMax"][1] - box["XyzMin"][1], box["XyzMax"][2] - box["XyzMin"][2]]
      pos = [(box["XyzMax"][0] + box["XyzMin"][0]) / 2, (box["XyzMax"][1] + box["XyzMin"][1]) / 2, (box["XyzMax"][2] + box["XyzMin"][2]) / 2]

      randomColour =  [random.random(), random.random(), random.random()]

      openScadData += f"translate([{pos[0]}, {pos[1]}, {pos[2]}]) color({randomColour}) cube([{span[0]}, {span[1]}, {span[2]}], center=true);\n"

    output_path = f"results/16_Visualization_{aiEngineName}_subpass{subPass}.png"
    vc.render_scadText_to_png(openScadData, output_path)
    print(f"Saved visualization to {output_path}")
    return "<img src=\"" + os.path.basename(output_path) + "\" />"


def postProcessScore(score, subPassIndex):
  if score < 70:
    # It's really easy to get a decent score via dumb packing, especially
    # "just place them all in a line" or other very naive solutions, so penalise 
    # any that isn't at least 70% efficient.
    return score / 2

  # I don't believe subpasses 3+ are solvable with 100% efficinecy. I haven't proved it,
  # but I'm happy to mulligan the very good results.
  return min(1,score / 0.95)

#gradeAnswer({ "boxes" : [
#            {"XyzMin": [0,0,0], "XyzMax": [5,3,2]},
#            {"XyzMin": [0,0,2], "XyzMax": [5,3,4]},
#            {"XyzMin": [0,0,4], "XyzMax": [5,3,6]},
#            {"XyzMin": [0,0,6], "XyzMax": [5,3,8]},
#            {"XyzMin": [0,0,8], "XyzMax": [5,3,10]},
#            {"XyzMin": [0,0,10], "XyzMax": [5,3,12]},
#            {"XyzMin": [0,0,12], "XyzMax": [5,3,14]},
#        ]}, 0)