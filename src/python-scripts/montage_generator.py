#!/usr/bin/env python3
"""
Montage Generator for Cench AI
Creates video montages from photos with music
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Optional
import subprocess
import threading
import time

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Required packages not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "pillow", "numpy"])
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont

class MontageGenerator:
    def __init__(self):
        self.temp_dir = None
        self.output_dir = Path.home() / "Documents" / "Cench AI Montages"
        self.output_dir.mkdir(exist_ok=True)
        
    def create_temp_directory(self):
        """Create temporary directory for processing"""
        self.temp_dir = tempfile.mkdtemp(prefix="cench_montage_")
        return self.temp_dir
    
    def cleanup_temp_directory(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def process_photos(self, photo_paths: List[str], progress_callback=None) -> List[str]:
        """Process and resize photos for montage"""
        processed_photos = []
        
        for i, photo_path in enumerate(photo_paths):
            if progress_callback:
                progress_callback(f"Processing photo {i+1}/{len(photo_paths)}")
            
            try:
                # Load and resize image
                img = Image.open(photo_path)
                
                # Resize to 1920x1080 maintaining aspect ratio
                target_size = (1920, 1080)
                img.thumbnail(target_size, Image.Resampling.LANCZOS)
                
                # Create new image with black background
                new_img = Image.new('RGB', target_size, (0, 0, 0))
                
                # Center the image
                x = (target_size[0] - img.size[0]) // 2
                y = (target_size[1] - img.size[1]) // 2
                new_img.paste(img, (x, y))
                
                # Save processed image
                processed_path = os.path.join(self.temp_dir, f"processed_{i:03d}.jpg")
                new_img.save(processed_path, "JPEG", quality=95)
                processed_photos.append(processed_path)
                
            except Exception as e:
                print(f"Error processing {photo_path}: {e}")
                continue
        
        return processed_photos
    
    def create_transitions(self, photo_paths: List[str], transition_duration: float = 1.0, progress_callback=None) -> str:
        """Create smooth transitions between photos"""
        if len(photo_paths) < 2:
            return photo_paths[0] if photo_paths else None
        
        fps = 30
        transition_frames = int(fps * transition_duration)
        
        # Create video writer
        output_path = os.path.join(self.temp_dir, "montage_with_transitions.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (1920, 1080))
        
        total_frames = len(photo_paths) * transition_frames
        current_frame = 0
        
        for i in range(len(photo_paths) - 1):
            img1 = cv2.imread(photo_paths[i])
            img2 = cv2.imread(photo_paths[i + 1])
            
            if img1 is None or img2 is None:
                continue
            
            # Create crossfade transition
            for frame in range(transition_frames):
                alpha = frame / transition_frames
                beta = 1.0 - alpha
                
                # Blend images
                blended = cv2.addWeighted(img1, beta, img2, alpha, 0)
                out.write(blended)
                
                current_frame += 1
                if progress_callback:
                    progress = int((current_frame / total_frames) * 100)
                    progress_callback(f"Creating transitions: {progress}%")
        
        out.release()
        return output_path
    
    def add_music(self, video_path: str, music_path: str, output_path: str, progress_callback=None) -> str:
        """Add music to the montage video"""
        if progress_callback:
            progress_callback("Adding music to montage...")
        
        try:
            # Use ffmpeg to add music
            cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-i', music_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
            
        except subprocess.CalledProcessError as e:
            print(f"Error adding music: {e}")
            # If ffmpeg fails, return video without music
            return video_path
        except FileNotFoundError:
            print("ffmpeg not found. Returning video without music.")
            return video_path
    
    def add_effects(self, video_path: str, progress_callback=None) -> str:
        """Add visual effects to the montage"""
        if progress_callback:
            progress_callback("Adding visual effects...")
        
        # For now, return the original video
        # This can be extended with more effects
        return video_path
    
    def generate_montage(self, photo_paths: List[str], music_path: Optional[str] = None, 
                        progress_callback=None) -> Dict[str, str]:
        """Generate complete montage from photos and music"""
        try:
            # Create temp directory
            self.create_temp_directory()
            
            if progress_callback:
                progress_callback("Starting montage generation...")
            
            # Process photos
            processed_photos = self.process_photos(photo_paths, progress_callback)
            
            if not processed_photos:
                raise Exception("No photos were processed successfully")
            
            # Create transitions
            video_path = self.create_transitions(processed_photos, progress_callback=progress_callback)
            
            # Add effects
            video_path = self.add_effects(video_path, progress_callback)
            
            # Add music if provided
            final_output = os.path.join(self.output_dir, f"montage_{int(time.time())}.mp4")
            if music_path and os.path.exists(music_path):
                video_path = self.add_music(video_path, music_path, final_output, progress_callback)
            else:
                # Copy video to final location
                shutil.copy2(video_path, final_output)
            
            if progress_callback:
                progress_callback("Montage generation complete!")
            
            return {
                "success": True,
                "output_path": final_output,
                "message": "Montage created successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create montage: {e}"
            }
        finally:
            self.cleanup_temp_directory()

def create_montage(photo_paths: List[str], music_path: Optional[str] = None, 
                  progress_callback=None) -> Dict[str, str]:
    """Main function to create montage"""
    generator = MontageGenerator()
    return generator.generate_montage(photo_paths, music_path, progress_callback)

if __name__ == "__main__":
    # Test the montage generator
    test_photos = [
        "/path/to/photo1.jpg",
        "/path/to/photo2.jpg",
        "/path/to/photo3.jpg"
    ]
    
    def test_progress(message):
        print(f"Progress: {message}")
    
    result = create_montage(test_photos, progress_callback=test_progress)
    print(json.dumps(result, indent=2))
