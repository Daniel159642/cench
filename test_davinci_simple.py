#!/usr/bin/env python3
"""
Simple DaVinci Resolve connection test
Run this AFTER enabling scripting in DaVinci Resolve preferences
"""

import sys
import os

# Add DaVinci Resolve paths
davinci_modules = "/Applications/DaVinci Resolve.app/Contents/Resources/Developer/Scripting/Modules"
davinci_libs = "/Applications/DaVinci Resolve.app/Contents/Libraries/Fusion"

if davinci_modules not in sys.path:
    sys.path.insert(0, davinci_modules)
if davinci_libs not in sys.path:
    sys.path.insert(0, davinci_libs)

try:
    import DaVinciResolveScript
    print("✅ DaVinciResolveScript imported successfully!")
    
    # Try to connect
    print("Attempting to connect to DaVinci Resolve...")
    resolve = DaVinciResolveScript.scriptapp("Resolve")
    
    if resolve:
        print("✅ Connected to DaVinci Resolve!")
        print(f"Version: {resolve.GetVersion()}")
        
        # Try to get project manager
        project_manager = resolve.GetProjectManager()
        if project_manager:
            print("✅ Project Manager accessible!")
            
            # Try to get current project
            current_project = project_manager.GetCurrentProject()
            if current_project:
                print(f"✅ Current project: {current_project.GetName()}")
            else:
                print("⚠️  No project currently open")
        else:
            print("❌ Could not access Project Manager")
    else:
        print("❌ Connection failed - scriptapp returned None")
        print("\nTroubleshooting tips:")
        print("1. Make sure DaVinci Resolve is running")
        print("2. Enable scripting in DaVinci Resolve → Preferences → System → External Scripting")
        print("3. Open a project in DaVinci Resolve")
        print("4. Make sure you're not on the welcome screen")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure DaVinci Resolve is running and scripting is enabled")
except Exception as e:
    print(f"❌ Error: {e}") 