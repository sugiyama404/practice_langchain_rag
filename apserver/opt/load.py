from .utils import get_embedding_model, get_db_conn

def similer_documents_search(query:str):
    """
    クエリの類似文書を検索する関数
    Args:
        query (str): 検索クエリ
    """
    # データベース接続とエンベディングモデルを取得
    client = get_db_conn()
    embedding_model = get_embedding_model()

    collection = client.get_collection(name="my_collection")
    # クエリのベクトル化
    query_vector = embedding_model.embed_documents(query)
    # 類似度検索の実行
    results = collection.query(query_vector, n_results=3)
    return results

if __name__ == "__main__":
    # 類似度検索クエリ
    query = "RAG（検索拡張生成）について簡潔に教えてください"
    results = similer_documents_search(query)
    print(results['documents'][0])
    print(results['metadatas'][0])

