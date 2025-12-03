"""
OpenAI ChatGPT AI Engine for MeshBenchmark

This module provides an interface to the OpenAI API using the Responses API.

Setup:
1. Install the SDK: pip install openai
2. Set your API key as an environment variable:
   - Windows: set OPENAI_API_KEY=your_api_key_here
   - Linux/Mac: export OPENAI_API_KEY=your_api_key_here
   
Get your API key from: https://platform.openai.com/api-keys

The SDK documentation can be found at: https://platform.openai.com/docs
Responses API reference: https://platform.openai.com/docs/api-reference/responses
"""

# Constants that fine tune which model, reasoning mode, and tools
import hashlib


MODEL = "gpt-5-nano" 

# REASONING controls reasoning mode:
# - False or 0: No special reasoning (standard mode)
# - "o1-preview": Use o1-preview model with extended reasoning
# - "o1-mini": Use o1-mini model (faster reasoning)
# - Integer (1-10): Reasoning effort level (for o1 models)
REASONING = False

# TOOLS enables tool capabilities:
# - False: No tools available
# - True: Enable ALL built-in tools (web_search, code_interpreter, file_search)
# - List of function definitions: Enable specific custom tools
# 
# Examples:
#   TOOLS = False                    # No tools
#   TOOLS = True                     # All built-in tools
#   TOOLS = [function_def]           # Custom function only
#   TOOLS = [func1, func2]           # Multiple custom functions
# 
# Note: Built-in tools require specific API access/models
TOOLS = False

configAndSettingsHash = hashlib.sha256(MODEL.encode() + str(REASONING).encode() + str(TOOLS).encode()).hexdigest()

def Configure(Model, Reasing, Tools):
    global MODEL
    global REASONING
    global TOOLS
    global configAndSettingsHash
    MODEL = Model
    REASONING = Reasing
    TOOLS = Tools
    configAndSettingsHash = hashlib.sha256(MODEL.encode() + str(REASONING).encode() + str(TOOLS).encode()).hexdigest()

import os
import json

def ChatGPTAIHook(prompt: str, structure: dict | None) -> dict | str:
    """
    This function is called by the test runner to get the AI's response to a prompt.
    
    Prompt is the question to ask the AI.
    Structure contains the JSON schema for the expected output. If it is None, the output is just a string.
    
    There is no memory between calls to this function, the 'conversation' doesn't persist.
    
    Uses the OpenAI Responses API.
    """
    from openai import OpenAI
    
    try:
        # Initialize the client - it will automatically use OPENAI_API_KEY environment variable
        client = OpenAI(timeout=3600)
    
        # Determine model to use
        model_to_use = MODEL
        
        # Override model if REASONING specifies an o1 model
        if isinstance(REASONING, str) and REASONING in ["o1-preview", "o1-mini"]:
            model_to_use = REASONING
        
        # Build Responses API parameters
        response_params = {
            "model": model_to_use,
            "input": prompt,
            "service_tier": "flex"
        }
        
        # Add reasoning effort
        if isinstance(REASONING, int) and REASONING > 0:
            # Map 1-10 scale to low/medium/high
            if REASONING <= 3:
                response_params["reasoning"] = {"effort": "low"}
            elif REASONING <= 7:
                response_params["reasoning"] = {"effort": "medium"}
            else:
                response_params["reasoning"] = {"effort": "high"}

            response_params["reasoning"]["summary"] = "auto"
        
        # Handle structured output using the text.format parameter
        if structure is not None:
            response_params["text"] = {
                "format": {
                    "type": "json_schema",
                    "name": "structured_response",
                    "schema": structure,
                    "strict": True
                }
            }
        
        # Add tools if specified
        if TOOLS is True:
            # Enable built-in hosted tools
            # Note: file_search requires a vector_store, so it's excluded
            response_params["tools"] = [
                {"type": "web_search"},
                {"type": "code_interpreter", "container": {"type": "auto"}}
            ]
        elif TOOLS and TOOLS is not False:
            # Convert function list to OpenAI tool format if needed
            tools_list = []
            for tool in (TOOLS if isinstance(TOOLS, list) else [TOOLS]):
                if isinstance(tool, dict):
                    # Already in correct format
                    tools_list.append(tool)
                elif callable(tool):
                    # Convert Python function to tool definition
                    import inspect
                    sig = inspect.signature(tool)
                    doc = inspect.getdoc(tool) or "No description"
                    
                    properties = {}
                    required = []
                    for param_name, param in sig.parameters.items():
                        param_type = "string"  # Default type
                        if param.annotation != inspect.Parameter.empty:
                            if param.annotation == int:
                                param_type = "integer"
                            elif param.annotation == float:
                                param_type = "number"
                            elif param.annotation == bool:
                                param_type = "boolean"
                        
                        properties[param_name] = {"type": param_type}
                        if param.default == inspect.Parameter.empty:
                            required.append(param_name)
                    
                    tool_def = {
                        "type": "function",
                        "name": tool.__name__,
                        "description": doc,
                        "parameters": {
                            "type": "object",
                            "properties": properties,
                            "required": required
                        }
                    }
                    tools_list.append(tool_def)
            
            if tools_list:
                response_params["tools"] = tools_list
        
        # Make the API call using Responses API with streaming
        stream = client.responses.create(stream=True, timeout=3600, **response_params)
        
        chainOfThought = ""
        output_text = ""
        current_reasoning_line = ""
        
        # Process streaming events
        for event in stream:
            event_type = event.type
            
            # Handle reasoning summary deltas - print line by line as they arrive
            if event_type == "response.reasoning_summary_text.delta":
                delta = event.delta
                current_reasoning_line += delta
                # Print complete lines as they arrive
                while "\n" in current_reasoning_line:
                    line, current_reasoning_line = current_reasoning_line.split("\n", 1)
                    print(f"Thinking: {line}", flush=True)
                    chainOfThought += line + "\n"
            
            # Handle reasoning summary done - flush any remaining text
            elif event_type == "response.reasoning_summary_text.done":
                if current_reasoning_line:
                    print(f"Thinking: {current_reasoning_line}", flush=True)
                    chainOfThought += current_reasoning_line
                    current_reasoning_line = ""
            
            # Handle output text deltas - accumulate silently
            elif event_type == "response.output_text.delta":
                output_text += event.delta
            
            # Handle completion
            elif event_type == "response.completed":
                # Final response is available if needed
                pass
        
        # Strip trailing newline from chain of thought if present
        chainOfThought = chainOfThought.rstrip("\n")
        
        print(output_text)

        # Extract content
        if structure is not None:
            # Parse JSON response
            if output_text:
                return json.loads(output_text), chainOfThought
            return {}, chainOfThought
        else:
            # Return text response
            return output_text or "", chainOfThought
            
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        # Return appropriate empty response based on structure
        if structure is not None:
            return {}
        else:
            return ""
