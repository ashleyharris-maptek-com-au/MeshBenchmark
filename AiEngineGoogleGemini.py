"""
Google Gemini AI Engine for MeshBenchmark

This module provides an interface to the Google Gemini API using the latest google-genai SDK.

Setup:
1. Install the SDK: pip install google-genai
2. Set your API key as an environment variable:
   - Windows: set GEMINI_API_KEY=your_api_key_here
   - Linux/Mac: export GEMINI_API_KEY=your_api_key_here
   
Get your API key from: https://ai.google.dev/

The SDK documentation can be found at: https://googleapis.github.io/python-genai/
"""

# Constants that fine tune which model, whether reasoning is used and how much, and whether tools
# are made available.
MODEL = "gemini-2.5-flash"

# REASONING controls the thinking budget for extended reasoning:
# - 0: Thinking disabled (fastest, no reasoning)
# - -1: Dynamic thinking (model decides based on complexity)
# - 1-24576: Fixed thinking token budget (higher = more reasoning)
# Recommended: Start with low values (128-1024) for development, increase for production
REASONING = 1

# TOOLS enables tool capabilities (both built-in and custom):
# - False: No tools available
# - "google_search": Enable Google Search grounding
# - "code_execution": Enable Python code execution
# - List of functions: Enable custom function calling
# - List of strings/functions: Mix built-in and custom tools
# 
# Examples:
#   TOOLS = False                              # No tools
#   TOOLS = "google_search"                    # Just Google Search
#   TOOLS = "code_execution"                   # Just code execution
#   TOOLS = ["google_search", "code_execution"] # Both built-in tools
#   TOOLS = [my_function]                      # Custom function calling
#   TOOLS = ["code_execution", my_function]    # Mix built-in + custom
TOOLS = False

import os
import json
from google import genai
from google.genai import types

def GeminiAIHook(prompt : str, structure : dict | None) -> dict | str:
    """
This function is called by the test runner to get the AI's response to a prompt.

Prompt is the question to ask the AI.
Structure contains the JSON schema for the expected output. If it is None, the output is just a string.

There is no memory between calls to this function, the 'conversation' doesn't persist.
"""
    # Initialize the client - it will automatically use the GEMINI_API_KEY or GOOGLE_API_KEY
    # environment variable
    client = genai.Client()
    
    try:
        # Build configuration based on constants
        config_params = {}
        
        # Add structured output if schema provided
        if structure is not None:
            config_params['response_mime_type'] = 'application/json'
            config_params['response_schema'] = structure
        
        # Add thinking/reasoning configuration if REASONING is set
        # For gemini-2.5 models, use thinking_budget parameter
        if REASONING is not None and REASONING != 0:
            if "2.5" in MODEL or "2.0" in MODEL:
                # For Gemini 2.x models: use thinking_budget
                # 0 = off, -1 = dynamic, 1-24576 = fixed token budget
                config_params['thinking_config'] = types.ThinkingConfig(
                    thinking_budget=REASONING if REASONING != 1 else 128
                )
            elif "3" in MODEL:
                # For Gemini 3+ models: use thinking_level
                # Map numeric values to level strings
                level = "high" if REASONING > 512 else "low"
                config_params['thinking_config'] = types.ThinkingConfig(
                    thinking_level=level
                )
        
        # Add tools if specified (supports built-in and custom tools)
        if TOOLS and TOOLS is not False:
            tools_list = []
            
            # Handle single tool or list of tools
            tools_to_process = TOOLS if isinstance(TOOLS, list) else [TOOLS]
            
            for tool in tools_to_process:
                if isinstance(tool, str):
                    # Built-in tool specified by name
                    if tool == "google_search":
                        tools_list.append(types.Tool(google_search=types.GoogleSearch()))
                    elif tool == "code_execution":
                        tools_list.append(types.Tool(code_execution=types.ToolCodeExecution()))
                    else:
                        print(f"Warning: Unknown built-in tool '{tool}', ignoring")
                else:
                    # Custom function - pass directly (SDK handles it)
                    tools_list.append(tool)
            
            if tools_list:
                config_params['tools'] = tools_list
        
        # Create config object
        config = types.GenerateContentConfig(**config_params) if config_params else None
        
        # Generate content
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=config
        )
        
        # Parse and return response
        if structure is not None:
            return json.loads(response.text)
        else:
            return response.text
            
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # Return appropriate empty response based on structure
        if structure is not None:
            return {}
        else:
            return ""