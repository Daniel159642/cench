#!/usr/bin/env python3
"""
Test After Effects automation - this is what Cench AI will do!
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
    
    print("🎬 TESTING AFTER EFFECTS AUTOMATION")
    print("="*50)
    print("This simulates what Cench AI will do automatically!")
    
    # Check connection first
    print("\n🔗 Checking After Effects connection...")
    result = check_after_effects_connection()
    
    if not result['success']:
        print("❌ After Effects not connected!")
        print("Make sure After Effects is running with a project open")
        sys.exit(1)
    
    print("✅ After Effects connected!")
    print(f"   Version: {result['version']}")
    
    print("\n" + "="*50)
    print("📋 AUTOMATION TEST")
    print("="*50)
    print("This will automatically execute commands in After Effects!")
    print("Make sure you have a composition open in After Effects.")
    
    input("\nPress Enter to start automation test...")
    
    # Test 1: Create text layer
    print("\n🚀 AUTOMATION 1: Creating text layer...")
    text_command = '''
// Create a text layer automatically
var comp = app.project.activeItem;
if (comp && comp instanceof CompItem) {
    var textLayer = comp.layers.addText("Cench AI Automated!");
    textLayer.position.setValue([comp.width/2, comp.height/2]);
    
    // Style the text
    var textDocument = textLayer.property("Source Text").value;
    textDocument.fontSize = 60;
    textDocument.fillColor = [0, 1, 0]; // Green color
    textLayer.property("Source Text").setValue(textDocument);
    
    $.writeln("Text layer created automatically by Cench AI!");
} else {
    $.writeln("Please open a composition first!");
}
'''
    
    print("Executing automation command...")
    result = execute_after_effects_script(text_command, result['path'])
    
    if result['success']:
        print("✅ AUTOMATION SUCCESSFUL!")
        print("   Text layer should appear in After Effects now!")
        print("   You should see green text saying 'Cench AI Automated!'")
    else:
        print("❌ Automation failed:")
        print(f"   Error: {result['message']}")
        sys.exit(1)
    
    # Wait a moment
    import time
    time.sleep(2)
    
    # Test 2: Add animation
    print("\n🎨 AUTOMATION 2: Adding animation...")
    animation_command = '''
// Add animation automatically
var comp = app.project.activeItem;
if (comp && comp instanceof CompItem) {
    var textLayer = comp.layer(1); // Get our text layer
    if (textLayer) {
        // Add wiggle animation
        var positionProp = textLayer.property("Position");
        positionProp.expression = "wiggle(1, 30);"; // Wiggle every 1 second, 30 pixels
        
        // Add scale animation
        var scaleProp = textLayer.property("Scale");
        scaleProp.expression = "wiggle(2, 20);"; // Wiggle scale every 2 seconds
        
        $.writeln("Animation added automatically by Cench AI!");
    }
} else {
    $.writeln("Please open a composition first!");
}
'''
    
    print("Executing animation automation...")
    result = execute_after_effects_script(animation_command, result['path'])
    
    if result['success']:
        print("✅ ANIMATION AUTOMATION SUCCESSFUL!")
        print("   Text should now be wiggling and scaling!")
        print("   This happened automatically - no manual work needed!")
    else:
        print("❌ Animation automation failed:")
        print(f"   Error: {result['message']}")
    
    print("\n" + "="*50)
    print("🎯 AUTOMATION DEMONSTRATION COMPLETE!")
    print("="*50)
    print("✅ Cench AI successfully automated After Effects!")
    print("✅ No manual script running required!")
    print("✅ Commands executed automatically!")
    print("✅ Real-time changes visible in After Effects!")
    
    print("\n" + "="*50)
    print("🔄 THIS IS WHAT CENCH AI WILL DO:")
    print("="*50)
    print("1. You type: 'Create a text layer'")
    print("2. Cench AI generates the code automatically")
    print("3. Code executes in After Effects automatically")
    print("4. You see the result instantly - no manual work!")
    
    print("\n" + "="*50)
    print("🚀 NEXT STEPS:")
    print("="*50)
    print("1. Restart the Cench AI app")
    print("2. Test the connection in Settings")
    print("3. Use natural language to control After Effects")
    print("4. Watch automation happen in real-time!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 