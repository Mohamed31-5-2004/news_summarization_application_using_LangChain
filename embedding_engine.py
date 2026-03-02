from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings


class EmbeddingEngine:
    def __init__(self, persist_dir="chroma_db", model_name: str = "all-MiniLM-L6-v2"):
        """Embedding engine using sentence-transformers and chromadb directly."""
        self.persist_dir = persist_dir
        model_id = model_name
        if not model_id.startswith("sentence-transformers/"):
            model_id = f"sentence-transformers/{model_name}"
        self.model = SentenceTransformer(model_id)
        # Create a Chroma client (use default settings). Persistency depends on installed chromadb version.
        try:
            self.client = chromadb.Client()
        except Exception:
            # fallback: plain client creation
            self.client = chromadb.Client()
        try:
            self.collection = self.client.get_collection("news")
        except Exception:
            self.collection = self.client.create_collection("news")

    def add_documents(self, texts, metadatas=None, ids=None):
        embeddings = [self.model.encode(t).tolist() for t in texts]
        self.collection.add(ids=ids, documents=texts, metadatas=metadatas or [{}] * len(texts), embeddings=embeddings)
        try:
            self.client.persist()
        except Exception:
            pass

    def get_query_embedding(self, text):
        return self.model.encode(text).tolist()

    def similarity_search(self, query, k=5):
        emb = self.get_query_embedding(query)
        res = self.collection.query(query_embeddings=[emb], n_results=k, include=["documents", "metadatas", "distances"])
        results = []
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        ids = res.get("ids", [[]])[0]
        for d, m, _id in zip(docs, metas, ids):
            class Result:
                pass

            r = Result()
            r.page_content = d
            r.metadata = m
            r.id = _id
            results.append(r)
        return results
