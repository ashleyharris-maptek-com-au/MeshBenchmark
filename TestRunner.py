import VolumeComparison
from typing import Dict, List, Any
import os
import base64
import html
from concurrent.futures import ThreadPoolExecutor, as_completed

def runTest(index: int, aiEngineHook : callable, aiEngineName : str) -> Dict[str, Any]:
    """
    Run a test and return results including score and any generated images.
    
    Returns a dictionary containing:
        - 'average_score': float - average score across all subpasses
        - 'total_score': float - sum of all subpass scores
        - 'subpass_count': int - number of subpasses completed
        - 'subpass_results': list of dicts with individual subpass results
    """
    # load test file, compile it, and get its globals in a map:
    g = {}

    if not os.path.exists(str(index) + ".py"):
        raise StopIteration
    
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
    

    # Parallelize AI engine calls
    results = []
    with ThreadPoolExecutor() as executor:
        # Submit all prompts in parallel
        future_to_index = {executor.submit(aiEngineHook, prompt, structure): i for i, prompt in enumerate(prompts)}
        
        # Collect results in the correct order
        results = [None] * len(prompts)
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            results[idx] = future.result()
    
    # Handle placebo mode
    if aiEngineName == "Placebo":
        first_result = next((r for r in results if r is not None), None)
        if first_result is not None:
            results = [r if r is not None else first_result for r in results]

    # Parallelize result processing and grading
    def process_subpass(subPass, result):
        score = 0
        subpass_data = {
            "subpass": subPass,
            "score": 0,
        }
        
        if not result:
            print(f"No answer generated for subpass {subPass}")
            subpass_data["score"] = 0
        elif "resultToImage" in g:
            score = g["gradeAnswer"](result, subPass, aiEngineName)
            output_path = g["resultToImage"](result, subPass, aiEngineName)
            if "resultToNiceReport" in g:
                subpass_data["output_nice"] = g["resultToNiceReport"](result, subPass, aiEngineName)
            else:
                subpass_data["output_text"] = result
                subpass_data["output_image"] = output_path
            subpass_data["score"] = score

        elif "referenceScad" in g:
            # Some tests require an OpenSCAD comparison to check if the generated
            # shape closely resembles some reference data.
            comparison_result = VolumeComparison.compareVolumeAgainstOpenScad(
                index, subPass, result, g
            )
            score = comparison_result["score"]
            subpass_data["score"] = score
            subpass_data["output_image"] = comparison_result.get("output_image")
            subpass_data["reference_image"] = comparison_result.get("reference_image")
            subpass_data["temp_dir"] = comparison_result.get("temp_dir")
        elif "gradeAnswer" in g:
            # Some tests require a custom grading function.
            score = g["gradeAnswer"](result, subPass, aiEngineName)
            subpass_data["score"] = score

            if "resultToNiceReport" in g:
                subpass_data["output_nice"] = g["resultToNiceReport"](result, subPass, aiEngineName)
            else:
                subpass_data["output_text"] = result
        
        return score, subpass_data
    
    totalScore = 0
    subpass_results = [None] * len(results)
    
    with ThreadPoolExecutor() as executor:
        # Submit all subpass processing in parallel
        future_to_subpass = {executor.submit(process_subpass, subPass, result): subPass 
                            for subPass, result in enumerate(results)}
        
        # Collect results in the correct order
        for future in as_completed(future_to_subpass):
            subPass = future_to_subpass[future]
            score, subpass_data = future.result()
            totalScore += score
            subpass_results[subPass] = subpass_data

    return {
        "average_score": totalScore / len(results) if results else 0,
        "total_score": totalScore,
        "subpass_count": len(subpass_results),
        "subpass_results": subpass_results
    }


def runAllTests(aiEngineHook : callable, aiEngineName : str):
    # Create a results directory if it doesn't exist
    if not os.path.exists("results"):
        os.makedirs("results")

    # Create a results file for the html results of this engines test run
    results_file = open("results/" + aiEngineName + ".html", "w", buffering=1)
    results_file.write("<html>\n<head>\n<style>\n")
    results_file.write("""    table { border-collapse: collapse; width: 100%; margin: 20px 0; }
    th, td { border: 1px solid #ddd; padding: 12px; text-align: left; vertical-align: top; }
    th { background-color: #4CAF50; color: white; }
    .test-header { background-color: #45a049; font-weight: bold; }
    .prompt-row { background-color: #f9f9f9; font-style: italic; }
    .subpass-row { background-color: #ffffff; }
    img { max-width: 100%; height: auto; border: 1px solid #ccc; }
    .score-good { color: green; font-weight: bold; }
    .score-bad { color: red; font-weight: bold; }
    h1 { color: #333; }
    h2 { color: #666; margin-top: 30px; }
""")
    results_file.write("</style>\n<meta charset='UTF-8'/> </head>\n<body>\n")
    results_file.write("<h1>Benchmark Results for " + aiEngineName + "</h1>\n")
    results_file.write("<table>\n")
    
    testIndex = 1
    overall_total_score = 0
    overall_max_score = 0
    
    while True:
        try:
            if not os.path.exists(str(testIndex) + ".py"):
                break
            test_result = {}
            # Load test metadata
            test_globals = {}
            exec(open(str(testIndex) + ".py").read(), test_globals)
            
            if testIndex == 19:
                test_result = runTest(testIndex, aiEngineHook, aiEngineName)
            else:
                test_result = {"total_score": 0, "subpass_count": 0, "subpass_results": []}

            testIndex += 1

            # Calculate max score for this test (1 point per subpass)
            max_score = test_result['subpass_count']
            overall_total_score += test_result['total_score']
            overall_max_score += max_score
            
        except StopIteration:
            break
        
        # Console output
        print("\n" + "="*60)
        print(f"TEST {testIndex-1} RESULTS")
        print("="*60)
        print(f"Score: {test_result['total_score']:.2f} / {max_score}")
        print(f"Subpasses Completed: {test_result['subpass_count']}")
        print("\nSubpass Details:")
        
        for subpass in test_result['subpass_results']:
            print(f"  Subpass {subpass['subpass']}: Score = {subpass['score']:.4f}")
        
        # HTML output
        
        # Header row: Test name, number of subpasses, score
        test_name = f"Test {testIndex-1}"
        
        # Extract test purpose from title or prompt (first line)
        test_purpose = ""
        if "title" in test_globals:
            test_purpose = test_globals["title"]
        elif "prompt" in test_globals:
            prompt_lines = test_globals["prompt"].strip().split("\n")
            test_purpose = prompt_lines[0] if prompt_lines else "No description available"
        else:
            test_purpose = "Unnamed test"
        
        score_class = "score-good" if test_result['total_score'] >= max_score * 0.7 else "score-bad"
        
        results_file.write("  <tr class='test-header'>\n")
        results_file.write(f"    <th colspan=2>{test_name}: {test_purpose}</th>\n")
        results_file.write(f"    <th>Subpasses: {test_result['subpass_count']}</th>\n")
        results_file.write(f"    <th class='{score_class}'>Score: {test_result['total_score']:.2f} / {max_score}</th>\n")
        results_file.write("  </tr>\n")
        
        # Prompt row: Typical prompt and how it changes
        results_file.write("  <tr class='prompt-row'>\n")
        results_file.write("    <td colspan='3'><strong>Typical Prompt:</strong><br>")
        
        if "prepareSubpassPrompt" in test_globals:
            # Show first subpass prompt
            try:
                first_prompt = test_globals["prepareSubpassPrompt"](0)
                results_file.write(first_prompt.replace("\n", "<br>"))
            except:
                results_file.write("Dynamic prompt generation")
        elif "prompt" in test_globals:
            prompt_text = test_globals["prompt"].strip()
            results_file.write(prompt_text.replace("\n", "<br>"))
        else:
            results_file.write("No prompt available")
        
        results_file.write("</td>\n")
        results_file.write("    <td><strong>Prompt Changes:</strong><br>")
        
        if "promptChangeSummary" in test_globals:
            results_file.write(test_globals["promptChangeSummary"])
        elif "prepareSubpassPrompt" in test_globals:
            results_file.write("Prompt parameters change between subpasses (increasing difficulty)")
        else:
            results_file.write("Prompt remains constant")
        
        results_file.write("</td>\n")
        results_file.write("  </tr>\n")
        
        # Subpass rows
        for subpass in test_result['subpass_results']:
            results_file.write("  <tr class='subpass-row'>\n")
            
            # Subpass overview
            results_file.write(f"    <td><strong>Subpass {subpass['subpass']}</strong><br>")
            if "subpassParamSummary" in test_globals and subpass['subpass'] < len(test_globals["subpassParamSummary"]):
                results_file.write(f"Parameters: {test_globals['subpassParamSummary'][subpass['subpass']]}<br>")
            elif "prepareSubpassPrompt" in test_globals:
                try:
                    subpass_prompt = test_globals["prepareSubpassPrompt"](subpass['subpass'])
                    # Extract parameters from prompt
                    results_file.write("Parameters: ")
                    if "PARAM_" in subpass_prompt:
                        results_file.write("(modified from base prompt)")
                    else:
                        results_file.write("(see typical prompt)")
                except:
                    results_file.write("Subpass configuration")
            else:
                results_file.write("Same as typical prompt")
            results_file.write("</td>\n")
            
            # Images
            if 'output_image' in subpass and subpass['output_image']:
                # Actual image
                results_file.write("    <td>")
                if os.path.exists(subpass['output_image']):
                    try:
                        with open(subpass['output_image'], 'rb') as img_file:
                            img_data = base64.b64encode(img_file.read()).decode('utf-8')
                            results_file.write(f"<img src='data:image/png;base64,{img_data}' alt='Output'>")
                    except:
                        results_file.write(f"<a href='../{subpass['output_image']}'>View Output Image</a>")
                else:
                    results_file.write("Image not found")
                results_file.write("</td>\n")
                
                # Reference image
                results_file.write("    <td>")
                if 'reference_image' in subpass and subpass['reference_image'] and os.path.exists(subpass['reference_image']):
                    try:
                        with open(subpass['reference_image'], 'rb') as img_file:
                            img_data = base64.b64encode(img_file.read()).decode('utf-8')
                            results_file.write(f"<img src='data:image/png;base64,{img_data}' alt='Reference'>")
                    except:
                        results_file.write(f"<a href='../{subpass['reference_image']}'>View Reference Image</a>")
                else:
                    results_file.write("No reference image")
                results_file.write("</td>\n")
            elif "output_nice" in subpass:
                # Nice preformatted output, if it contains table cells just display as is:
                if "</td><td>" in subpass["output_nice"]:
                    results_file.write(subpass["output_nice"])
                else:
                    results_file.write("    <td colspan='2'>" + subpass["output_nice"] + "</td>\n")
            elif "output_text" in subpass:
                # Text output only
                results_file.write("    <td colspan='2'><pre>" + html.escape(str(subpass["output_text"])) + "</pre></td>\n")
            else:
                # No images for this test type
                results_file.write("    <td>N/A (LLM did not answer)</td>\n")
                results_file.write("    <td>N/A (Test forfeited)</td>\n")
            
            # Score
            score_class = "score-good" if subpass['score'] >= 0.7 else "score-bad"
            results_file.write(f"    <td class='{score_class}'><strong>{subpass['score']:.4f}</strong></td>\n")
            results_file.write("  </tr>\n")
        
    
    # Overall summary
    results_file.write("<h2>Overall Summary</h2>\n")
    results_file.write("<table>\n")
    results_file.write("  <tr class='test-header'>\n")
    results_file.write("    <th>Total Tests</th>\n")
    results_file.write("    <th>Overall Score</th>\n")
    results_file.write("    <th>Percentage</th>\n")
    results_file.write("  </tr>\n")
    results_file.write("  <tr>\n")
    results_file.write(f"    <td>{testIndex - 1}</td>\n")
    results_file.write(f"    <td>{overall_total_score:.2f} / {overall_max_score}</td>\n")
    percentage = (overall_total_score / overall_max_score * 100) if overall_max_score > 0 else 0
    results_file.write(f"    <td>{percentage:.1f}%</td>\n")
    results_file.write("  </tr>\n")
    results_file.write("</table>\n")
    
    results_file.write("</body>\n</html>\n")
    results_file.close()
    
    print("\n" + "="*60)
    print("BENCHMARK COMPLETE")
    print("="*60)
    print(f"Total Score: {overall_total_score:.2f} / {overall_max_score} ({percentage:.1f}%)")
    print(f"Results saved to: results/{aiEngineName}.html")
    print("="*60)

    scores = {}

    if not os.path.exists("results/results.txt"):
        with open("results/results.txt", "w") as f:
            f.write("\n")

    with open("results/results.txt", "r") as f:
        for line in f:
            if ":" in line:
                scores[line.split(":")[0].strip()] = line.split(":")[1].strip()

    scores[aiEngineName] = overall_total_score / overall_max_score

    with open("results/results.txt", "w") as f:
        for key, value in scores.items():
            f.write(f"{key}: {value}\n")

    # Generate a summary page of the results, suitable for use as a github landing page,
    # including a big graph of the results by engine name
    
    import matplotlib.pyplot as plt 
    import pandas as pd
    
    df = pd.read_csv("results/results.txt", sep=":", header=None, names=["Engine", "Score"])
    df.plot(kind="bar", x="Engine", y="Score", legend=False)
    plt.title("Mesh Benchmark Results")
    plt.xlabel("Engine")
    plt.ylabel("Score")
    plt.savefig("results/topLevelResults.png")
    plt.close()
    
    # Generate index.html landing page
    with open("results/index.html", "w", encoding="utf-8") as index_file:
        index_file.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mesh Benchmark Results</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1 {
            margin: 0 0 10px 0;
            font-size: 2.5em;
        }
        .subtitle {
            opacity: 0.9;
            font-size: 1.1em;
        }
        .graph-container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .graph-container img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }
        .results-table {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th {
            background-color: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 15px;
            border-bottom: 1px solid #eee;
        }
        tr:hover {
            background-color: #f8f9fa;
        }
        tr:last-child td {
            border-bottom: none;
        }
        .score-cell {
            font-weight: bold;
            font-size: 1.1em;
        }
        .score-high {
            color: #10b981;
        }
        .score-medium {
            color: #f59e0b;
        }
        .score-low {
            color: #ef4444;
        }
        a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        a:hover {
            text-decoration: underline;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
        }
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 600;
            margin-left: 10px;
        }
        .badge-best {
            background-color: #dcfce7;
            color: #166534;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔺 Mesh Benchmark Results</h1>
        <p class="subtitle">Comparative performance analysis of AI engines on mesh-related tasks</p>
    </div>
    
    <div class="graph-container">
        <h2 style="margin-top: 0; color: #333;">Performance Overview</h2>
        <img src="topLevelResults.png" alt="Benchmark Results Graph">
    </div>
    
    <div class="results-table">
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Engine Name</th>
                    <th>Score</th>
                    <th>Percentage</th>
                    <th>Detailed Results</th>
                </tr>
            </thead>
            <tbody>
""")
        
        # Sort engines by score (descending)
        sorted_engines = sorted(scores.items(), key=lambda x: float(x[1]), reverse=True)
        best_score = float(sorted_engines[0][1]) if sorted_engines else 0
        
        for rank, (engine_name, score) in enumerate(sorted_engines, 1):
            score_float = float(score)
            percentage = score_float * 100
            
            # Determine score class
            if percentage >= 70:
                score_class = "score-high"
            elif percentage >= 40:
                score_class = "score-medium"
            else:
                score_class = "score-low"
            
            # Add best badge
            badge = '<span class="badge badge-best">BEST</span>' if rank == 1 else ''
            
            index_file.write(f"""                <tr>
                    <td><strong>#{rank}</strong></td>
                    <td>{html.escape(engine_name)}{badge}</td>
                    <td class="score-cell {score_class}">{score_float:.4f}</td>
                    <td class="{score_class}">{percentage:.1f}%</td>
                    <td><a href="{html.escape(engine_name)}.html">View Details →</a></td>
                </tr>
""")

        index_file.write("""            </tbody>
        </table>
    </div>
    
    <div class="footer">
        <p>Generated automatically by TestRunner.py</p>
        <p>Last updated: """ + __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
</body>
</html>
""")
    
    print(f"Landing page saved to: results/index.html")

    

if __name__ == "__main__":
    import AiEnginePlacebo
    runAllTests(AiEnginePlacebo.PlaceboAIHook, "Placebo")