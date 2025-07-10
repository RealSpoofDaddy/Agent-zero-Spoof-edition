"""
Test script for ForgeCore AI plugin
Run this in Blender's Python console to test the plugin
"""

import bpy
import sys
import os

def test_plugin_structure():
    """Test the plugin structure and basic functionality"""
    print("=== ForgeCore AI Plugin Test ===")
    
    # Test 1: Check if addon is registered
    try:
        addon_name = "forgecore_ai"
        if addon_name in bpy.context.preferences.addons:
            print("✓ Addon is registered")
        else:
            print("✗ Addon is not registered")
    except Exception as e:
        print(f"✗ Error checking addon registration: {e}")
    
    # Test 2: Check if properties are available
    try:
        scene = bpy.context.scene
        if hasattr(scene, 'forgecore_prompt'):
            print("✓ Scene properties are available")
        else:
            print("✗ Scene properties are missing")
    except Exception as e:
        print(f"✗ Error checking properties: {e}")
    
    # Test 3: Test agent core functionality
    try:
        # Import the agent core
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        
        from agent_core.main import handle_prompt
        
        # Test a simple prompt
        test_prompt = "Create a red cube"
        result = handle_prompt(test_prompt)
        
        if result and not result.startswith("# Error"):
            print("✓ Agent core is working")
            print(f"Generated code: {result[:100]}...")
        else:
            print("✗ Agent core failed")
            print(f"Error: {result}")
            
    except Exception as e:
        print(f"✗ Error testing agent core: {e}")
    
    # Test 4: Check memory system
    try:
        memory_dir = os.path.join(current_dir, "agent_core", "memory")
        memory_file = os.path.join(memory_dir, "memory_store.json")
        
        if os.path.exists(memory_file):
            print("✓ Memory system is accessible")
        else:
            print("✗ Memory system is not accessible")
    except Exception as e:
        print(f"✗ Error checking memory system: {e}")
    
    print("=== Test Complete ===")

def test_prompt_execution():
    """Test prompt execution functionality"""
    print("\n=== Testing Prompt Execution ===")
    
    test_prompts = [
        "Create a blue sphere",
        "Make a metallic material",
        "Set up studio lighting",
        "Add a camera"
    ]
    
    for prompt in test_prompts:
        try:
            print(f"\nTesting prompt: '{prompt}'")
            
            # Set the prompt in the scene
            bpy.context.scene.forgecore_prompt = prompt
            
            # Execute the prompt (this would normally be done via UI)
            from agent_core.main import handle_prompt
            result = handle_prompt(prompt)
            
            if result and not result.startswith("# Error"):
                print(f"✓ Success: Generated {len(result.split())} lines of code")
            else:
                print(f"✗ Failed: {result}")
                
        except Exception as e:
            print(f"✗ Error: {e}")

def test_journal_functionality():
    """Test journal functionality"""
    print("\n=== Testing Journal Functionality ===")
    
    try:
        # Test saving a journal entry
        from ui_panel import save_journal_entry
        
        success = save_journal_entry(
            goal="Test the ForgeCore AI plugin",
            progress="Successfully created test objects"
        )
        
        if success:
            print("✓ Journal entry saved successfully")
        else:
            print("✗ Failed to save journal entry")
            
    except Exception as e:
        print(f"✗ Error testing journal: {e}")

if __name__ == "__main__":
    # Run all tests
    test_plugin_structure()
    test_prompt_execution()
    test_journal_functionality()
    
    print("\n=== All Tests Complete ===")
    print("Check the console output above for results.")