from memory.vector_store import VectorStore
from memory.redis_store import RedisStore


class MemoryManager:
    def __init__(self):
        self.vector_store = VectorStore()
        self.redis_store = RedisStore()

    def save_long_term_memory(self, text: str, metadata=None):
        return self.vector_store.add_memory(text, metadata)

    def retrieve_long_term_memory(self, query_vector, limit=5):
        return self.vector_store.search_memory(query_vector, limit)

    def delete_long_term_memory(self, point_id: str):
        self.vector_store.delete_memory(point_id)

    def save_short_term_memory(self, key: str, value, ttl=None):
        self.redis_store.set_cache(key, value, ttl)

    def retrieve_short_term_memory(self, key: str):
        return self.redis_store.get_cache(key)

    def delete_short_term_memory(self, key: str):
        self.redis_store.delete_cache(key)

    def memory_exists(self, key: str) -> bool:
        return self.redis_store.exists(key)