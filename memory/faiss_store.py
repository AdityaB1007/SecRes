from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

# Local embedding model using Ollama
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

faiss_db = None  # Global FAISS index


def add_to_faiss(document: Document):
    global faiss_db
    
    if not isinstance(document, Document):
        raise TypeError("Expected a Document object")
    
    if faiss_db is None:
        # Create new FAISS index
        faiss_db = FAISS.from_documents([document], embedding_model)
    else:
        # Add to existing index
        faiss_db.add_documents([document])


def get_faiss_db():
    global faiss_db
    if faiss_db is None:
        raise ValueError("FAISS DB is not initialized. Add some documents first.")
    return faiss_db