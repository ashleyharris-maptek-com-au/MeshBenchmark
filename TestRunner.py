import VolumeComparison

def runTest(index : int):
    # load test file, compile it, and get its globals in a map:
    g = {}
    exec(open("" + str(index) + ".py").read(), g)
    
    prompts = []
    structure = g["structure"]

    if "prepareSubpassPrompt" in g:
        # get the prompt and structure from the globals:
        subPass = 0
        while True:
            try:
                prompts.append(g["prepareSubpassPrompt"](subPass))
                subPass += 1
            except StopIteration:
                break
    else:
        prompts.append(g["prompt"])
    

    #results = []
    #for prompt in prompts:
    #    results.append(aiHook(prompt, structure))

    results = g["gemini3Answer"]; 

    totalScore = 0

    for subPass, result in enumerate(results):
        # Some tests create data against a reference OpenSCAD data:
        if "referenceScad" in g:
            score = VolumeComparison.compareVolumeAgainstOpenScad(index, subPass, result, g)
            totalScore += score
        elif "gradeAnswer" in g:
            totalScore += g["gradeAnswer"](result, subPass)

    return totalScore / len(results)

score = runTest(5)
print(score)