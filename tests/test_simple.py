import sys
import os

os.environ["TEST_MODE"] = "true"

def test_import_fastapi():
    try:
        import fastapi
        print(f"✅ fastapi 导入成功: {fastapi.__version__}")
    except Exception as e:
        print(f"❌ fastapi 导入失败: {e}")
        sys.exit(1)

def test_import_pydantic():
    try:
        import pydantic
        print(f"✅ pydantic 导入成功: {pydantic.__version__}")
    except Exception as e:
        print(f"❌ pydantic 导入失败: {e}")
        sys.exit(1)

def test_import_sqlalchemy():
    try:
        import sqlalchemy
        print(f"✅ sqlalchemy 导入成功: {sqlalchemy.__version__}")
    except Exception as e:
        print(f"❌ sqlalchemy 导入失败: {e}")
        sys.exit(1)

def test_import_auth():
    try:
        from core import auth
        print("✅ core.auth 导入成功")
    except Exception as e:
        print(f"❌ core.auth 导入失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=== 开始测试 ===")
    test_import_fastapi()
    test_import_pydantic()
    test_import_sqlalchemy()
    test_import_auth()
    print("=== 所有测试通过 ===")