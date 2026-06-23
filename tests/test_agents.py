import pytest
from agents.code_generator import CodeGeneratorAgent
from agents.code_reviewer import CodeReviewerAgent
from agents.document_writer import DocumentWriterAgent


class TestCodeGeneratorAgent:
    def test_agent_name(self):
        agent = CodeGeneratorAgent()
        assert "代码生成" in agent.name

    def test_execute_returns_dict(self):
        agent = CodeGeneratorAgent()
        result = agent.execute("print('hello')")
        assert isinstance(result, dict)
        assert "agent" in result
        assert "task" in result
        assert "result" in result
        assert "status" in result


class TestCodeReviewerAgent:
    def test_agent_name(self):
        agent = CodeReviewerAgent()
        assert "代码审查" in agent.name

    def test_execute_returns_dict(self):
        agent = CodeReviewerAgent()
        result = agent.execute("def hello(): return 'hello'")
        assert isinstance(result, dict)
        assert "agent" in result
        assert "task" in result
        assert "result" in result
        assert "status" in result


class TestDocumentWriterAgent:
    def test_agent_name(self):
        agent = DocumentWriterAgent()
        assert "文档编写" in agent.name

    def test_execute_returns_dict(self):
        agent = DocumentWriterAgent()
        result = agent.execute("编写一个函数的文档")
        assert isinstance(result, dict)
        assert "agent" in result
        assert "task" in result
        assert "result" in result
        assert "status" in result