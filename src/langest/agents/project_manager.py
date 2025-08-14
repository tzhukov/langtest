"""Project Manager Agent for the development team."""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()


class ProjectManagerAgent:
    """Project Manager AI Agent."""
    
    def __init__(self, model: str = "mixtral-8x7b-32768", temperature: float = 0.2):
        """Initialize the Project Manager agent.
        
        Args:
            model: Groq model to use
            temperature: Temperature for response generation
        """
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.system_prompt = """You are an experienced Project Manager with expertise in software development projects. Your responsibilities:
        1. Analyze and interpret project requirements thoroughly
        2. Create comprehensive project plans and timelines
        3. Define clear project scope, objectives, and success criteria
        4. Identify and assess project risks and dependencies
        5. Coordinate team activities and ensure quality deliverables
        6. Manage stakeholder expectations and communications
        7. Ensure projects are delivered on time, within budget, and to specification
        
        Project Management Expertise:
        - Requirements analysis and documentation
        - Work breakdown structure (WBS) creation
        - Resource allocation and timeline planning
        - Risk identification and mitigation strategies
        - Quality assurance and control processes
        - Stakeholder management and communication
        - Agile and traditional project methodologies
        
        Planning and Coordination:
        - Define project phases and milestones
        - Create detailed task breakdowns
        - Estimate effort and timeline requirements
        - Identify critical path and dependencies
        - Plan resource allocation and team coordination
        - Establish quality gates and review processes
        - Define success metrics and acceptance criteria
        
        Risk Management:
        - Identify technical, schedule, and resource risks
        - Assess probability and impact of risks
        - Develop mitigation and contingency plans
        - Monitor and control risk throughout project lifecycle
        - Communicate risks to stakeholders appropriately
        
        Always provide:
        - Clear project overview and objectives
        - Detailed task breakdown and timeline
        - Resource requirements and allocation
        - Risk assessment with mitigation strategies
        - Success criteria and quality metrics
        - Communication and reporting plans"""
    
    def create_project_plan(self, project_request: str) -> str:
        """Create a comprehensive project plan from requirements.
        
        Args:
            project_request: Original project requirements and objectives
            
        Returns:
            Detailed project plan with timeline, tasks, and risk assessment
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""
            Project Request: {project_request}
            
            Please create a comprehensive project plan including:
            1. Project Overview and Objectives
            2. Scope Definition (In-scope and Out-of-scope)
            3. Success Criteria and Acceptance Criteria
            4. Work Breakdown Structure (WBS)
            5. Timeline and Milestones
            6. Resource Requirements
            7. Risk Assessment and Mitigation Strategies
            8. Quality Assurance Plan
            9. Communication and Reporting Plan
            10. Dependencies and Assumptions
            11. Budget Considerations (if applicable)
            12. Next Steps and Action Items
            
            Ensure the plan is detailed enough to guide the development team through successful project completion.
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def review_deliverables(self, project_request: str, project_plan: str, 
                          code_implementation: str, test_results: str, 
                          documentation: str) -> str:
        """Conduct final review of all project deliverables.
        
        Args:
            project_request: Original project requirements
            project_plan: Original project plan
            code_implementation: Code deliverable from Software Engineer
            test_results: Testing results from QA Engineer
            documentation: Documentation from Technical Writer
            
        Returns:
            Final project review and deliverable package
        """
        messages = [
            SystemMessage(content=self.system_prompt + """
            
            For final project review:
            - Assess completeness against original requirements
            - Verify quality of all deliverables
            - Identify any gaps or missing elements
            - Evaluate overall project success
            - Provide recommendations for deployment
            - Create executive summary for stakeholders
            - Plan post-deployment activities"""),
            HumanMessage(content=f"""
            Original Project Request: {project_request}
            
            Project Plan: {project_plan}
            
            Code Implementation: {code_implementation}
            
            Test Results: {test_results}
            
            Documentation: {documentation}
            
            Please conduct a comprehensive final review including:
            1. Executive Summary
            2. Requirements Compliance Assessment
            3. Quality Evaluation of All Deliverables
            4. Gap Analysis and Outstanding Issues
            5. Project Success Metrics Evaluation
            6. Final Deliverable Package Organization
            7. Deployment Readiness Assessment
            8. Post-Deployment Recommendations
            9. Lessons Learned and Improvements
            10. Stakeholder Communication Summary
            11. Project Closure Activities
            12. Maintenance and Support Transition Plan
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def assess_project_risks(self, project_description: str, timeline: str, resources: str) -> str:
        """Assess and analyze project risks.
        
        Args:
            project_description: Description of the project
            timeline: Project timeline
            resources: Available resources
            
        Returns:
            Risk assessment with mitigation strategies
        """
        messages = [
            SystemMessage(content=self.system_prompt + """
            
            Focus on comprehensive risk assessment:
            - Technical risks and complexity
            - Schedule and timeline risks
            - Resource and skill availability risks
            - External dependency risks
            - Quality and performance risks
            - Budget and cost risks
            - Stakeholder and communication risks"""),
            HumanMessage(content=f"""
            Project Description: {project_description}
            
            Timeline: {timeline}
            
            Resources: {resources}
            
            Please provide a comprehensive risk assessment including:
            1. Risk Identification and Categorization
            2. Probability and Impact Analysis
            3. Risk Priority Matrix
            4. Mitigation Strategies for High-Priority Risks
            5. Contingency Plans
            6. Risk Monitoring and Control Processes
            7. Risk Communication Plan
            8. Early Warning Indicators
            9. Risk Response Strategies
            10. Overall Risk Profile Assessment
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def create_status_report(self, project_plan: str, current_progress: str, 
                           issues: str, next_steps: str) -> str:
        """Create project status report.
        
        Args:
            project_plan: Original project plan
            current_progress: Current project progress
            issues: Current issues and blockers
            next_steps: Planned next steps
            
        Returns:
            Formatted project status report
        """
        messages = [
            SystemMessage(content=self.system_prompt + """
            
            For status reporting:
            - Provide clear progress summary
            - Highlight key achievements and milestones
            - Identify issues and blockers with impact
            - Communicate risks and mitigation actions
            - Define clear next steps and timeline
            - Include metrics and KPIs
            - Format for stakeholder consumption"""),
            HumanMessage(content=f"""
            Project Plan: {project_plan}
            
            Current Progress: {current_progress}
            
            Issues: {issues}
            
            Next Steps: {next_steps}
            
            Please create a professional status report including:
            1. Executive Summary
            2. Project Health Dashboard
            3. Progress Against Plan
            4. Key Achievements This Period
            5. Current Issues and Blockers
            6. Risk Status Update
            7. Budget and Resource Status
            8. Upcoming Milestones
            9. Next Steps and Action Items
            10. Stakeholder Action Required
            11. Success Metrics and KPIs
            12. Overall Project Health Assessment
            """)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
