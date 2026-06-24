import pytest
from fastapi.testclient import TestClient


class TestBasic:
    def test_import_fastapi(self):
        try:
            import fastapi
            assert hasattr(fastapi, 'FastAPI')
        except ImportError:
            pytest.fail("fastapi 导入失败")

    def test_import_pydantic(self):
        try:
            import pydantic
            assert hasattr(pydantic, 'BaseModel')
        except ImportError:
            pytest.fail("pydantic 导入失败")

    def test_import_sqlalchemy(self):
        try:
            import sqlalchemy
            assert hasattr(sqlalchemy, 'create_engine')
        except ImportError:
            pytest.fail("sqlalchemy 导入失败")


class TestAPI:
    def test_health_endpoint(self):
        from main import app
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data
        assert "redis" in data

    def test_root_endpoint(self):
        from main import app
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")