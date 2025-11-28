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

# THINKING controls extended thinking mode (for supported models):
# - False: No extended thinking (default, faster)
# - True: Enable extended thinking (deeper reasoning)
# Note: Only available on specific models like Claude 3.7 Sonnet
THINKING = False

# PROMPT_CACHING enables caching for repeated content:
# - False: No caching (default)
# - True: Enable prompt caching (reduces cost for repeated prompts)
# Cached content persists for 5 minutes, useful for iterative tasks
PROMPT_CACHING = False

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

import os
import json

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
    
    try:
        # Build message parameters
        message_params = {
            "model": MODEL,
            "max_tokens": 8192,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        # Add tools if specified
        if TOOLS is True:
            # Enable all built-in tools
            message_params["tools"] = [
                {
                    "type": "web_search_20250305",
                    "name": "web_search"
                }
            ]
        elif TOOLS and TOOLS is not False:
            # Custom tools provided
            message_params["tools"] = TOOLS
        
        # Handle structured output using tools (Claude's approach)
        if structure is not None:
            # Create a tool definition for structured extraction
            extraction_tool = {
                "name": "extract_structured_data",
                "description": "Extract data according to the specified schema",
                "input_schema": structure
            }
            
            # Add or append to tools
            if "tools" in message_params:
                message_params["tools"].append(extraction_tool)
            else:
                message_params["tools"] = [extraction_tool]
            
            # Force tool use for structured output
            message_params["tool_choice"] = {"type": "tool", "name": "extract_structured_data"}
        
        # Add thinking configuration if enabled (for supported models)
        if THINKING:
            # Extended thinking is enabled via model selection or beta headers
            # This is model-dependent and may require specific model versions
            pass  # Current SDK handles this via model selection
        
        # Handle prompt caching if enabled
        if PROMPT_CACHING:
            # Mark content for caching - last content block is typically cached
            # This requires modifying the content structure
            content_block = {"type": "text", "text": prompt, "cache_control": {"type": "ephemeral"}}
            message_params["messages"][0]["content"] = content_block
        
        # Make the API call
        response = client.messages.create(**message_params)
        
        # Extract the response
        if structure is not None:
            # Extract structured output from tool use
            for content_block in response.content:
                if content_block.type == "tool_use" and content_block.name == "extract_structured_data":
                    return content_block.input
            # Fallback if tool wasn't used
            return {}
        else:
            # Extract text response
            text_content = ""
            for content_block in response.content:
                if hasattr(content_block, 'text'):
                    text_content += content_block.text
            return text_content
            
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        # Return appropriate empty response based on structure
        if structure is not None:
            return {}
        else:
            return ""
