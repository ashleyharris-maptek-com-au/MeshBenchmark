"""
Simple test script to verify the Google Gemini AI Engine works correctly.

Before running:
1. Install google-genai: pip install google-genai
2. Set your API key: set GEMINI_API_KEY=your_api_key_here
"""

from AiEngineGoogleGemini import GeminiAIHook

def test_text_response():
    """Test simple text response without structure."""
    print("Testing text response...")
    prompt = "Say 'Hello from Gemini!' in a friendly way."
    response = GeminiAIHook(prompt, None)
    print(f"Response type: {type(response)}")
    print(f"Response: {response}")
    assert isinstance(response, str), "Expected string response"
    print("✓ Text response test passed\n")

def test_json_response():
    """Test structured JSON response."""
    print("Testing JSON response with structure...")
    prompt = "Create a simple user profile with name 'Alice' and age 30."
    structure = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        },
        "required": ["name", "age"]
    }
    response = GeminiAIHook(prompt, structure)
    print(f"Response type: {type(response)}")
    print(f"Response: {response}")
    assert isinstance(response, dict), "Expected dict response"
    assert "name" in response, "Expected 'name' field in response"
    assert "age" in response, "Expected 'age' field in response"
    print("✓ JSON response test passed\n")

def test_complex_structure():
    """Test with a more complex structure similar to the benchmark."""
    print("Testing complex structure (like brick placement)...")
    prompt = "Generate 3 brick placements with centroids and rotation degrees."
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
            }
        }
    }
    response = GeminiAIHook(prompt, structure)
    print(f"Response type: {type(response)}")
    print(f"Number of bricks: {len(response.get('bricks', []))}")
    print(f"First brick: {response.get('bricks', [{}])[0] if response.get('bricks') else 'None'}")
    assert isinstance(response, dict), "Expected dict response"
    assert "bricks" in response, "Expected 'bricks' field in response"
    assert isinstance(response["bricks"], list), "Expected bricks to be a list"
    print("✓ Complex structure test passed\n")

if __name__ == "__main__":
    try:
        print("="*60)
        print("Google Gemini AI Engine Test Suite")
        print("="*60 + "\n")
        
        test_text_response()
        test_json_response()
        test_complex_structure()
        
        print("="*60)
        print("All tests passed! ✓")
        print("="*60)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
