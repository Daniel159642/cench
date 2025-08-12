#!/usr/bin/env python3
import sys
import json
import os

# Add DaVinci Resolve module path to Python path
davinci_module_path = "/Applications/DaVinci Resolve.app/Contents/Resources/Developer/Scripting/Modules"
if davinci_module_path not in sys.path:
    sys.path.insert(0, davinci_module_path)

import DaVinciResolveScript as dvr_script

def connect_to_resolve():
    """Connect to DaVinci Resolve"""
    try:
        resolve = dvr_script.scriptapp("Resolve")
        if resolve:
            return resolve
        else:
            raise Exception("Could not connect to DaVinci Resolve")
    except Exception as e:
        raise Exception(f"DaVinci Resolve connection failed: {str(e)}")

def check_connection():
    """Check if DaVinci Resolve is accessible"""
    try:
        resolve = connect_to_resolve()
        project_manager = resolve.GetProjectManager()
        
        if project_manager:
            return {
                "success": True,
                "message": "Successfully connected to DaVinci Resolve",
                "version": getattr(resolve, 'GetVersion', lambda: 'Unknown')()
            }
        else:
            return {
                "success": False,
                "message": "Could not get project manager"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Connection failed: {str(e)}"
        }

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

def execute_code(code, resolve):
    """Execute Python code safely in DaVinci context"""
    try:
        # Safety check
        if not is_safe_code(code):
            return {
                "success": False,
                "message": "Code contains potentially dangerous operations",
                "error": "Safety check failed"
            }
        
        # Create safe execution environment
        safe_globals = {
            'resolve': resolve,
            'projectManager': resolve.GetProjectManager(),
            'project': None,
            'mediaPool': None,
            'timeline': None
        }
        
        # Get current project and timeline
        try:
            safe_globals['project'] = safe_globals['projectManager'].GetCurrentProject()
            if safe_globals['project']:
                safe_globals['mediaPool'] = safe_globals['project'].GetMediaPool()
                safe_globals['timeline'] = safe_globals['project'].GetCurrentTimeline()
        except:
            pass
        
        # Execute code
        exec(code, safe_globals)
        
        return {
            "success": True,
            "message": "Command executed successfully",
            "result": "OK"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Execution error: {str(e)}",
            "error": str(e)
        }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "message": "No arguments provided"}))
        return

    if sys.argv[1] == '--check':
        # Connection check mode
        result = check_connection()
        print(json.dumps(result))
        return

    # Code execution mode
    code = sys.argv[1]
    
    try:
        resolve = connect_to_resolve()
        result = execute_code(code, resolve)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({
            "success": False,
            "message": str(e),
            "error": str(e)
        }))

if __name__ == "__main__":
    main() 