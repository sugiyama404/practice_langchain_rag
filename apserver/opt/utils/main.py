from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings

def get_embedding_model()->HuggingFaceEmbeddings:
    """
    HuggingFaceの事前学習済みのモデルをロードして返す関数
    戻り値:
        HuggingFaceEmbeddingsオブジェクト: 事前学習済みのモデルをラップしたオブジェクト
    """
    return HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-large"
    )

def get_db_conn()->chromadb.HttpClient:
    """
    ChromaDBデータベースへの接続を確立して返す関数
    戻り値:
        Chromadb.HttpClientオブジェクト: ChromaDBデータベースへの接続を表現するオブジェクト
    """
    client = chromadb.HttpClient(
        host="db",
        port=8000,
        settings=Settings(allow_reset=True, anonymized_telemetry=False),
        )
    return client

def remove_duplicates(data:list)->str:
    """
    入力されたリストの重複要素を削除し、sourceの値のみを出力する関数
    引数:
        data: 重複を含むリスト
    戻り値:
        重複要素を除いたsourceの値のリスト
    """
    unique_sources = []

    for item in data:
        for i in item:
            source = i['source']
            if source not in unique_sources:
                unique_sources.append(source)

    docs = "[参考文献]"
    for source in unique_sources:
        docs += f"\n{source}"

    return docs
