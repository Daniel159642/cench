#!/usr/bin/env python3
import sys
import os

# Add the correct paths for DaVinci Resolve modules
davinci_modules = "/Applications/DaVinci Resolve.app/Contents/Resources/Developer/Scripting/Modules"
davinci_libs = "/Applications/DaVinci Resolve.app/Contents/Libraries/Fusion"

if davinci_modules not in sys.path:
    sys.path.insert(0, davinci_modules)

if davinci_libs not in sys.path:
    sys.path.insert(0, davinci_libs)

print("Python path:")
for path in sys.path:
    print(f"  {path}")

print(f"\nChecking for DaVinci modules...")
print(f"DaVinci modules path exists: {os.path.exists(davinci_modules)}")
print(f"DaVinci libs path exists: {os.path.exists(davinci_libs)}")

# Check environment variables
print(f"\nEnvironment variables:")
print(f"RESOLVE_SCRIPT_LIB: {os.getenv('RESOLVE_SCRIPT_LIB', 'Not set')}")
print(f"RESOLVE_SCRIPT_API: {os.getenv('RESOLVE_SCRIPT_API', 'Not set')}")
print(f"RESOLVE_SCRIPT_FRAMEWORK: {os.getenv('RESOLVE_SCRIPT_FRAMEWORK', 'Not set')}")

try:
    # Try to import the module
    import DaVinciResolveScript
    print("\n✅ Successfully imported DaVinciResolveScript!")
    
    # Try different connection methods
    print("\nTrying different connection methods...")
    
    # Method 1: scriptapp("Resolve")
    try:
        resolve = DaVinciResolveScript.scriptapp("Resolve")
        if resolve:
            print("✅ Method 1 (scriptapp) successful!")
            print(f"Version: {resolve.GetVersion()}")
            
            # Try to get project manager
            project_manager = resolve.GetProjectManager()
            if project_manager:
                print("✅ Successfully got project manager!")
            else:
                print("❌ Could not get project manager")
        else:
            print("❌ Method 1 (scriptapp) returned None")
    except Exception as e:
        print(f"❌ Method 1 (scriptapp) error: {e}")
    
    # Method 2: Try without argument
    try:
        resolve = DaVinciResolveScript.scriptapp()
        if resolve:
            print("✅ Method 2 (scriptapp no arg) successful!")
        else:
            print("❌ Method 2 (scriptapp no arg) returned None")
    except Exception as e:
        print(f"❌ Method 2 (scriptapp no arg) error: {e}")
    
    # Method 3: Try with different app names
    app_names = ["Resolve", "DaVinci Resolve", "DaVinciResolve", "resolve", "davinci"]
    for app_name in app_names:
        try:
            resolve = DaVinciResolveScript.scriptapp(app_name)
            if resolve:
                print(f"✅ Method 3 ({app_name}) successful!")
                break
            else:
                print(f"❌ Method 3 ({app_name}) returned None")
        except Exception as e:
            print(f"❌ Method 3 ({app_name}) error: {e}")
    
    # Method 4: Check available methods
    print(f"\nAvailable methods in DaVinciResolveScript:")
    for method in dir(DaVinciResolveScript):
        if not method.startswith('_'):
            print(f"  {method}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ General error: {e}")

print(f"\nNote: DaVinci Resolve scripting API typically requires:")
print(f"1. DaVinci Resolve to be running")
print(f"2. A project to be open (sometimes)")
print(f"3. Scripting to be enabled in preferences")
print(f"4. The correct version of DaVinci Resolve") 