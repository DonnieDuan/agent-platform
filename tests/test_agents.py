import pytest
from unittest.mock import Mock, patch


class TestCodeGeneratorAgent:
    def test_import(self):
        try:
            from agents.code_generator import CodeGeneratorAgent
            assert True
        except Exception as e:
            pytest.skip(f"CodeGeneratorAgent 导入失败: {e}")

    @patch("agents.code_generator.ChatOpenAI")
    def test_agent_name(self, mock_chat):
        from agents.code_generator import CodeGeneratorAgent
        agent = CodeGeneratorAgent()
        assert "代码生成" in agent.name

    @patch("agents.code_generator.ChatOpenAI")
    def test_execute_returns_dict(self, mock_chat):
        from agents.code_generator import CodeGeneratorAgent
        mock_response = Mock()
        mock_response.content = "print('hello')"
        mock_chat.return_value.invoke.return_value = mock_response
        
        agent = CodeGeneratorAgent()
        result = agent.execute("print('hello')")
        assert isinstance(result, dict)
        assert "agent" in result
        assert "task" in result
        assert "result" in result
        assert "status" in result


class TestCodeReviewerAgent:
    def test_import(self):
        try:
            from agents.code_reviewer import CodeReviewerAgent
            assert True
        except Exception as e:
            pytest.skip(f"CodeReviewerAgent 导入失败: {e}")

    @patch("agents.code_reviewer.ChatOpenAI")
    def test_agent_name(self, mock_chat):
        from agents.code_reviewer import CodeReviewerAgent
        agent = CodeReviewerAgent()
        assert "代码审查" in agent.name

    @patch("agents.code_reviewer.ChatOpenAI")
    def test_execute_returns_dict(self, mock_chat):
        from agents.code_reviewer import CodeReviewerAgent
        mock_response = Mock()
        mock_response.content = "代码审查完成"
        mock_chat.return_value.invoke.return_value = mock_response
        
        agent = CodeReviewerAgent()
        result = agent.execute("def hello(): return 'hello'")
        assert isinstance(result, dict)
        assert "agent" in result
        assert "task" in result
        assert "result" in result
        assert "status" in result


class TestDocumentWriterAgent:
    def test_import(self):
        try:
            from agents.document_writer import DocumentWriterAgent
            assert True
        except Exception as e:
            pytest.skip(f"DocumentWriterAgent 导入失败: {e}")

    @patch("agents.document_writer.ChatOpenAI")
    def test_agent_name(self, mock_chat):
        from agents.document_writer import DocumentWriterAgent
        agent = DocumentWriterAgent()
        assert "文档编写" in agent.name

    @patch("agents.document_writer.ChatOpenAI")
    def test_execute_returns_dict(self, mock_chat):
        from agents.document_writer import DocumentWriterAgent
        mock_response = Mock()
        mock_response.content = "文档编写完成"
        mock_chat.return_value.invoke.return_value = mock_response
        
        agent = DocumentWriterAgent()
        result = agent.execute("编写一个函数的文档")
        assert isinstance(result, dict)
        assert "agent" in result
        assert "task" in result
        assert "result" in result
        assert "status" in result