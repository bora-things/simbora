import sys
import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from typing import Iterable
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from simbora.repositories.chroma_repository import ChromaRepository

# FIXME: why isn't this function in the class?
def load_pdfs(pdfs: Iterable[str]) -> list[Document]:
    """
    loads the pdfs into Documents
    :param pdfs: list of filepaths to pdfs files
    :return: list of Documents
    """
    docs = []
    if pdfs:
        for pdf_file in pdfs:
            loader = PyMuPDFLoader(pdf_file)
            pages = loader.load()
            for page in pages:
                page.metadata["title"] = os.path.basename(pdf_file).removesuffix(".pdf")
                
            docs.extend(pages)

    return docs

# FIXME: why isn't this function in the class?
def split_docs(docs: list[Document]) -> list[Document]:
    """
    splits the documents into smaller sizes for the database
    :param docs: list of documents to split
    :return: list of split documents
    """
    if docs:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        return splits


class ChromaService:
    def __init__(
        self,
        chroma_repository: ChromaRepository,
        knowledge_directory: str
    ):
        self._chroma_repository = chroma_repository
        self._knowledge_directory = knowledge_directory

    def _get_pdfs_paths_from_dir(self) -> list[str]:
        """
        Recursively gets a list of pdf paths in the knowledge directory and its subdirectories.
        Each path is relative to the knowledge directory, e.g., 'bcc/ppc/PPC-BCC.pdf'.
        :return: list of absolute file paths to the pdfs in the directory tree
        """
        pdfs_paths: list[str] = []
        for root, _, files in os.walk(self._knowledge_directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    abs_path = os.path.join(root, file)
                    pdfs_paths.append(abs_path)
        return pdfs_paths

    def _compare_files(self) -> tuple[set[str], set[str]]:
        """
            gets mismatched files between the Chroma database and the directory and returns them as two sets

            :return: a tuple where the first member is the set of files only in the directory, and
            the second is the set of files only in the database
        """

        paths: set[str] = set(self._get_pdfs_paths_from_dir())

        sources: set[str] = set(self._chroma_repository.get_sources())
        
        directory_only = paths.difference(sources)
        database_only = sources.difference(paths)

        return directory_only, database_only


    def _update_knowledge(self):
        """
            add or remove RAG knowledge based on knowledge folder new or removed files
            if the file exists only at chromadb, it was removed
            if the file exists only at knowledge folder, it is a new one
        """
        directory_only, database_only = self._compare_files()

        new_docs_from_directory = split_docs(load_pdfs(directory_only))

        self._chroma_repository.add_docs(new_docs_from_directory)
        self._chroma_repository.remove_docs(database_only)


    def load_retriever(self, search_kwargs={}) -> VectorStoreRetriever:
        """
            :return: chromadb as a retriever to the RAG
        """
        # TODO: make this method more efficient, it is called every time the retriever is needed
        self._update_knowledge()

        retriever = self._chroma_repository.as_retriever(search_kwargs=search_kwargs)

        return retriever

if __name__ == "__main__":
    print("Initializing Chroma repository...")

    chroma_repo = ChromaRepository(
        host=os.getenv("CHROMA_HOST", "localhost"),
        port=int(os.getenv("CHROMA_PORT", 8000)),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-large"),
        collection_name=os.getenv("CHROMA_COLLECTION_NAME", "simbora")
    )

    print("Chroma repository initialized.")

    knowledge_directory = os.getenv("KNOWLEDGE_BASE_PDF_DIR", "./knowledge")

    service = ChromaService(chroma_repository=chroma_repo, knowledge_directory=knowledge_directory)
    retriever = service.load_retriever()
    relevant_docs = retriever.invoke("O que é o curso de Ciência da Computação?")

    print(f"Retriever loaded with {len(relevant_docs)} documents.")