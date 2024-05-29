from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings


def get_embedding_model()->HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-large"
    )

def db_connect():
    client = chromadb.HttpClient(
        host="db",
        port=8000,
        settings=Settings(allow_reset=True, anonymized_telemetry=False),
        )
    return client
