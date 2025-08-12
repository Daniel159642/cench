-- Essential DaVinci Resolve commands
INSERT OR IGNORE INTO davinci_commands (command_name, description, api_method, parameters, example_usage, python_code, category) VALUES
('add_video_track', 'Add a new video track to the timeline', 'timeline.AddTrack', 'track_type, track_index', 'Add video track above current tracks', 'timeline.AddTrack("video")', 'timeline'),
('set_clip_speed', 'Change the playback speed of selected clips', 'timeline.SetClipSpeed', 'timeline_item, speed', 'Speed up clip to 2x', 'timeline_item.SetClipSpeed(200)', 'editing'),
('add_transition', 'Add transition between clips', 'timeline.AddTransition', 'transition_name', 'Add cross dissolve', 'timeline.AddTransition("Cross Dissolve")', 'effects'),
('import_media', 'Import media files into media pool', 'mediaPool.ImportMedia', 'file_paths', 'Import video files', 'mediaPool.ImportMedia(["/path/to/file.mp4"])', 'media'),
('create_timeline', 'Create a new timeline', 'mediaPool.CreateEmptyTimeline', 'timeline_name', 'Create new timeline', 'mediaPool.CreateEmptyTimeline("New Timeline")', 'timeline'),
('add_title', 'Add text/title to timeline', 'timeline.AddTitle', 'title_text, duration', 'Add title overlay', 'timeline.AddTitle("My Title", 300)', 'graphics'),
('color_correct', 'Apply basic color correction', 'timeline.SetClipColor', 'clip, parameters', 'Adjust brightness', 'timeline_item.SetClipColor({"Brightness": 10})', 'color'),
('add_audio_track', 'Add new audio track', 'timeline.AddTrack', 'track_type', 'Add audio track', 'timeline.AddTrack("audio")', 'audio'),
('export_timeline', 'Export/render current timeline', 'project.LoadRenderPreset', 'preset_name', 'Export H264', 'project.LoadRenderPreset("H.264 Master")', 'export'),
('delete_clip', 'Delete selected clips', 'timeline.DeleteClips', 'timeline_items', 'Delete selected clips', 'timeline.DeleteClips(selected_items)', 'editing');

-- Natural language examples
INSERT OR IGNORE INTO command_examples (command_id, natural_language, expected_code) VALUES
(1, 'add a new video track', 'timeline.AddTrack("video")'),
(1, 'create another video layer', 'timeline.AddTrack("video")'),
(2, 'speed up the clip to 2x', 'timeline_item.SetClipSpeed(200)'),
(2, 'make it twice as fast', 'timeline_item.SetClipSpeed(200)'),
(2, 'slow down to half speed', 'timeline_item.SetClipSpeed(50)'),
(3, 'add a cross dissolve transition', 'timeline.AddTransition("Cross Dissolve")'),
(3, 'fade between clips', 'timeline.AddTransition("Cross Dissolve")'),
(4, 'import my video files', 'mediaPool.ImportMedia(file_paths)'),
(5, 'create a new timeline called Main Edit', 'mediaPool.CreateEmptyTimeline("Main Edit")'),
(6, 'add title that says Hello World', 'timeline.AddTitle("Hello World", 300)');

-- Default settings
INSERT OR IGNORE INTO user_settings (setting_key, setting_value) VALUES
('openai_api_key', ''),
('auto_execute', 'false'),
('overlay_opacity', '0.95'),
('shortcut_key', 'CommandOrControl+Shift+C'),
('theme', 'dark'); 