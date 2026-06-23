from config.settings import settings
import socket

def test_mysql():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((settings.DB_HOST, settings.DB_PORT))
        sock.close()
        if result == 0:
            print(f"✅ MySQL 连接成功 - {settings.DB_HOST}:{settings.DB_PORT}")
            return True
        else:
            print(f"❌ MySQL 连接失败 - {settings.DB_HOST}:{settings.DB_PORT}")
            return False
    except Exception as e:
        print(f"❌ MySQL 连接异常: {e}")
        return False

def test_redis():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((settings.REDIS_HOST, settings.REDIS_PORT))
        sock.close()
        if result == 0:
            print(f"✅ Redis 连接成功 - {settings.REDIS_HOST}:{settings.REDIS_PORT}")
            return True
        else:
            print(f"❌ Redis 连接失败 - {settings.REDIS_HOST}:{settings.REDIS_PORT}")
            return False
    except Exception as e:
        print(f"❌ Redis 连接异常: {e}")
        return False

def test_qdrant():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((settings.QDRANT_HOST, settings.QDRANT_PORT))
        sock.close()
        if result == 0:
            print(f"✅ Qdrant 连接成功 - {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
            return True
        else:
            print(f"❌ Qdrant 连接失败 - {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
            return False
    except Exception as e:
        print(f"❌ Qdrant 连接异常: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("服务连接测试")
    print("=" * 50)
    
    mysql_ok = test_mysql()
    redis_ok = test_redis()
    qdrant_ok = test_qdrant()
    
    print("=" * 50)
    if mysql_ok and redis_ok and qdrant_ok:
        print("✅ 所有服务连接正常！")
    else:
        print("❌ 部分服务连接失败，请检查配置和服务状态")