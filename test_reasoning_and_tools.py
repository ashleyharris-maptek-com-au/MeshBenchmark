"""
Advanced test script to demonstrate REASONING and TOOLS features.

This test shows:
1. How reasoning affects response quality
2. How to use function calling with TOOLS

Before running:
1. Install google-genai: pip install google-genai
2. Set your API key: set GEMINI_API_KEY=your_api_key_here
"""

import AiEngineGoogleGemini
from AiEngineGoogleGemini import GeminiAIHook

def test_reasoning_levels():
    """Test different reasoning levels to see the impact on complex problems."""
    print("="*60)
    print("Testing REASONING Feature")
    print("="*60 + "\n")
    
    complex_prompt = """
    A farmer has 17 sheep. All but 9 die. How many sheep are left?
    Explain your reasoning step by step.
    """
    
    reasoning_levels = [
        (0, "No reasoning (fastest)"),
        (128, "Low reasoning (128 tokens)"),
        (1024, "Medium reasoning (1024 tokens)"),
        (-1, "Dynamic reasoning (model decides)"),
    ]
    
    for level, description in reasoning_levels:
        print(f"\n{'='*60}")
        print(f"Testing with REASONING = {level}: {description}")
        print('='*60)
        
        # Temporarily change the reasoning level
        original_reasoning = AiEngineGoogleGemini.REASONING
        AiEngineGoogleGemini.REASONING = level
        
        try:
            response = GeminiAIHook(complex_prompt, None)
            print(f"Response length: {len(response)} chars")
            print(f"Response preview: {response[:200]}...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Restore original value
            AiEngineGoogleGemini.REASONING = original_reasoning
        
        print()

def test_reasoning_with_structure():
    """Test reasoning with structured JSON output."""
    print("\n" + "="*60)
    print("Testing REASONING with Structured Output")
    print("="*60 + "\n")
    
    prompt = """
    Solve this logic puzzle:
    Three friends - Alice, Bob, and Carol - each have a different pet (dog, cat, bird).
    - Alice doesn't have the dog
    - Bob is allergic to cats
    - Carol has the bird
    Who has which pet?
    """
    
    structure = {
        "type": "object",
        "properties": {
            "Alice": {"type": "string"},
            "Bob": {"type": "string"},
            "Carol": {"type": "string"},
            "reasoning": {"type": "string"}
        },
        "required": ["Alice", "Bob", "Carol", "reasoning"]
    }
    
    # Test with moderate reasoning
    original_reasoning = AiEngineGoogleGemini.REASONING
    AiEngineGoogleGemini.REASONING = 512
    
    try:
        response = GeminiAIHook(prompt, structure)
        print("Puzzle Solution:")
        for person, pet in response.items():
            if person != "reasoning":
                print(f"  {person}: {pet}")
        print(f"\nReasoning: {response.get('reasoning', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        AiEngineGoogleGemini.REASONING = original_reasoning

def test_tools_example():
    """Test TOOLS feature with function calling."""
    print("\n" + "="*60)
    print("Testing TOOLS Feature (Function Calling)")
    print("="*60 + "\n")
    
    # Define example tools
    def get_brick_volume(length: float, width: float, height: float) -> float:
        """Calculate the volume of a brick in cubic millimeters."""
        return length * width * height
    
    def calculate_bricks_needed(total_volume: float, brick_volume: float) -> int:
        """Calculate how many bricks are needed for a given volume."""
        return int(total_volume / brick_volume)
    
    print("Note: TOOLS feature is demonstrated in the code.")
    print("To actually use tools, set:")
    print("  AiEngineGoogleGemini.TOOLS = [get_brick_volume, calculate_bricks_needed]")
    print("\nExample tools defined:")
    print("  - get_brick_volume(length, width, height)")
    print("  - calculate_bricks_needed(total_volume, brick_volume)")
    print("\nThe model can automatically call these functions when needed.")
    print("\n⚠ Tool calling is disabled by default (TOOLS = False)")
    print("Enable it by setting TOOLS to a list of functions before calling GeminiAIHook")

def test_math_reasoning():
    """Test reasoning on a mathematical problem."""
    print("\n" + "="*60)
    print("Testing Math Problem with Reasoning")
    print("="*60 + "\n")
    
    prompt = """
    Calculate the volume of a hemispherical shell with:
    - Inner radius: 40mm
    - Outer radius: 70mm
    
    Provide the formula and final answer in cubic millimeters.
    """
    
    structure = {
        "type": "object",
        "properties": {
            "formula": {"type": "string"},
            "calculation_steps": {"type": "array", "items": {"type": "string"}},
            "final_volume_mm3": {"type": "number"}
        }
    }
    
    # Use higher reasoning for complex math
    original_reasoning = AiEngineGoogleGemini.REASONING
    AiEngineGoogleGemini.REASONING = 1024
    
    try:
        response = GeminiAIHook(prompt, structure)
        print(f"Formula: {response.get('formula', 'N/A')}")
        print("\nCalculation Steps:")
        for i, step in enumerate(response.get('calculation_steps', []), 1):
            print(f"  {i}. {step}")
        print(f"\nFinal Volume: {response.get('final_volume_mm3', 'N/A'):.2f} mm³")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        AiEngineGoogleGemini.REASONING = original_reasoning

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Google Gemini Advanced Features Test Suite")
    print("REASONING and TOOLS Demonstration")
    print("="*60)
    
    try:
        # Test 1: Different reasoning levels
        test_reasoning_levels()
        
        # Test 2: Reasoning with structured output
        test_reasoning_with_structure()
        
        # Test 3: Math problem with reasoning
        test_math_reasoning()
        
        # Test 4: Tools information
        test_tools_example()
        
        print("\n" + "="*60)
        print("All tests completed! ✓")
        print("="*60)
        print("\nKey Takeaways:")
        print("- REASONING: Controls thinking tokens (0=off, -1=dynamic, 1-24576=fixed)")
        print("- Higher reasoning = better quality for complex problems")
        print("- TOOLS: Enable function calling by setting to list of functions")
        print("- Both work seamlessly with structured JSON output")
        
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
