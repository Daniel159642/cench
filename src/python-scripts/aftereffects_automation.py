#!/usr/bin/env python3
"""
FULLY AUTOMATED After Effects integration for Cench AI
No manual script running required!
"""

import sys
import json
import os
import subprocess
import platform
import time
import threading
import queue
from pathlib import Path

class AfterEffectsAutomation:
    def __init__(self):
        self.script_queue = queue.Queue()
        self.watch_thread = None
        self.is_running = False
        self.scripts_dir = os.path.expanduser("~/Documents/Cench AI Scripts")
        
        # Create scripts directory
        os.makedirs(self.scripts_dir, exist_ok=True)
        
        # Start automation
        self.start_automation()
    
    def start_automation(self):
        """Start the automation system"""
        self.is_running = True
        
        # Start script execution thread
        self.execution_thread = threading.Thread(target=self._script_executor, daemon=True)
        self.execution_thread.start()
        
        # Start file watcher thread
        self.watch_thread = threading.Thread(target=self._file_watcher, daemon=True)
        self.watch_thread.start()
        
        print("🚀 After Effects automation started!")
        print(f"   Watching: {self.scripts_dir}")
        print("   Scripts will execute automatically!")
    
    def stop_automation(self):
        """Stop the automation system"""
        self.is_running = False
        if self.watch_thread:
            self.watch_thread.join(timeout=1)
        print("⏹️ After Effects automation stopped")
    
    def _file_watcher(self):
        """Watch for new script files and queue them for execution"""
        last_modified = {}
        
        while self.is_running:
            try:
                # Check for new or modified .jsx files
                for script_file in Path(self.scripts_dir).glob("*.jsx"):
                    file_path = str(script_file)
                    mtime = script_file.stat().st_mtime
                    
                    # If file is new or modified, queue it
                    if file_path not in last_modified or last_modified[file_path] < mtime:
                        last_modified[file_path] = mtime
                        
                        # Wait a moment for file to be fully written
                        time.sleep(0.5)
                        
                        # Read and queue the script
                        try:
                            with open(file_path, 'r') as f:
                                script_content = f.read()
                            
                            # Only queue if it's a Cench AI script
                            if "Cench AI" in script_content:
                                self.script_queue.put({
                                    'file_path': file_path,
                                    'content': script_content,
                                    'timestamp': mtime
                                })
                                print(f"📝 New script detected: {script_file.name}")
                        except Exception as e:
                            print(f"❌ Error reading script {file_path}: {e}")
                
                time.sleep(0.1)  # Check every 100ms
                
            except Exception as e:
                print(f"❌ File watcher error: {e}")
                time.sleep(1)
    
    def _script_executor(self):
        """Execute scripts from the queue automatically"""
        while self.is_running:
            try:
                # Get script from queue (non-blocking)
                try:
                    script_data = self.script_queue.get(timeout=0.1)
                except queue.Empty:
                    continue
                
                # Execute the script
                self._execute_script_automatically(script_data)
                
            except Exception as e:
                print(f"❌ Script executor error: {e}")
                time.sleep(1)
    
    def _execute_script_automatically(self, script_data):
        """Execute a script automatically without user intervention"""
        try:
            file_path = script_data['file_path']
            print(f"🚀 Executing script automatically: {os.path.basename(file_path)}")
            
            # Method 1: Try using ExtendScript Toolkit (if available)
            if self._try_extendscript_execution(file_path):
                return True
            
            # Method 2: Try AppleScript with improved syntax
            if self._try_applescript_execution(file_path):
                return True
            
            # Method 3: Try command-line execution
            if self._try_commandline_execution(file_path):
                return True
            
            # Method 4: Create a launcher script
            return self._create_launcher_script(file_path)
            
        except Exception as e:
            print(f"❌ Automatic execution failed: {e}")
            return False
    
    def _try_extendscript_execution(self, script_path):
        """Try to execute using ExtendScript Toolkit"""
        try:
            # Look for ExtendScript Toolkit
            estk_paths = [
                "/Applications/Adobe ExtendScript Toolkit CC/ExtendScript Toolkit.app",
                "/Applications/Adobe ExtendScript Toolkit CS6/ExtendScript Toolkit.app"
            ]
            
            for estk_path in estk_paths:
                if os.path.exists(estk_path):
                    cmd = [estk_path, "-run", script_path]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        print("✅ Executed via ExtendScript Toolkit")
                        return True
            return False
        except:
            return False
    
    def _try_applescript_execution(self, script_path):
        """Try to execute using improved AppleScript"""
        try:
            # Use a more reliable AppleScript approach
            apple_script = f'''
tell application "Adobe After Effects 2025"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "Adobe After Effects 2025"
        -- Try to use the Scripts menu
        click menu item "Run Script File..." of menu "Scripts" of menu bar 1
        delay 0.5
        
        -- Type the script path
        keystroke "g" using command down
        delay 0.5
        keystroke "{script_path}"
        delay 0.5
        keystroke return
    end tell
end tell
'''
            
            result = subprocess.run(['osascript', '-e', apple_script], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Executed via AppleScript")
                return True
            else:
                print(f"❌ AppleScript failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ AppleScript error: {e}")
            return False
    
    def _try_commandline_execution(self, script_path):
        """Try to execute using command line"""
        try:
            # Try different command line approaches
            ae_paths = [
                "/Applications/Adobe After Effects 2025/Adobe After Effects 2025.app/Contents/MacOS/After Effects",
                "/Applications/Adobe After Effects 2024/Adobe After Effects 2024.app/Contents/MacOS/After Effects"
            ]
            
            for ae_path in ae_paths:
                if os.path.exists(ae_path):
                    # Try different command line options
                    for option in ["-script", "-s", "-run"]:
                        try:
                            cmd = [ae_path, option, script_path]
                            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                            if result.returncode == 0:
                                print(f"✅ Executed via command line ({option})")
                                return True
                        except:
                            continue
            
            return False
        except:
            return False
    
    def _create_launcher_script(self, script_path):
        """Create a launcher script that can be run manually"""
        try:
            launcher_path = script_path.replace('.jsx', '_LAUNCHER.scpt')
            
            # Create AppleScript launcher
            launcher_content = f'''
tell application "Adobe After Effects 2025"
    activate
    delay 1
    do script file (POSIX file "{script_path}")
end tell
'''
            
            with open(launcher_path, 'w') as f:
                f.write(launcher_content)
            
            # Try to execute the launcher
            result = subprocess.run(['osascript', launcher_path], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Executed via launcher script")
                return True
            else:
                print(f"❌ Launcher failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Launcher creation failed: {e}")
            return False
    
    def execute_script_now(self, code):
        """Execute a script immediately (for testing)"""
        try:
            # Create a temporary script
            timestamp = int(time.time())
            script_filename = f"cench_auto_{timestamp}.jsx"
            script_path = os.path.join(self.scripts_dir, script_filename)
            
            # Create the script content
            script_content = f"""// After Effects Script generated by Cench AI
// Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}
// This script will execute automatically!

{code}

// Log completion
$.writeln("Cench AI script executed automatically!");
alert("Cench AI automation completed!");
"""
            
            # Write the script file
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            print(f"📝 Script created: {script_filename}")
            print("🚀 It should execute automatically in a few seconds...")
            
            return {
                "success": True,
                "message": "Script created and queued for automatic execution",
                "script_path": script_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Script creation failed: {str(e)}",
                "error": str(e)
            }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "message": "No arguments provided"}))
        return

    if sys.argv[1] == '--start':
        # Start automation system
        automation = AfterEffectsAutomation()
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            automation.stop_automation()
            print("👋 Automation stopped")
    
    elif sys.argv[1] == '--execute':
        # Execute a script immediately
        if len(sys.argv) < 3:
            print(json.dumps({"success": False, "message": "No code provided"}))
            return
        
        code = sys.argv[2]
        automation = AfterEffectsAutomation()
        result = automation.execute_script_now(code)
        print(json.dumps(result))
        
        # Stop automation after execution
        automation.stop_automation()
    
    else:
        print(json.dumps({"success": False, "message": "Invalid argument"}))

if __name__ == "__main__":
    main() 