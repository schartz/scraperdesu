from src.raga import RAGAFramework, RAGADocument


doc_content = "At its core is the Bun runtime, a fast JavaScript runtime designed as a drop-in replacement for Node.js. It's written in Zig and powered by JavaScriptCore under the hood, dramatically reducing startup times and memory usage."
doc_metadata = {"url": "https://bun.sh/docs"}

# with RAGAFramework(
#     embedding_provider="ollama",
#     llm_provider="ollama",
#     vectorstore_provider="faiss",
#     api_keys={"local": "ollama"},
# ) as rag:
#     documents = [RAGADocument(doc_content, doc_metadata)]
#     rag.add_documents(documents)
#
#     query = "wher is zig p[]"
#     response = rag.query(query)
#     print(f"query: {query}")
#     print(f"response: {response}")

raga = RAGAFramework(
    embedding_provider="ollama",
    llm_provider="ollama",
    vectorstore_provider="chroma",
    api_keys={"local": "ollama"},
)

documents = [RAGADocument(doc_content, doc_metadata)]
raga.add_documents(documents)

query = "what is bun?"
response = raga.query(query)
print(f"query: {query}")
print(f"response: {response}")
