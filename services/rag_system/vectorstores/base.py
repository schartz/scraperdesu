from abc import ABC, abstractmethod
from typing import List
from ..document import RAGADocument


class BaseVectorStore(ABC):
    @abstractmethod
    def add_documents(
        self, documents: List[RAGADocument], embeddings: List[List[float]]
    ):
        pass

    @abstractmethod
    def similarity_search(
        self, query_embedding: List[float], k: int = 4
    ) -> List[RAGADocument]:
        pass
