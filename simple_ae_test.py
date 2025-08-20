#!/usr/bin/env python3
"""
Very simple After Effects test
"""

import sys
import os

# Add the project path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src', 'python-scripts'))

try:
    from aftereffects_execute import (
        check_after_effects_connection,
        execute_after_effects_script
    )
    
    print("🎬 SIMPLE AFTER EFFECTS TEST")
    print("="*50)
    
    # Check connection
    print("🔗 Checking After Effects connection...")
    result = check_after_effects_connection()
    
    if not result['success']:
        print("❌ After Effects not connected!")
        sys.exit(1)
    
    print("✅ After Effects connected!")
    print(f"   Version: {result['version']}")
    print(f"   Path: {result['path']}")
    
    # Try a very simple command
    print("\n🚀 Testing simple command execution...")
    simple_command = '''
// Very simple test
$.writeln("Hello from Cench AI!");
alert("Cench AI is working!");
'''
    
    print("Executing simple command...")
    result = execute_after_effects_script(simple_command, result['path'])
    
    print(f"Result: {result}")
    
    if result['success']:
        print("✅ SUCCESS! After Effects automation is working!")
        print("   You should see an alert in After Effects!")
    else:
        print("❌ Failed:")
        print(f"   Message: {result['message']}")
        print(f"   Error: {result.get('error', 'No error details')}")
        
        print("\n💡 Troubleshooting:")
        print("1. Make sure After Effects is running")
        print("2. Make sure no dialogs are open")
        print("3. Try creating a new project and composition")
        print("4. Check if scripting is enabled in preferences")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 