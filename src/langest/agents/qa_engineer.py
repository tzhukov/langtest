"""QA Engineer Agent for the development team."""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()


class QAEngineerAgent:
    """QA Engineer AI Agent."""
    
    def __init__(self, model: str = "gemma-7b-it", temperature: float = 0.1):
        """Initialize the QA Engineer agent.
        
        Args:
            model: Groq model to use
            temperature: Temperature for response generation
        """
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.system_prompt = """You are a Senior QA Engineer with expertise in software testing. Your responsibilities:
        1. Analyze requirements and code implementation thoroughly
        2. Create comprehensive test plans covering all scenarios
        3. Design functional, integration, and performance tests
        4. Identify edge cases, error conditions, and security vulnerabilities
        5. Validate that implementation meets all requirements
        6. Perform risk assessment and quality evaluation
        7. Recommend testing strategies and automation approaches
        
        Test Planning Expertise:
        - Unit testing strategies
        - Integration testing approaches
        - End-to-end testing scenarios
        - Performance and load testing
        - Security testing methodologies
        - Accessibility testing
        - Cross-platform compatibility testing
        
        Quality Assurance Focus:
        - Requirements traceability
        - Test case design and optimization
        - Bug identification and classification
        - Risk-based testing approach
        - Test automation recommendations
        - Quality metrics and reporting
        
        Always provide:
        - Comprehensive test plan with detailed test cases
        - Risk assessment and mitigation strategies
        - Quality evaluation of the implementation
        - Bug reports with severity classifications
        - Recommendations for improvements and fixes
        - Test automation suggestions"""
    
    def create_test_plan(self, project_request: str, project_plan: str, code_implementation: str) -> str:
        """Create a comprehensive test plan.
        
        Args:
            project_request: Original project requirements
            project_plan: Project plan from Project Manager
            code_implementation: Code from Software Engineer
            
        Returns:
            Detailed test plan with test cases and quality assessment
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""
            Project Request: {project_request}
            
            Project Plan: {project_plan}
            
            Code Implementation: {code_implementation}
            
            Please create a comprehensive test plan including:
            1. Test strategy and approach
            2. Detailed functional test cases
            3. Integration test scenarios
            4. Edge cases and error conditions
            5. Performance testing considerations
            6. Security testing requirements
            7. Test data requirements
            8. Expected results for each test case
            9. Risk assessment and mitigation
            10. Quality evaluation of the code
            11. Bug reports and recommendations
            12. Test automation suggestions
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def execute_test_analysis(self, test_plan: str, code: str) -> str:
        """Analyze code execution against test plan.
        
        Args:
            test_plan: Test plan to execute
            code: Code to analyze
            
        Returns:
            Test execution results and analysis
        """
        messages = [
            SystemMessage(content=self.system_prompt + """
            
            For test execution analysis:
            - Simulate test case execution mentally
            - Identify potential failures and issues
            - Assess code coverage and completeness
            - Evaluate error handling effectiveness
            - Check for security vulnerabilities
            - Validate performance characteristics"""),
            HumanMessage(content=f"""
            Test Plan: {test_plan}
            
            Code to Analyze: {code}
            
            Please provide test execution analysis including:
            1. Test case execution results (simulated)
            2. Issues and bugs identified
            3. Code coverage assessment
            4. Security vulnerability analysis
            5. Performance bottlenecks identified
            6. Error handling evaluation
            7. Overall quality score and recommendations
            8. Priority ranking of issues found
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def quality_assessment(self, requirements: str, implementation: str) -> str:
        """Perform overall quality assessment.
        
        Args:
            requirements: Original requirements
            implementation: Implementation to assess
            
        Returns:
            Quality assessment report
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""
            Requirements: {requirements}
            
            Implementation: {implementation}
            
            Please provide a comprehensive quality assessment including:
            1. Requirements compliance analysis
            2. Code quality evaluation
            3. Security assessment
            4. Performance evaluation
            5. Maintainability assessment
            6. Scalability considerations
            7. Overall quality rating (1-10 scale)
            8. Critical issues that must be fixed
            9. Recommendations for improvement
            10. Go/No-go recommendation for release
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
