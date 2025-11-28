"""
Examples of using built-in tools in Google Gemini:
1. Google Search (grounding)
2. Code Execution

These are separate from custom function calling and are provided by Google.

Before running:
1. Install google-genai: pip install google-genai
2. Set your API key: set GEMINI_API_KEY=your_api_key_here
"""

from google import genai
from google.genai import types

def example_google_search():
    """
    Example: Using Google Search grounding for real-time information.
    
    The model will automatically search Google when it needs up-to-date info.
    """
    print("="*70)
    print("EXAMPLE 1: Google Search Grounding")
    print("="*70 + "\n")
    
    client = genai.Client()
    
    # Create the Google Search tool
    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )
    
    # Configure with the search tool
    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )
    
    # Ask a question that needs current information
    prompt = "What are the latest developments in AI models released in 2024?"
    
    print(f"Prompt: {prompt}\n")
    print("Searching Google and generating response...\n")
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )
    
    print("Response:")
    print(response.text)
    print("\n" + "="*70 + "\n")

def example_code_execution():
    """
    Example: Using code execution for computational tasks.
    
    The model will generate Python code, execute it, and use the results.
    Available libraries: numpy, scipy, matplotlib, pandas, sympy, and more.
    """
    print("="*70)
    print("EXAMPLE 2: Code Execution")
    print("="*70 + "\n")
    
    client = genai.Client()
    
    # Create the code execution tool
    code_tool = types.Tool(
        code_execution=types.ToolCodeExecution()
    )
    
    # Configure with the code execution tool
    config = types.GenerateContentConfig(
        tools=[code_tool]
    )
    
    # Ask a computational question
    prompt = """
    Calculate the volume of a hemispherical shell with:
    - Inner radius: 4 cm
    - Outer radius: 7 cm
    
    Use Python code to calculate this. Show the code and result.
    """
    
    print(f"Prompt: {prompt}\n")
    print("Generating and executing code...\n")
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )
    
    # The response contains multiple parts: text, code, and execution results
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print("Text Response:")
            print(part.text)
            print()
        
        if part.executable_code is not None:
            print("Generated Code:")
            print(part.executable_code.code)
            print()
        
        if part.code_execution_result is not None:
            print("Execution Result:")
            print(part.code_execution_result.output)
            print()
    
    print("="*70 + "\n")

def example_combined_tools():
    """
    Example: Using both Google Search and Code Execution together.
    
    The model can search for information AND execute code in the same request.
    """
    print("="*70)
    print("EXAMPLE 3: Combined Tools (Search + Code Execution)")
    print("="*70 + "\n")
    
    client = genai.Client()
    
    # Create both tools
    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )
    code_tool = types.Tool(
        code_execution=types.ToolCodeExecution()
    )
    
    # Configure with both tools
    config = types.GenerateContentConfig(
        tools=[grounding_tool, code_tool]
    )
    
    prompt = """
    Find the current population of the 5 largest cities in the world,
    then calculate their total combined population. Show your work.
    """
    
    print(f"Prompt: {prompt}\n")
    print("Using search and code execution...\n")
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )
    
    # Display all parts
    for i, part in enumerate(response.candidates[0].content.parts):
        if part.text is not None:
            print(f"Text Part {i+1}:")
            print(part.text)
            print()
        
        if part.executable_code is not None:
            print(f"Code Part {i+1}:")
            print(part.executable_code.code)
            print()
        
        if part.code_execution_result is not None:
            print(f"Execution Result {i+1}:")
            print(part.code_execution_result.output)
            print()
    
    print("="*70 + "\n")

def example_with_structured_output():
    """
    Example: Using code execution with structured JSON output.
    
    You can combine built-in tools with structured output schemas.
    """
    print("="*70)
    print("EXAMPLE 4: Code Execution + Structured JSON Output")
    print("="*70 + "\n")
    
    client = genai.Client()
    
    # Create the code execution tool
    code_tool = types.Tool(
        code_execution=types.ToolCodeExecution()
    )
    
    # Define JSON schema
    structure = {
        "type": "object",
        "properties": {
            "volume_formula": {"type": "string"},
            "volume_mm3": {"type": "number"},
            "calculation_code": {"type": "string"}
        },
        "required": ["volume_formula", "volume_mm3", "calculation_code"]
    }
    
    # Configure with both tool and structured output
    config = types.GenerateContentConfig(
        tools=[code_tool],
        response_mime_type='application/json',
        response_schema=structure
    )
    
    prompt = """
    Calculate the volume of a hemisphere with radius 50mm.
    Provide the formula, the calculated volume, and the Python code used.
    """
    
    print(f"Prompt: {prompt}\n")
    print("Generating structured response with code execution...\n")
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )
    
    print("Structured JSON Response:")
    import json
    result = json.loads(response.text)
    print(json.dumps(result, indent=2))
    
    print("\n" + "="*70 + "\n")

def example_mesh_benchmark_use_case():
    """
    Example: How code execution could help with MeshBenchmark tasks.
    """
    print("="*70)
    print("EXAMPLE 5: MeshBenchmark Use Case")
    print("="*70 + "\n")
    
    client = genai.Client()
    
    # Code execution for geometry calculations
    code_tool = types.Tool(
        code_execution=types.ToolCodeExecution()
    )
    
    # Structure for brick placements
    structure = {
        "type": "object",
        "properties": {
            "bricks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "Centroid": {
                            "type": "array",
                            "items": {"type": "number"}
                        },
                        "RotationDegrees": {"type": "number"}
                    }
                }
            },
            "total_bricks": {"type": "integer"},
            "calculation_notes": {"type": "string"}
        }
    }
    
    config = types.GenerateContentConfig(
        tools=[code_tool],
        response_mime_type='application/json',
        response_schema=structure
    )
    
    prompt = """
    Generate positions for 5 lego bricks (32mm x 16mm x 9.6mm) arranged in a circle
    pattern around the origin. Calculate their positions using code.
    """
    
    print(f"Prompt: {prompt}\n")
    print("Generating brick placements with code execution...\n")
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )
    
    print("Generated Brick Placements:")
    import json
    result = json.loads(response.text)
    print(json.dumps(result, indent=2))
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Google Gemini Built-in Tools Examples")
    print("="*70 + "\n")
    
    try:
        # Example 1: Google Search
        example_google_search()
        
        # Example 2: Code Execution
        example_code_execution()
        
        # Example 3: Combined Tools
        example_combined_tools()
        
        # Example 4: Structured Output + Code
        example_with_structured_output()
        
        # Example 5: MeshBenchmark Use Case
        example_mesh_benchmark_use_case()
        
        print("="*70)
        print("All examples completed! ✓")
        print("="*70)
        print("\nKey Takeaways:")
        print("- Google Search: types.Tool(google_search=types.GoogleSearch())")
        print("- Code Execution: types.Tool(code_execution=types.ToolCodeExecution())")
        print("- Can combine both tools in one request")
        print("- Works with structured JSON output")
        print("- Code execution has numpy, scipy, matplotlib, pandas, sympy available")
        
    except Exception as e:
        print(f"\n✗ Examples failed with error: {e}")
        import traceback
        traceback.print_exc()
