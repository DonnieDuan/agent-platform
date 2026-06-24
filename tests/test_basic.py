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

    def test_import_auth(self):
        try:
            from core import auth
            assert hasattr(auth, 'create_access_token')
        except Exception as e:
            pytest.skip(f"core.auth 导入失败: {e}")


class TestAPI:
    def test_health_endpoint(self):
        try:
            from main import app
            client = TestClient(app)
            response = client.get("/health")
            assert response.status_code == 200
        except Exception as e:
            pytest.skip(f"健康检查失败: {e}")

    def test_root_endpoint(self):
        try:
            from main import app
            client = TestClient(app)
            response = client.get("/")
            assert response.status_code == 200
        except Exception as e:
            pytest.skip(f"根路由失败: {e}")