"""
xAI Grok AI Engine for MeshBenchmark

This module provides an interface to the xAI Grok API using the official xai-sdk.

Setup:
1. Install the SDK: pip install xai-sdk
2. Set your API key as an environment variable:
   - Windows: set XAI_API_KEY=your_api_key_here
   - Linux/Mac: export XAI_API_KEY=your_api_key_here
   
Get your API key from: https://console.x.ai/

The SDK documentation can be found at: https://docs.x.ai/
"""

import hashlib

# Constants that fine tune which model, whether reasoning is used and how much, and whether tools
# are made available.
MODEL = "grok-3-mini"

# REASONING controls reasoning effort on a 0-10 scale:
# - 0 or False: No reasoning (fastest)
# - 1-3: Low reasoning effort
# - 4-7: Medium reasoning effort
# - 8-10: High reasoning effort
REASONING = False

# TOOLS enables tool capabilities:
# - False: No tools available
# - True: Enable built-in tools (web_search, x_search, code_execution)
# - List of function definitions: Enable specific custom tools
# 
# Examples:
#   TOOLS = False                    # No tools
#   TOOLS = True                     # All built-in tools
#   TOOLS = ["web_search"]           # Just web search
#   TOOLS = [function_def]           # Custom function only
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

def GrokAIHook(prompt: str, structure: dict | None) -> tuple:
    """
    This function is called by the test runner to get the AI's response to a prompt.
    
    Prompt is the question to ask the AI.
    Structure contains the JSON schema for the expected output. If it is None, the output is just a string.
    
    There is no memory between calls to this function, the 'conversation' doesn't persist.
    
    Returns tuple of (result, chainOfThought).
    """
    from xai_sdk import Client
    from xai_sdk.chat import user
    
    try:
        # Initialize the client - uses XAI_API_KEY environment variable
        client = Client(timeout=3600)
        
        # Build chat creation parameters
        chat_params = {
            "model": MODEL
        }
        
        # Add reasoning effort if specified
        # Map 0-10 scale to low/medium/high
        if REASONING and REASONING != 0:
            if isinstance(REASONING, int):
                if REASONING <= 3:
                    chat_params["reasoning_effort"] = "low"
                elif REASONING <= 7:
                    chat_params["reasoning_effort"] = "medium"
                else:
                    chat_params["reasoning_effort"] = "high"
            else:
                chat_params["reasoning_effort"] = "medium"
        
        # Add structured output if schema provided
        if structure is not None:
            chat_params["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_response",
                    "strict": True,
                    "schema": structure
                }
            }
        
        # Add tools if specified
        if TOOLS is True:
            chat_params["tools"] = [
                {"type": "web_search"},
                {"type": "x_search"},
                {"type": "code_execution"}
            ]
        elif TOOLS and TOOLS is not False:
            if isinstance(TOOLS, list):
                chat_params["tools"] = TOOLS
        
        # Create chat and add user message
        chat = client.chat.create(**chat_params)
        chat.append(user(prompt))
        
        # Stream to capture reasoning/thinking content in real-time
        chainOfThought = ""
        output_text = ""
        current_thinking_line = ""
        
        for response, chunk in chat.stream():
            # Check if this chunk contains reasoning/thinking content
            if hasattr(chunk, 'reasoning_content') and chunk.reasoning_content:
                current_thinking_line += chunk.reasoning_content
                # Print complete lines as they arrive
                while "\n" in current_thinking_line:
                    line, current_thinking_line = current_thinking_line.split("\n", 1)
                    print(f"Thinking: {line}", flush=True)
                    chainOfThought += line + "\n"
            
            # Regular content
            if hasattr(chunk, 'content') and chunk.content:
                output_text += chunk.content
        
        # Flush any remaining thinking content
        if current_thinking_line:
            print(f"Thinking: {current_thinking_line}", flush=True)
            chainOfThought += current_thinking_line
        
        # Strip trailing newline from chain of thought
        chainOfThought = chainOfThought.rstrip("\n")
        
        # Also check final response for reasoning content if not captured during streaming
        if not chainOfThought and hasattr(response, 'reasoning_content') and response.reasoning_content:
            chainOfThought = response.reasoning_content
            for line in chainOfThought.split("\n"):
                print(f"Thinking: {line}", flush=True)
        
        # Get final content from response if streaming didn't capture it
        if not output_text and hasattr(response, 'content'):
            output_text = response.content or ""
        
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
        print(f"Error calling xAI Grok API: {e}")
        # Return appropriate empty response based on structure
        if structure is not None:
            return {}, ""
        else:
            return "", ""
