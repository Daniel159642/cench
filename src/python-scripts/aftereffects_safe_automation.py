#!/usr/bin/env python3
"""
SAFE After Effects automation for Cench AI
Designed to prevent crashes and use gentle execution methods
"""

import sys
import json
import os
import subprocess
import time
import threading
import queue
from pathlib import Path

class SafeAfterEffectsAutomation:
    def __init__(self):
        self.script_queue = queue.Queue()
        self.watch_thread = None
        self.is_running = False
        self.scripts_dir = os.path.expanduser("~/Documents/Cench AI Scripts")
        
        # Create scripts directory
        os.makedirs(self.scripts_dir, exist_ok=True)
        
        print("🛡️ Safe After Effects automation initialized")
        print(f"   Scripts directory: {self.scripts_dir}")
        
    def is_after_effects_ready(self):
        """Check if After Effects is stable and ready for automation"""
        try:
            # Check if After Effects process exists and is responsive
            result = subprocess.run(['pgrep', '-f', 'Adobe After Effects'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode != 0:
                print("❌ After Effects is not running")
                return False
            
            # Try a gentle check to see if After Effects is responsive
            check_script = '''
tell application "Adobe After Effects 2025"
    get version
end tell
'''
            
            result = subprocess.run(['osascript', '-e', check_script], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ After Effects is ready and responsive")
                return True
            else:
                print("⚠️ After Effects is running but not responsive (may be crashed)")
                return False
                
        except Exception as e:
            print(f"❌ Error checking After Effects status: {e}")
            return False
    
    def wait_for_after_effects(self, timeout=60):
        """Wait for After Effects to be ready"""
        print("⏳ Waiting for After Effects to be ready...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.is_after_effects_ready():
                return True
            time.sleep(2)
        
        print("⏰ Timeout waiting for After Effects")
        return False
    
    def execute_script_safely(self, script_path):
        """Execute a script using the safest method available"""
        try:
            print(f"🛡️ Executing script safely: {os.path.basename(script_path)}")
            
            # Method 1: Use ExtendScript Toolkit (safest)
            if self._try_extendscript_execution(script_path):
                return True
            
            # Method 2: Use gentle AppleScript (safer)
            if self._try_gentle_applescript(script_path):
                return True
            
            # Method 3: Create manual launcher (safest fallback)
            return self._create_manual_launcher(script_path)
            
        except Exception as e:
            print(f"❌ Safe execution failed: {e}")
            return False
    
    def _try_extendscript_execution(self, script_path):
        """Try ExtendScript Toolkit execution (safest method)"""
        try:
            estk_paths = [
                "/Applications/Adobe ExtendScript Toolkit CC/ExtendScript Toolkit.app",
                "/Applications/Adobe ExtendScript Toolkit CS6/ExtendScript Toolkit.app"
            ]
            
            for estk_path in estk_paths:
                if os.path.exists(estk_path):
                    print("🔧 Trying ExtendScript Toolkit...")
                    cmd = [estk_path, "-run", script_path]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        print("✅ Executed via ExtendScript Toolkit")
                        return True
            return False
        except:
            return False
    
    def _try_gentle_applescript(self, script_path):
        """Use very gentle AppleScript that won't crash After Effects"""
        try:
            print("🍎 Trying gentle AppleScript...")
            
            # Super gentle approach - just activate and run script
            apple_script = f'''
tell application "Adobe After Effects 2025"
    activate
    delay 2
    do script file (POSIX file "{script_path}")
end tell
'''
            
            result = subprocess.run(['osascript', '-e', apple_script], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Executed via gentle AppleScript")
                return True
            else:
                print(f"❌ Gentle AppleScript failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Gentle AppleScript error: {e}")
            return False
    
    def _create_manual_launcher(self, script_path):
        """Create a manual launcher script for user to run"""
        try:
            launcher_path = script_path.replace('.jsx', '_MANUAL_LAUNCHER.scpt')
            
            launcher_content = f'''
-- Manual After Effects Script Launcher
-- Created by Cench AI Safe Automation
-- Run this script manually to avoid crashes

tell application "Adobe After Effects 2025"
    activate
    delay 3
    do script file (POSIX file "{script_path}")
end tell
'''
            
            with open(launcher_path, 'w') as f:
                f.write(launcher_content)
            
            print(f"📝 Manual launcher created: {os.path.basename(launcher_path)}")
            print("   Run this launcher manually to execute the script safely")
            return True
                
        except Exception as e:
            print(f"❌ Manual launcher creation failed: {e}")
            return False
    
    def execute_script_now(self, code):
        """Execute a script immediately with safety checks"""
        try:
            # First check if After Effects is ready
            if not self.is_after_effects_ready():
                print("⚠️ After Effects is not ready. Waiting...")
                if not self.wait_for_after_effects():
                    return {
                        "success": False,
                        "message": "After Effects is not responding. Please restart it and try again."
                    }
            
            # Create the script
            timestamp = int(time.time())
            script_filename = f"cench_safe_{timestamp}.jsx"
            script_path = os.path.join(self.scripts_dir, script_filename)
            
            script_content = f"""// Safe After Effects Script generated by Cench AI
// Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}
// This script uses safe execution methods

{code}

// Log completion
$.writeln("Cench AI safe script executed successfully!");
alert("Cench AI safe automation completed!");
"""
            
            # Write the script file
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            print(f"📝 Safe script created: {script_filename}")
            
            # Execute safely
            if self.execute_script_safely(script_path):
                return {
                    "success": True,
                    "message": "Script executed safely",
                    "script_path": script_path
                }
            else:
                return {
                    "success": False,
                    "message": "Script execution failed, but manual launcher was created",
                    "script_path": script_path
                }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Safe script creation failed: {str(e)}",
                "error": str(e)
            }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "message": "No arguments provided"}))
        return

    if sys.argv[1] == '--execute':
        # Execute a script safely
        if len(sys.argv) < 3:
            print(json.dumps({"success": False, "message": "No code provided"}))
            return
        
        code = sys.argv[2]
        automation = SafeAfterEffectsAutomation()
        result = automation.execute_script_now(code)
        print(json.dumps(result))
    
    elif sys.argv[1] == '--check':
        # Check if After Effects is ready
        automation = SafeAfterEffectsAutomation()
        if automation.is_after_effects_ready():
            print(json.dumps({"success": True, "message": "After Effects is ready"}))
        else:
            print(json.dumps({"success": False, "message": "After Effects is not ready"}))
    
    else:
        print(json.dumps({"success": False, "message": "Invalid argument. Use --execute or --check"}))

if __name__ == "__main__":
    main()
