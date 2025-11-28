"""
Test that built-in tools work through the AiEngineGoogleGemini module.

This validates that the TOOLS constant properly handles:
- "google_search" string
- "code_execution" string  
- List of built-in tools
- Mix of built-in and custom functions

Before running:
1. Install google-genai: pip install google-genai
2. Set your API key: set GEMINI_API_KEY=your_api_key_here
"""

import AiEngineGoogleGemini
from AiEngineGoogleGemini import GeminiAIHook

def test_code_execution_tool():
    """Test code execution through the module."""
    print("="*70)
    print("Test 1: Code Execution Tool")
    print("="*70 + "\n")
    
    # Configure to use code execution
    original_tools = AiEngineGoogleGemini.TOOLS
    AiEngineGoogleGemini.TOOLS = "code_execution"
    
    try:
        prompt = """
        Calculate the volume of a hemisphere with radius 50mm.
        Use Python code to compute this precisely.
        Formula: V = (2/3) * π * r³
        """
        
        print(f"Prompt: {prompt}\n")
        print("Calling GeminiAIHook with code_execution enabled...\n")
        
        response = GeminiAIHook(prompt, None)
        
        print("Response:")
        print(response[:500] + "..." if len(response) > 500 else response)
        print("\n✓ Code execution test passed\n")
        
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
    finally:
        AiEngineGoogleGemini.TOOLS = original_tools

def test_google_search_tool():
    """Test Google Search through the module."""
    print("="*70)
    print("Test 2: Google Search Tool")
    print("="*70 + "\n")
    
    # Configure to use Google Search
    original_tools = AiEngineGoogleGemini.TOOLS
    AiEngineGoogleGemini.TOOLS = "google_search"
    
    try:
        prompt = "What is the latest version of Python released in 2024?"
        
        print(f"Prompt: {prompt}\n")
        print("Calling GeminiAIHook with google_search enabled...\n")
        
        response = GeminiAIHook(prompt, None)
        
        print("Response:")
        print(response[:500] + "..." if len(response) > 500 else response)
        print("\n✓ Google Search test passed\n")
        
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
    finally:
        AiEngineGoogleGemini.TOOLS = original_tools

def test_both_tools():
    """Test using both built-in tools together."""
    print("="*70)
    print("Test 3: Both Built-in Tools Combined")
    print("="*70 + "\n")
    
    # Configure to use both tools
    original_tools = AiEngineGoogleGemini.TOOLS
    AiEngineGoogleGemini.TOOLS = ["google_search", "code_execution"]
    
    try:
        prompt = """
        Find the radius of Earth in kilometers, then calculate its volume.
        Show the calculation.
        """
        
        print(f"Prompt: {prompt}\n")
        print("Calling GeminiAIHook with both tools enabled...\n")
        
        response = GeminiAIHook(prompt, None)
        
        print("Response:")
        print(response[:500] + "..." if len(response) > 500 else response)
        print("\n✓ Combined tools test passed\n")
        
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
    finally:
        AiEngineGoogleGemini.TOOLS = original_tools

def test_code_execution_with_structure():
    """Test code execution with structured JSON output."""
    print("="*70)
    print("Test 4: Code Execution + Structured Output")
    print("="*70 + "\n")
    
    # Configure to use code execution
    original_tools = AiEngineGoogleGemini.TOOLS
    AiEngineGoogleGemini.TOOLS = "code_execution"
    
    try:
        prompt = """
        Calculate volumes for hemispheres with radii: 10mm, 20mm, 30mm.
        Use code to compute all three.
        """
        
        structure = {
            "type": "object",
            "properties": {
                "volumes": {
                    "type": "array",
                    "items": {"type": "number"}
                },
                "formula_used": {"type": "string"}
            },
            "required": ["volumes", "formula_used"]
        }
        
        print(f"Prompt: {prompt}\n")
        print("Calling GeminiAIHook with structure and code_execution...\n")
        
        response = GeminiAIHook(prompt, structure)
        
        print("Structured Response:")
        import json
        print(json.dumps(response, indent=2))
        print("\n✓ Structured output test passed\n")
        
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
    finally:
        AiEngineGoogleGemini.TOOLS = original_tools

def test_meshbenchmark_use_case():
    """Test a realistic MeshBenchmark use case."""
    print("="*70)
    print("Test 5: MeshBenchmark Use Case (Geometry Calculation)")
    print("="*70 + "\n")
    
    # Configure for geometry tasks
    original_tools = AiEngineGoogleGemini.TOOLS
    original_reasoning = AiEngineGoogleGemini.REASONING
    
    AiEngineGoogleGemini.REASONING = 512
    AiEngineGoogleGemini.TOOLS = "code_execution"
    
    try:
        prompt = """
        Calculate the volume of a hemispherical shell:
        - Inner radius: 40mm
        - Outer radius: 70mm
        
        Then determine approximately how many 32x16x9.6mm bricks
        would be needed to fill this volume.
        """
        
        structure = {
            "type": "object",
            "properties": {
                "shell_volume_mm3": {"type": "number"},
                "brick_volume_mm3": {"type": "number"},
                "estimated_bricks": {"type": "integer"}
            }
        }
        
        print(f"Prompt: {prompt}\n")
        print("Calling with REASONING=512 and code_execution...\n")
        
        response = GeminiAIHook(prompt, structure)
        
        print("MeshBenchmark Response:")
        import json
        print(json.dumps(response, indent=2))
        print("\n✓ MeshBenchmark use case test passed\n")
        
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
    finally:
        AiEngineGoogleGemini.TOOLS = original_tools
        AiEngineGoogleGemini.REASONING = original_reasoning

def test_custom_function_with_code_execution():
    """Test mixing custom function with code execution."""
    print("="*70)
    print("Test 6: Custom Function + Code Execution")
    print("="*70 + "\n")
    
    # Define a custom function
    def brick_volume(length: float, width: float, height: float) -> float:
        """Calculate brick volume in cubic millimeters."""
        return length * width * height
    
    # Configure with both
    original_tools = AiEngineGoogleGemini.TOOLS
    AiEngineGoogleGemini.TOOLS = ["code_execution", brick_volume]
    
    try:
        prompt = """
        Calculate the volume of a hemisphere with radius 50mm,
        then use the brick_volume function to check a 32x16x9.6mm brick volume.
        """
        
        print(f"Prompt: {prompt}\n")
        print("Calling with code_execution + custom function...\n")
        
        response = GeminiAIHook(prompt, None)
        
        print("Response:")
        print(response[:500] + "..." if len(response) > 500 else response)
        print("\n✓ Mixed tools test passed\n")
        
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
    finally:
        AiEngineGoogleGemini.TOOLS = original_tools

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Built-in Tools Integration Test Suite")
    print("Testing TOOLS configuration in AiEngineGoogleGemini.py")
    print("="*70 + "\n")
    
    try:
        # Test 1: Code Execution
        test_code_execution_tool()
        
        # Test 2: Google Search
        test_google_search_tool()
        
        # Test 3: Both Tools
        test_both_tools()
        
        # Test 4: Structured Output
        test_code_execution_with_structure()
        
        # Test 5: MeshBenchmark Use Case
        test_meshbenchmark_use_case()
        
        # Test 6: Custom + Built-in
        test_custom_function_with_code_execution()
        
        print("="*70)
        print("All integration tests completed! ✓")
        print("="*70)
        print("\nConfiguration Examples:")
        print('  TOOLS = "code_execution"           # Single built-in tool')
        print('  TOOLS = "google_search"            # Search grounding')
        print('  TOOLS = ["google_search", "code_execution"]  # Both')
        print('  TOOLS = [my_function]              # Custom function')
        print('  TOOLS = ["code_execution", my_fn]  # Mixed')
        
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
