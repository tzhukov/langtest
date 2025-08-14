"""
LangServ Autonomous Debug Agent for generated_fullstack_service
"""

from langest.agents.autonomous_debugger import AutonomousDebuggingAgent
import os

class GeneratedFullstackDebugAgent:
    """
    Autonomous agent for debugging the generated_fullstack_service project using LangServ.
    """
    def __init__(self, project_path=None):
        if project_path is None:
            project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../generated_fullstack_service'))
        self.project_path = project_path
        self.agent = AutonomousDebuggingAgent()

    def debug(self):
        """
        Run comprehensive autonomous debugging for the generated_fullstack_service project.
        """
        return self.agent.run_comprehensive_debug(self.project_path)

if __name__ == "__main__":
    agent = GeneratedFullstackDebugAgent()
    results = agent.debug()
    print("\nFinal Debug Results:", results)
