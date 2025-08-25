#!/usr/bin/env python3
"""
Simple Hello Test for After Effects
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
    
    print("🎬 SIMPLE HELLO TEST FOR AFTER EFFECTS")
    print("="*50)
    
    # Check connection
    print("\n🔗 Checking After Effects connection...")
    result = check_after_effects_connection()
    
    if not result['success']:
        print("❌ After Effects not connected!")
        sys.exit(1)
    
    print("✅ After Effects connected!")
    
    # Create a very simple script
    print("\n📝 Creating simple 'Hello' text script...")
    simple_command = '''
// SIMPLE HELLO TEST
// This will create basic text in After Effects

try {
    // Check if we have an active composition
    var comp = app.project.activeItem;
    
    if (!comp || !(comp instanceof CompItem)) {
        // Create a new composition if none exists
        comp = app.project.items.addComp("Hello Test", 1920, 1080, 1, 5, 30);
        alert("Created new composition: Hello Test");
    }
    
    // Create text layer
    var textLayer = comp.layers.addText("Hello!");
    
    // Position text in center
    textLayer.position.setValue([comp.width/2, comp.height/2]);
    
    // Make text visible and large
    var textDocument = textLayer.property("Source Text").value;
    textDocument.fontSize = 120;
    textDocument.fillColor = [1, 1, 1]; // White text
    textDocument.font = "Arial-BoldMT";
    textLayer.property("Source Text").setValue(textDocument);
    
    // Success message
    alert("✅ SUCCESS! Hello text created!");
    $.writeln("Hello text created successfully in After Effects");
    
} catch (error) {
    alert("❌ Error: " + error.toString());
    $.writeln("Error: " + error.toString());
}
'''
    
    # Execute the script
    print("Executing simple hello script...")
    result = execute_after_effects_script(simple_command, result['path'])
    
    if result['success']:
        print("✅ SIMPLE HELLO SCRIPT EXECUTED!")
        print("   Script saved to:", result.get('script_path', 'Unknown'))
        print("\n🎯 WHAT TO DO NEXT:")
        print("   1. Look at your After Effects window")
        print("   2. You should see a success alert")
        print("   3. Check your composition for 'Hello!' text")
        print("   4. The text should be white and centered")
    else:
        print("❌ Script execution failed:", result.get('message', 'Unknown error'))
        
except ImportError as e:
    print("❌ Import error:", e)
    print("Make sure you're in the correct directory")
except Exception as e:
    print("❌ Unexpected error:", e)
