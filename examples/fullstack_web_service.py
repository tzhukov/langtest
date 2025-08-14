#!/usr/bin/env python3
"""Generate a full-stack web service with Go backend, React frontend, and Tilt configuration."""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from langest.graphs.dev_team_graph import create_dev_team_graph


def generate_fullstack_service():
    """Generate a complete full-stack web service using the AI development team."""
    
    # Define the project requirements
    project_request = """
    Create a full-stack web service with the following requirements:

    BACKEND (Go):
    - REST API server using Go with Gin framework
    - CRUD operations for managing tasks/todos
    - JSON API endpoints: GET /tasks, POST /tasks, PUT /tasks/:id, DELETE /tasks/:id
    - In-memory data storage (slice/map) for simplicity
    - CORS enabled for React frontend
    - Health check endpoint at /health
    - Structured logging
    - Graceful shutdown handling
    - Dockerfile for containerization

    FRONTEND (React):
    - Modern React application with functional components and hooks
    - Task management UI with create, read, update, delete operations
    - Clean, responsive design
    - API integration with the Go backend
    - Error handling and loading states
    - TypeScript for type safety
    - Dockerfile for containerization

    LOCAL DEVELOPMENT (Tilt):
    - Tiltfile configuration for local development
    - Hot reloading for both backend and frontend
    - Docker Compose setup for services
    - Automatic rebuilding on code changes
    - Port forwarding configuration
    - Development environment variables

    PROJECT STRUCTURE:
    - Organized monorepo structure
    - Separate directories for backend, frontend, and deployment configs
    - Documentation for setup and development
    - Makefile for common tasks

    DEPLOYMENT:
    - Kubernetes manifests for production deployment
    - Docker images optimized for production
    - Environment-specific configurations
    - Health checks and readiness probes

    The service should be production-ready but simple enough for local development and testing.
    """
    
    print("🚀 Generating Full-Stack Web Service")
    print("   📋 Go Backend + React Frontend + Tilt Development")
    print("=" * 70)
    
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
    
    print("⚡ Development Team Workflow:")
    print("   🎯 Project Manager (Planning & Architecture)")
    print("   💻 Software Engineer (Go Backend + React Frontend + Tilt)")
    print("   🧪 QA Engineer (Testing Strategy & Quality Assurance)")
    print("   📚 Tech Writer (Complete Documentation)")
    print("   📋 Final Review & Deliverables")
    print()
    
    # Execute the workflow
    try:
        print("🔄 Executing workflow... (This may take a few minutes)")
        result = graph.invoke(initial_state)
        
        print("\n✅ FULL-STACK WEB SERVICE GENERATED!")
        print("=" * 70)
        
        # Save deliverables to files
        save_deliverables_to_files(result)
        
        # Display summary
        display_project_summary(result)
        
        return result
        
    except Exception as e:
        print(f"❌ Error during generation: {str(e)}")
        print("💡 Make sure you have set your GROQ_API_KEY in the .env file")
        return None


def save_deliverables_to_files(result):
    """Save the generated deliverables to files for easy access."""
    
    output_dir = "generated_fullstack_service"
    os.makedirs(output_dir, exist_ok=True)
    
    deliverables = [
        ("01_project_plan.md", result["project_plan"]),
        ("02_code_implementation.md", result["code_implementation"]),
        ("03_qa_testing.md", result["test_results"]),
        ("04_documentation.md", result["documentation"]),
        ("05_final_deliverable.md", result["final_deliverable"])
    ]
    
    print(f"\n💾 Saving deliverables to ./{output_dir}/")
    
    for filename, content in deliverables:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   📄 {filename}")
    
    # Create a summary file with quick start instructions
    create_quick_start_guide(output_dir, result)


def create_quick_start_guide(output_dir, result):
    """Create a quick start guide for the generated project."""
    
    quick_start = f"""# Quick Start Guide - Full-Stack Web Service

## Generated Project Overview
- **Backend**: Go with Gin framework
- **Frontend**: React with TypeScript
- **Development**: Tilt for local development
- **Deployment**: Docker + Kubernetes

## Quick Start Commands

1. **Prerequisites**:
   ```bash
   # Install required tools
   - Go 1.19+
   - Node.js 18+
   - Docker & Docker Compose
   - Tilt (https://tilt.dev)
   ```

2. **Setup Project**:
   ```bash
   # Create project directory
   mkdir my-fullstack-service
   cd my-fullstack-service
   
   # Copy generated files (see code_implementation.md for file structure)
   # Extract files from the generated code implementation
   ```

3. **Local Development with Tilt**:
   ```bash
   # Start development environment
   tilt up
   
   # Access services:
   # - Frontend: http://localhost:3000
   # - Backend API: http://localhost:8080
   # - Tilt UI: http://localhost:10350
   ```

4. **Manual Development** (without Tilt):
   ```bash
   # Terminal 1 - Backend
   cd backend
   go mod tidy
   go run main.go
   
   # Terminal 2 - Frontend
   cd frontend
   npm install
   npm start
   ```

## Generated Files
- 📋 Project Plan: `01_project_plan.md`
- 💻 Complete Code: `02_code_implementation.md`
- 🧪 Testing Guide: `03_qa_testing.md`
- 📚 Documentation: `04_documentation.md`
- 📦 Final Package: `05_final_deliverable.md`

## Next Steps
1. Review the project plan and architecture
2. Extract code files from the implementation guide
3. Follow setup instructions in the documentation
4. Run tests as described in the QA guide
5. Use Tilt for seamless local development

Generated on: {os.path.basename(output_dir)}
"""
    
    quick_start_path = os.path.join(output_dir, "README_QUICK_START.md")
    with open(quick_start_path, 'w', encoding='utf-8') as f:
        f.write(quick_start)
    
    print(f"   📄 README_QUICK_START.md")


def display_project_summary(result):
    """Display a summary of the generated project."""
    
    print("\n📊 PROJECT SUMMARY")
    print("-" * 50)
    print("🎯 Project Plan:")
    print(f"   {len(result['project_plan'])} characters of detailed planning")
    
    print("\n💻 Code Implementation:")
    print(f"   {len(result['code_implementation'])} characters of code and config")
    print("   Includes: Go backend, React frontend, Tilt config, Docker files")
    
    print("\n🧪 QA & Testing:")
    print(f"   {len(result['test_results'])} characters of testing strategy")
    print("   Covers: Unit tests, integration tests, e2e tests")
    
    print("\n📚 Documentation:")
    print(f"   {len(result['documentation'])} characters of comprehensive docs")
    print("   Includes: Setup, API docs, user guides, troubleshooting")
    
    print("\n📋 Final Deliverable:")
    print(f"   {len(result['final_deliverable'])} characters of project summary")
    print("   Executive summary and deployment readiness assessment")
    
    print("\n🚀 READY TO DEPLOY!")
    print("   Check the generated_fullstack_service/ directory for all files")
    print("   Follow the README_QUICK_START.md for setup instructions")


def main():
    """Main function."""
    
    print("🌐 Full-Stack Web Service Generator")
    print("   Using AI Development Team: Go + React + Tilt")
    print("=" * 70)
    
    # Check if .env file exists
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    if not os.path.exists(env_file):
        print("⚠️  WARNING: .env file not found!")
        print("   Please copy .env.example to .env and add your GROQ_API_KEY")
        print("   Get your API key from: https://console.groq.com/keys")
        print()
        
        continue_anyway = input("Continue anyway? (y/N): ").lower().strip()
        if continue_anyway != 'y':
            print("👋 Setup your .env file and try again!")
            return
    
    try:
        result = generate_fullstack_service()
        
        if result:
            print("\n🎉 SUCCESS! Your full-stack web service has been generated!")
            print("\n💡 Next Steps:")
            print("   1. Check the generated_fullstack_service/ directory")
            print("   2. Follow the README_QUICK_START.md guide")
            print("   3. Extract code files and start development")
            print("   4. Use 'tilt up' for seamless local development")
        else:
            print("\n❌ Generation failed. Please check your configuration.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("💡 Make sure all dependencies are installed and .env is configured")


if __name__ == "__main__":
    main()
