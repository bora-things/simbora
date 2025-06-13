import os
from typing import List
from langchain.schema import Document
from simbora.services.retriever import get_retriever

KNOWLEDGE_DIR = os.getenv("KNOWLEDGE_DIR", "./knowledge")

def obter_caminhos_documentos() -> List[str]:
    """Obtém todos os caminhos de documentos PDF que podem ser utilizados para responder às perguntas dos usuários."""
    pdfs_paths: list[str] = []
    for file in os.listdir(KNOWLEDGE_DIR):
        if file.lower().endswith('.pdf'):
            abs_path = os.path.join(KNOWLEDGE_DIR, file)
            pdfs_paths.append(abs_path)
    return pdfs_paths

def enriquecer_solicitacao_do_usuario(entrada_usuario: str, caminhos_documentos_relevantes_pro_usuario: List[str]) -> List[Document]:
    """
    Obtém informações relevantes dos documentos baseados na entrada do usuário para contextualizar a resposta final.

    :param str entrada_usuario: A entrada do usuário que será usada para buscar informações relevantes.
    :param List[str] caminhos_documentos_relevantes_pro_usuario: Lista de caminhos dos documentos que são relevantes para responder à pergunta do usuário.
    Seja rigoroso na filtragem dos documentos, garantindo que apenas os mais relevantes sejam utilizados. Evite ao máximo misturar informações de diferentes cursos, a menos que seja absolutamente necessário para responder à pergunta do usuário.
    """
    retriever = get_retriever(search_kwargs={
        "k": 5,
        "filter": {
            "source": {"$in": caminhos_documentos_relevantes_pro_usuario}
        }
    })
    docs = retriever.invoke(entrada_usuario)
    return docs
