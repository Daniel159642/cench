#!/usr/bin/env python3
"""
Real-time After Effects testing
This script will execute actual commands in After Effects
"""

import sys
import os
import time

# Add the project path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src', 'python-scripts'))

try:
    from aftereffects_execute import (
        check_after_effects_connection,
        execute_after_effects_script
    )
    
    print("🎬 REAL-TIME AFTER EFFECTS TESTING")
    print("="*50)
    
    # Check connection first
    print("🔗 Checking After Effects connection...")
    result = check_after_effects_connection()
    
    if not result['success']:
        print("❌ After Effects not connected!")
        print("Make sure After Effects is running with a project open")
        sys.exit(1)
    
    print("✅ After Effects connected!")
    print(f"   Version: {result['version']}")
    
    print("\n" + "="*50)
    print("📋 PREREQUISITES CHECK")
    print("="*50)
    print("Before running these tests, make sure:")
    print("1. ✅ After Effects is running")
    print("2. ✅ You have a project open")
    print("3. ✅ You have a composition open")
    print("4. ✅ The composition is visible on screen")
    
    input("\nPress Enter when you're ready to test real-time commands...")
    
    print("\n" + "="*50)
    print("🚀 TEST 1: Create a Text Layer")
    print("="*50)
    
    text_command = '''
// Create a text layer
var comp = app.project.activeItem;
if (comp && comp instanceof CompItem) {
    var textLayer = comp.layers.addText("Hello from Cench AI!");
    textLayer.position.setValue([comp.width/2, comp.height/2]);
    $.writeln("Text layer created successfully!");
} else {
    $.writeln("Please open a composition first!");
}
'''
    
    print("Executing: Create text layer with 'Hello from Cench AI!'")
    result = execute_after_effects_script(text_command, result['path'])
    
    if result['success']:
        print("✅ Text layer created! You should see it in After Effects now!")
        print("   Output:", result.get('output', 'No output'))
    else:
        print("❌ Failed to create text layer:")
        print("   Error:", result.get('error', 'Unknown error'))
    
    time.sleep(2)
    
    print("\n" + "="*50)
    print("🎨 TEST 2: Change Text Color")
    print("="*50)
    
    color_command = '''
// Change text color to red
var comp = app.project.activeItem;
if (comp && comp instanceof CompItem) {
    var textLayer = comp.layer(1); // Get the first layer (our text layer)
    if (textLayer && textLayer.property("Source Text")) {
        var textDocument = textLayer.property("Source Text").value;
        textDocument.fillColor = [1, 0, 0]; // Red color
        textLayer.property("Source Text").setValue(textDocument);
        $.writeln("Text color changed to red!");
    } else {
        $.writeln("Text layer not found!");
    }
} else {
    $.writeln("Please open a composition first!");
}
'''
    
    print("Executing: Change text color to red")
    result = execute_after_effects_script(color_command, result['path'])
    
    if result['success']:
        print("✅ Text color changed! You should see red text now!")
        print("   Output:", result.get('output', 'No output'))
    else:
        print("❌ Failed to change text color:")
        print("   Error:", result.get('error', 'Unknown error'))
    
    time.sleep(2)
    
    print("\n" + "="*50)
    print("✨ TEST 3: Add Animation (Position Wiggle)")
    print("="*50)
    
    animation_command = '''
// Add wiggle animation to text position
var comp = app.project.activeItem;
if (comp && comp instanceof CompItem) {
    var textLayer = comp.layer(1); // Get the first layer
    if (textLayer) {
        var positionProp = textLayer.property("Position");
        positionProp.expression = "wiggle(2, 50);"; // Wiggle every 2 seconds, 50 pixels
        $.writeln("Wiggle animation added to text!");
    } else {
        $.writeln("Text layer not found!");
    }
} else {
    $.writeln("Please open a composition first!");
}
'''
    
    print("Executing: Add wiggle animation to text")
    result = execute_after_effects_script(animation_command, result['path'])
    
    if result['success']:
        print("✅ Animation added! Your text should now be wiggling!")
        print("   Output:", result.get('output', 'No output'))
    else:
        print("❌ Failed to add animation:")
        print("   Error:", result.get('error', 'Unknown error'))
    
    print("\n" + "="*50)
    print("🎯 REAL-TIME WORKFLOW SUMMARY")
    print("="*50)
    print("✅ You should now see in After Effects:")
    print("   1. A text layer saying 'Hello from Cench AI!'")
    print("   2. The text should be RED in color")
    print("   3. The text should be WIGGLING around")
    
    print("\n" + "="*50)
    print("🔄 HOW TO USE WITH CENCH AI")
    print("="*50)
    print("1. Keep After Effects open with your project")
    print("2. Use Cench AI to send commands like:")
    print("   - 'Make the text bigger'")
    print("   - 'Change text to blue'")
    print("   - 'Add a drop shadow'")
    print("   - 'Create a new solid layer'")
    print("3. See changes happen in real-time!")
    
    print("\n" + "="*50)
    print("💡 TIPS FOR REAL-TIME WORKFLOW")
    print("="*50)
    print("• Keep After Effects visible while using Cench AI")
    print("• Use specific, clear commands")
    print("• Check the After Effects console for feedback")
    print("• Save your project frequently")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 