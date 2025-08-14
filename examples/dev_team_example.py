#!/usr/bin/env python3
"""Example script demonstrating the AI Development Team workflow."""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from langest.graphs.dev_team_graph import create_dev_team_graph


def run_dev_team_project(project_request: str):
    """Run a project through the AI development team.
    
    Args:
        project_request: Description of the project to be developed
    """
    print("🚀 Starting AI Development Team Project")
    print("=" * 60)
    print(f"📋 Project Request: {project_request}")
    print("=" * 60)
    
    # Create the development team graph
    graph = create_dev_team_graph()
    
    # Initialize the state
    initial_state = {
        "project_request": project_request,
        "messages": [],
        "project_plan": "",
        "code_implementation": "",
        "test_plan": "",
        "test_results": "",
        "documentation": "",
        "final_deliverable": "",
        "current_agent": "",
        "next_step": "project_manager"
    }
    
    print("⚡ Executing development workflow...")
    print("   🎯 Project Manager → 💻 Software Engineer → 🧪 QA Engineer → 📚 Tech Writer → 📋 Final Review")
    print()
    
    # Run the workflow
    try:
        result = graph.invoke(initial_state)
        
        # Display results
        print("✅ PROJECT COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        print("\n🎯 PROJECT PLAN:")
        print("-" * 40)
        print(result["project_plan"][:500] + "..." if len(result["project_plan"]) > 500 else result["project_plan"])
        
        print("\n💻 CODE IMPLEMENTATION:")
        print("-" * 40)
        print(result["code_implementation"][:500] + "..." if len(result["code_implementation"]) > 500 else result["code_implementation"])
        
        print("\n🧪 QA TESTING:")
        print("-" * 40)
        print(result["test_results"][:500] + "..." if len(result["test_results"]) > 500 else result["test_results"])
        
        print("\n📚 DOCUMENTATION:")
        print("-" * 40)
        print(result["documentation"][:500] + "..." if len(result["documentation"]) > 500 else result["documentation"])
        
        print("\n📋 FINAL DELIVERABLE:")
        print("-" * 40)
        print(result["final_deliverable"][:500] + "..." if len(result["final_deliverable"]) > 500 else result["final_deliverable"])
        
        return result
        
    except Exception as e:
        print(f"❌ Error during project execution: {str(e)}")
        return None


def main():
    """Main function with example project requests."""
    
    # Example projects
    example_projects = [
        "Create a Python CLI tool that helps developers manage their Git repositories by providing quick statistics, branch information, and commit summaries",
        
        "Build a REST API for a task management system that allows users to create, update, delete, and organize tasks with categories and due dates",
        
        "Develop a Python library for processing CSV files with advanced filtering, sorting, and data transformation capabilities",
        
        "Create a web scraping tool that can extract product information from e-commerce websites and save the data in various formats"
    ]
    
    print("🎯 AI Development Team - Project Examples")
    print("=" * 60)
    
    for i, project in enumerate(example_projects, 1):
        print(f"{i}. {project}")
    
    print(f"{len(example_projects) + 1}. Enter custom project")
    print("0. Exit")
    
    try:
        choice = input("\nSelect a project (0-{}): ".format(len(example_projects) + 1))
        choice = int(choice)
        
        if choice == 0:
            print("👋 Goodbye!")
            return
        elif 1 <= choice <= len(example_projects):
            project_request = example_projects[choice - 1]
        elif choice == len(example_projects) + 1:
            project_request = input("Enter your custom project request: ").strip()
            if not project_request:
                print("❌ Empty project request. Exiting.")
                return
        else:
            print("❌ Invalid choice. Exiting.")
            return
        
        # Run the selected project
        result = run_dev_team_project(project_request)
        
        if result:
            print("\n🎉 Project completed successfully!")
            print("💡 Tip: Check the deliverables above for complete project implementation.")
        else:
            print("\n❌ Project execution failed.")
            
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
