from typing import List
import faiss
import numpy as np
from .base import BaseVectorStore
from ..document import RAGADocument


class FAISSVectorStore(BaseVectorStore):
    def __init__(self):
        self.index = None
        self.documents = []

    def add_documents(
        self, documents: List[RAGADocument], embeddings: List[List[float]]
    ):
        if self.index is None:
            self.index = faiss.IndexFlatL2(len(embeddings[0]))

        self.index.add(np.array(embeddings, dtype=np.float32))  # type: ignore
        self.documents.extend(documents)

    def similarity_search(
        self, query_embedding: List[float], k: int = 4
    ) -> List[RAGADocument]:
        D, I = self.index.search(np.array([query_embedding], dtype=np.float32), k)  # type: ignore
        return [self.documents[i] for i in I[0]]
