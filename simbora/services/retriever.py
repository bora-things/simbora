import os
from simbora.services.chroma_service import ChromaService
from simbora.repositories.chroma_repository import ChromaRepository

chroma_repo = ChromaRepository(
    host=os.getenv("CHROMA_HOST", "localhost"),
    port=int(os.getenv("CHROMA_PORT", 8000)),
    embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-large"),
    collection_name=os.getenv("CHROMA_COLLECTION_NAME", "simbora")
)

knowledge_directory = os.getenv("KNOWLEDGE_BASE_PDF_DIR", "./knowledge")

service = ChromaService(chroma_repository=chroma_repo, knowledge_directory=knowledge_directory)

get_retriever = lambda search_kwargs=None: service.load_retriever(search_kwargs)
