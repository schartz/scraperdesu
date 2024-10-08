from typing import List
import chromadb
from .base import BaseVectorStore
from ..document import RAGADocument


class ChromaVectorStore(BaseVectorStore):
    def __init__(self, collection_name: str = "default_collection"):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(collection_name)

    def add_documents(
        self, documents: List[RAGADocument], embeddings: List[List[float]]
    ):
        self.collection.add(
            embeddings=embeddings,  # pyright: ignore
            documents=[doc.content for doc in documents],
            metadatas=[doc.metadata for doc in documents],
            ids=[str(i) for i in range(len(documents))],
        )

    def similarity_search(
        self, query_embedding: List[float], k: int = 4
    ) -> List[RAGADocument]:
        results = self.collection.query(query_embeddings=[query_embedding], n_results=k)
        return [
            RAGADocument(content=doc, metadata=meta)  # pyright: ignore
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])  # pyright: ignore
        ]
