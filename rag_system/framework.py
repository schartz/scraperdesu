from typing import List, Literal, Optional, Dict
from .document import RAGADocument
from .embeddings import get_embedding_model
from .vectorstores import get_vectorstore
from .llms import get_llm
from .utils.text_splitter import SimpleTextSplitter
from .retrievers.similarity import SimilarityRetriever
from .session import Session


EmbeddingTypes = Literal["ollama", "mistral", "openai"]
LLMTypes = Literal["ollama", "mistral", "openai"]
VectorDBTypes = Literal["chroma", "faiss"]
# LLMModelNames = Literal["llama3.1", "mistral", "mistral-meno", "gemma2", "gemeni-pro"]


class RAGAFramework:
    def __init__(
        self,
        embedding_provider: EmbeddingTypes,
        vectorstore_provider: VectorDBTypes,
        llm_provider: LLMTypes,
        api_keys: Dict[str, str],
        embedding_model: str = "nomic-embed-text",
        llm_model: str = "mistral",
        system_prompt: Optional[str] = None,
        text_splitter: Optional[SimpleTextSplitter] = None,
    ):
        """
        RAGAFramework class - A multi-purpose AI assistant framework that utilizes embedding, vectorstore, and LLM services in a unified manner.

        Provides methods to add documents, query the model, and customize the system prompt. The framework uses context from the stored documents to generate responses.

        Usage example:
        ```
        from RAGAFramework import RAGAFramework

        # Initialize the RAGAFramework instance with certain configurations
        framework = RAGAFramework(embedding_provider="HuggingFace", vectorstore_provider="DrQA", llm_provider="RiversideCode")

        # Add documents to the framework
        # Assuming documents is a list of Document objects as per the SDK's definition
        framework.add_documents(documents)

        # Set a custom system prompt (optional, defaults to the default one)
        framework.system_prompt = "You are an assistant that helps with specific tasks. Please perform the task asked by the user."

        # Query the framework with a given question
        response = framework.query("What is the capital of France?")

        # Print the generated response from the query
        print(response)
        ```
        """
        self.session = Session()
        self.session.set_api_keys(api_keys)

        self.embedding = get_embedding_model(
            embedding_provider,
            self.session.get_api_key(embedding_provider),
            embedding_model,
        )
        self.vectorstore = get_vectorstore(
            vectorstore_provider, self.session.get_api_key(vectorstore_provider)
        )
        self.llm = get_llm(
            llm_provider, self.session.get_api_key(llm_provider), llm_model
        )

        self.system_prompt = system_prompt or self._default_system_prompt()
        self.text_splitter = text_splitter or SimpleTextSplitter()
        self.retriever = SimilarityRetriever(self.vectorstore, self.embedding)

    def _default_system_prompt(self) -> str:
        return (
            "You are a helpful AI assistant. Use the provided context to answer "
            "questions. If you're unsure or the answer isn't in the context, "
            "say you don't know."
        )

    def add_documents(self, documents: List[RAGADocument]):
        split_docs = []
        for doc in documents:
            chunks = self.text_splitter.split_text(doc.content)
            split_docs.extend([RAGADocument(chunk, doc.metadata) for chunk in chunks])

        embeddings = self.embedding.embed_batch([doc.content for doc in split_docs])
        self.vectorstore.add_documents(split_docs, embeddings)

    def query(self, query: str, k: int = 4) -> str:
        retrieved_docs = self.retriever.retrieve(query, k)
        context = "\n\n".join([doc.content for doc in retrieved_docs])

        prompt = f"{self.system_prompt}\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"

        return self.llm.generate(prompt)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.clear_api_keys()
