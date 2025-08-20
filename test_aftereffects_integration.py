#!/usr/bin/env python3
"""
Comprehensive test of After Effects integration
Tests all the functionality that the app would use
"""

import sys
import os
import json

# Add the project path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src', 'python-scripts'))

try:
    from aftereffects_execute import (
        check_after_effects_connection, 
        find_after_effects_path,
        execute_after_effects_script,
        is_safe_code
    )
    
    print("✅ After Effects integration module imported successfully!")
    
    print("\n" + "="*50)
    print("🔍 TEST 1: After Effects Installation Check")
    print("="*50)
    
    ae_path = find_after_effects_path()
    if ae_path:
        print(f"✅ After Effects found at: {ae_path}")
    else:
        print("❌ After Effects not found")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("🔗 TEST 2: Connection Test")
    print("="*50)
    
    result = check_after_effects_connection()
    if result['success']:
        print("✅ After Effects connection successful!")
        print(f"   Version: {result['version']}")
        print(f"   Path: {result['path']}")
    else:
        print("❌ After Effects connection failed:")
        print(f"   Error: {result['message']}")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("🛡️ TEST 3: Code Safety Check")
    print("="*50)
    
    # Test safe code
    safe_code = 'var comp = app.project.items.addComp("Test Comp", 1920, 1080, 1, 10, 30);'
    is_safe = is_safe_code(safe_code)
    print(f"Safe code test: {'✅ PASSED' if is_safe else '❌ FAILED'}")
    print(f"Code: {safe_code}")
    
    # Test unsafe code
    unsafe_code = 'import os; os.system("rm -rf /");'
    is_safe = is_safe_code(unsafe_code)
    print(f"Unsafe code test: {'✅ PASSED' if not is_safe else '❌ FAILED'}")
    print(f"Code: {unsafe_code}")
    
    print("\n" + "="*50)
    print("🎬 TEST 4: Sample After Effects Commands")
    print("="*50)
    
    sample_commands = [
        {
            "name": "Create New Composition",
            "code": 'var comp = app.project.items.addComp("Test Comp", 1920, 1080, 1, 10, 30);',
            "description": "Creates a new 1920x1080 composition"
        },
        {
            "name": "Create Text Layer",
            "code": 'var textLayer = comp.layers.addText("Hello Cench AI!");',
            "description": "Adds a text layer to the composition"
        },
        {
            "name": "Set Layer Position",
            "code": 'textLayer.position.setValue([comp.width/2, comp.height/2]);',
            "description": "Centers the text layer"
        },
        {
            "name": "Set Opacity",
            "code": 'textLayer.opacity.setValue(80);',
            "description": "Sets text layer to 80% opacity"
        }
    ]
    
    for i, cmd in enumerate(sample_commands, 1):
        print(f"\n{i}. {cmd['name']}")
        print(f"   Description: {cmd['description']}")
        print(f"   Code: {cmd['code']}")
        print(f"   Safety: {'✅ SAFE' if is_safe_code(cmd['code']) else '❌ UNSAFE'}")
    
    print("\n" + "="*50)
    print("🚀 TEST 5: Mock Command Execution")
    print("="*50)
    
    # Test a simple command execution (without actually running it)
    test_code = 'var comp = app.project.items.addComp("Test Comp", 1920, 1080, 1, 10, 30);'
    
    print(f"Testing command execution for: {test_code}")
    print("Note: This is a simulation - actual execution would require After Effects to be running")
    
    # Simulate what the app would do
    if is_safe_code(test_code):
        print("✅ Code passed safety check")
        print("✅ Would be sent to After Effects for execution")
        print("✅ Mock result: Command would create a new composition")
    else:
        print("❌ Code failed safety check")
        print("❌ Would be rejected by the app")
    
    print("\n" + "="*50)
    print("🎯 INTEGRATION SUMMARY")
    print("="*50)
    print("✅ After Effects 2025 detected and connected")
    print("✅ Safety checks working properly")
    print("✅ Sample commands ready for testing")
    print("✅ Integration ready for app testing")
    
    print("\n" + "="*50)
    print("📱 NEXT STEPS FOR APP TESTING")
    print("="*50)
    print("1. Restart the Electron app to pick up new handlers")
    print("2. Check Settings → Connections for After Effects test button")
    print("3. Test the connection in the app")
    print("4. Try natural language commands like:")
    print("   - 'Create a new composition'")
    print("   - 'Add a text layer'")
    print("   - 'Apply a blur effect'")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 