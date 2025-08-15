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
        5. Iteratively solve complex multi-step problems by learning from past failures
        6. Verify fixes by running tests and health checks
        7. Avoid repeating unsuccessful fixes for the same error
        
        Your debugging approach:
        - Analyze error messages carefully and identify root causes
        - Provide EXACT file contents and commands to fix issues
        - **If a fix fails, propose a DIFFERENT strategy. Do not repeat failed attempts.**
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
    
    def read_file(self, file_path: str, project_path: str) -> str:
        """Read the content of a file, ensuring it's within the project directory."""
        try:
            # Security: Ensure the file path is within the project directory
            abs_project_path = os.path.abspath(project_path)
            abs_file_path = os.path.abspath(file_path)
            
            if not abs_file_path.startswith(abs_project_path):
                return f"ERROR: Access to file {file_path} is restricted outside the project directory."

            with open(abs_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"📖 Read file: {file_path}")
            return content
        except FileNotFoundError:
            print(f"⚠️  File not found: {file_path}")
            return f"ERROR: File not found at {file_path}"
        except Exception as e:
            print(f"❌ Failed to read {file_path}: {str(e)}")
            return f"ERROR: Could not read file {file_path}. Reason: {str(e)}"

    def list_files(self, dir_path: str, project_path: str) -> str:
        """List files in a directory, ensuring it's within the project directory."""
        try:
            # Security: Ensure the directory path is within the project directory
            abs_project_path = os.path.abspath(project_path)
            abs_dir_path = os.path.abspath(dir_path)

            if not abs_dir_path.startswith(abs_project_path):
                return f"ERROR: Access to directory {dir_path} is restricted outside the project directory."
            
            if not os.path.isdir(abs_dir_path):
                return f"ERROR: Path is not a directory: {dir_path}"

            print(f"📂 Listing files in: {dir_path}")
            files = os.listdir(abs_dir_path)
            # Add a trailing slash to subdirectories for clarity
            listing = [f + '/' if os.path.isdir(os.path.join(abs_dir_path, f)) else f for f in files]
            return f"Contents of {dir_path}:\n- " + "\n- ".join(listing)
        except FileNotFoundError:
            return f"ERROR: Directory not found at {dir_path}"
        except Exception as e:
            return f"ERROR: Could not list files in {dir_path}. Reason: {str(e)}"

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

                **CRITICAL INSTRUCTIONS:**
                1.  **Analyze the PREVIOUS DEBUG HISTORY.** If previous attempts to fix this exact error have failed, you **MUST** propose a **NEW and DIFFERENT** solution.
                2.  **Do not repeat a fix that has already failed.** If updating a file didn't work, consider other causes. Is a configuration file missing? Is a dependency incorrect? Is an environment variable missing?
                3.  **Think step-by-step.** The error might be a symptom of a deeper problem. For example, a React test failing might not be the component's fault, but a missing test setup file (like `setupTests.js`).


                **YOUR TASK:**
                Analyze this error and provide an EXACT solution. If file contents or directory listings are provided in the 'ADDITIONAL CONTEXT', use them to inform your diagnosis. Your response must include:

                1. ROOT_CAUSE: Brief explanation of what's wrong
                2. SOLUTION_TYPE: One of [FILE_CREATE, FILE_UPDATE, COMMAND_RUN]
                3. FILES_TO_CREATE: A list of files to create, including their full relative path and exact content.
                4. FILES_TO_UPDATE: A list of files to update, including their full relative path and complete new content.
                5. COMMANDS_TO_RUN: A list of commands to execute to apply the fix. Note: The original failing command will be re-run automatically for verification. If a command like `npm` needs to run in a subdirectory, you must include the `cd` command (e.g., `cd frontend && npm install some-package`).

                **IMPORTANT**: Your response MUST be a single, valid JSON object. Do not include any text outside of the JSON.

                JSON Response Format:
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
                    "commands_to_run": ["cd frontend && npm install some-package"]
                }}
                """
            ))
        ]
        
        for attempt in range(2): # Allow one retry for JSON parsing
            try:
                response = self.llm.invoke(messages)
                
                # Try to extract JSON from the response
                response_text = response.content
                json_text = None

                # 1. Best case: Find a JSON markdown block
                json_markdown_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                if json_markdown_match:
                    json_text = json_markdown_match.group(1)
                else:
                    # 2. Fallback: Find the first '{' and last '}'
                    first_brace = response_text.find('{')
                    last_brace = response_text.rfind('}')
                    if first_brace != -1 and last_brace > first_brace:
                        json_text = response_text[first_brace:last_brace + 1]

                if json_text:
                    try:
                        solution = json.loads(json_text)
                        return solution
                    except json.JSONDecodeError as e:
                        print(f"⚠️  JSON decode failed on attempt {attempt + 1}: {e}")
                        if attempt == 0:
                            print("   Retrying with a stricter prompt...")
                            # Add a message to the history to guide the LLM
                            messages.append(response) # Add the bad response
                            messages.append(HumanMessage(content="Your last response was not valid JSON. Please correct it and provide ONLY the JSON object without any other text."))
                            continue # Go to the next attempt in the loop
                        else:
                            print(f"   Problematic JSON text (first 500 chars): {json_text[:500]}...")
                else:
                    print("⚠️  Could not find any JSON in the AI response.")

                # If we are here, parsing failed even after a retry
                return {
                    "root_cause": "Failed to parse AI response",
                    "solution_type": "MANUAL_ANALYSIS",
                    "raw_response": response_text
                }
                
            except Exception as e:
                print(f"❌ AI analysis failed with an unexpected error: {e}")

        # Fallback if all attempts fail
        return { "root_cause": "AI analysis failed after multiple attempts.", "solution_type": "ERROR" }
    
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
            
            # --- NEW: Use the read_file tool to gather more context ---
            context = f"This is debugging iteration {iteration + 1}/{self.max_iterations} for command: '{target_command}'"
            error_output = result.get("stderr", "") + result.get("stdout", "")
            
            files_to_read = set()

            # Find file paths mentioned in the error output
            mentioned_files = re.findall(r'[\./\w-]+\.(?:js|go|py|json|yaml|yml|toml|mod|sum|html|css|ts|tsx|jsx|test\.js)', error_output)
            files_to_read.update(mentioned_files)
            
            # Heuristic: If a startup command fails, read its log file for more context.
            log_file_match = re.search(r'>\s*([\w\./-]+\.log)', target_command)
            if log_file_match:
                log_file_name = log_file_match.group(1)
                log_file_path = ""
                if 'cd backend' in target_command:
                    log_file_path = os.path.join("backend", log_file_name)
                elif 'cd frontend' in target_command:
                    log_file_path = os.path.join("frontend", log_file_name)
                
                if log_file_path:
                    files_to_read.add(log_file_path)

            # Heuristic: Find directory paths mentioned in the error output
            # e.g., "directory 'path/to/dir'" or "'path/to/dir/'"
            mentioned_dirs_raw = re.findall(r"directory\s+'([^']+)'|'([\./\w-]+/)'", error_output)
            dirs_to_list = {item.strip() for tpl in mentioned_dirs_raw for item in tpl if item}

            if files_to_read:
                print(f"💡 Reading context from files: {list(files_to_read)}")
                file_contents_context = "\n\nRELEVANT FILE CONTENTS (truncated to 1000 chars):\n"
                for file in files_to_read:
                    full_file_path = os.path.join(project_path, file)
                    if os.path.exists(full_file_path):
                        content = self.read_file(full_file_path, project_path)
                        file_contents_context += f"--- START OF {file} ---\n{content[:1000]}\n--- END OF {file} ---\n\n"
                context += file_contents_context

            if dirs_to_list:
                print(f"💡 Found mentions of directories in logs: {list(dirs_to_list)}")
                dir_listings_context = "\n\nDIRECTORY LISTINGS:\n"
                for directory in dirs_to_list:
                    full_dir_path = os.path.join(project_path, directory)
                    if os.path.isdir(full_dir_path):
                        listing = self.list_files(full_dir_path, project_path)
                        dir_listings_context += f"--- START OF {directory} LISTING ---\n{listing}\n--- END OF {directory} LISTING ---\n\n"
                context += dir_listings_context

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
            
            # Give a moment for changes to take effect before retrying
            time.sleep(1)
            print(f"✅ Solution applied in iteration {iteration + 1}. Retrying target command...")
        
        # If we get here, we've exhausted all iterations
        print(f"\n❌ DEBUGGING FAILED after {self.max_iterations} iterations")
        print("🔍 Debug history:")
        for entry in self.debug_history:
            print(f"   Iteration {entry['iteration']}: {entry['solution'].get('root_cause', 'Unknown')}")
        
        return False
    
    def _cleanup_ports(self, ports: list[int], project_path: str):
        """Kill any processes using the specified ports to ensure a clean state."""
        print("\n🧹 Cleaning up ports...")
        for port in ports:
            # Use lsof which is generally available. Fallback to fuser.
            # These commands are designed to not require sudo and to fail silently.
            commands = [
                f"lsof -t -i:{port} | xargs kill -9 2>/dev/null || true",
                f"fuser -k {port}/tcp 2>/dev/null || true"
            ]
            for cmd in commands:
                # Use a shorter timeout for cleanup commands
                self.execute_command(cmd, cwd=project_path, timeout=10)
        time.sleep(1) # Give a moment for processes to terminate

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
            "backend_start": False,
            "frontend_start": False,
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

        # 5. Test backend startup
        print("\n5️⃣  TESTING BACKEND STARTUP")
        # Proactively clean up ports to avoid "address already in use" errors
        self._cleanup_ports([8080, 3000], project_path)
        print("-" * 30)

        # This command is designed to be more robust for background processes.
        # 1. `nohup ... &` ensures the process detaches and keeps running.
        # 2. Output is redirected to a log file for later inspection if needed.
        # 3. `sleep 5` gives the Go server ample time to start.
        # 4. `curl` checks if the server is healthy.
        backend_startup_command = (
            'bash -c "cd backend && nohup go run main.go > backend.log 2>&1 &" && '
            'sleep 5 && curl -f http://localhost:8080/health'
        )
        backend_test = self.debug_until_working(backend_startup_command, project_path)
        if backend_test:
            results["backend_start"] = True

        # 6. Test frontend startup
        print("\n6️⃣  TESTING FRONTEND STARTUP")
        print("-" * 30)
        # This command is for the frontend service.
        # `BROWSER=none` prevents opening a browser tab.
        # `sleep 15` gives React dev server time to compile and start.
        frontend_startup_command = (
            'bash -c "cd frontend && BROWSER=none nohup npm start > frontend.log 2>&1 &" && '
            'sleep 15 && curl -f http://localhost:3000'
        )
        frontend_test = self.debug_until_working(frontend_startup_command, project_path)
        if frontend_test:
            results["frontend_start"] = True

        # 7. Run tests
        print("\n7️⃣  RUNNING TESTS")
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
