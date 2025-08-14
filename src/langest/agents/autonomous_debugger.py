"""Autonomous Debugging Agent that fixes issues until application works."""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
import subprocess
import time
import json
import re
from dotenv import load_dotenv

load_dotenv()


class AutonomousDebuggingAgent:
    """AI Agent that autonomously debugs and fixes issues until application works."""
    
    def __init__(self, model: str = "llama3-70b-8192", temperature: float = 0.1):
        """Initialize the autonomous debugging agent.
        
        Args:
            model: Groq model to use (using larger model for complex debugging)
            temperature: Low temperature for precise debugging
        """
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.max_iterations = 10  # Maximum debugging attempts
        self.debug_history = []   # Track all debugging attempts
        
        self.system_prompt = """You are an Expert Autonomous Debugging Agent with the ability to:
        1. Execute commands and analyze their output
        2. Identify root causes of errors from logs and output
        3. Generate precise fixes for configuration, code, and deployment issues
        4. Create missing files, configurations, and dependencies
        5. Iteratively solve complex multi-step problems
        6. Verify fixes by running tests and health checks
        
        Your debugging approach:
        - Analyze error messages carefully and identify root causes
        - Provide EXACT file contents and commands to fix issues
        - Test fixes immediately to ensure they work
        - Handle dependencies, missing files, configuration errors
        - Always verify the solution works before moving to next issue
        
        When providing fixes:
        - Give complete, working file contents (not partial)
        - Include all necessary imports, configurations, and dependencies
        - Provide exact commands to execute
        - Explain the reasoning behind each fix
        - Prioritize the most critical issues first
        
        You can fix:
        - Tiltfile syntax and configuration errors
        - Docker build issues and Dockerfile problems
        - Kubernetes manifest errors
        - Missing dependencies and package issues
        - Port conflicts and networking problems
        - File permission and path issues
        - Environment variable and configuration problems"""
    
    def execute_command(self, command: str, cwd: str = None, timeout: int = 60) -> dict:
        """Execute a command and return detailed results."""
        print(f"🔧 Executing: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            execution_result = {
                "command": command,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "success": result.returncode == 0,
                "cwd": cwd or os.getcwd()
            }
            
            # Print results for visibility
            if execution_result["success"]:
                print(f"✅ Command succeeded")
                if execution_result["stdout"]:
                    print(f"📤 Output: {execution_result['stdout'][:200]}...")
            else:
                print(f"❌ Command failed (exit code: {result.returncode})")
                if execution_result["stderr"]:
                    print(f"📤 Error: {execution_result['stderr'][:300]}...")
                    
            return execution_result
            
        except subprocess.TimeoutExpired:
            return {
                "command": command,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "return_code": 124,
                "success": False,
                "cwd": cwd or os.getcwd()
            }
        except Exception as e:
            return {
                "command": command,
                "stdout": "",
                "stderr": str(e),
                "return_code": 1,
                "success": False,
                "cwd": cwd or os.getcwd()
            }
    
    def write_file(self, file_path: str, content: str) -> bool:
        """Write content to a file, creating directories if needed."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"📝 Created/Updated: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to write {file_path}: {str(e)}")
            return False
    
    def analyze_and_fix_issue(self, command: str, execution_result: dict, context: str = "") -> dict:
        """Analyze an issue and generate a fix using AI, truncating context to avoid token limit errors."""
        # Truncate debug history to last 2 entries
        debug_history_short = self.debug_history[-2:] if self.debug_history else []
        # Truncate stdout/stderr to first 1000 characters (preserve start of error/log)
        stdout_short = execution_result.get('stdout', 'No output')[:1000]
        stderr_short = execution_result.get('stderr', 'No errors')[:1000]
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=(
                f"""
                DEBUGGING CONTEXT:
                Command executed: {command}
                Working directory: {execution_result.get('cwd', 'unknown')}
                Exit code: {execution_result.get('return_code', 'unknown')}

                STDOUT (truncated):
                {stdout_short}

                STDERR (truncated):
                {stderr_short}

                ADDITIONAL CONTEXT:
                {context}

                PREVIOUS DEBUG HISTORY (last 2):
                {json.dumps(debug_history_short, indent=2) if debug_history_short else 'None'}

                TASK:
                Analyze this error and provide an EXACT solution. Your response must include:

                1. ROOT_CAUSE: Brief explanation of what's wrong
                2. SOLUTION_TYPE: One of [FILE_CREATE, FILE_UPDATE, COMMAND_RUN, DEPENDENCY_INSTALL, CONFIG_FIX]
                3. FILES_TO_CREATE: List of files to create with exact content
                4. FILES_TO_UPDATE: List of files to update with exact content
                5. COMMANDS_TO_RUN: List of commands to execute
                6. VERIFICATION_COMMAND: Command to verify the fix worked

                Format your response as JSON:
                {{
                    "root_cause": "explanation",
                    "solution_type": "type",
                    "files_to_create": [
                        {{
                            "path": "relative/path/to/file",
                            "content": "exact file content here"
                        }}
                    ],
                    "files_to_update": [
                        {{
                            "path": "relative/path/to/file",
                            "content": "complete updated file content"
                        }}
                    ],
                    "commands_to_run": ["command1", "command2"],
                    "verification_command": "command to test fix"
                }}
                """
            ))
        ]
        
        try:
            response = self.llm.invoke(messages)
            
            # Try to extract JSON from the response
            response_text = response.content
            
            # Find JSON in the response (handle cases where LLM adds explanation)
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(0)
                try:
                    solution = json.loads(json_text)
                    return solution
                except json.JSONDecodeError:
                    pass
            
            # If JSON parsing fails, create a basic solution from the text
            return {
                "root_cause": "Failed to parse AI response",
                "solution_type": "MANUAL_ANALYSIS",
                "files_to_create": [],
                "files_to_update": [],
                "commands_to_run": [],
                "verification_command": command,
                "raw_response": response_text
            }
            
        except Exception as e:
            return {
                "root_cause": f"AI analysis failed: {str(e)}",
                "solution_type": "ERROR",
                "files_to_create": [],
                "files_to_update": [],
                "commands_to_run": [],
                "verification_command": command
            }
    
    def apply_solution(self, solution: dict, project_path: str) -> bool:
        """Apply the solution generated by AI."""
        
        print(f"\n🔧 Applying solution: {solution.get('solution_type', 'Unknown')}")
        print(f"💡 Root cause: {solution.get('root_cause', 'Unknown')}")
        
        success = True
        
        # Create new files
        for file_info in solution.get("files_to_create", []):
            file_path = os.path.join(project_path, file_info["path"])
            if not self.write_file(file_path, file_info["content"]):
                success = False
        
        # Update existing files
        for file_info in solution.get("files_to_update", []):
            file_path = os.path.join(project_path, file_info["path"])
            if not self.write_file(file_path, file_info["content"]):
                success = False
        
        # Run commands
        for command in solution.get("commands_to_run", []):
            result = self.execute_command(command, cwd=project_path)
            if not result["success"]:
                print(f"⚠️  Command failed: {command}")
                # Don't fail completely on command errors - some may be non-critical
        
        return success
    
    def verify_solution(self, solution: dict, project_path: str) -> bool:
        """Verify that the solution worked."""
        
        verification_cmd = solution.get("verification_command")
        if not verification_cmd:
            return True  # No verification needed
        
        print(f"\n✅ Verifying solution with: {verification_cmd}")
        result = self.execute_command(verification_cmd, cwd=project_path)
        
        return result["success"]
    
    def debug_until_working(self, target_command: str, project_path: str = None) -> bool:
        """Autonomously debug until the target command works."""
        
        if not project_path:
            project_path = os.getcwd()
        
        print(f"🚀 Starting autonomous debugging session")
        print(f"🎯 Target command: {target_command}")
        print(f"📁 Project path: {project_path}")
        print(f"🔄 Max iterations: {self.max_iterations}")
        print("=" * 70)
        
        for iteration in range(self.max_iterations):
            print(f"\n🔄 ITERATION {iteration + 1}/{self.max_iterations}")
            print("-" * 50)
            
            # Execute target command
            result = self.execute_command(target_command, cwd=project_path)
            
            # If successful, we're done!
            if result["success"]:
                print(f"\n🎉 SUCCESS! Command '{target_command}' completed successfully!")
                print("✅ Application debugging completed")
                return True
            
            # Analyze the error and get a solution
            print(f"\n🔍 Analyzing error (iteration {iteration + 1})...")
            
            context = f"This is debugging iteration {iteration + 1}/{self.max_iterations} for command: {target_command}"
            solution = self.analyze_and_fix_issue(target_command, result, context)
            
            # Store debug history
            self.debug_history.append({
                "iteration": iteration + 1,
                "command": target_command,
                "error": result.get("stderr", "Unknown error"),
                "solution": solution
            })
            
            # Apply the solution
            if not self.apply_solution(solution, project_path):
                print(f"❌ Failed to apply solution in iteration {iteration + 1}")
                continue
            
            # Give a moment for changes to take effect
            time.sleep(1)
            
            # Verify the solution
            if solution.get("verification_command"):
                if not self.verify_solution(solution, project_path):
                    print(f"⚠️  Solution verification failed, continuing to next iteration")
                    continue
            
            print(f"✅ Solution applied successfully in iteration {iteration + 1}")
        
        # If we get here, we've exhausted all iterations
        print(f"\n❌ DEBUGGING FAILED after {self.max_iterations} iterations")
        print("🔍 Debug history:")
        for entry in self.debug_history:
            print(f"   Iteration {entry['iteration']}: {entry['solution'].get('root_cause', 'Unknown')}")
        
        return False
    
    def run_comprehensive_debug(self, project_path: str = None) -> dict:
        """Run comprehensive debugging for a full-stack application."""
        # Always use top-level generated_fullstack_service for all operations
        if not project_path:
            project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../generated_fullstack_service'))

        print("🎯 COMPREHENSIVE APPLICATION DEBUGGING")
        print("=" * 70)

        results = {
            "backend_build": False,
            "frontend_build": False, 
            "dependencies": False,
            "tilt_setup": False,
            "application_start": False,
            "tests": False
        }

        # 1. Check and fix dependencies
        print("\n1️⃣  CHECKING DEPENDENCIES")
        print("-" * 30)
        backend_path = os.path.join(project_path, "backend")
        frontend_path = os.path.join(project_path, "frontend")
        backend_deps = self.debug_until_working("go mod tidy", backend_path)
        frontend_deps = self.debug_until_working("npm install", frontend_path)
        if backend_deps and frontend_deps:
            results["dependencies"] = True

        # 2. Fix backend build
        print("\n2️⃣  DEBUGGING BACKEND BUILD")
        print("-" * 30)
        if self.debug_until_working("cd backend && go build", project_path):
            results["backend_build"] = True

        # 3. Fix frontend build
        print("\n3️⃣  DEBUGGING FRONTEND BUILD")
        print("-" * 30)
        if self.debug_until_working("cd frontend && npm run build", project_path):
            results["frontend_build"] = True

        # 4. Fix Tilt configuration
        print("\n4️⃣  DEBUGGING TILT SETUP")
        print("-" * 30)
        if self.debug_until_working("tilt doctor", project_path):
            results["tilt_setup"] = True

        # 5. Test application startup
        print("\n5️⃣  TESTING APPLICATION STARTUP")
        print("-" * 30)
        backend_test = self.debug_until_working("timeout 10s bash -c 'cd backend && go run main.go &' && sleep 2 && curl -f http://localhost:8080/health", project_path)
        if backend_test:
            results["application_start"] = True

        # 6. Run tests
        print("\n6️⃣  RUNNING TESTS")
        print("-" * 30)
        if self.debug_until_working("make test", project_path):
            results["tests"] = True

        # Summary
        print("\n📊 DEBUGGING SUMMARY")
        print("=" * 50)
        for component, status in results.items():
            status_icon = "✅" if status else "❌"
            print(f"{status_icon} {component.replace('_', ' ').title()}")
        total_success = sum(results.values())
        total_components = len(results)
        print(f"\n🎯 Overall Success: {total_success}/{total_components} components working")
        return results
