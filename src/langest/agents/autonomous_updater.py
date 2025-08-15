"""Autonomous Code Updater Agent that implements new features based on requirements."""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
import subprocess
import time
import json
import re
from dotenv import load_dotenv

load_dotenv()


class AutonomousUpdaterAgent:
    """AI Agent that autonomously updates a codebase based on new requirements."""

    def __init__(self, model: str = "llama3-70b-8192", temperature: float = 0.2):
        """Initialize the autonomous updater agent."""
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.max_iterations = 5  # Max update attempts for a single run
        self.update_history = []

        self.system_prompt = """You are an Expert Autonomous Software Development Agent. Your goal is to update an existing codebase to implement new features based on a set of requirements.

        Your capabilities:
        1.  Analyze existing code to understand its structure and functionality.
        2.  Read requirement documents to understand new features.
        3.  Modify existing files with new code.
        4.  Create new files needed for the new features.
        5.  Run commands to install dependencies or run build steps.
        6.  Iteratively refine the code until it meets the requirements and all tests pass.

        Your process:
        -   First, carefully review the requirements and the existing code.
        -   Propose a set of changes (file creations, updates, and commands).
        -   Provide complete, working file contents. Do not use placeholders or partial code.
        -   After applying changes, the system will run tests to verify the implementation.
        -   If tests fail, analyze the error and propose a new set of changes to fix the issue.
        -   Do not suggest running test commands yourself; the system handles verification.
        """

    def execute_command(self, command: str, cwd: str = None, timeout: int = 60) -> dict:
        """Execute a command and return detailed results."""
        print(f"🔧 Executing: {command}")
        try:
            result = subprocess.run(
                command, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout
            )
            execution_result = {
                "command": command, "stdout": result.stdout, "stderr": result.stderr,
                "return_code": result.returncode, "success": result.returncode == 0, "cwd": cwd or os.getcwd()
            }
            if execution_result["success"]:
                print(f"✅ Command succeeded")
            else:
                print(f"❌ Command failed (exit code: {result.returncode})")
                if execution_result["stderr"]:
                    print(f"📤 Error: {execution_result['stderr'][:300]}...")
            return execution_result
        except Exception as e:
            return {"command": command, "stdout": "", "stderr": str(e), "return_code": 1, "success": False, "cwd": cwd or os.getcwd()}

    def write_file(self, file_path: str, content: str) -> bool:
        """Write content to a file, creating directories if needed."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📝 Wrote to: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to write {file_path}: {str(e)}")
            return False

    def read_file(self, file_path: str) -> str:
        """Read the content of a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"📖 Read file: {file_path}")
            return content
        except Exception as e:
            print(f"⚠️  Could not read file {file_path}: {e}")
            return f"ERROR: Could not read file {file_path}. Reason: {str(e)}"

    def get_project_context(self, project_path: str, files_to_read: list = None) -> str:
        """Get the project context by listing files and reading key files."""
        context = "Project file structure:\n"
        file_list = []
        for root, _, files in os.walk(project_path):
            for name in files:
                # Ignore some common noisy directories/files
                if '.git' in root or 'node_modules' in root or '.DS_Store' in name:
                    continue
                rel_path = os.path.relpath(os.path.join(root, name), project_path)
                file_list.append(rel_path)
        
        context += "\n".join(sorted(file_list))
        context += "\n\n"

        if files_to_read:
            context += "Contents of relevant files:\n"
            for file in files_to_read:
                full_path = os.path.join(project_path, file)
                if os.path.exists(full_path):
                    content = self.read_file(full_path)
                    context += f"--- START OF {file} ---\n{content}\n--- END OF {file} ---\n\n"
        return context

    def analyze_and_propose_changes(self, requirements: str, project_context: str, test_error: str = None) -> dict:
        """Analyze requirements and project context to propose changes."""
        history_short = self.update_history[-2:]
        
        prompt = f"""
        **REQUIREMENTS:**
        {requirements}

        **CURRENT PROJECT CONTEXT:**
        {project_context}

        **PREVIOUS UPDATE HISTORY (last 2 attempts):**
        {json.dumps(history_short, indent=2) if history_short else 'None'}
        """

        if test_error:
            prompt += f"""
            **VERIFICATION FAILED:**
            The last update was applied, but the tests failed with the following error. You must fix this.
            
            **Test Error:**
            {test_error}
            """

        prompt += """
        **YOUR TASK:**
        Based on the requirements and the current project state, provide a set of changes to implement the features.
        If the previous attempt failed, analyze the error and provide a fix.
        Your response must be a single, valid JSON object.

        JSON Response Format:
        {
            "plan": "A brief, step-by-step plan of the changes you are about to make.",
            "files_to_create": [
                {
                    "path": "relative/path/to/new_file.js",
                    "content": "exact file content here"
                }
            ],
            "files_to_update": [
                {
                    "path": "relative/path/to/existing_file.go",
                    "content": "complete updated file content"
                }
            ],
            "commands_to_run": ["cd frontend && npm install new-package"]
        }
        """

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]

        response = self.llm.invoke(messages)
        response_text = response.content
        
        try:
            # Simple JSON extraction
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                raise ValueError("No JSON object found in the response.")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"❌ Failed to parse AI response: {e}")
            return {"plan": "Failed to parse AI response.", "raw_response": response_text}

    def apply_changes(self, changes: dict, project_path: str) -> bool:
        """Apply the changes proposed by the AI."""
        print(f"\n💡 Plan: {changes.get('plan', 'No plan provided.')}")
        success = True
        for file_info in changes.get("files_to_create", []):
            path = os.path.join(project_path, file_info["path"])
            if not self.write_file(path, file_info["content"]):
                success = False
        for file_info in changes.get("files_to_update", []):
            path = os.path.join(project_path, file_info["path"])
            if not self.write_file(path, file_info["content"]):
                success = False
        for command in changes.get("commands_to_run", []):
            result = self.execute_command(command, cwd=project_path)
            if not result["success"]:
                print(f"⚠️  Command failed: {command}")
        return success

    def run_update(self, project_path: str, requirements_path: str, verification_command: str = "make test"):
        """Run the autonomous update process."""
        print("🚀 Starting autonomous code update session.")
        
        try:
            with open(requirements_path, 'r', encoding='utf-8') as f:
                requirements = f.read()
        except FileNotFoundError:
            print(f"❌ Requirements file not found at: {requirements_path}")
            return False

        print(f"🎯 Requirements loaded from: {requirements_path}")
        print(f"📁 Project path: {project_path}")
        print("=" * 70)

        test_error = None
        for i in range(self.max_iterations):
            print(f"\n🔄 UPDATE ITERATION {i + 1}/{self.max_iterations}")
            print("-" * 50)

            # Get project context - for now, let's not read all files to save tokens,
            # the agent can ask for them if needed.
            project_context = self.get_project_context(project_path)

            changes = self.analyze_and_propose_changes(requirements, project_context, test_error)
            
            self.update_history.append({
                "iteration": i + 1,
                "plan": changes.get("plan"),
                "changes": {k: v for k, v in changes.items() if k != 'plan'}
            })

            if not changes.get("files_to_create") and not changes.get("files_to_update") and not changes.get("commands_to_run"):
                print("⚠️ Agent proposed no changes. Ending session.")
                break

            if not self.apply_changes(changes, project_path):
                print("❌ Failed to apply changes. Aborting.")
                return False

            print("\n✅ Verifying changes with tests...")
            verification_result = self.execute_command(verification_command, cwd=project_path)

            if verification_result["success"]:
                print("\n🎉 SUCCESS! Update implemented and tests passed!")
                return True
            else:
                print("❌ Verification failed. The agent will try to fix it.")
                test_error = verification_result["stderr"] + "\n" + verification_result["stdout"]
                time.sleep(1)

        print(f"\n❌ UPDATE FAILED after {self.max_iterations} iterations.")
        return False