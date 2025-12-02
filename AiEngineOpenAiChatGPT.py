"""
OpenAI ChatGPT AI Engine for MeshBenchmark

This module provides an interface to the OpenAI API using the latest openai SDK.

Setup:
1. Install the SDK: pip install openai
2. Set your API key as an environment variable:
   - Windows: set OPENAI_API_KEY=your_api_key_here
   - Linux/Mac: export OPENAI_API_KEY=your_api_key_here
   
Get your API key from: https://platform.openai.com/api-keys

The SDK documentation can be found at: https://platform.openai.com/docs
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
    """
    from openai import OpenAI
    
    try:
        # Initialize the client - it will automatically use OPENAI_API_KEY environment variable
        client = OpenAI(timeout=1800)
    
        # Determine model to use
        model_to_use = MODEL
        
        # Override model if REASONING specifies an o1 model
        if isinstance(REASONING, str) and REASONING in ["o1-preview", "o1-mini"]:
            model_to_use = REASONING
        
        # Build message parameters
        message_params = {
            "model": model_to_use,
            "messages": [{"role": "user", "content": prompt}],
            "service_tier": "flex"
        }
        
        # Add reasoning effort for o1 models
        if isinstance(REASONING, int) and REASONING > 0:
            # Map 1-10 scale to low/medium/high
            if REASONING <= 3:
                message_params["reasoning_effort"] = "low"
            elif REASONING <= 7:
                message_params["reasoning_effort"] = "medium"
            else:
                message_params["reasoning_effort"] = "high"
        
        # Handle structured output
        if structure is not None:
            # Use OpenAI's Structured Outputs feature
            message_params["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_response",
                    "strict": True,
                    "schema": structure
                }
            }
        
        # Add tools if specified (not available for o1 models)
        if TOOLS is True:
            # Enable all built-in tools
            # Note: These require appropriate API access and may use Assistants/Responses API
            message_params["tools"] = [
                {"type": "web_search"},
                {"type": "code_interpreter"},
                {"type": "file_search"}
            ]
            message_params["tool_choice"] = "auto"
        elif TOOLS and TOOLS is not False:
            # Convert function list to OpenAI tool format if needed
            tools_list = []
            for tool in (TOOLS if isinstance(TOOLS, list) else [TOOLS]):
                if isinstance(tool, dict):
                    # Already in correct format
                    tools_list.append(tool)
                elif callable(tool):
                    # Convert Python function to tool definition
                    # This requires inspecting the function
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
                        "function": {
                            "name": tool.__name__,
                            "description": doc,
                            "parameters": {
                                "type": "object",
                                "properties": properties,
                                "required": required
                            }
                        }
                    }
                    tools_list.append(tool_def)
            
            if tools_list:
                message_params["tools"] = tools_list
                message_params["tool_choice"] = "auto"
        
        # Make the API call
        response = client.chat.completions.create(timeout=1800, **message_params)
        
        chainOfThought = ""

        # Extract the response
        message = response.choices[0].message
        
        # Handle tool calls if present
        if hasattr(message, 'tool_calls') and message.tool_calls:
            # If tools were called, this would require a follow-up
            # For now, just return the text response
            pass
        
        print(message.content)

        # Extract content
        if structure is not None:
            # Parse JSON response
            content = message.content
            if content:
                return json.loads(content), chainOfThought
            return {}, chainOfThought
        else:
            # Return text response
            return message.content or "", chainOfThought
            
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        # Return appropriate empty response based on structure
        if structure is not None:
            return {}
        else:
            return ""
