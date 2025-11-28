"""
Test all three AI engines to verify they work correctly.

Before running:
1. Install SDKs:
   pip install google-genai anthropic openai

2. Set API keys:
   set GEMINI_API_KEY=your_key
   set ANTHROPIC_API_KEY=your_key
   set OPENAI_API_KEY=your_key
"""

def test_gemini():
    """Test Google Gemini engine."""
    print("="*70)
    print("Testing Google Gemini")
    print("="*70 + "\n")
    
    try:
        from AiEngineGoogleGemini import GeminiAIHook
        
        # Test 1: Simple text
        print("Test 1: Simple text response")
        response = GeminiAIHook("Say 'Hello from Gemini'", None)
        print(f"Response: {response}\n")
        
        # Test 2: Structured JSON
        print("Test 2: Structured JSON response")
        structure = {
            "type": "object",
            "properties": {
                "greeting": {"type": "string"},
                "number": {"type": "integer"}
            }
        }
        response = GeminiAIHook("Create a greeting with number 42", structure)
        print(f"Response: {response}\n")
        
        print("✓ Gemini tests passed\n")
        return True
        
    except Exception as e:
        print(f"✗ Gemini test failed: {e}\n")
        return False

def test_claude():
    """Test Anthropic Claude engine."""
    print("="*70)
    print("Testing Anthropic Claude")
    print("="*70 + "\n")
    
    try:
        from AiEngineAnthropicClaude import ClaudeAIHook
        
        # Test 1: Simple text
        print("Test 1: Simple text response")
        response = ClaudeAIHook("Say 'Hello from Claude'", None)
        print(f"Response: {response}\n")
        
        # Test 2: Structured JSON
        print("Test 2: Structured JSON response")
        structure = {
            "type": "object",
            "properties": {
                "greeting": {"type": "string"},
                "number": {"type": "integer"}
            },
            "required": ["greeting", "number"]
        }
        response = ClaudeAIHook("Create a greeting with number 42", structure)
        print(f"Response: {response}\n")
        
        print("✓ Claude tests passed\n")
        return True
        
    except Exception as e:
        print(f"✗ Claude test failed: {e}\n")
        return False

def test_chatgpt():
    """Test OpenAI ChatGPT engine."""
    print("="*70)
    print("Testing OpenAI ChatGPT")
    print("="*70 + "\n")
    
    try:
        from AiEngineOpenAiChatGPT import ChatGPTAIHook
        
        # Test 1: Simple text
        print("Test 1: Simple text response")
        response = ChatGPTAIHook("Say 'Hello from ChatGPT'", None)
        print(f"Response: {response}\n")
        
        # Test 2: Structured JSON
        print("Test 2: Structured JSON response")
        structure = {
            "type": "object",
            "properties": {
                "greeting": {"type": "string"},
                "number": {"type": "integer"}
            },
            "required": ["greeting", "number"],
            "additionalProperties": False
        }
        response = ChatGPTAIHook("Create a greeting with number 42", structure)
        print(f"Response: {response}\n")
        
        print("✓ ChatGPT tests passed\n")
        return True
        
    except Exception as e:
        print(f"✗ ChatGPT test failed: {e}\n")
        return False

def test_meshbenchmark_structure():
    """Test all engines with MeshBenchmark-like structure."""
    print("="*70)
    print("Testing MeshBenchmark Structure (All Engines)")
    print("="*70 + "\n")
    
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
    
    prompt = "Generate 3 brick placements with centroids [0,0,0], [10,0,0], [20,0,0] and rotation 0"
    
    results = {}
    
    # Test Gemini
    try:
        from AiEngineGoogleGemini import GeminiAIHook
        print("Testing Gemini with brick structure...")
        response = GeminiAIHook(prompt, structure)
        results['gemini'] = len(response.get('bricks', [])) if isinstance(response, dict) else 0
        print(f"Gemini returned {results['gemini']} bricks\n")
    except Exception as e:
        print(f"Gemini failed: {e}\n")
        results['gemini'] = 0
    
    # Test Claude
    try:
        from AiEngineAnthropicClaude import ClaudeAIHook
        print("Testing Claude with brick structure...")
        response = ClaudeAIHook(prompt, structure)
        results['claude'] = len(response.get('bricks', [])) if isinstance(response, dict) else 0
        print(f"Claude returned {results['claude']} bricks\n")
    except Exception as e:
        print(f"Claude failed: {e}\n")
        results['claude'] = 0
    
    # Test ChatGPT
    try:
        from AiEngineOpenAiChatGPT import ChatGPTAIHook
        print("Testing ChatGPT with brick structure...")
        response = ChatGPTAIHook(prompt, structure)
        results['chatgpt'] = len(response.get('bricks', [])) if isinstance(response, dict) else 0
        print(f"ChatGPT returned {results['chatgpt']} bricks\n")
    except Exception as e:
        print(f"ChatGPT failed: {e}\n")
        results['chatgpt'] = 0
    
    print("MeshBenchmark Structure Test Results:")
    for engine, count in results.items():
        status = "✓" if count > 0 else "✗"
        print(f"  {status} {engine.capitalize()}: {count} bricks")
    print()
    
    return all(count > 0 for count in results.values())

if __name__ == "__main__":
    print("\n" + "="*70)
    print("AI Engines Integration Test Suite")
    print("Testing Gemini, Claude, and ChatGPT")
    print("="*70 + "\n")
    
    results = {
        'gemini': False,
        'claude': False,
        'chatgpt': False,
        'meshbenchmark': False
    }
    
    try:
        # Test each engine
        results['gemini'] = test_gemini()
        results['claude'] = test_claude()
        results['chatgpt'] = test_chatgpt()
        
        # Test MeshBenchmark structure
        results['meshbenchmark'] = test_meshbenchmark_structure()
        
        # Summary
        print("="*70)
        print("FINAL RESULTS")
        print("="*70)
        
        for engine, passed in results.items():
            status = "✓ PASSED" if passed else "✗ FAILED"
            print(f"{status}: {engine.capitalize()}")
        
        all_passed = all(results.values())
        
        print("\n" + "="*70)
        if all_passed:
            print("All tests PASSED! ✓")
        else:
            print("Some tests FAILED! ✗")
            print("\nMake sure:")
            print("1. All SDKs are installed (google-genai, anthropic, openai)")
            print("2. API keys are set as environment variables")
            print("3. You have internet connectivity")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
