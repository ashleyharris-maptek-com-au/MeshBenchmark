from textwrap import dedent
import hashlib

configAndSettingsHash = hashlib.sha256(b"Placebo").hexdigest()

def PlaceboAIHook(prompt: str, structure: dict | None) -> dict | str:
    h = hashlib.sha256(prompt.strip().encode()).hexdigest()
    
    if h == "8fcd5803eb9e781f9662e3554188f78ccbd6fd2edf13847226a6e33a25627730":
        # Question 1
        return {
        "pipes": [
            {
                "xCentre":0,
                "yCentre": 0,
                "rotationDegrees": 0
            },
            {
                "xCentre": -2.55,
                "yCentre": 2.5,
                "rotationDegrees": 90
            },
            {
                "xCentre": 2.55,
                "yCentre": 2.5,
                "rotationDegrees": 90
            },
            {
                "xCentre": -2.55,
                "yCentre": -2.5,
                "rotationDegrees": 90
            },
            {
                "xCentre": 2.55,
                "yCentre": -2.5,
                "rotationDegrees": 90
            }
        ],
        "Reasoning": "This was manually calculated. Half of 10cm is 5cm, so the 10cm wide pipes center is offset by 5cm."
    }, "Placebo thinking... hmmm..."

    if h == "1a77d1817254df5c0d6a3d340d389744ab77e002685fd25578550a3da7f5482d":
      return {
        "bricks": [
            {"Centroid": [0, 48, 4.8], "RotationDegrees": 0},
            {"Centroid": [0, -48, 4.8], "RotationDegrees": 0},
            {"Centroid": [0, 64, 4.8], "RotationDegrees": 0},
            {"Centroid": [0, -64, 4.8], "RotationDegrees": 0},
            {"Centroid": [32, 32, 4.8], "RotationDegrees": 0},
            {"Centroid": [32, 48, 4.8], "RotationDegrees": 0},
            {"Centroid": [32, -32, 4.8], "RotationDegrees": 0},
            {"Centroid": [32, -48, 4.8], "RotationDegrees": 0},
            {"Centroid": [-32, 32, 4.8], "RotationDegrees": 0},
            {"Centroid": [-32, 48, 4.8], "RotationDegrees": 0},
            {"Centroid": [-32, -32, 4.8], "RotationDegrees": 0},
            {"Centroid": [-32, -48, 4.8], "RotationDegrees": 0},
            {"Centroid": [64, 0, 4.8], "RotationDegrees": 0},
            {"Centroid": [-64, 0, 4.8], "RotationDegrees": 0},
            {"Centroid": [64, 16, 4.8], "RotationDegrees": 0},
            {"Centroid": [64, -16, 4.8], "RotationDegrees": 0},
            {"Centroid": [-64, 16, 4.8], "RotationDegrees": 0},
            {"Centroid": [-64, -16, 4.8], "RotationDegrees": 0},
            {"Centroid": [48, 0, 14.4], "RotationDegrees": 90},
            {"Centroid": [-48, 0, 14.4], "RotationDegrees": 90},
            {"Centroid": [64, 0, 14.4], "RotationDegrees": 90},
            {"Centroid": [-64, 0, 14.4], "RotationDegrees": 90},
            {"Centroid": [32, 32, 14.4], "RotationDegrees": 90},
            {"Centroid": [32, -32, 14.4], "RotationDegrees": 90},
            {"Centroid": [-32, 32, 14.4], "RotationDegrees": 90},
            {"Centroid": [-32, -32, 14.4], "RotationDegrees": 90},
            {"Centroid": [48, 32, 14.4], "RotationDegrees": 90},
            {"Centroid": [48, -32, 14.4], "RotationDegrees": 90},
            {"Centroid": [-48, 32, 14.4], "RotationDegrees": 90},
            {"Centroid": [-48, -32, 14.4], "RotationDegrees": 90},
            {"Centroid": [0, 64, 14.4], "RotationDegrees": 90},
            {"Centroid": [0, -64, 14.4], "RotationDegrees": 90},
            {"Centroid": [16, 64, 14.4], "RotationDegrees": 90},
            {"Centroid": [16, -64, 14.4], "RotationDegrees": 90},
            {"Centroid": [-16, 64, 14.4], "RotationDegrees": 90},
            {"Centroid": [-16, -64, 14.4], "RotationDegrees": 90},
            {"Centroid": [0, 32, 24.0], "RotationDegrees": 0},
            {"Centroid": [0, -32, 24.0], "RotationDegrees": 0},
            {"Centroid": [0, 48, 24.0], "RotationDegrees": 0},
            {"Centroid": [0, -48, 24.0], "RotationDegrees": 0},
            {"Centroid": [0, 64, 24.0], "RotationDegrees": 0},
            {"Centroid": [0, -64, 24.0], "RotationDegrees": 0},
            {"Centroid": [32, 0, 24.0], "RotationDegrees": 0},
            {"Centroid": [-32, 0, 24.0], "RotationDegrees": 0},
            {"Centroid": [32, 16, 24.0], "RotationDegrees": 0},
            {"Centroid": [32, -16, 24.0], "RotationDegrees": 0},
            {"Centroid": [-32, 16, 24.0], "RotationDegrees": 0},
            {"Centroid": [-32, -16, 24.0], "RotationDegrees": 0},
            {"Centroid": [32, 32, 24.0], "RotationDegrees": 0},
            {"Centroid": [32, -32, 24.0], "RotationDegrees": 0},
            {"Centroid": [-32, 32, 24.0], "RotationDegrees": 0},
            {"Centroid": [-32, -32, 24.0], "RotationDegrees": 0},
            {"Centroid": [32, 48, 24.0], "RotationDegrees": 0},
            {"Centroid": [32, -48, 24.0], "RotationDegrees": 0},
            {"Centroid": [-32, 48, 24.0], "RotationDegrees": 0},
            {"Centroid": [-32, -48, 24.0], "RotationDegrees": 0},
            {"Centroid": [64, 0, 24.0], "RotationDegrees": 0},
            {"Centroid": [-64, 0, 24.0], "RotationDegrees": 0},
            {"Centroid": [32, 0, 33.6], "RotationDegrees": 90},
            {"Centroid": [-32, 0, 33.6], "RotationDegrees": 90},
            {"Centroid": [48, 0, 33.6], "RotationDegrees": 90},
            {"Centroid": [-48, 0, 33.6], "RotationDegrees": 90},
            {"Centroid": [0, 32, 33.6], "RotationDegrees": 90},
            {"Centroid": [0, -32, 33.6], "RotationDegrees": 90},
            {"Centroid": [16, 32, 33.6], "RotationDegrees": 90},
            {"Centroid": [16, -32, 33.6], "RotationDegrees": 90},
            {"Centroid": [-16, 32, 33.6], "RotationDegrees": 90},
            {"Centroid": [-16, -32, 33.6], "RotationDegrees": 90},
            {"Centroid": [32, 32, 33.6], "RotationDegrees": 90},
            {"Centroid": [32, -32, 33.6], "RotationDegrees": 90},
            {"Centroid": [-32, 32, 33.6], "RotationDegrees": 90},
            {"Centroid": [-32, -32, 33.6], "RotationDegrees": 90},
            {"Centroid": [48, 32, 33.6], "RotationDegrees": 90},
            {"Centroid": [48, -32, 33.6], "RotationDegrees": 90},
            {"Centroid": [-48, 32, 33.6], "RotationDegrees": 90},
            {"Centroid": [-48, -32, 33.6], "RotationDegrees": 90},
            {"Centroid": [0, 0, 43.2], "RotationDegrees": 0},
            {"Centroid": [0, 16, 43.2], "RotationDegrees": 0},
            {"Centroid": [0, -16, 43.2], "RotationDegrees": 0},
            {"Centroid": [0, 32, 43.2], "RotationDegrees": 0},
            {"Centroid": [0, -32, 43.2], "RotationDegrees": 0},
            {"Centroid": [0, 48, 43.2], "RotationDegrees": 0},
            {"Centroid": [0, -48, 43.2], "RotationDegrees": 0},
            {"Centroid": [32, 0, 43.2], "RotationDegrees": 0},
            {"Centroid": [-32, 0, 43.2], "RotationDegrees": 0},
            {"Centroid": [32, 16, 43.2], "RotationDegrees": 0},
            {"Centroid": [32, -16, 43.2], "RotationDegrees": 0},
            {"Centroid": [-32, 16, 43.2], "RotationDegrees": 0},
            {"Centroid": [-32, -16, 43.2], "RotationDegrees": 0},
            {"Centroid": [32, 32, 43.2], "RotationDegrees": 0},
            {"Centroid": [32, -32, 43.2], "RotationDegrees": 0},
            {"Centroid": [-32, 32, 43.2], "RotationDegrees": 0},
            {"Centroid": [-32, -32, 43.2], "RotationDegrees": 0},
            {"Centroid": [0, 0, 52.8], "RotationDegrees": 90},
            {"Centroid": [16, 0, 52.8], "RotationDegrees": 90},
            {"Centroid": [-16, 0, 52.8], "RotationDegrees": 90},
            {"Centroid": [32, 0, 52.8], "RotationDegrees": 90},
            {"Centroid": [-32, 0, 52.8], "RotationDegrees": 90},
            {"Centroid": [0, 32, 52.8], "RotationDegrees": 90},
            {"Centroid": [0, -32, 52.8], "RotationDegrees": 90},
            {"Centroid": [16, 32, 52.8], "RotationDegrees": 90},
            {"Centroid": [16, -32, 52.8], "RotationDegrees": 90},
            {"Centroid": [-16, 32, 52.8], "RotationDegrees": 90},
            {"Centroid": [-16, -32, 52.8], "RotationDegrees": 90},
            {"Centroid": [32, 32, 52.8], "RotationDegrees": 90},
            {"Centroid": [32, -32, 52.8], "RotationDegrees": 90},
            {"Centroid": [-32, 32, 52.8], "RotationDegrees": 90},
            {"Centroid": [-32, -32, 52.8], "RotationDegrees": 90},
            {"Centroid": [0, 0, 62.4], "RotationDegrees": 0},
            {"Centroid": [0, 16, 62.4], "RotationDegrees": 0},
            {"Centroid": [0, -16, 62.4], "RotationDegrees": 0}
        ],
        "Reasoning": "I generated this from the Gemini 2.5 pro API playground while developing the test. It's a bit 'meh'"
        }, "Placebo thinking... hmmm..."

    if h == "b999904f5b38b765fa59ba4cf4ed3ad93fa77cdee60126375adca350bff8e55d":
        # Question 2, subpass 1
        return {
        "bricks": [
            { "Centroid": [ 96, 0, 4.8 ], "RotationDegrees": 0 },
            { "Centroid": [ -96, 0, 4.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 0, 96, 4.8 ], "RotationDegrees": 90 },
            { "Centroid": [ 0, -96, 4.8 ], "RotationDegrees": 90 },
            { "Centroid": [ 64, 64, 4.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 64, -64, 4.8 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, 64, 4.8 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, -64, 4.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 80, 32, 4.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 80, -32, 4.8 ], "RotationDegrees": 0 },
            { "Centroid": [ -80, 32, 4.8 ], "RotationDegrees": 0 },
            { "Centroid": [ -80, -32, 4.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 32, 80, 4.8 ], "RotationDegrees": 90 },
            { "Centroid": [ 32, -80, 4.8 ], "RotationDegrees": 90 },
            { "Centroid": [ -32, 80, 4.8 ], "RotationDegrees": 90 },
            { "Centroid": [ -32, -80, 4.8 ], "RotationDegrees": 90 },
            { "Centroid": [ 96, 16, 14.4 ], "RotationDegrees": 0 },
            { "Centroid": [ -96, 16, 14.4 ], "RotationDegrees": 0 },
            { "Centroid": [ 96, -16, 14.4 ], "RotationDegrees": 0 },
            { "Centroid": [ -96, -16, 14.4 ], "RotationDegrees": 0 },
            { "Centroid": [ 16, 96, 14.4 ], "RotationDegrees": 90 },
            { "Centroid": [ 16, -96, 14.4 ], "RotationDegrees": 90 },
            { "Centroid": [ -16, 96, 14.4 ], "RotationDegrees": 90 },
            { "Centroid": [ -16, -96, 14.4 ], "RotationDegrees": 90 },
            { "Centroid": [ 64, 48, 14.4 ], "RotationDegrees": 0 },
            { "Centroid": [ 64, -48, 14.4 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, 48, 14.4 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, -48, 14.4 ], "RotationDegrees": 0 },
            { "Centroid": [ 48, 64, 14.4 ], "RotationDegrees": 90 },
            { "Centroid": [ 48, -64, 14.4 ], "RotationDegrees": 90 },
            { "Centroid": [ -48, 64, 14.4 ], "RotationDegrees": 90 },
            { "Centroid": [ -48, -64, 14.4 ], "RotationDegrees": 90 },
            { "Centroid": [ 96, 0, 24.0 ], "RotationDegrees": 0 },
            { "Centroid": [ -96, 0, 24.0 ], "RotationDegrees": 0 },
            { "Centroid": [ 0, 96, 24.0 ], "RotationDegrees": 90 },
            { "Centroid": [ 0, -96, 24.0 ], "RotationDegrees": 90 },
            { "Centroid": [ 80, 48, 24.0 ], "RotationDegrees": 0 },
            { "Centroid": [ 80, -48, 24.0 ], "RotationDegrees": 0 },
            { "Centroid": [ -80, 48, 24.0 ], "RotationDegrees": 0 },
            { "Centroid": [ -80, -48, 24.0 ], "RotationDegrees": 0 },
            { "Centroid": [ 48, 80, 24.0 ], "RotationDegrees": 90 },
            { "Centroid": [ 48, -80, 24.0 ], "RotationDegrees": 90 },
            { "Centroid": [ -48, 80, 24.0 ], "RotationDegrees": 90 },
            { "Centroid": [ -48, -80, 24.0 ], "RotationDegrees": 90 },
            { "Centroid": [ 88, 24, 33.6 ], "RotationDegrees": 0 },
            { "Centroid": [ -88, 24, 33.6 ], "RotationDegrees": 0 },
            { "Centroid": [ 88, -24, 33.6 ], "RotationDegrees": 0 },
            { "Centroid": [ -88, -24, 33.6 ], "RotationDegrees": 0 },
            { "Centroid": [ 24, 88, 33.6 ], "RotationDegrees": 90 },
            { "Centroid": [ 24, -88, 33.6 ], "RotationDegrees": 90 },
            { "Centroid": [ -24, 88, 33.6 ], "RotationDegrees": 90 },
            { "Centroid": [ -24, -88, 33.6 ], "RotationDegrees": 90 },
            { "Centroid": [ 64, 64, 33.6 ], "RotationDegrees": 0 },
            { "Centroid": [ 64, -64, 33.6 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, 64, 33.6 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, -64, 33.6 ], "RotationDegrees": 0 },
            { "Centroid": [ 80, 0, 43.2 ], "RotationDegrees": 0 },
            { "Centroid": [ -80, 0, 43.2 ], "RotationDegrees": 0 },
            { "Centroid": [ 0, 80, 43.2 ], "RotationDegrees": 90 },
            { "Centroid": [ 0, -80, 43.2 ], "RotationDegrees": 90 },
            { "Centroid": [ 64, 48, 43.2 ], "RotationDegrees": 0 },
            { "Centroid": [ 64, -48, 43.2 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, 48, 43.2 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, -48, 43.2 ], "RotationDegrees": 0 },
            { "Centroid": [ 48, 64, 43.2 ], "RotationDegrees": 90 },
            { "Centroid": [ 48, -64, 43.2 ], "RotationDegrees": 90 },
            { "Centroid": [ -48, 64, 43.2 ], "RotationDegrees": 90 },
            { "Centroid": [ -48, -64, 43.2 ], "RotationDegrees": 90 },
            { "Centroid": [ 88, 16, 52.8 ], "RotationDegrees": 0 },
            { "Centroid": [ -88, 16, 52.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 88, -16, 52.8 ], "RotationDegrees": 0 },
            { "Centroid": [ -88, -16, 52.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 16, 88, 52.8 ], "RotationDegrees": 90 },
            { "Centroid": [ 16, -88, 52.8 ], "RotationDegrees": 90 },
            { "Centroid": [ -16, 88, 52.8 ], "RotationDegrees": 90 },
            { "Centroid": [ -16, -88, 52.8 ], "RotationDegrees": 90 },
            { "Centroid": [ 56, 56, 52.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 56, -56, 52.8 ], "RotationDegrees": 0 },
            { "Centroid": [ -56, 56, 52.8 ], "RotationDegrees": 0 },
            { "Centroid": [ -56, -56, 52.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 80, 32, 62.4 ], "RotationDegrees": 0 },
            { "Centroid": [ 80, -32, 62.4 ], "RotationDegrees": 0 },
            { "Centroid": [ -80, 32, 62.4 ], "RotationDegrees": 0 },
            { "Centroid": [ -80, -32, 62.4 ], "RotationDegrees": 0 },
            { "Centroid": [ 32, 80, 62.4 ], "RotationDegrees": 90 },
            { "Centroid": [ 32, -80, 62.4 ], "RotationDegrees": 90 },
            { "Centroid": [ -32, 80, 62.4 ], "RotationDegrees": 90 },
            { "Centroid": [ -32, -80, 62.4 ], "RotationDegrees": 90 },
            { "Centroid": [ 64, 0, 62.4 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, 0, 62.4 ], "RotationDegrees": 0 },
            { "Centroid": [ 0, 64, 62.4 ], "RotationDegrees": 90 },
            { "Centroid": [ 0, -64, 62.4 ], "RotationDegrees": 90 },
            { "Centroid": [ 64, 32, 72.0 ], "RotationDegrees": 0 },
            { "Centroid": [ 64, -32, 72.0 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, 32, 72.0 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, -32, 72.0 ], "RotationDegrees": 0 },
            { "Centroid": [ 32, 64, 72.0 ], "RotationDegrees": 90 },
            { "Centroid": [ 32, -64, 72.0 ], "RotationDegrees": 90 },
            { "Centroid": [ -32, 64, 72.0 ], "RotationDegrees": 90 },
            { "Centroid": [ -32, -64, 72.0 ], "RotationDegrees": 90 },
            { "Centroid": [ 80, 0, 72.0 ], "RotationDegrees": 0 },
            { "Centroid": [ -80, 0, 72.0 ], "RotationDegrees": 0 },
            { "Centroid": [ 0, 80, 72.0 ], "RotationDegrees": 90 },
            { "Centroid": [ 0, -80, 72.0 ], "RotationDegrees": 90 },
            { "Centroid": [ 0, 0, 81.6 ], "RotationDegrees": 0 },
            { "Centroid": [ 32, 0, 81.6 ], "RotationDegrees": 0 },
            { "Centroid": [ -32, 0, 81.6 ], "RotationDegrees": 0 },
            { "Centroid": [ 0, 32, 81.6 ], "RotationDegrees": 90 },
            { "Centroid": [ 0, -32, 81.6 ], "RotationDegrees": 90 },
            { "Centroid": [ 48, 48, 81.6 ], "RotationDegrees": 0 },
            { "Centroid": [ 48, -48, 81.6 ], "RotationDegrees": 0 },
            { "Centroid": [ -48, 48, 81.6 ], "RotationDegrees": 0 },
            { "Centroid": [ -48, -48, 81.6 ], "RotationDegrees": 0 },
            { "Centroid": [ 64, 16, 81.6 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, 16, 81.6 ], "RotationDegrees": 0 },
            { "Centroid": [ 64, -16, 81.6 ], "RotationDegrees": 0 },
            { "Centroid": [ -64, -16, 81.6 ], "RotationDegrees": 0 },
            { "Centroid": [ 16, 64, 81.6 ], "RotationDegrees": 90 },
            { "Centroid": [ 16, -64, 81.6 ], "RotationDegrees": 90 },
            { "Centroid": [ -16, 64, 81.6 ], "RotationDegrees": 90 },
            { "Centroid": [ -16, -64, 81.6 ], "RotationDegrees": 90 },
            { "Centroid": [ 0, 0, 91.2 ], "RotationDegrees": 0 },
            { "Centroid": [ 32, 16, 91.2 ], "RotationDegrees": 0 },
            { "Centroid": [ 32, -16, 91.2 ], "RotationDegrees": 0 },
            { "Centroid": [ -32, 16, 91.2 ], "RotationDegrees": 0 },
            { "Centroid": [ -32, -16, 91.2 ], "RotationDegrees": 0 },
            { "Centroid": [ 16, 32, 91.2 ], "RotationDegrees": 90 },
            { "Centroid": [ 16, -32, 91.2 ], "RotationDegrees": 90 },
            { "Centroid": [ -16, 32, 91.2 ], "RotationDegrees": 90 },
            { "Centroid": [ -16, -32, 91.2 ], "RotationDegrees": 90 },
            { "Centroid": [ 48, 0, 91.2 ], "RotationDegrees": 0 },
            { "Centroid": [ -48, 0, 91.2 ], "RotationDegrees": 0 },
            { "Centroid": [ 0, 48, 91.2 ], "RotationDegrees": 90 },
            { "Centroid": [ 0, -48, 91.2 ], "RotationDegrees": 90 },
            { "Centroid": [ 0, 0, 100.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 32, 0, 100.8 ], "RotationDegrees": 0 },
            { "Centroid": [ -32, 0, 100.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 0, 32, 100.8 ], "RotationDegrees": 90 },
            { "Centroid": [ 0, -32, 100.8 ], "RotationDegrees": 90 },
            { "Centroid": [ 16, 16, 100.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 16, -16, 100.8 ], "RotationDegrees": 0 },
            { "Centroid": [ -16, 16, 100.8 ], "RotationDegrees": 0 },
            { "Centroid": [ -16, -16, 100.8 ], "RotationDegrees": 0 },
            { "Centroid": [ 0, 0, 110.4 ], "RotationDegrees": 0 },
            { "Centroid": [ 16, 0, 110.4 ], "RotationDegrees": 90 },
            { "Centroid": [ -16, 0, 110.4 ], "RotationDegrees": 90 },
            { "Centroid": [ 0, 16, 110.4 ], "RotationDegrees": 0 },
            { "Centroid": [ 0, -16, 110.4 ], "RotationDegrees": 0 }
            ]
        }, "Placebo thinking... hmmm..."

    if h in [
        "930c6e1538bb651872c517cb657ac56976cd08b940980c48be62da0a61a1f7a8",
        "c0b2d0d5828f0fead1c361e8c0c0d3ed89007bcff1bd852af95104e423746e6d",
        "01c34565f890e2d15661a4c03e6945d83bbb946718f573d6f4cfe3aba479f032"]:
        # Question 3, subpass 0-2

        return {
            "polyhedron": {
                "vertex": [
                {
                    "xyz": [10.0, -5.0, -10.0]
                },
                {
                    "xyz": [10.0, 15.0, -10.0]
                },
                {
                    "xyz": [10.0, 15.0, 20.0]
                },
                {
                    "xyz": [10.0, -5.0, 20.0]
                },
                {
                    "xyz": [0.0, -5.0, 20.0]
                },
                {
                    "xyz": [0.0, 15.0, 20.0]
                },
                {
                    "xyz": [0.0, 15.0, -10.0]
                },
                {
                    "xyz": [-12.5, -12.5, -12.5]
                },
                {
                    "xyz": [2.5, -12.5, -12.5]
                },
                {
                    "xyz": [2.5, 2.5, -12.5]
                },
                {
                    "xyz": [-12.5, 2.5, -12.5]
                },
                {
                    "xyz": [-12.5, -12.5, 2.5]
                },
                {
                    "xyz": [2.5, -12.5, 2.5]
                },
                {
                    "xyz": [-12.5, 2.5, 2.5]
                },
                {
                    "xyz": [2.5, 2.5, -10.0]
                },
                {
                    "xyz": [2.5, -5.0, -10.0]
                },
                {
                    "xyz": [2.5, -5.0, 2.5]
                },
                {
                    "xyz": [0.0, 2.5, 2.5]
                },
                {
                    "xyz": [0.0, 2.5, -10.0]
                },
                {
                    "xyz": [0.0, -5.0, 2.5]
                }
                ],
                "faces": [
                {
                    "vertex": [0, 1, 2, 3]
                },
                {
                    "vertex": [8, 9, 14, 15, 16, 12]
                },
                {
                    "vertex": [13, 10, 7, 11]
                },
                {
                    "vertex": [6, 18, 17, 19, 4, 5]
                },
                {
                    "vertex": [2, 1, 6, 5]
                },
                {
                    "vertex": [9, 10, 13, 17, 18, 14]
                },
                {
                    "vertex": [7, 8, 12, 11]
                },
                {
                    "vertex": [0, 3, 4, 19, 16, 15]
                },
                {
                    "vertex": [4, 3, 2, 5]
                },
                {
                    "vertex": [11, 12, 16, 19, 17, 13]
                },
                {
                    "vertex": [7, 10, 9, 8]
                },
                {
                    "vertex": [0, 15, 14, 18, 6, 1]
                }
                ]
            },
            "Reasoning": "I generated this from the Gemini 2.5 API playground while developing the test.  It appears correct for the 1st test."
        }, "Placebo thinking... hmmm..."

    if h in ["9e73ddadee00ffc7691fc719f63c1f04e7c14e02250ae3204c7d900cbfde671e",
             "c4ba3af199a7cee6f160152dc2e596b9b4aeda2bab8b3252170a03838bb1e343",
             "daecbf3ef90e83d1cbbba06b9e0b82a04f06980fcefad4c810263baf660f1f72"]:
        # Question 4
        return [
                {"x" : -1.500000, "y" : 2.598076, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : -0.500000, "y" : 2.598076, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 0.500000, "y" : 2.598076, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 1.500000, "y" : 2.598076, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 2.500000, "y" : 2.598076, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},

                {"x" : -2.000000, "y" : 1.732051, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : -1.000000, "y" : 1.732051, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : -1.000000, "y" : 1.732051, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 0.000000, "y" : 1.732051, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 0.000000, "y" : 1.732051, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 1.000000, "y" : 1.732051, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 1.000000, "y" : 1.732051, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 2.000000, "y" : 1.732051, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 2.000000, "y" : 1.732051, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},

                {"x" : -2.500000, "y" : 0.866025, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : -1.500000, "y" : 0.866025, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : -1.500000, "y" : 0.866025, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : -0.500000, "y" : 0.866025, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : -0.500000, "y" : 0.866025, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 0.500000, "y" : 0.866025, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 0.500000, "y" : 0.866025, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 1.500000, "y" : 0.866025, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 1.500000, "y" : 0.866025, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 2.500000, "y" : 0.866025, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},

                {"x" : -2.000000, "y" : 0.000000, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : -2.000000, "y" : 0.000000, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : -1.000000, "y" : 0.000000, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : -1.000000, "y" : 0.000000, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 0.000000, "y" : 0.000000, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 0.000000, "y" : 0.000000, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 1.000000, "y" : 0.000000, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 1.000000, "y" : 0.000000, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 2.000000, "y" : 0.000000, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 2.000000, "y" : 0.000000, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},

                {"x" : -2.500000, "y" : -0.866025, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : -1.500000, "y" : -0.866025, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : -1.500000, "y" : -0.866025, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : -0.500000, "y" : -0.866025, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : -0.500000, "y" : -0.866025, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 0.500000, "y" : -0.866025, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 0.500000, "y" : -0.866025, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 1.500000, "y" : -0.866025, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 1.500000, "y" : -0.866025, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 2.500000, "y" : -0.866025, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 2.500000, "y" : -0.866025, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},

                {"x" : -2.000000, "y" : -1.732051, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : -1.000000, "y" : -1.732051, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : -1.000000, "y" : -1.732051, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 0.000000, "y" : -1.732051, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 0.000000, "y" : -1.732051, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 1.000000, "y" : -1.732051, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 1.000000, "y" : -1.732051, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : 2.000000, "y" : -1.732051, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 2.000000, "y" : -1.732051, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},

                {"x" : -1.500000, "y" : -2.598076, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : -1.500000, "y" : -2.598076, "z" : 0.000000, "q0" : 1.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 0.000000},
                {"x" : -0.500000, "y" : -2.598076, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 0.500000, "y" : -2.598076, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 1.500000, "y" : -2.598076, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
                {"x" : 2.500000, "y" : -2.598076, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000}
                ], "Placebo thinking... hmmm..."

    if h == '4ec098719613af4f77793beffc8324b8d5d561206c1edbb09175af5f13583c34':
        # Question 5 subpass 0
        return     dedent("""
            ################
            #A..#...#.....##
            ###.#.#.#.###.##
            # #...#.#.# #.##
            # #####.#.# #.##
            #.....#...#...##
            #.###.#####.####
            #..B#...#...# ##
            #######.#.### ##
            #.......#.....##
            #.###########.##
            #.....#.......##
            # ###.#.########
            #   #...      ##
            ################
            ################
                """).strip(), "Placebo thinking... hmmm..."

    if h == "7ce26dc6b41137ef5598b8bd045ce675a714f89d93621640f781b231e22ebb30":
        return {
            "voxels": [
                {"xyz": [0, 0, 0]},
                {"xyz": [0, 0, 1]},
                {"xyz": [0, 0, 2]},
                {"xyz": [0, 0, 3]},
                {"xyz": [0, 0, 4]},
                {"xyz": [0, 0, 5]},
                {"xyz": [0, 1, 0]},
                {"xyz": [0, 1, 1]},
                {"xyz": [0, 1, 2]},
                {"xyz": [0, 1, 3]},
                {"xyz": [0, 1, 4]},
                {"xyz": [0, 1, 5]},
                {"xyz": [0, 2, 0]},
                {"xyz": [0, 2, 1]},
                {"xyz": [0, 2, 2]},
                {"xyz": [0, 2, 3]},
                {"xyz": [0, 2, 4]},
                {"xyz": [0, 3, 3]},
                {"xyz": [0, 4, 4]},
                {"xyz": [0, 5, 5]},
                {"xyz": [1, 0, 1]},
                {"xyz": [1, 1, 2]},
                {"xyz": [1, 2, 3]},
                {"xyz": [1, 3, 4]},
                {"xyz": [1, 4, 5]},
                {"xyz": [1, 5, 0]},
                {"xyz": [2, 0, 2]},
                {"xyz": [2, 1, 3]},
                {"xyz": [2, 2, 4]},
                {"xyz": [2, 3, 5]},
                {"xyz": [2, 4, 0]},
                {"xyz": [2, 5, 1]},
                {"xyz": [3, 0, 3]},
                {"xyz": [3, 1, 4]},
                {"xyz": [3, 2, 5]},
                {"xyz": [3, 3, 0]},
                {"xyz": [3, 4, 1]},
                {"xyz": [3, 5, 2]},
                {"xyz": [4, 0, 4]},
                {"xyz": [4, 1, 5]},
                {"xyz": [4, 2, 0]},
                {"xyz": [4, 3, 1]},
                {"xyz": [4, 4, 2]},
                {"xyz": [4, 5, 3]},
                {"xyz": [5, 0, 5]},
                {"xyz": [5, 1, 0]},
                {"xyz": [5, 2, 1]},
                {"xyz": [5, 3, 2]},
                {"xyz": [5, 4, 3]},
                {"xyz": [5, 5, 4]}
              ]
            }, "Placebo thinking... hmmm..."

    if h == "953c1a17d7a9c14cadd44942f291f6084308f5e29796984716d3c65b3f68b35e":
        return dedent("""
            A5550
            2B201
            30150
            45551
            01010
        """
        ), "Placebo thinking... hmmm..."

    if h == "4d38874bab4d3e2c1943216a7d2b75d8745a77387aa4bf18b3a8c9b64551d8ca":
        return dedent("""
            def f(x,y):
                return -162*x*x*x - 854*x*x + 945*x + 653*y*y*y - 1881*y*y - 145*y + 2829
        """.strip()), "Placebo thinking... hmmm..."


    if h == "14de40d06d620c8e898c9aa289b6e8cefc28db5a0b77f47e35697aacbed0a667":
        return dedent("""
            def f(x,y):
                return -5 * x - 4 * y + 30
        """.strip()), "Placebo thinking... hmmm..."

    if h == "b95339286451148c0cb2797d43a29a7560e2abf20f94238c14d84173e0bf0fe3":
        return {
            "steps": [
                { "xy": [1, 1] },
                { "xy": [2, 1] },
                { "xy": [3, 1] },
                { "xy": [4, 1] },
                { "xy": [4, 2] },
                { "xy": [4, 3] },
                { "xy": [4, 4] },
                { "xy": [3, 4] },
                { "xy": [2, 4] },
                { "xy": [1, 4] },
                { "xy": [1, 3] },
                { "xy": [2, 3] },
                { "xy": [3, 3] },
                { "xy": [3, 2] },
                { "xy": [2, 2] },
                { "xy": [1, 2] }
            ]
            }, "Placebo thinking... hmmm..."

    if h == "a4b11c00377b6658bc85341c17bf29173a8db227048f47dc664be0000bc90de3":
        return {
            "painting" : dedent("""
              ##
             ####
             "#''
             ""''
             ""''
              "'
                             ##
                            ####
                            "##'
  #                         "#''
 ###                        ""''
"###                        ""'
""''          
""''         
"intentional 
 "mistake
               




                             #
                            ###
                           "###'
        ##                 ""#''
       ####                "\""''
       ####'               "\""''
       "##''                ""'
       ""'''                 "
       ""'''
        "''
         '
        """.rstrip().lstrip("\n"))
        }, "Placebo thinking... hmmm..."
        
    if h == "b6b9e8e242e9a29cba115d4421bb5baf5d3be9371e7bac10ef162ea3f7476b8e":
        return {
            "path": [
                { "pos": [0, 0, 0] },
                { "pos": [1, 0, 0] },
                { "pos": [2, 0, 0] },
                { "pos": [3, 0, 0] },
                { "pos": [3, 1, 0] },
                { "pos": [2, 1, 0] },
                { "pos": [1, 1, 0] },
                { "pos": [0, 1, 0] },
                { "pos": [0, 2, 0] },
                { "pos": [1, 2, 0] },
                { "pos": [2, 2, 0] },
                { "pos": [3, 2, 0] },
                { "pos": [3, 3, 0] },
                { "pos": [2, 3, 0] },
                { "pos": [1, 3, 0] },
                { "pos": [0, 3, 0] },
                { "pos": [0, 3, 1] },
                { "pos": [1, 3, 1] },
                { "pos": [2, 3, 1] },
                { "pos": [3, 3, 1] },
                { "pos": [3, 2, 1] },
                { "pos": [2, 2, 1] },
                { "pos": [1, 2, 1] },
                { "pos": [0, 2, 1] },
                { "pos": [0, 1, 1] },
                { "pos": [1, 1, 1] },
                { "pos": [2, 1, 1] },
                { "pos": [3, 1, 1] },
                { "pos": [3, 0, 1] },
                { "pos": [2, 0, 1] },
                { "pos": [1, 0, 1] },
                { "pos": [0, 0, 1] },
                { "pos": [0, 0, 2] },
                { "pos": [1, 0, 2] },
                { "pos": [2, 0, 2] },
                { "pos": [3, 0, 2] },
                { "pos": [3, 1, 2] },
                { "pos": [2, 1, 2] },
                { "pos": [1, 1, 2] },
                { "pos": [0, 1, 2] },
                { "pos": [0, 2, 2] },
                { "pos": [1, 2, 2] },
                { "pos": [2, 2, 2] },
                { "pos": [3, 2, 2] },
                { "pos": [3, 3, 2] },
                { "pos": [2, 3, 2] },
                { "pos": [1, 3, 2] },
                { "pos": [0, 3, 2] },
                { "pos": [0, 3, 3] },
                { "pos": [1, 3, 3] },
                { "pos": [2, 3, 3] },
                { "pos": [3, 3, 3] },
                { "pos": [3, 2, 3] },
                { "pos": [2, 2, 3] },
                { "pos": [1, 2, 3] },
                { "pos": [0, 2, 3] },
                { "pos": [0, 1, 3] },
                { "pos": [1, 1, 3] },
                { "pos": [2, 1, 3] },
                { "pos": [3, 1, 3] },
                { "pos": [3, 0, 3] },
                { "pos": [2, 0, 3] },
                { "pos": [1, 0, 3] },
                { "pos": [0, 0, 3] }
            ]
            }, "Placebo thinking... hmmm..."

    if h == "3615798fb71a1ef05c70e7d3663d18dc2300ada153e259e7cc0001c712c901dc":
        return {
            "points" : [
                {"x": 0.0, "y" : 0.0},
                {"x": 1.0, "y" : 0.0},
                {"x": 0.5, "y" : 0.8660254038 }
            ]
        }, "Placebo thinking... hmmm..."

    if h == "79b61603d0169c516ed73490f4a53fbe4de9fd3455986f639445428195ec6ea3":
        return { "people": [
                {"xy" : [-10,-10]},
                {"xy" : [-11,-11]},
                {"xy" : [-10,-11]},
                {"xy" : [-10,-4.5]}
            ]
        }, "Placebo thinking... hmmm..."

    if h == "da05bd008e3e50e15fbf80e05800a34677515723141985e41855b34ca5a87fd9":
        # Question 14 _ 0
        return {
            "lines": [{"a": -0.5, "b": 4}, {"a": 0, "b": 7}]
        }, "Placebo thinking... hmmm..."

    if h == "e15cd2f415bc44a301fab0fcbadbe397a46575c70361a8f5df47d9a40a3b76c9":
        # Question 14 _ 1 Just test we can do squares
        return {
            "lines" : [
                {"a" : float("inf"), "b" : 10},
                {"a" : 0, "b" : 8},

            ]
        }, "Placebo thinking... hmmm..."

    if h in ["65005dd7285e22ba61db002a6e82cfc43b7525b27eea14655f7967f4460b8d86",
             "54d67aa2d94ee2a1391ecbf9b0f2de2a7bd4d1348f60a128fc723f786814f5c2",
             "af992743cffd7d15428baf290509378504f9360423fd0e287df590280ca19bc5",
             "fb8463620dd03e3aff518f77e41308d3adf20631684df87d215e30f34f437ff6"]:
        # A rather poor tetris run:
        return{
            "moves" :[
                    {"translationCount": 8, "rotationCount": 2},
                    {"translationCount": 5, "rotationCount": 2},
                    {"translationCount": 2, "rotationCount": 2},
                    {"translationCount": 9, "rotationCount": 1},
                    # And that's one row! Yay!. Now do a few random ones:
                    {"translationCount": 5, "rotationCount": 0},
                    {"translationCount": 1, "rotationCount": 1},
                    {"translationCount": 6, "rotationCount": 2},
                    {"translationCount": 4, "rotationCount": 3},
                    {"translationCount": 9, "rotationCount": 0},
                    {"translationCount": 1, "rotationCount": 1},
                    {"translationCount": 2, "rotationCount": 2},
                    {"translationCount": 3, "rotationCount": 3},
                    {"translationCount": 5, "rotationCount": 0},
                    {"translationCount": 1, "rotationCount": 1},
                    ]
                }, "Placebo thinking... hmmm..."

    if h == "01956a7a56f56435c831265792360719e0b05c155160bf0eaf3d7a1f92873efe":
        # ChatGPT 5.1 Thinking returned this, this is wrong, the volume is correct, but:
        # - The cone goes all the way to the ground/wall intersection. The cone should rest a bit up the wall.
        # - The angle of repose is way too steep. This isn't 33 degrees.
        # - The cone is not supposed to be pin-prick sharp, the pipe diameter is 25NB, which is 33.7mm ID,
        #   how is that 33.7mm wide circle of sand supposed to end up so sharp?

        return """
            cylinder(h=6.981743147997059, r1=4.533997014063981, r2=0, $fn=50);
        """, "Placebo thinking... hmmm..."

    if h in ["91ccb279941937df81a302c117e67586a1d63c477f92585abbc540883e9b16a7",
             "afda666b86b1fa2f9bab7816db7786fbe563f079bf440944b7631f07579c5743",
             "f3cbb75532fd330657e6238f603ce84b325ca322eba2342c4947e7e703329f7b",
             "86cd0c5e1fd11a405cc027d4db50f91c4d27f7d9c81d8d12f8613624536636ff"]:
        return "rotate([0,0,45]) cylinder(r1=30, r2=0,h=30, $fn=4);", "Placebo thinking... hmmm..."

    if h == "780ac9d70a12589ad9dcff02a5d50a6d5ce94ef42d05fc312044d6b91e58ccbb":
        return { "boxes" : [
            {"XyzMin": [0,0,0], "XyzMax": [5,3,2]},
            {"XyzMin": [0,0,2], "XyzMax": [5,3,4]},
            {"XyzMin": [0,0,4], "XyzMax": [5,3,6]},
            {"XyzMin": [0,0,6], "XyzMax": [5,3,8]},
            {"XyzMin": [0,0,8], "XyzMax": [5,3,10]},
            {"XyzMin": [0,0,10], "XyzMax": [5,3,12]},
            {"XyzMin": [0,0,12], "XyzMax": [5,3,14]},
        ]}, "Placebo thinking... hmmm..."

    if h == "23a9783ba0a22a989fe8de2436a8a5435f7406da2774969d4b3a433d7c59a7fd":
        return [
            {"x" : -1.500000, "y" : 2.598076, "z" : 0.000000, "q0" : 0.000000, "q1" : 0.000000, "q2" : 0.000000, "q3" : 1.000000},
        ], "Placebo thinking... hmmm..."

    if h == "0fbf410f5c365dbc0e05c62d5c9651f94a8f218ea98f601adadbf013ea97ae4e":
        return """
def m(l,b):
 r=math.radians
 return (l+180)/360,.5-math.log(math.tan(math.pi/4+r(b)/2))/(2*math.pi)
A=[(114,-35),(135,-35),(150,-37),(153,-28),(143,-11),(129,-14),(114,-22)]
T=[(144,-44),(147,-44),(148,-42),(146,-41),(144,-42)]
PA=[m(l,b)for l,b in A];PT=[m(l,b)for l,b in T];C=PA+PT
mx=min(p[0]for p in C);Mx=max(p[0]for p in C);my=min(p[1]for p in C);My=max(p[1]for p in C)
def s(P):return[((x-mx)/(Mx-mx),(y-my)/(My-my))for x,y in P]
PA,PT=s(PA),s(PT)
def h(x,y,P):
 c=False
 for i in range(len(P)):
  x1,y1=P[i-1];x2,y2=P[i]
  if((y1>y)!=(y2>y))and(x<(x2-x1)*(y-y1)/(y2-y1)+x1):c=not c
 return c
def f(x,y):return 1 if h(x,y,PA)or h(x,y,PT)else-1
""", "Placebo thinking... hmmm... Ash opens ChatGPT website and copy/pasted this... hmmm..."


    if h == "9de73558fd26633642b603790929dd6a15c468bf2170e03ea02f48da160b00a5":
        # Question 24
        return {
            "pointSequence" : [4, 10, 14, 15],
            "reasoning" : "Ash is just typing random numbers in."
        }, "They looked nice."

    if h == "a94fc81dfc2c2952ae38febdb9a0d2f14848e43b66ff40b15faf567606b3ab89":
        # Question 25
        return {
            "reasoning" : "Ash is just guessing",
            "triangles" : [[0,1,2],[3,4,5], [6,7,8], [9,10,11],[12,13,14],[15,0,1]]
        }, "Placebo thinking... hmmm..."

    if h == "c55ce2dea0508481f4643a0461798fe7b0e89b220473f7b9953da8cc02fd2f3f":
        # Question 26
        return {
            "reasoning" : "Ash is not even trying here. Sorry it's late and I have a meeting in the morning.",
            "nodes" : ["000000", "111111"]
        }, "Placebo thinking... hmmm..."

    if h == "":
        # Question 27
        moves = []
        for i in range(100):
            moves.append({"cellX" : random.randint(1, 29), "cellY" : random.randint(1, 5), "direction" : random.choice(["up", "down", "left", "right"])})
        return { "moves" : moves }, "Placebo thinking... hmmm..."
