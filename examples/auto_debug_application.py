#!/usr/bin/env python3
"""Autonomously debug the full-stack application until it works."""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from langest.agents.autonomous_debugger import AutonomousDebuggingAgent


def main():
    """Main function to run autonomous debugging."""
    
    print("🤖 AUTONOMOUS APPLICATION DEBUGGING SYSTEM")
    print("=" * 70)
    print("🎯 Goal: Fix all issues until the application is fully working")
    print("🔧 Agent: AI-powered autonomous debugging with iterative fixes")
    print("📋 Scope: Go backend, React frontend, Tilt, Docker, tests")
    print()
    
    # Check environment
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    if not os.path.exists(env_file):
        print("⚠️  WARNING: .env file not found!")
        print("   The debugging agent needs your GROQ_API_KEY to function")
        return
    
    # Initialize the autonomous debugging agent
    print("🚀 Initializing Autonomous Debugging Agent...")
    debugger = AutonomousDebuggingAgent()
    
    # Set project path
    project_path = "/home/txz/dev/langest/generated_fullstack_service"
    
    print(f"📁 Project: {project_path}")
    print()
    
    # Start with a specific command that was failing
    print("🎯 PHASE 1: Fix Tilt Configuration")
    print("-" * 50)
    
    # First try to fix Tilt validation
    tilt_success = debugger.debug_until_working("tilt validate", project_path)
    
    if tilt_success:
        print("\n✅ Tilt configuration fixed!")
        
        # Now try the full tilt up command  
        print("\n🎯 PHASE 2: Test Full Tilt Startup")
        print("-" * 50)
        
        # Use a timeout for tilt up since it's a long-running command
        tilt_up_success = debugger.debug_until_working("timeout 30s tilt up --stream=false", project_path)
        
        if tilt_up_success:
            print("\n🎉 Tilt startup successful!")
        else:
            print("\n⚠️  Tilt startup had issues, but validation worked")
    
    # Run comprehensive debugging
    print("\n🎯 PHASE 3: Comprehensive Application Debugging")
    print("-" * 50)
    
    results = debugger.run_comprehensive_debug(project_path)
    
    # Final report
    print("\n" + "=" * 70)
    print("📊 FINAL DEBUGGING REPORT")
    print("=" * 70)
    
    total_working = sum(results.values())
    total_components = len(results)
    success_rate = (total_working / total_components) * 100
    
    print(f"✅ Components Working: {total_working}/{total_components} ({success_rate:.0f}%)")
    print()
    
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        component_name = component.replace('_', ' ').title()
        print(f"{status_icon} {component_name}")
    
    print()
    
    if total_working == total_components:
        print("🎉 FULL SUCCESS! All components are working!")
        print("🚀 Your application is ready for development and deployment!")
        print()
        print("💡 Next steps:")
        print("   • Run 'make tilt' to start the development environment")
        print("   • Access frontend: http://localhost:3000")
        print("   • Access backend: http://localhost:8080")
        print("   • Monitor with Tilt UI: http://localhost:10350")
        
    elif total_working >= total_components * 0.7:  # 70% success
        print("🟡 PARTIAL SUCCESS! Most components are working.")
        print("🔧 Some issues remain but core functionality should work")
        print()
        print("💡 You can try:")
        print("   • Run 'make backend' and 'make frontend' separately")
        print("   • Check the debug history for remaining issues")
        
    else:
        print("🔴 MULTIPLE ISSUES REMAINING")
        print("🔍 Check the debug history above for details")
        print("🛠️  You may need to manually address some issues")
    
    print()
    print("🤖 Autonomous debugging session completed!")
    
    return total_working == total_components


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Debugging interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
