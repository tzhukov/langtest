"""Software Engineer Agent for the development team."""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()


class SoftwareEngineerAgent:
    """Software Engineer AI Agent."""
    
    def __init__(self, model: str = "llama2-70b-4096", temperature: float = 0.3):
        """Initialize the Software Engineer agent.
        
        Args:
            model: Groq model to use
            temperature: Temperature for response generation
        """
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.system_prompt = """You are a Senior Software Engineer. Your responsibilities:
        1. Review project requirements and plan thoroughly
        2. Design robust software architecture and implementation strategy
        3. Write clean, efficient, and maintainable code
        4. Follow industry best practices and coding standards
        5. Consider scalability, security, and performance implications
        6. Provide clear code comments and documentation
        7. Structure code for easy testing and maintenance
        
        When implementing solutions:
        - Use appropriate design patterns
        - Implement error handling and input validation
        - Consider edge cases and potential failures
        - Write modular, reusable code
        - Include comprehensive logging
        - Follow SOLID principles
        
        Always provide:
        - Architecture overview and design decisions
        - Complete, working code implementation
        - Setup and installation instructions
        - Key technical decisions explained
        - Performance and security considerations"""
    
    def process_request(self, project_request: str, project_plan: str) -> str:
        """Process the software engineering request.
        
        Args:
            project_request: Original project requirements
            project_plan: Project plan from Project Manager
            
        Returns:
            Code implementation and technical documentation
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""
            Project Request: {project_request}
            
            Project Plan: {project_plan}
            
            Please provide a complete software implementation including:
            1. Architecture design and rationale
            2. Full code implementation with proper structure
            3. Error handling and input validation
            4. Installation and setup instructions
            5. Key technical decisions explained
            6. Performance and security considerations
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def review_code(self, code: str, requirements: str) -> str:
        """Review existing code against requirements.
        
        Args:
            code: Code to review
            requirements: Original requirements
            
        Returns:
            Code review with suggestions
        """
        messages = [
            SystemMessage(content=self.system_prompt + """
            
            Additionally, when reviewing code:
            - Check for bugs and potential issues
            - Verify alignment with requirements
            - Suggest improvements for readability and performance
            - Identify security vulnerabilities
            - Recommend refactoring opportunities"""),
            HumanMessage(content=f"""
            Requirements: {requirements}
            
            Code to Review:
            {code}
            
            Please provide a comprehensive code review including:
            1. Overall code quality assessment
            2. Bugs or issues identified
            3. Security considerations
            4. Performance optimization suggestions
            5. Code structure and maintainability feedback
            6. Specific improvement recommendations
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
