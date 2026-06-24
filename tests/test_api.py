import pytest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert "database" in response.json()
        assert "redis" in response.json()


class TestRootEndpoint:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestAgentEndpoints:
    @patch("agents.code_generator.ChatOpenAI")
    def test_code_generate_endpoint(self, mock_chat):
        mock_response = Mock()
        mock_response.content = "print('hello')"
        mock_chat.return_value.invoke.return_value = mock_response
        
        response = client.post(
            "/agent/code/generate",
            json={"task": "print('hello')", "context": {}}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @patch("agents.code_reviewer.ChatOpenAI")
    def test_code_review_endpoint(self, mock_chat):
        mock_response = Mock()
        mock_response.content = "代码审查完成"
        mock_chat.return_value.invoke.return_value = mock_response
        
        response = client.post(
            "/agent/code/review",
            json={"task": "def hello(): return 'hello'", "context": {}}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @patch("agents.document_writer.ChatOpenAI")
    def test_document_write_endpoint(self, mock_chat):
        mock_response = Mock()
        mock_response.content = "文档编写完成"
        mock_chat.return_value.invoke.return_value = mock_response
        
        response = client.post(
            "/agent/document/write",
            json={"task": "编写文档", "context": {}}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)


class TestAuthEndpoints:
    def test_login_endpoint(self):
        response = client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        assert response.status_code == 200 or response.status_code == 401

    def test_register_endpoint(self):
        response = client.post(
            "/auth/register",
            json={"username": "testuser", "email": "test@example.com", "password": "test123"}
        )
        assert response.status_code == 200 or response.status_code == 400


class TestTaskEndpoints:
    def test_get_tasks_endpoint(self):
        response = client.get("/tasks/")
        assert response.status_code == 200

    def test_create_task_endpoint(self):
        response = client.post(
            "/tasks/",
            json={"title": "测试任务", "description": "测试描述"}
        )
        assert response.status_code == 200 or response.status_code == 503


class TestProjectEndpoints:
    def test_get_projects_endpoint(self):
        response = client.get("/projects/")
        assert response.status_code == 200

    def test_create_project_endpoint(self):
        response = client.post(
            "/projects/",
            json={"name": "测试项目", "description": "测试描述"}
        )
        assert response.status_code == 200 or response.status_code == 503