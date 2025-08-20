#!/usr/bin/env python3
"""
Adobe After Effects integration for Cench AI
Handles After Effects scripting and automation
"""

import sys
import json
import os
import subprocess
import platform
import tempfile

def check_after_effects_connection():
    """Check if After Effects is accessible"""
    try:
        # Try to find After Effects installation
        ae_path = find_after_effects_path()
        if ae_path:
            return {
                "success": True,
                "message": "After Effects found and accessible",
                "version": get_ae_version(ae_path),
                "path": ae_path
            }
        else:
            return {
                "success": False,
                "message": "After Effects not found"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Connection check failed: {str(e)}"
        }

def find_after_effects_path():
    """Find After Effects installation path based on platform"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        possible_paths = [
            "/Applications/Adobe After Effects 2025/Adobe After Effects 2025.app",
            "/Applications/Adobe After Effects 2024/Adobe After Effects 2024.app",
            "/Applications/Adobe After Effects 2023/Adobe After Effects 2023.app",
            "/Applications/Adobe After Effects 2022/Adobe After Effects 2022.app",
            "/Applications/Adobe After Effects 2021/Adobe After Effects 2021.app",
            "/Applications/Adobe After Effects 2020/Adobe After Effects 2020.app"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
    elif system == "Windows":
        # Windows paths would go here
        possible_paths = [
            "C:\\Program Files\\Adobe\\Adobe After Effects 2024\\Support Files\\AfterFX.exe",
            "C:\\Program Files\\Adobe\\Adobe After Effects 2023\\Support Files\\AfterFX.exe",
            "C:\\Program Files\\Adobe\\Adobe After Effects 2022\\Support Files\\AfterFX.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
    
    return None

def get_ae_version(ae_path):
    """Get After Effects version from the installation"""
    try:
        if platform.system() == "Darwin":  # macOS
            # Extract version from app bundle
            info_plist = os.path.join(ae_path, "Contents", "Info.plist")
            if os.path.exists(info_plist):
                result = subprocess.run(['plutil', '-p', info_plist], 
                                      capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'CFBundleShortVersionString' in line:
                        return line.split('"')[-2]
        else:
            # Windows version detection
            pass
            
        return "Unknown"
    except:
        return "Unknown"

def is_safe_code(code):
    """Check if the code is safe to execute"""
    dangerous_patterns = [
        r'import\s+os',
        r'import\s+subprocess',
        r'import\s+sys',
        r'exec\s*\(',
        r'eval\s*\(',
        r'__import__\s*\(',
        r'open\s*\(',
        r'file\s*\(',
        r'\.system\s*\(',
        r'\.popen\s*\(',
        r'\.call\s*\(',
        r'globals\s*\(',
        r'locals\s*\('
    ]
    
    import re
    for pattern in dangerous_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            return False
    return True

def execute_after_effects_script(code, ae_path):
    """Execute After Effects script with FULL AUTOMATION"""
    try:
        # Safety check
        if not is_safe_code(code):
            return {
                "success": False,
                "message": "Code contains potentially dangerous operations",
                "error": "Safety check failed"
            }
        
        # Try to use the automation system first
        automation_result = _try_automation_execution(code)
        if automation_result['success']:
            return automation_result
        
        # Fallback to manual execution if automation fails
        return _manual_execution(code, ae_path)
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Script execution error: {str(e)}",
            "error": str(e)
        }

def _try_automation_execution(code):
    """Try to execute using the automation system"""
    try:
        # Import the automation module
        automation_path = os.path.join(os.path.dirname(__file__), 'aftereffects_automation.py')
        
        if not os.path.exists(automation_path):
            return {"success": False, "message": "Automation system not available"}
        
        # Try to execute using the automation system
        cmd = [sys.executable, automation_path, '--execute', code]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            try:
                # Parse the JSON response
                response = json.loads(result.stdout)
                if response['success']:
                    return {
                        "success": True,
                        "message": "Script executed automatically via automation system!",
                        "automation": True,
                        "script_path": response.get('script_path', 'Unknown')
                    }
            except:
                pass
        
        return {"success": False, "message": "Automation execution failed"}
        
    except Exception as e:
        return {"success": False, "message": f"Automation error: {str(e)}"}

def _manual_execution(code, ae_path):
    """Fallback to manual execution method"""
    try:
        # Create a script file in the user's Documents folder
        docs_dir = os.path.expanduser("~/Documents")
        script_dir = os.path.join(docs_dir, "Cench AI Scripts")
        
        # Create the directory if it doesn't exist
        os.makedirs(script_dir, exist_ok=True)
        
        # Create a unique script filename
        import time
        timestamp = int(time.time())
        script_filename = f"cench_script_{timestamp}.jsx"
        script_path = os.path.join(script_dir, script_filename)
        
        # Create the script content
        script_content = f"""// After Effects Script generated by Cench AI
// Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}

{code}

// Log completion
$.writeln("Cench AI script execution completed successfully!");
alert("Cench AI script completed!");
"""
        
        # Write the script file
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Try to activate After Effects
        if platform.system() == "Darwin":
            try:
                subprocess.run(['osascript', '-e', 'tell application "Adobe After Effects 2025" to activate'], 
                              capture_output=True, timeout=10)
            except:
                pass
        
        return {
            "success": True,
            "message": "Script saved. Run it in After Effects: File → Scripts → Run Script File...",
            "automation": False,
            "script_path": script_path,
            "instructions": [
                "1. The script has been saved to your Documents folder",
                "2. In After Effects, go to: File → Scripts → Run Script File...",
                "3. Navigate to: ~/Documents/Cench AI Scripts/",
                "4. Select the script and run it",
                "5. You'll see the results immediately in After Effects!"
            ]
        }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Script creation error: {str(e)}",
            "error": str(e)
        }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "message": "No arguments provided"}))
        return

    if sys.argv[1] == '--check':
        # Connection check mode
        result = check_after_effects_connection()
        print(json.dumps(result))
        return

    # Code execution mode
    code = sys.argv[1]
    
    try:
        ae_path = find_after_effects_path()
        if not ae_path:
            print(json.dumps({
                "success": False,
                "message": "After Effects not found"
            }))
            return
            
        result = execute_after_effects_script(code, ae_path)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({
            "success": False,
            "message": str(e),
            "error": str(e)
        }))

if __name__ == "__main__":
    main() 