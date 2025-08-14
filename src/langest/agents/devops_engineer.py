"""DevOps Engineer Agent with execution and debugging capabilities."""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
import subprocess
import json
from dotenv import load_dotenv

load_dotenv()


class DevOpsEngineerAgent:
    """DevOps Engineer AI Agent with execution capabilities."""
    
    def __init__(self, model: str = "llama3-8b-8192", temperature: float = 0.2):
        """Initialize the DevOps Engineer agent.
        
        Args:
            model: Groq model to use
            temperature: Temperature for response generation
        """
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.system_prompt = """You are a Senior DevOps Engineer with expertise in:
        1. Code execution and debugging
        2. Environment setup and configuration  
        3. CI/CD pipeline design and troubleshooting
        4. Infrastructure automation
        5. Monitoring and logging
        6. Container orchestration with Docker and Kubernetes
        7. Local development with Tilt
        8. Error diagnosis and resolution
        
        Your capabilities include:
        - Analyzing execution logs and error messages
        - Suggesting fixes for compilation and runtime errors
        - Automating deployment and setup processes
        - Creating debugging and monitoring solutions
        - Optimizing development workflows
        
        When providing solutions:
        - Give specific, actionable commands
        - Explain the reasoning behind each step
        - Consider different environments (development, staging, production)
        - Prioritize automation and repeatability
        - Include error handling and rollback strategies"""
    
    def execute_command(self, command: str, cwd: str = None) -> dict:
        """Execute a shell command and return results.
        
        Args:
            command: Command to execute
            cwd: Working directory for command execution
            
        Returns:
            Dictionary with stdout, stderr, return_code
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": "Command timed out after 30 seconds",
                "return_code": 124,
                "success": False
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "return_code": 1,
                "success": False
            }
    
    def debug_application(self, project_path: str, error_description: str) -> str:
        """Debug an application by analyzing errors and providing fixes.
        
        Args:
            project_path: Path to the project directory
            error_description: Description of the error encountered
            
        Returns:
            Debug analysis and fix recommendations
        """
        # First, gather information about the project
        project_info = self._analyze_project_structure(project_path)
        
        # Try to reproduce the error if possible
        execution_results = self._run_diagnostics(project_path)
        
        messages = [
            SystemMessage(content=self.system_prompt + """
            
            For debugging tasks:
            - Analyze the error message and context
            - Identify the root cause
            - Provide step-by-step fix instructions
            - Include prevention strategies
            - Test the solution if possible"""),
            HumanMessage(content=f"""
            Project Path: {project_path}
            Error Description: {error_description}
            
            Project Structure Analysis: {project_info}
            
            Diagnostic Results: {execution_results}
            
            Please provide:
            1. Root cause analysis
            2. Step-by-step fix instructions
            3. Commands to resolve the issue
            4. Prevention strategies for the future
            5. Testing recommendations to verify the fix
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def setup_development_environment(self, project_path: str, requirements: dict) -> str:
        """Set up a complete development environment.
        
        Args:
            project_path: Path to the project
            requirements: Dictionary with setup requirements
            
        Returns:
            Setup instructions and status
        """
        setup_results = []
        
        # Check prerequisites
        if requirements.get("go"):
            go_check = self.execute_command("go version")
            setup_results.append(f"Go check: {go_check}")
        
        if requirements.get("node"):
            node_check = self.execute_command("node --version")
            npm_check = self.execute_command("npm --version")
            setup_results.append(f"Node check: {node_check}")
            setup_results.append(f"NPM check: {npm_check}")
        
        if requirements.get("docker"):
            docker_check = self.execute_command("docker --version")
            setup_results.append(f"Docker check: {docker_check}")
        
        if requirements.get("tilt"):
            tilt_check = self.execute_command("tilt version")
            setup_results.append(f"Tilt check: {tilt_check}")
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""
            Project Path: {project_path}
            Requirements: {json.dumps(requirements, indent=2)}
            
            Current Environment Status:
            {chr(10).join(str(result) for result in setup_results)}
            
            Please provide:
            1. Complete setup instructions for the development environment
            2. Commands to install missing prerequisites
            3. Project-specific setup steps
            4. Verification commands to ensure everything works
            5. Common troubleshooting tips
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def create_deployment_pipeline(self, project_description: str, target_environment: str) -> str:
        """Create a CI/CD deployment pipeline.
        
        Args:
            project_description: Description of the project
            target_environment: Target deployment environment
            
        Returns:
            Deployment pipeline configuration and instructions
        """
        messages = [
            SystemMessage(content=self.system_prompt + """
            
            For deployment pipeline creation:
            - Design automated CI/CD workflows
            - Include testing, building, and deployment stages
            - Consider security and compliance requirements
            - Provide rollback strategies
            - Include monitoring and alerting"""),
            HumanMessage(content=f"""
            Project Description: {project_description}
            Target Environment: {target_environment}
            
            Please create a complete deployment pipeline including:
            1. CI/CD workflow configuration (GitHub Actions, GitLab CI, etc.)
            2. Build and test automation
            3. Containerization strategy
            4. Deployment scripts and configurations
            5. Monitoring and health checks
            6. Rollback procedures
            7. Security scanning and compliance checks
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def optimize_performance(self, project_path: str, performance_metrics: dict) -> str:
        """Analyze and optimize application performance.
        
        Args:
            project_path: Path to the project
            performance_metrics: Current performance metrics
            
        Returns:
            Performance optimization recommendations
        """
        # Analyze project for performance bottlenecks
        project_analysis = self._analyze_project_structure(project_path)
        
        messages = [
            SystemMessage(content=self.system_prompt + """
            
            For performance optimization:
            - Identify bottlenecks in code and infrastructure
            - Suggest specific optimizations
            - Consider scalability and resource efficiency
            - Provide monitoring strategies
            - Include load testing recommendations"""),
            HumanMessage(content=f"""
            Project Path: {project_path}
            Current Performance Metrics: {json.dumps(performance_metrics, indent=2)}
            
            Project Analysis: {project_analysis}
            
            Please provide:
            1. Performance bottleneck analysis
            2. Specific optimization recommendations
            3. Infrastructure improvements
            4. Code-level optimizations
            5. Monitoring and alerting setup
            6. Load testing strategy
            7. Scalability planning
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def _analyze_project_structure(self, project_path: str) -> dict:
        """Analyze the project structure and gather basic information."""
        analysis = {}
        
        # Get directory structure
        tree_result = self.execute_command(f"find {project_path} -type f -name '*.go' -o -name '*.js' -o -name '*.json' -o -name '*.yaml' -o -name '*.yml' -o -name 'Dockerfile' -o -name 'Makefile' | head -20")
        analysis["files"] = tree_result
        
        # Check for common config files
        config_files = ["package.json", "go.mod", "docker-compose.yml", "Dockerfile", "Makefile"]
        for config_file in config_files:
            file_check = self.execute_command(f"ls {project_path}/{config_file}", cwd=project_path)
            analysis[f"{config_file}_exists"] = file_check["success"]
        
        return analysis
    
    def _run_diagnostics(self, project_path: str) -> dict:
        """Run basic diagnostic commands on the project."""
        diagnostics = {}
        
        # Try to build/compile
        if os.path.exists(os.path.join(project_path, "backend", "go.mod")):
            go_build = self.execute_command("go build", cwd=os.path.join(project_path, "backend"))
            diagnostics["go_build"] = go_build
        
        if os.path.exists(os.path.join(project_path, "frontend", "package.json")):
            npm_check = self.execute_command("npm ls", cwd=os.path.join(project_path, "frontend"))
            diagnostics["npm_dependencies"] = npm_check
        
        return diagnostics
