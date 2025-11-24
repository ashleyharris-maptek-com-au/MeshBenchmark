import subprocess
import tempfile
import StlVolume
import os

openScadPath = R"C:\Program Files (x86)\OpenSCAD\openscad.exe"

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
        # get the reference scad and result to scad from the globals:
        if "referenceScad" in g:
            resultToScad = g["resultToScad"]
        
            if "prepareSubpassReferenceScad" in g:
                referenceScad = g["prepareSubpassReferenceScad"](subPass)
            else:
                referenceScad = g["referenceScad"]

            resultAsScad = resultToScad(result)

            # Dump the result to temp directory as result_{index}_{subPass}.scad:
            resultFile = os.path.join(tempfile.gettempdir(), "result_" + str(index) + "_" + str(subPass) + ".scad")
            with open(resultFile, "w") as f:
                if "scadModules" in g:
                  f.write(g["scadModules"])
                f.write(resultAsScad)
                f.write("minkowski(){cube(0.001);result();}")

            # Dump the reference to temp directory as reference_{index}_{subPass}.scad:
            referenceFile = os.path.join(tempfile.gettempdir(), "reference_" + str(index) + "_" + str(subPass) + ".scad")
            with open(referenceFile, "w") as f:
                if "scadModules" in g:
                  f.write(g["scadModules"])
                f.write(referenceScad)
                f.write("minkowski(){cube(0.001);reference();}")

            compareFile1 = os.path.join(tempfile.gettempdir(), "compare1_" + str(index) + "_" + str(subPass) + ".scad")
            compareFile2 = os.path.join(tempfile.gettempdir(), "compare2_" + str(index) + "_" + str(subPass) + ".scad")

            with open(compareFile1, "w") as f:
                f.write((
                    "use <result_" + str(index) + "_" + str(subPass) + ".scad>;\n"
                    "use <reference_" + str(index) + "_" + str(subPass) + ".scad>;\n").
                        replace("{index}", str(index)).replace("{subPass}", str(subPass)))

                if "scadModules" in g:
                  f.write(g["scadModules"])

                f.write("""
    minkowski(){
        cube(0.001);
        intersection() 
        {
            result();
            reference();
        }
    }""")


            with open(compareFile2, "w") as f:
                f.write((
                    "use <result_" + str(index) + "_" + str(subPass) + ".scad>;\n"
                    "use <reference_" + str(index) + "_" + str(subPass) + ".scad>;\n").
                        replace("{index}", str(index)).replace("{subPass}", str(subPass)))

                if "scadModules" in g:
                  f.write(g["scadModules"])

                f.write("""
    minkowski(){
        cube(0.001);
    difference() 
    {
        union() 
        {
            result();   
            reference();
        }   
        intersection() 
        {
            result();
            reference();
        }        
    }}""")

            try: 
                os.remove("reference_" + str(index) + "_" + str(subPass) + ".stl") 
            except: pass
            try: 
                os.remove("output_" + str(index) + "_" + str(subPass) + ".stl") 
            except: pass
            try: 
                os.remove("result1_" + str(index) + "_" + str(subPass) + ".stl") 
            except: pass
            try:
                os.remove("result2_" + str(index) + "_" + str(subPass) + ".stl") 
            except: pass

            subprocess.run([openScadPath, "-o", "reference_" + str(index) + "_" + str(subPass) + ".stl", referenceFile])
            subprocess.run([openScadPath, "-o", "output_" + str(index) + "_" + str(subPass) + ".stl", resultFile])
            subprocess.run([openScadPath, "-o", "result1_" + str(index) + "_" + str(subPass) + ".stl", compareFile1])
            subprocess.run([openScadPath, "-o", "result2_" + str(index) + "_" + str(subPass) + ".stl", compareFile2])
            

            resultVolume = StlVolume.calculate_stl_volume("output_" + str(index) + "_" + str(subPass) + ".stl")
            referenceVolume = StlVolume.calculate_stl_volume("reference_" + str(index) + "_" + str(subPass) + ".stl")
            intersectionVolume = StlVolume.calculate_stl_volume("result1_" + str(index) + "_" + str(subPass) + ".stl")
            differenceVolume = StlVolume.calculate_stl_volume("result2_" + str(index) + "_" + str(subPass) + ".stl")
            
            print("Result Volume: " + str(resultVolume))
            print("Reference Volume: " + str(referenceVolume))
            print("Intersection Volume: " + str(intersectionVolume))
            print("Difference Volume: " + str(differenceVolume))

            score = intersectionVolume / referenceVolume

            if "volumeValidateDelta" in g:
                # Adjust the scores
                score += g["volumeValidateDelta"](result, resultVolume, referenceVolume, intersectionVolume, differenceVolume)

            score -= differenceVolume / referenceVolume
            score = max(0, score)
            totalScore += score

        elif "gradeAnswer" in g:
            totalScore += g["gradeAnswer"](result, subPass)

    return totalScore / len(results)

score = runTest(5)
print(score)