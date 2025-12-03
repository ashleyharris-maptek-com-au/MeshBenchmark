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

import hashlib

# Constants that fine tune which model, whether reasoning is used and how much, and whether tools
# are made available.
MODEL = "gemini-2.5-flash"

# REASONING controls reasoning effort on a 0-10 scale:
# - 0 or False: Thinking disabled (fastest, no reasoning)
# - 1-3: Low reasoning (maps to ~128-1024 token budget)
# - 4-7: Medium reasoning (maps to ~2048-8192 token budget)  
# - 8-10: High reasoning (maps to ~12288-24576 token budget)
REASONING = False

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

configAndSettingsHash = hashlib.sha256(MODEL.encode() + str(REASONING).encode() + str(TOOLS).encode()).hexdigest()

def Configure(Model, Reasoning, Tools):
    global MODEL
    global REASONING
    global TOOLS
    global configAndSettingsHash
    MODEL = Model
    REASONING = Reasoning
    TOOLS = Tools
    configAndSettingsHash = hashlib.sha256(MODEL.encode() + str(REASONING).encode() + str(TOOLS).encode()).hexdigest()

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
    
    Returns tuple of (result, chainOfThought).
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
        # Map 0-10 scale to Gemini's thinking_budget (0-24576)
        if REASONING and REASONING != 0:
            # Map 1-10 to appropriate token budgets
            if isinstance(REASONING, int) and REASONING > 0:
                if REASONING <= 3:
                    thinking_budget = 128 * (2 ** (REASONING - 1))  # 128, 256, 512
                elif REASONING <= 7:
                    thinking_budget = 1024 * (2 ** (REASONING - 4))  # 1024, 2048, 4096, 8192
                else:
                    thinking_budget = 8192 * (2 ** (REASONING - 7))  # 8192, 16384, 24576 (capped)
                thinking_budget = min(thinking_budget, 24576)  # Cap at max
            else:
                thinking_budget = 1024  # Default for truthy non-int values
            
            config_params['thinking_config'] = types.ThinkingConfig(
                thinking_budget=thinking_budget
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
        
        # Generate content with streaming to capture thinking in real-time
        chainOfThought = ""
        output_text = ""
        current_thinking_line = ""
        
        stream = client.models.generate_content_stream(
            model=MODEL,
            contents=prompt,
            config=config
        )
        
        for chunk in stream:
            # Process each candidate in the chunk
            for candidate in chunk.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        # Check if this is a thinking part
                        if hasattr(part, 'thought') and part.thought:
                            # This is thinking content
                            thought_text = part.text if hasattr(part, 'text') else ""
                            current_thinking_line += thought_text
                            # Print complete lines as they arrive
                            while "\n" in current_thinking_line:
                                line, current_thinking_line = current_thinking_line.split("\n", 1)
                                print(f"Thinking: {line}", flush=True)
                                chainOfThought += line + "\n"
                        elif hasattr(part, 'text') and part.text:
                            # This is regular output content
                            output_text += part.text
        
        # Flush any remaining thinking content
        if current_thinking_line:
            print(f"Thinking: {current_thinking_line}", flush=True)
            chainOfThought += current_thinking_line
        
        # Strip trailing newline from chain of thought
        chainOfThought = chainOfThought.rstrip("\n")
        
        if chainOfThought:
            print()  # Blank line after thinking
        
        print(output_text)
        
        # Parse and return response
        if structure is not None:
            if output_text:
                return json.loads(output_text), chainOfThought
            return {}, chainOfThought
        else:
            return output_text or "", chainOfThought
            
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # Return appropriate empty response based on structure
        if structure is not None:
            return {}, ""
        else:
            return "", ""