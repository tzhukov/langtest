"""Development team graph with 4 AI agents: Software Engineer, QA Engineer, Tech Writer, and Project Manager."""

from typing import TypedDict, Annotated, Literal
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DevTeamState(TypedDict):
    """State for the development team workflow."""
    messages: Annotated[list, operator.add]
    project_request: str
    project_plan: str
    code_implementation: str
    test_plan: str
    test_results: str
    documentation: str
    final_deliverable: str
    current_agent: str
    next_step: Literal["project_manager", "software_engineer", "qa_engineer", "tech_writer", "review", "end"]


def project_manager_node(state: DevTeamState) -> DevTeamState:
    """Project Manager agent - Plans and coordinates the project."""
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.2,
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    messages = [
        SystemMessage(content="""You are an experienced Project Manager. Your responsibilities:
        1. Analyze project requirements thoroughly
        2. Break down the project into clear, actionable tasks
        3. Define project scope, timeline, and deliverables
        4. Identify potential risks and dependencies
        5. Create a structured project plan
        6. Coordinate between team members
        
        Provide a comprehensive project plan with:
        - Project overview and objectives
        - Task breakdown
        - Success criteria
        - Timeline estimates
        - Risk assessment"""),
        HumanMessage(content=f"Project Request: {state['project_request']}")
    ]
    
    response = llm.invoke(messages)
    
    return {
        **state,
        "project_plan": response.content,
        "messages": [response],
        "current_agent": "Project Manager",
        "next_step": "software_engineer"
    }


def software_engineer_node(state: DevTeamState) -> DevTeamState:
    """Software Engineer agent - Implements the code solution."""
    llm = ChatGroq(
        model="llama3-70b-8192",
        temperature=0.3,
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    messages = [
        SystemMessage(content="""You are a Senior Software Engineer. Your responsibilities:
        1. Review project requirements and plan
        2. Design software architecture and implementation strategy
        3. Write clean, efficient, and maintainable code
        4. Follow best practices and coding standards
        5. Consider scalability, security, and performance
        6. Provide clear code comments and structure
        
        Deliver:
        - Architecture overview
        - Complete code implementation
        - Code comments explaining key decisions
        - Setup/installation instructions"""),
        HumanMessage(content=f"""
        Project Request: {state['project_request']}
        Project Plan: {state['project_plan']}
        
        Please implement the software solution based on the requirements and plan.
        """)
    ]
    
    response = llm.invoke(messages)
    
    return {
        **state,
        "code_implementation": response.content,
        "messages": state["messages"] + [response],
        "current_agent": "Software Engineer",
        "next_step": "qa_engineer"
    }


def qa_engineer_node(state: DevTeamState) -> DevTeamState:
    """QA Engineer agent - Creates test plans and validates the implementation."""
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.1,
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    messages = [
        SystemMessage(content="""You are a Senior QA Engineer. Your responsibilities:
        1. Review project requirements and code implementation
        2. Create comprehensive test plans and test cases
        3. Identify potential bugs, edge cases, and security issues
        4. Design both functional and non-functional tests
        5. Validate that implementation meets requirements
        6. Recommend improvements and fixes
        
        Deliver:
        - Detailed test plan with test cases
        - Test execution results/analysis
        - Bug reports and recommendations
        - Quality assessment of the implementation"""),
        HumanMessage(content=f"""
        Project Request: {state['project_request']}
        Project Plan: {state['project_plan']}
        Code Implementation: {state['code_implementation']}
        
        Please create a comprehensive test plan and analyze the code quality.
        """)
    ]
    
    response = llm.invoke(messages)
    
    return {
        **state,
        "test_plan": response.content,
        "test_results": response.content,
        "messages": state["messages"] + [response],
        "current_agent": "QA Engineer",
        "next_step": "tech_writer"
    }


def tech_writer_node(state: DevTeamState) -> DevTeamState:
    """Tech Writer agent - Creates comprehensive documentation."""
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.4,
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    messages = [
        SystemMessage(content="""You are an experienced Technical Writer. Your responsibilities:
        1. Review all project deliverables and create user-friendly documentation
        2. Write clear, concise, and comprehensive documentation
        3. Create user guides, API documentation, and developer guides
        4. Ensure documentation is accessible to different audience levels
        5. Include examples, tutorials, and troubleshooting guides
        6. Structure information logically with proper formatting
        
        Deliver:
        - User documentation and guides
        - Technical/API documentation
        - Installation and setup instructions
        - Examples and tutorials
        - FAQ and troubleshooting section"""),
        HumanMessage(content=f"""
        Project Request: {state['project_request']}
        Project Plan: {state['project_plan']}
        Code Implementation: {state['code_implementation']}
        Test Plan & Results: {state['test_plan']}
        
        Please create comprehensive documentation for this project.
        """)
    ]
    
    response = llm.invoke(messages)
    
    return {
        **state,
        "documentation": response.content,
        "messages": state["messages"] + [response],
        "current_agent": "Tech Writer",
        "next_step": "review"
    }


def review_and_finalize_node(state: DevTeamState) -> DevTeamState:
    """Final review node - Project Manager reviews all deliverables."""
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.1,
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    messages = [
        SystemMessage(content="""You are the Project Manager conducting a final review. Your tasks:
        1. Review all team deliverables for completeness and quality
        2. Ensure the solution meets original requirements
        3. Identify any gaps or missing elements
        4. Create a final project summary and deliverable package
        5. Provide next steps and recommendations
        
        Create a comprehensive final deliverable that includes:
        - Executive summary
        - All key deliverables organized clearly
        - Quality assessment
        - Recommendations for deployment/next steps"""),
        HumanMessage(content=f"""
        Original Request: {state['project_request']}
        
        Team Deliverables:
        - Project Plan: {state['project_plan']}
        - Code Implementation: {state['code_implementation']}
        - Test Plan & Results: {state['test_results']}
        - Documentation: {state['documentation']}
        
        Please create the final project deliverable package.
        """)
    ]
    
    response = llm.invoke(messages)
    
    return {
        **state,
        "final_deliverable": response.content,
        "messages": state["messages"] + [response],
        "current_agent": "Project Manager (Final Review)",
        "next_step": "end"
    }


def route_next_step(state: DevTeamState) -> str:
    """Route to the next step based on current state."""
    return state["next_step"]


def create_dev_team_graph() -> StateGraph:
    """Create the development team workflow graph."""
    workflow = StateGraph(DevTeamState)
    
    # Add all agent nodes
    workflow.add_node("project_manager", project_manager_node)
    workflow.add_node("software_engineer", software_engineer_node)
    workflow.add_node("qa_engineer", qa_engineer_node)
    workflow.add_node("tech_writer", tech_writer_node)
    workflow.add_node("review", review_and_finalize_node)
    
    # Set entry point
    workflow.set_entry_point("project_manager")
    
    # Add edges following the workflow: PM -> SE -> QA -> TW -> Review -> End
    workflow.add_conditional_edges(
        "project_manager",
        route_next_step,
        {
            "software_engineer": "software_engineer",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "software_engineer",
        route_next_step,
        {
            "qa_engineer": "qa_engineer",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "qa_engineer",
        route_next_step,
        {
            "tech_writer": "tech_writer",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "tech_writer",
        route_next_step,
        {
            "review": "review",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "review",
        route_next_step,
        {
            "end": END
        }
    )
    
    return workflow.compile()


if __name__ == "__main__":
    # Example usage
    graph = create_dev_team_graph()
    
    result = graph.invoke({
        "project_request": "Create a Python CLI tool that helps developers manage their Git repositories by providing quick statistics, branch information, and commit summaries",
        "messages": [],
        "project_plan": "",
        "code_implementation": "",
        "test_plan": "",
        "test_results": "",
        "documentation": "",
        "final_deliverable": "",
        "current_agent": "",
        "next_step": "project_manager"
    })
    
    print("=" * 60)
    print("DEVELOPMENT TEAM PROJECT DELIVERABLE")
    print("=" * 60)
    print("\n🎯 PROJECT PLAN:")
    print("-" * 40)
    print(result["project_plan"])
    
    print("\n💻 CODE IMPLEMENTATION:")
    print("-" * 40)
    print(result["code_implementation"])
    
    print("\n🧪 QA TESTING:")
    print("-" * 40)
    print(result["test_results"])
    
    print("\n📚 DOCUMENTATION:")
    print("-" * 40)
    print(result["documentation"])
    
    print("\n📋 FINAL DELIVERABLE:")
    print("-" * 40)
    print(result["final_deliverable"])
