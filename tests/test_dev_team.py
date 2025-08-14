"""Tests for the development team agents and workflow."""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from langest.agents import (
    ProjectManagerAgent,
    SoftwareEngineerAgent, 
    QAEngineerAgent,
    TechWriterAgent
)


class TestDevTeamAgents(unittest.TestCase):
    """Test cases for development team agents."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_project_request = "Create a simple Python calculator CLI tool"
        self.sample_project_plan = "Basic project plan for calculator tool"
        self.sample_code = "def add(a, b): return a + b"
        self.sample_test_results = "All tests passed"
        self.sample_documentation = "User guide for calculator"
    
    @patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'})
    @patch('langest.agents.project_manager.ChatGroq')
    def test_project_manager_initialization(self, mock_chat_groq):
        """Test ProjectManager agent initialization."""
        mock_llm = MagicMock()
        mock_chat_groq.return_value = mock_llm
        
        agent = ProjectManagerAgent()
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.llm, mock_llm)
        mock_chat_groq.assert_called_once()
    
    @patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'})
    @patch('langest.agents.software_engineer.ChatGroq')
    def test_software_engineer_initialization(self, mock_chat_groq):
        """Test SoftwareEngineer agent initialization."""
        mock_llm = MagicMock()
        mock_chat_groq.return_value = mock_llm
        
        agent = SoftwareEngineerAgent()
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.llm, mock_llm)
        mock_chat_groq.assert_called_once()
    
    @patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'})
    @patch('langest.agents.qa_engineer.ChatGroq')
    def test_qa_engineer_initialization(self, mock_chat_groq):
        """Test QAEngineer agent initialization."""
        mock_llm = MagicMock()
        mock_chat_groq.return_value = mock_llm
        
        agent = QAEngineerAgent()
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.llm, mock_llm)
        mock_chat_groq.assert_called_once()
    
    @patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'})
    @patch('langest.agents.tech_writer.ChatGroq')
    def test_tech_writer_initialization(self, mock_chat_groq):
        """Test TechWriter agent initialization."""
        mock_llm = MagicMock()
        mock_chat_groq.return_value = mock_llm
        
        agent = TechWriterAgent()
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.llm, mock_llm)
        mock_chat_groq.assert_called_once()
    
    @patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'})
    @patch('langest.agents.project_manager.ChatGroq')
    def test_project_manager_create_plan(self, mock_chat_groq):
        """Test project manager plan creation."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Sample project plan"
        mock_llm.invoke.return_value = mock_response
        mock_chat_groq.return_value = mock_llm
        
        agent = ProjectManagerAgent()
        result = agent.create_project_plan(self.sample_project_request)
        
        self.assertEqual(result, "Sample project plan")
        mock_llm.invoke.assert_called_once()
    
    @patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'})
    @patch('langest.agents.software_engineer.ChatGroq')
    def test_software_engineer_process_request(self, mock_chat_groq):
        """Test software engineer request processing."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Sample code implementation"
        mock_llm.invoke.return_value = mock_response
        mock_chat_groq.return_value = mock_llm
        
        agent = SoftwareEngineerAgent()
        result = agent.process_request(self.sample_project_request, self.sample_project_plan)
        
        self.assertEqual(result, "Sample code implementation")
        mock_llm.invoke.assert_called_once()
    
    @patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'})
    @patch('langest.agents.qa_engineer.ChatGroq')
    def test_qa_engineer_create_test_plan(self, mock_chat_groq):
        """Test QA engineer test plan creation."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Sample test plan"
        mock_llm.invoke.return_value = mock_response
        mock_chat_groq.return_value = mock_llm
        
        agent = QAEngineerAgent()
        result = agent.create_test_plan(
            self.sample_project_request, 
            self.sample_project_plan, 
            self.sample_code
        )
        
        self.assertEqual(result, "Sample test plan")
        mock_llm.invoke.assert_called_once()
    
    @patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'})
    @patch('langest.agents.tech_writer.ChatGroq')
    def test_tech_writer_create_documentation(self, mock_chat_groq):
        """Test tech writer documentation creation."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Sample documentation"
        mock_llm.invoke.return_value = mock_response
        mock_chat_groq.return_value = mock_llm
        
        agent = TechWriterAgent()
        result = agent.create_documentation(
            self.sample_project_request,
            self.sample_project_plan,
            self.sample_code,
            self.sample_test_results
        )
        
        self.assertEqual(result, "Sample documentation")
        mock_llm.invoke.assert_called_once()


class TestAgentIntegration(unittest.TestCase):
    """Integration tests for agent interactions."""
    
    @patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'})
    def test_agent_imports(self):
        """Test that all agents can be imported successfully."""
        try:
            from langest.agents import (
                ProjectManagerAgent,
                SoftwareEngineerAgent,
                QAEngineerAgent,
                TechWriterAgent
            )
            
            # Test that classes are properly defined
            self.assertTrue(callable(ProjectManagerAgent))
            self.assertTrue(callable(SoftwareEngineerAgent))
            self.assertTrue(callable(QAEngineerAgent))
            self.assertTrue(callable(TechWriterAgent))
            
        except ImportError as e:
            self.fail(f"Failed to import agents: {e}")


if __name__ == '__main__':
    unittest.main()
