import sys
sys.path.append('/app')
from opt.utils.main import get_embedding_model, get_db_conn

def similer_documents_search(query:str)->list:
    """
    クエリの類似文書を検索する関数
    Args:
        query (str): 検索クエリ
    戻り値:
        クエリの類似文書を検索した値のリスト
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
    query = "黒（ヘイ）について教えてください"
    results = similer_documents_search(query)
    print(results['documents'])
    print(results['metadatas'][0])

