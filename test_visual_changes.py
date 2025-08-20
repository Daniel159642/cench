#!/usr/bin/env python3
"""
Test visual changes in After Effects
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
    
    print("🎬 CREATING VISUAL AFTER EFFECTS AUTOMATION")
    print("="*60)
    print("This will create a script that makes BIG visual changes!")
    
    # Check connection
    print("\n🔗 Checking After Effects connection...")
    result = check_after_effects_connection()
    
    if not result['success']:
        print("❌ After Effects not connected!")
        sys.exit(1)
    
    print("✅ After Effects connected!")
    
    # Create a dramatic visual script
    print("\n🎨 Creating dramatic visual automation script...")
    visual_command = '''
// CENCH AI - DRAMATIC VISUAL AUTOMATION
// This will create a stunning visual composition automatically!

var comp = app.project.activeItem;

if (comp && comp instanceof CompItem) {
    // 1. Create animated text
    var textLayer = comp.layers.addText("CENCH AI");
    textLayer.position.setValue([comp.width/2, comp.height/2]);
    
    // Style the text dramatically
    var textDocument = textLayer.property("Source Text").value;
    textDocument.fontSize = 120;
    textDocument.fillColor = [1, 0, 0]; // Bright red
    textDocument.strokeColor = [1, 1, 0]; // Yellow stroke
    textDocument.strokeWidth = 8;
    textDocument.font = "Arial-BoldMT";
    textLayer.property("Source Text").setValue(textDocument);
    
    // 2. Add dramatic animation
    var positionProp = textLayer.property("Position");
    positionProp.expression = "wiggle(0.5, 100);"; // Fast wiggle
    
    var scaleProp = textLayer.property("Scale");
    scaleProp.expression = "wiggle(1, 50);"; // Scale wiggle
    
    var rotationProp = textLayer.property("Rotation");
    rotationProp.expression = "wiggle(2, 45);"; // Rotation wiggle
    
    // 3. Create background solid
    var solidLayer = comp.layers.addSolid([0.1, 0.1, 0.3], "Background", comp.width, comp.height, 1);
    solidLayer.moveTo(1); // Move to back
    
    // 4. Add glow effect to text
    var glowEffect = textLayer.Effects.addProperty("Glow");
    glowEffect.property("Glow Intensity").setValue(3);
    glowEffect.property("Glow Radius").setValue(30);
    glowEffect.property("Glow Colors").setValue(1); // A and B colors
    
    // 5. Add drop shadow
    var shadowEffect = textLayer.Effects.addProperty("Drop Shadow");
    shadowEffect.property("Shadow Color").setValue([0, 0, 0]);
    shadowEffect.property("Shadow Distance").setValue(20);
    shadowEffect.property("Shadow Softness").setValue(50);
    
    // 6. Create additional animated elements
    var circleLayer = comp.layers.addSolid([0, 1, 1], "Circle", 200, 200, 1);
    circleLayer.position.setValue([comp.width/4, comp.height/4]);
    circleLayer.property("Scale").expression = "wiggle(1, 30);";
    
    var squareLayer = comp.layers.addSolid([1, 0, 1], "Square", 150, 150, 1);
    squareLayer.position.setValue([comp.width*3/4, comp.height*3/4]);
    squareLayer.property("Rotation").expression = "time * 90;"; // Continuous rotation
    
    // 7. Add camera shake effect
    var cameraLayer = comp.layers.addCamera("Camera", [comp.width/2, comp.height/2]);
    cameraLayer.property("Position").expression = "wiggle(0.3, 20);";
    
    $.writeln("🎉 CENCH AI created a DRAMATIC visual composition!");
    $.writeln("✅ Animated text with glow and shadow");
    $.writeln("✅ Background solid");
    $.writeln("✅ Animated shapes");
    $.writeln("✅ Camera shake effect");
    
    alert("🎬 CENCH AI AUTOMATION COMPLETE!\n\nYour composition now has:\n• Animated red text\n• Glowing effects\n• Animated shapes\n• Camera shake\n• Background elements\n\nCheck your timeline and preview!");
    
} else {
    $.writeln("❌ Please open a composition first!");
    alert("Please create a new composition first, then run this script!");
}
'''
    
    print("Executing visual automation command...")
    result = execute_after_effects_script(visual_command, result['path'])
    
    if result['success']:
        print("✅ VISUAL AUTOMATION SCRIPT CREATED!")
        print(f"   Script saved to: {result['script_path']}")
        print("\n🎯 NEXT STEPS TO SEE CHANGES:")
        for instruction in result['instructions']:
            print(f"   {instruction}")
        
        print("\n🎬 WHAT YOU'LL SEE:")
        print("   • Bright red animated text 'CENCH AI'")
        print("   • Glowing effects and shadows")
        print("   • Animated shapes (circle & square)")
        print("   • Camera shake effect")
        print("   • Dramatic background")
        print("   • Success alert when complete")
        
    else:
        print("❌ Visual automation failed:")
        print(f"   Error: {result['message']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 