#!/usr/bin/env python3
"""
Test FULL AUTOMATION - No manual script running needed!
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
    
    print("🚀 TESTING FULL AFTER EFFECTS AUTOMATION")
    print("="*60)
    print("This will execute scripts AUTOMATICALLY - no manual work!")
    
    # Check connection
    print("\n🔗 Checking After Effects connection...")
    result = check_after_effects_connection()
    
    if not result['success']:
        print("❌ After Effects not connected!")
        sys.exit(1)
    
    print("✅ After Effects connected!")
    print(f"   Version: {result['version']}")
    
    # Test 1: Simple text creation
    print("\n🎬 AUTOMATION TEST 1: Creating animated text...")
    text_command = '''
// Create animated text automatically
var comp = app.project.activeItem;
if (comp && comp instanceof CompItem) {
    var textLayer = comp.layers.addText("FULLY AUTOMATED!");
    textLayer.position.setValue([comp.width/2, comp.height/2]);
    
    // Style the text
    var textDocument = textLayer.property("Source Text").value;
    textDocument.fontSize = 80;
    textDocument.fillColor = [0, 1, 0]; // Green color
    textDocument.strokeColor = [1, 1, 0]; // Yellow stroke
    textDocument.strokeWidth = 5;
    textLayer.property("Source Text").setValue(textDocument);
    
    // Add animation
    var scaleProp = textLayer.property("Scale");
    scaleProp.expression = "wiggle(1, 40);";
    
    $.writeln("Fully automated text created!");
} else {
    $.writeln("Please open a composition first!");
}
'''
    
    print("Executing automation command...")
    result = execute_after_effects_script(text_command, result['path'])
    
    if result['success']:
        if result.get('automation', False):
            print("🎉 FULL AUTOMATION SUCCESS!")
            print("   Script executed automatically!")
            print("   You should see the text in After Effects NOW!")
            print("   No manual script running needed!")
        else:
            print("✅ Script created successfully!")
            print("   You'll need to run it manually in After Effects")
            print("   Automation system will be available after restart")
    else:
        print("❌ Automation failed:")
        print(f"   Error: {result['message']}")
    
    # Wait a moment
    import time
    time.sleep(2)
    
    # Test 2: Complex visual effects
    print("\n🎨 AUTOMATION TEST 2: Creating complex effects...")
    effects_command = '''
// Create complex visual effects automatically
var comp = app.project.activeItem;
if (comp && comp instanceof CompItem) {
    // Create background
    var bgLayer = comp.layers.addSolid([0.2, 0.1, 0.4], "Background", comp.width, comp.height, 1);
    bgLayer.moveTo(1);
    
    // Create animated shapes
    var circleLayer = comp.layers.addSolid([1, 0.5, 0], "Orange Circle", 150, 150, 1);
    circleLayer.position.setValue([comp.width/3, comp.height/3]);
    circleLayer.property("Scale").expression = "wiggle(0.8, 25);";
    
    var squareLayer = comp.layers.addSolid([0, 0.8, 1], "Blue Square", 120, 120, 1);
    squareLayer.position.setValue([comp.width*2/3, comp.height*2/3]);
    squareLayer.property("Rotation").expression = "time * 120;";
    
    // Add camera movement
    var cameraLayer = comp.layers.addCamera("Camera", [comp.width/2, comp.height/2]);
    cameraLayer.property("Position").expression = "wiggle(0.5, 15);";
    
    $.writeln("Complex effects created automatically!");
} else {
    $.writeln("Please open a composition first!");
}
'''
    
    print("Executing complex effects automation...")
    result = execute_after_effects_script(effects_command, result['path'])
    
    if result['success']:
        if result.get('automation', False):
            print("🎉 COMPLEX EFFECTS AUTOMATION SUCCESS!")
            print("   All effects created automatically!")
            print("   Check After Effects - everything should be there!")
        else:
            print("✅ Complex effects script created!")
            print("   Run it manually in After Effects")
    else:
        print("❌ Complex effects failed:")
        print(f"   Error: {result['message']}")
    
    print("\n" + "="*60)
    print("🎯 AUTOMATION TEST COMPLETE!")
    print("="*60)
    
    if result.get('automation', False):
        print("🎉 FULL AUTOMATION IS WORKING!")
        print("✅ Scripts execute automatically")
        print("✅ No manual intervention needed")
        print("✅ Real-time control achieved")
        print("✅ This is what you wanted!")
    else:
        print("📝 Scripts created successfully")
        print("🔄 Automation system needs to be started")
        print("🚀 After restart, everything will be automatic!")
    
    print("\n" + "="*60)
    print("🚀 NEXT STEPS:")
    print("="*60)
    print("1. Check After Effects for the created content")
    print("2. Restart Cench AI app to enable full automation")
    print("3. Use natural language to control After Effects")
    print("4. Watch automation happen in real-time!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 