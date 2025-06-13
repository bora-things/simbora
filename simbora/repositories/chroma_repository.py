import os
import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings
from typing import Iterable

class ChromaRepository:
    def __init__(
        self,
        host: str,
        port: int,
        embedding_model: str,
        collection_name: str,
    ):
        try:
            embedding_function = OpenAIEmbeddings(model=embedding_model)
            client = chromadb.HttpClient(host, port, settings=Settings(allow_reset=True, anonymized_telemetry=False))
            self._db = Chroma(
                client=client,
                embedding_function=embedding_function,
                collection_name=collection_name
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Chroma repository: {e}")


    def add_docs(self, docs: list[Document]):
        """
        add a list of langchain documents into the chromadb
        :param docs: list of langchain documents
        """
        if docs:
            for i in range(0, len(docs), 100):
                self._db.add_documents(docs[i:i+100])


    def remove_docs(self, sources: Iterable[str]):
        """
        hard remove all langchain documents at database based on its sources metadata
        :param sources: list of sources metadatas
        """
        if sources:
            for source in sources:
                docs = self._db.get(where={"source": source})
                self._db.delete(ids=docs["ids"])


    def as_retriever(self, search_kwargs={}) -> VectorStoreRetriever:
        """
        :return: chromadb as a vector store retrievier important to the RAG chain
        """
        return self._db.as_retriever(search_kwargs=search_kwargs)


    def get_sources(self) -> list[str]:
        """
        :return: list of all source metadata of all documents in the database
        """
        docs = self._db.get()
        sources = [metadata["source"] for metadata in docs["metadatas"]]

        return sources

if __name__ == "__main__":
    embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    embedding_function = OpenAIEmbeddings(model=embedding_model)
    test_embedding = embedding_function.embed_query("Teste de embedding")
    print(f"Test embedding: {test_embedding[:5]}...")

    chroma_repo = ChromaRepository(
        host=os.getenv("CHROMA_HOST", "localhost"),
        port=int(os.getenv("CHROMA_PORT", 8000)),
        embedding_model=embedding_model,
        collection_name=os.getenv("CHROMA_COLLECTION_NAME", "simbora")
    )

    print("Chroma repository initialized.")
    sources = chroma_repo.get_sources()
    print(f"Sources in the database: {len(sources)}")