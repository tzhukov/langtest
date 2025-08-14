"""Technical Writer Agent for the development team."""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()


class TechWriterAgent:
    """Technical Writer AI Agent."""
    
    def __init__(self, model: str = "mixtral-8x7b-32768", temperature: float = 0.4):
        """Initialize the Technical Writer agent.
        
        Args:
            model: Groq model to use
            temperature: Temperature for response generation
        """
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.system_prompt = """You are an experienced Technical Writer specializing in software documentation. Your responsibilities:
        1. Create clear, comprehensive, and user-friendly documentation
        2. Translate technical information into accessible language
        3. Structure information logically for different audiences
        4. Ensure documentation completeness and accuracy
        5. Design documentation for easy maintenance and updates
        6. Include practical examples and tutorials
        7. Create troubleshooting guides and FAQs
        
        Documentation Expertise:
        - User guides and manuals
        - API documentation and references
        - Installation and setup guides
        - Developer documentation
        - Troubleshooting and FAQ sections
        - Code examples and tutorials
        - Architecture and design documentation
        
        Writing Standards:
        - Clear, concise, and jargon-free language
        - Logical information hierarchy
        - Consistent formatting and style
        - Appropriate use of visuals and diagrams
        - Comprehensive cross-referencing
        - Version control and update processes
        - Accessibility compliance
        
        Target Audiences:
        - End users (varying technical levels)
        - Developers and technical staff
        - System administrators
        - Project stakeholders
        - Support teams
        
        Always provide:
        - Complete user documentation
        - Technical/developer documentation
        - Installation and configuration guides
        - Code examples with explanations
        - Troubleshooting guides
        - FAQ sections
        - Glossary of terms when needed"""
    
    def create_documentation(self, project_request: str, project_plan: str, 
                           code_implementation: str, test_results: str) -> str:
        """Create comprehensive project documentation.
        
        Args:
            project_request: Original project requirements
            project_plan: Project plan from Project Manager
            code_implementation: Code from Software Engineer
            test_results: Test results from QA Engineer
            
        Returns:
            Complete documentation package
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""
            Project Request: {project_request}
            
            Project Plan: {project_plan}
            
            Code Implementation: {code_implementation}
            
            Test Results: {test_results}
            
            Please create comprehensive documentation including:
            1. Executive Summary and Overview
            2. User Guide with step-by-step instructions
            3. Installation and Setup Guide
            4. Configuration and Customization
            5. API Documentation (if applicable)
            6. Code Examples and Tutorials
            7. Troubleshooting Guide
            8. FAQ Section
            9. Technical Architecture Overview
            10. Developer Guide (for maintenance)
            11. Glossary of Terms
            12. Version History and Updates
            
            Structure the documentation for easy navigation and ensure it serves both technical and non-technical audiences.
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def create_user_guide(self, project_description: str, features: str, usage_examples: str) -> str:
        """Create focused user guide documentation.
        
        Args:
            project_description: Description of the project
            features: List of features
            usage_examples: Usage examples
            
        Returns:
            User guide documentation
        """
        messages = [
            SystemMessage(content=self.system_prompt + """
            
            Focus on creating user-centric documentation that:
            - Uses simple, clear language
            - Provides step-by-step instructions
            - Includes practical examples
            - Anticipates user questions
            - Offers multiple ways to accomplish tasks"""),
            HumanMessage(content=f"""
            Project Description: {project_description}
            
            Features: {features}
            
            Usage Examples: {usage_examples}
            
            Please create a comprehensive user guide including:
            1. Getting Started section
            2. Feature overview with benefits
            3. Step-by-step tutorials
            4. Common use cases and examples
            5. Tips and best practices
            6. Common issues and solutions
            7. Where to get help
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def create_api_documentation(self, code: str, api_details: str) -> str:
        """Create API documentation from code and details.
        
        Args:
            code: Source code containing API
            api_details: Additional API details
            
        Returns:
            API documentation
        """
        messages = [
            SystemMessage(content=self.system_prompt + """
            
            For API documentation, focus on:
            - Clear endpoint descriptions
            - Request/response examples
            - Parameter specifications
            - Error codes and handling
            - Authentication requirements
            - Rate limiting information
            - SDK/library usage examples"""),
            HumanMessage(content=f"""
            Source Code: {code}
            
            API Details: {api_details}
            
            Please create comprehensive API documentation including:
            1. API Overview and Purpose
            2. Authentication and Authorization
            3. Endpoint Reference
            4. Request/Response Formats
            5. Error Codes and Messages
            6. Code Examples in Multiple Languages
            7. SDK Usage Examples
            8. Rate Limiting and Best Practices
            9. Changelog and Versioning
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def review_documentation(self, documentation: str, requirements: str) -> str:
        """Review and improve existing documentation.
        
        Args:
            documentation: Documentation to review
            requirements: Original requirements to check against
            
        Returns:
            Documentation review with improvement suggestions
        """
        messages = [
            SystemMessage(content=self.system_prompt + """
            
            When reviewing documentation:
            - Check for completeness against requirements
            - Verify clarity and readability
            - Ensure logical organization
            - Identify missing information
            - Suggest improvements for user experience
            - Check for consistency in style and tone"""),
            HumanMessage(content=f"""
            Requirements: {requirements}
            
            Documentation to Review: {documentation}
            
            Please provide a documentation review including:
            1. Completeness assessment
            2. Clarity and readability evaluation
            3. Organization and structure feedback
            4. Missing information identification
            5. Suggestions for improvement
            6. Consistency check results
            7. Overall quality rating
            8. Priority recommendations for updates
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
