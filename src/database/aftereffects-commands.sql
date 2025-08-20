-- After Effects commands database
CREATE TABLE IF NOT EXISTS aftereffects_commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command_name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    api_method TEXT NOT NULL,
    parameters TEXT,
    example_usage TEXT NOT NULL,
    javascript_code TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    safety_level TEXT DEFAULT 'safe',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample After Effects commands
INSERT OR REPLACE INTO aftereffects_commands (command_name, description, api_method, parameters, example_usage, javascript_code, category, safety_level) VALUES
('Create New Composition', 'Create a new composition with specified settings', 'app.project.items.addComp', 'name, width, height, duration', 'Create a new composition called "Main Comp" with 1920x1080 resolution and 10 second duration', 'var comp = app.project.items.addComp("Main Comp", 1920, 1080, 1, 10, 30);', 'composition', 'safe'),

('Import Media', 'Import media files into the project', 'app.project.importFile', 'file_path', 'Import a video file from the desktop', 'var importOptions = new ImportOptions(File("~/Desktop/video.mp4")); app.project.importFile(importOptions);', 'media', 'safe'),

('Add Layer to Composition', 'Add a layer to the active composition', 'comp.layers.add', 'source', 'Add the first imported item as a layer', 'var layer = comp.layers.add(importedItem);', 'composition', 'safe'),

('Set Layer Position', 'Set the position of a layer', 'layer.position.setValue', 'position_array', 'Move layer to center of composition', 'layer.position.setValue([comp.width/2, comp.height/2]);', 'animation', 'safe'),

('Add Keyframe', 'Add a keyframe to a layer property', 'property.setValueAtTime', 'time, value', 'Add position keyframe at 2 seconds', 'layer.position.setValueAtTime(2, [100, 100]);', 'animation', 'safe'),

('Create Text Layer', 'Create a new text layer', 'comp.layers.addText', 'text_string', 'Add a text layer saying "Hello World"', 'var textLayer = comp.layers.addText("Hello World");', 'text', 'safe'),

('Apply Effect', 'Apply an effect to a layer', 'layer.Effects.addProperty', 'effect_name', 'Apply a blur effect to the layer', 'var blurEffect = layer.Effects.addProperty("Gaussian Blur");', 'effects', 'safe'),

('Set Layer Opacity', 'Set the opacity of a layer', 'layer.opacity.setValue', 'opacity_percentage', 'Set layer to 50% opacity', 'layer.opacity.setValue(50);', 'animation', 'safe'),

('Create Solid Layer', 'Create a solid color layer', 'comp.layers.addSolid', 'color, name, width, height, duration', 'Create a red solid layer', 'var solid = comp.layers.addSolid([1, 0, 0], "Red Solid", 100, 100, 1);', 'composition', 'safe'),

('Add Expression', 'Add an expression to a layer property', 'property.expression', 'expression_string', 'Add wiggle expression to position', 'layer.position.expression = "wiggle(2, 50);";', 'animation', 'safe');

-- Create table for After Effects examples
CREATE TABLE IF NOT EXISTS aftereffects_examples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command_id INTEGER NOT NULL,
    natural_language TEXT NOT NULL,
    expected_code TEXT NOT NULL,
    context_tags TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (command_id) REFERENCES aftereffects_commands (id)
);

-- Insert sample examples
INSERT OR REPLACE INTO aftereffects_examples (command_id, natural_language, expected_code, context_tags) VALUES
(1, 'Create a new composition', 'var comp = app.project.items.addComp("New Comp", 1920, 1080, 1, 10, 30);', 'composition, new, setup'),
(2, 'Import a video file', 'var importOptions = new ImportOptions(File("~/Desktop/video.mp4")); app.project.importFile(importOptions);', 'import, media, file'),
(3, 'Add a layer to the composition', 'var layer = comp.layers.add(importedItem);', 'layer, add, composition'),
(4, 'Move the layer to the center', 'layer.position.setValue([comp.width/2, comp.height/2]);', 'position, center, move'),
(5, 'Add a keyframe at 2 seconds', 'layer.position.setValueAtTime(2, [100, 100]);', 'keyframe, animation, timing'),
(6, 'Create a text layer', 'var textLayer = comp.layers.addText("Hello World");', 'text, create, layer'),
(7, 'Apply a blur effect', 'var blurEffect = layer.Effects.addProperty("Gaussian Blur");', 'effect, blur, apply'),
(8, 'Set the layer to 50% opacity', 'layer.opacity.setValue(50);', 'opacity, transparency'),
(9, 'Create a red solid layer', 'var solid = comp.layers.addSolid([1, 0, 0], "Red Solid", 100, 100, 1);', 'solid, color, create'),
(10, 'Add a wiggle expression', 'layer.position.expression = "wiggle(2, 50);";', 'expression, wiggle, animation'); 