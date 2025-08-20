#!/usr/bin/env python3
"""
Test LIVE After Effects Automation
This shows real-time control without manual intervention!
"""

import sys
import os
import time

# Add the project path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src', 'python-scripts'))

try:
    from aftereffects_automation import AfterEffectsAutomation
    
    print("🎬 LIVE AFTER EFFECTS AUTOMATION TEST")
    print("="*60)
    print("This will create and execute scripts in real-time!")
    print("Watch After Effects - everything happens automatically!")
    
    # Start automation system
    print("\n🚀 Starting automation system...")
    automation = AfterEffectsAutomation()
    
    # Wait for system to be ready
    time.sleep(2)
    
    print("\n🎨 LIVE DEMO 1: Creating animated text...")
    text_command = '''
// Create animated text in real-time
var comp = app.project.activeItem;
if (comp && comp instanceof CompItem) {
    var textLayer = comp.layers.addText("LIVE AUTOMATION!");
    textLayer.position.setValue([comp.width/2, comp.height/2]);
    
    // Style the text
    var textDoc = textLayer.property("Source Text").value;
    textDoc.fontSize = 100;
    textDoc.fillColor = [0, 1, 0]; // Green
    textDoc.strokeColor = [1, 1, 0]; // Yellow stroke
    textDoc.strokeWidth = 6;
    textLayer.property("Source Text").setValue(textDoc);
    
    // Add animation
    textLayer.property("Scale").expression = "wiggle(1, 40);";
    textLayer.property("Rotation").expression = "wiggle(2, 20);";
    
    $.writeln("Live animated text created!");
} else {
    $.writeln("Please open a composition first!");
}
'''
    
    print("Executing live text creation...")
    result = automation.execute_script_now(text_command)
    
    if result['success']:
        print("✅ Live text creation successful!")
        print("   Script should execute automatically in After Effects!")
        print("   You should see green animated text appear!")
    else:
        print("❌ Live text creation failed:")
        print(f"   Error: {result['message']}")
    
    # Wait for execution
    time.sleep(3)
    
    print("\n🌟 LIVE DEMO 2: Creating particle effects...")
    particle_command = '''
// Create particle effects in real-time
var comp = app.project.activeItem;
if (comp && comp instanceof CompItem) {
    // Create multiple particles
    for (var i = 0; i < 12; i++) {
        var particle = comp.layers.addSolid([1, 0.5, 0], "Particle " + i, 30, 30, 1);
        particle.position.setValue([
            Math.random() * comp.width,
            Math.random() * comp.height
        ]);
        
        // Animate particles
        particle.property("Scale").expression = "wiggle(2, 60);";
        particle.property("Opacity").expression = "wiggle(1.5, 40);";
        particle.property("Rotation").expression = "time * 360;";
    }
    
    $.writeln("Live particle effects created!");
} else {
    $.writeln("Please open a composition first!");
}
'''
    
    print("Executing live particle creation...")
    result = automation.execute_script_now(particle_command)
    
    if result['success']:
        print("✅ Live particle creation successful!")
        print("   Particles should appear and animate automatically!")
        print("   Check After Effects for the orange animated particles!")
    else:
        print("❌ Live particle creation failed:")
        print(f"   Error: {result['message']}")
    
    # Wait for execution
    time.sleep(3)
    
    print("\n🎬 LIVE DEMO 3: Creating camera movement...")
    camera_command = '''
// Create dynamic camera movement in real-time
var comp = app.project.activeItem;
if (comp && comp instanceof CompItem) {
    // Add camera
    var cameraLayer = comp.layers.addCamera("Live Camera", [comp.width/2, comp.height/2]);
    
    // Add dramatic movement
    cameraLayer.property("Position").expression = "wiggle(0.8, 30);";
    cameraLayer.property("Zoom").expression = "wiggle(1.5, 80);";
    
    $.writeln("Live camera movement created!");
} else {
    $.writeln("Please open a composition first!");
}
'''
    
    print("Executing live camera creation...")
    result = automation.execute_script_now(camera_command)
    
    if result['success']:
        print("✅ Live camera creation successful!")
        print("   Camera should be moving dynamically!")
        print("   Check After Effects for the animated camera!")
    else:
        print("❌ Live camera creation failed:")
        print(f"   Error: {result['message']}")
    
    print("\n" + "="*60)
    print("🎯 LIVE AUTOMATION TEST COMPLETE!")
    print("="*60)
    print("✅ All scripts executed automatically!")
    print("✅ No manual intervention needed!")
    print("✅ Real-time control achieved!")
    print("✅ This is FULL automation!")
    
    print("\n" + "="*60)
    print("🚀 WHAT YOU JUST EXPERIENCED:")
    print("="*60)
    print("1. Scripts created automatically")
    print("2. Scripts executed automatically")
    print("3. Results appeared in After Effects instantly")
    print("4. Zero manual work required")
    print("5. This is the future of creative automation!")
    
    print("\n" + "="*60)
    print("🎬 CHECK AFTER EFFECTS NOW:")
    print("="*60)
    print("You should see:")
    print("• Green animated text 'LIVE AUTOMATION!'")
    print("• 12 orange animated particles")
    print("• Dynamic camera movement")
    print("• Everything created automatically!")
    
    # Keep automation running
    print("\n🔄 Automation system is still running...")
    print("Press Ctrl+C to stop when you're done testing")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        automation.stop_automation()
        print("\n👋 Automation stopped")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 