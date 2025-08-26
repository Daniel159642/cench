#!/usr/bin/env python3
"""
Montage Integration for Cench AI
Handles montage requests from React frontend
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

# Add the project path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / 'src' / 'python-scripts'))

from montage_generator import create_montage

def handle_montage_request(request_data: Dict) -> Dict:
    """Handle montage creation request from frontend"""
    try:
        # Extract data from request
        photo_files = request_data.get('photos', [])
        music_file = request_data.get('music', None)
        
        if not photo_files:
            return {
                'success': False,
                'error': 'No photos provided',
                'message': 'Please select at least one photo'
            }
        
        # Create temporary files for processing
        temp_photos = []
        temp_music = None
        
        try:
            # Save photos to temporary files
            for i, photo_data in enumerate(photo_files):
                if isinstance(photo_data, dict) and 'data' in photo_data:
                    # Handle base64 data
                    import base64
                    photo_bytes = base64.b64decode(photo_data['data'].split(',')[1])
                    temp_path = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                    temp_path.write(photo_bytes)
                    temp_path.close()
                    temp_photos.append(temp_path.name)
                elif isinstance(photo_data, str):
                    # Handle file paths
                    temp_photos.append(photo_data)
            
            # Save music to temporary file if provided
            if music_file:
                if isinstance(music_file, dict) and 'data' in music_file:
                    import base64
                    music_bytes = base64.b64decode(music_file['data'].split(',')[1])
                    temp_music_path = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
                    temp_music_path.write(music_bytes)
                    temp_music_path.close()
                    temp_music = temp_music_path.name
                elif isinstance(music_file, str):
                    temp_music = music_file
            
            # Create progress callback
            progress_messages = []
            def progress_callback(message):
                progress_messages.append(message)
                print(f"Montage Progress: {message}")
            
            # Generate montage
            result = create_montage(temp_photos, temp_music, progress_callback)
            
            # Add progress messages to result
            result['progress_messages'] = progress_messages
            
            return result
            
        finally:
            # Clean up temporary files
            for temp_photo in temp_photos:
                if os.path.exists(temp_photo):
                    os.unlink(temp_photo)
            
            if temp_music and os.path.exists(temp_music):
                os.unlink(temp_music)
                
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f'Failed to create montage: {e}'
        }

def get_music_recommendations() -> List[Dict]:
    """Get AI-recommended music options"""
    return [
        {
            'id': 1,
            'title': 'Epic Adventure',
            'genre': 'Cinematic',
            'duration': '2:30',
            'mood': 'epic',
            'description': 'Perfect for action and adventure montages'
        },
        {
            'id': 2,
            'title': 'Summer Vibes',
            'genre': 'Pop',
            'duration': '3:15',
            'mood': 'upbeat',
            'description': 'Great for vacation and happy moments'
        },
        {
            'id': 3,
            'title': 'Emotional Journey',
            'genre': 'Ambient',
            'duration': '4:20',
            'mood': 'emotional',
            'description': 'Ideal for sentimental and touching montages'
        },
        {
            'id': 4,
            'title': 'Upbeat Energy',
            'genre': 'Electronic',
            'duration': '2:45',
            'mood': 'energetic',
            'description': 'Perfect for sports and high-energy content'
        },
        {
            'id': 5,
            'title': 'Peaceful Moments',
            'genre': 'Acoustic',
            'duration': '3:30',
            'mood': 'calm',
            'description': 'Great for nature and peaceful scenes'
        }
    ]

def validate_photo_files(photo_paths: List[str]) -> Dict:
    """Validate uploaded photo files"""
    valid_photos = []
    errors = []
    
    for path in photo_paths:
        if not os.path.exists(path):
            errors.append(f"File not found: {path}")
            continue
            
        # Check file size (max 50MB)
        file_size = os.path.getsize(path) / (1024 * 1024)  # MB
        if file_size > 50:
            errors.append(f"File too large: {path} ({file_size:.1f}MB)")
            continue
            
        # Check file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.heic', '.bmp']
        file_ext = Path(path).suffix.lower()
        if file_ext not in valid_extensions:
            errors.append(f"Unsupported format: {path}")
            continue
            
        valid_photos.append(path)
    
    return {
        'valid_photos': valid_photos,
        'errors': errors,
        'total_photos': len(photo_paths),
        'valid_count': len(valid_photos)
    }

if __name__ == "__main__":
    # Test the integration
    test_request = {
        'photos': [
            '/path/to/photo1.jpg',
            '/path/to/photo2.jpg'
        ],
        'music': None
    }
    
    result = handle_montage_request(test_request)
    print(json.dumps(result, indent=2))
