import pytest
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
    def test_code_generate_endpoint(self):
        response = client.post(
            "/agent/code/generate",
            json={"task": "print('hello')", "context": {}}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_code_review_endpoint(self):
        response = client.post(
            "/agent/code/review",
            json={"task": "def hello(): return 'hello'", "context": {}}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_document_write_endpoint(self):
        response = client.post(
            "/agent/document/write",
            json={"task": "编写文档", "context": {}}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)


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