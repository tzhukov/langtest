#!/usr/bin/env python3
"""Demonstrate debugging capabilities with DevOps Agent."""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from langest.agents.devops_engineer import DevOpsEngineerAgent


def debug_current_project():
    """Debug the current full-stack project."""
    
    print("🔧 DevOps Agent - Debugging Full-Stack Application")
    print("=" * 60)
    
    # Initialize the DevOps agent
    devops_agent = DevOpsEngineerAgent()
    
    # Define the project path
    project_path = "/home/txz/dev/langest/generated_fullstack_service"
    
    # Define the error we encountered
    error_description = """
    Error encountered when trying to build the Go backend:
    
    # command-line-arguments
    ./main.go:4:2: "net/http" imported and not used
    
    The Go compiler is failing because there's an unused import in the main.go file.
    This prevents the backend from starting.
    """
    
    print("🔍 Analyzing project and debugging issue...")
    print(f"📁 Project Path: {project_path}")
    print(f"⚠️  Error: Go build failing due to unused import")
    print()
    
    try:
        # Use the DevOps agent to debug the issue
        debug_analysis = devops_agent.debug_application(
            project_path=project_path,
            error_description=error_description
        )
        
        print("🤖 DevOps Agent Analysis:")
        print("-" * 40)
        print(debug_analysis)
        
        # Also demonstrate environment setup analysis
        print("\n🛠️  Environment Setup Analysis:")
        print("-" * 40)
        
        requirements = {
            "go": True,
            "node": True,
            "docker": True,
            "tilt": False  # Most people don't have Tilt installed
        }
        
        setup_analysis = devops_agent.setup_development_environment(
            project_path=project_path,
            requirements=requirements
        )
        
        print(setup_analysis)
        
    except Exception as e:
        print(f"❌ Error during debugging: {str(e)}")
        return False
    
    return True


def demonstrate_other_capabilities():
    """Demonstrate other DevOps agent capabilities."""
    
    print("\n🚀 Additional DevOps Agent Capabilities:")
    print("=" * 60)
    
    devops_agent = DevOpsEngineerAgent()
    
    # Demonstrate deployment pipeline creation
    print("\n📦 Creating Deployment Pipeline...")
    pipeline = devops_agent.create_deployment_pipeline(
        project_description="Go + React Task Management Application with REST API",
        target_environment="AWS EKS with GitHub Actions CI/CD"
    )
    
    print("Deployment Pipeline Configuration:")
    print("-" * 40)
    print(pipeline[:500] + "..." if len(pipeline) > 500 else pipeline)
    
    # Demonstrate performance optimization
    print("\n⚡ Performance Optimization Analysis...")
    performance_metrics = {
        "response_time_ms": 250,
        "memory_usage_mb": 128,
        "cpu_usage_percent": 45,
        "concurrent_users": 100,
        "database_query_time_ms": 50
    }
    
    optimization = devops_agent.optimize_performance(
        project_path="/home/txz/dev/langest/generated_fullstack_service",
        performance_metrics=performance_metrics
    )
    
    print("Performance Optimization Recommendations:")
    print("-" * 40)
    print(optimization[:500] + "..." if len(optimization) > 500 else optimization)


def main():
    """Main function."""
    
    print("🎯 AI-Powered DevOps Agent - Execution & Debugging Demo")
    print("=" * 70)
    print()
    
    # Check if we have the required environment
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    if not os.path.exists(env_file):
        print("⚠️  WARNING: .env file not found!")
        print("   The DevOps agent needs your GROQ_API_KEY to function")
        print("   Set up your .env file and try again")
        return
    
    try:
        # Debug the current project
        success = debug_current_project()
        
        if success:
            # Demonstrate other capabilities
            demonstrate_other_capabilities()
            
            print("\n✅ DevOps Agent Demo Completed Successfully!")
            print("\n💡 Key Capabilities Demonstrated:")
            print("   🔧 Automatic error diagnosis and debugging")
            print("   🛠️  Environment setup and validation")
            print("   📦 CI/CD pipeline generation")  
            print("   ⚡ Performance optimization analysis")
            print("   🔍 Real-time project analysis")
            
            print("\n🚀 The DevOps agent can:")
            print("   ✅ Execute shell commands and analyze results")
            print("   ✅ Debug compilation and runtime errors")
            print("   ✅ Set up development environments") 
            print("   ✅ Create deployment pipelines")
            print("   ✅ Optimize application performance")
            print("   ✅ Provide specific, actionable fixes")
        else:
            print("\n❌ Demo encountered issues")
            
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
