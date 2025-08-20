#!/usr/bin/env python3
"""
Test script for After Effects integration
"""

import sys
import os

# Add the project path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src', 'python-scripts'))

try:
    from aftereffects_execute import check_after_effects_connection, find_after_effects_path
    
    print("✅ After Effects integration module imported successfully!")
    
    print("\n🔍 Checking After Effects installation...")
    ae_path = find_after_effects_path()
    
    if ae_path:
        print(f"✅ After Effects found at: {ae_path}")
        
        print("\n🔗 Testing connection...")
        result = check_after_effects_connection()
        
        if result['success']:
            print("✅ After Effects connection successful!")
            print(f"   Version: {result['version']}")
            print(f"   Path: {result['path']}")
        else:
            print("❌ After Effects connection failed:")
            print(f"   Error: {result['message']}")
    else:
        print("❌ After Effects not found")
        print("\n💡 Make sure After Effects is installed in one of these locations:")
        print("   - /Applications/Adobe After Effects 2024/")
        print("   - /Applications/Adobe After Effects 2023/")
        print("   - /Applications/Adobe After Effects 2022/")
        print("   - /Applications/Adobe After Effects 2021/")
        print("   - /Applications/Adobe After Effects 2020/")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🎯 Next steps:")
print("1. Make sure After Effects is installed")
print("2. Run the app and test the connection in Settings")
print("3. Try natural language commands for After Effects") 