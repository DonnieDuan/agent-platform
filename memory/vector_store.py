from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from config.settings import settings
from typing import List, Dict, Optional
import uuid


class VectorStore:
    def __init__(self):
        self.client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self._create_collection()

    def _create_collection(self):
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )

    def add_memory(self, text: str, metadata: Dict = None, vector: List[float] = None):
        if vector is None:
            vector = [0.0] * 1536
        point_id = str(uuid.uuid4())
        point = PointStruct(
            id=point_id,
            vector=vector,
            payload={"text": text, **(metadata or {})}
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])
        return point_id

    def search_memory(self, query_vector: List[float], limit: int = 5) -> List[Dict]:
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        return [{"text": r.payload.get("text"), "score": r.score, "metadata": r.payload} for r in results]

    def delete_memory(self, point_id: str):
        self.client.delete(collection_name=self.collection_name, points_selector=[point_id])

    def get_collection_info(self):
        return self.client.get_collection(collection_name=self.collection_name)