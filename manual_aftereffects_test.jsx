// Manual After Effects Test Script for Cench AI
// Save this file and run it from After Effects: File → Scripts → Run Script File...

// Check if we have an active composition
var comp = app.project.activeItem;

if (comp && comp instanceof CompItem) {
    // We have a composition, let's create some content!
    
    // Create a text layer
    var textLayer = comp.layers.addText("Hello from Cench AI!");
    
    // Center the text
    textLayer.position.setValue([comp.width/2, comp.height/2]);
    
    // Set text properties
    var textDocument = textLayer.property("Source Text").value;
    textDocument.fontSize = 48;
    textDocument.fillColor = [1, 0, 0]; // Red color
    textLayer.property("Source Text").setValue(textDocument);
    
    // Add some animation
    var positionProp = textLayer.property("Position");
    positionProp.expression = "wiggle(2, 50);"; // Wiggle every 2 seconds, 50 pixels
    
    // Create a background solid
    var solidLayer = comp.layers.addSolid([0.1, 0.1, 0.1], "Background", comp.width, comp.height, 1);
    solidLayer.moveTo(1); // Move to back
    
    // Add a glow effect to the text
    var glowEffect = textLayer.Effects.addProperty("Glow");
    glowEffect.property("Glow Intensity").setValue(2);
    glowEffect.property("Glow Radius").setValue(20);
    glowEffect.property("Glow Colors").setValue(1); // A and B colors
    
    // Log success
    $.writeln("🎉 Cench AI test completed successfully!");
    $.writeln("✅ Text layer created and animated");
    $.writeln("✅ Background solid added");
    $.writeln("✅ Glow effect applied");
    $.writeln("✅ Wiggle animation added");
    
} else {
    // No composition open
    $.writeln("❌ Please open a composition first!");
    $.writeln("   Go to: Composition → New Composition");
    $.writeln("   Then run this script again");
}

// Show completion message
alert("Cench AI Test Complete!\n\nCheck your composition for:\n• Red animated text\n• Background solid\n• Glow effects\n• Wiggle animation"); 