"""
Anthropic Claude AI Engine for MeshBenchmark

This module provides an interface to the Anthropic Claude API using the latest anthropic SDK.

Setup:
1. Install the SDK: pip install anthropic
2. Set your API key as an environment variable:
   - Windows: set ANTHROPIC_API_KEY=your_api_key_here
   - Linux/Mac: export ANTHROPIC_API_KEY=your_api_key_here
   
Get your API key from: https://console.anthropic.com/

The SDK documentation can be found at: https://github.com/anthropics/anthropic-sdk-python
"""

# Constants that fine tune which model, whether thinking is used, prompt caching, and tools
MODEL = "claude-sonnet-4-20250514"  # Latest Claude Sonnet 4

# REASONING controls extended thinking mode (for supported models):
# - False: No extended thinking (default, faster)
# - integer 1 - 10: Enable extended thinking (deeper reasoning)
REASONING = False

# PROMPT_CACHING enables caching for repeated content:
# - False: No caching (default)
# - True: Enable prompt caching (reduces cost for repeated prompts)
# Cached content persists for 5 minutes, useful for iterative tasks
PROMPT_CACHING = True

# TOOLS enables tool capabilities:
# - False: No tools available
# - True: Enable ALL built-in tools (web_search)
# - List of tool definitions: Enable specific custom tools
# 
# Examples:
#   TOOLS = False                    # No tools
#   TOOLS = True                     # All built-in tools (web search)
#   TOOLS = [tool_definition]        # Custom tool only
#   TOOLS = [tool1, tool2]           # Multiple custom tools
TOOLS = False

import os, json, hashlib

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

def ClaudeAIHook(prompt: str, structure: dict | None) -> dict | str:
    """
    This function is called by the test runner to get the AI's response to a prompt.
    
    Prompt is the question to ask the AI.
    Structure contains the JSON schema for the expected output. If it is None, the output is just a string.
    
    There is no memory between calls to this function, the 'conversation' doesn't persist.
    """
    from anthropic import Anthropic
    
    # Initialize the client - it will automatically use ANTHROPIC_API_KEY environment variable
    client = Anthropic()
    
    # Get the model's max tokens
    if "claude-sonnet-4-5" in MODEL:
        max_tokens = 64000
    else:
        max_tokens = 6400000
    
    try:
        betas = []
        if TOOLS:
            betas.append("code-execution-2025-08-25")
        if structure:
            betas.append("structured-outputs-2025-11-13")


        # Build message parameters
        message_params = {
            "model": MODEL,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }
        
        if len(betas) > 0:
            message_params["betas"] = betas

        # Add tools if specified
        if TOOLS is True:
            # Enable all built-in tools
            message_params["tools"] = [
                {
                    "type": "web_search_20250305",
                    "name": "web_search"
                },
                {
                    "type": "code_execution_20250825",
                    "name": "code_execution"
                }
            ]
        elif TOOLS and TOOLS is not False:
            # Custom tools provided
            message_params["tools"] = TOOLS
        
        # Handle structured output using tools (Claude's approach)
        if structure is not None:
  
            # Recursively remove "PropertyOrdering", as it's required under OpenAI but banned
            # with Anthropic.
            def remove_property_ordering(schema):
                if isinstance(schema, dict):
                    if "propertyOrdering" in schema:
                        del schema["propertyOrdering"]
                    for key, value in schema.items():
                        remove_property_ordering(value)
                elif isinstance(schema, list):
                    for item in schema:
                        remove_property_ordering(item)

            remove_property_ordering(structure)

            message_params["output_format"] = {
                "type": "json_schema",
                "schema": structure
            }

        
        # Add thinking configuration if enabled (for supported models)
        if REASONING:
            # Extended thinking is enabled via model selection or beta headers
            # This is model-dependent and may require specific model versions
            message_params["thinking"] = {
                "type": "enabled",
                "budget_tokens": 32768 * REASONING // 10
            }
        
        # Handle prompt caching if enabled
        if PROMPT_CACHING:
            # Mark content for caching - last content block is typically cached
            # This requires modifying the content structure
            content_block = [{"type": "text", "text": prompt, "cache_control": {"type": "ephemeral"}}]
            message_params["messages"][0]["content"] = content_block
        
        # Make the API call
        responseStream = client.beta.messages.create(**message_params)
        
        chainOfThought = ""
        textOutput = ""
        thinkingBuffer = ""

        for content_block in responseStream:
            if content_block.type == "content_block_delta":
                if hasattr(content_block.delta, "thinking"):
                    chainOfThought += content_block.delta.thinking
                    thinkingBuffer += content_block.delta.thinking
                    # Print complete lines from the buffer
                    while '\n' in thinkingBuffer:
                        line, thinkingBuffer = thinkingBuffer.split('\n', 1)
                        print("Thinking: " + line)
                elif hasattr(content_block.delta, "text"):
                    textOutput += content_block.delta.text

        #print(textOutput)

        if structure is not None:
            return json.loads(textOutput), chainOfThought
        else:
            return textOutput, chainOfThought

    except Exception as e:
        print(f"Error calling Claude API: {e}")
        # Return appropriate empty response based on structure
        if structure is not None:
            return {}, str(e)
        else:
            return "", str(e)

if __name__ == "__main__":
    Configure("claude-sonnet-4-5-20250929", False, False)
    print(ClaudeAIHook("What's the 7th prime number after 101?", None))

    Configure("claude-sonnet-4-5-20250929", True, True)
    print(ClaudeAIHook("What is the closest Australian city to New York?", None))

    print(ClaudeAIHook("What is the furtherest Australian city from New York?", 
    {
        "type": "object",
        "properties": {
            "cityName": {"type": "string"},
            "longitude": {"type": "number"},
            "latitude": {"type": "number"}
        },
        "required": ["cityName", "longitude", "latitude"],
        "additionalProperties": False
    }
    ))