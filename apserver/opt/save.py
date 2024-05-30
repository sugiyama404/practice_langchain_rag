from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma

import sys
sys.path.append('/app')
from opt.utils.main import get_embedding_model, get_db_conn

def save():
    """
    ドキュメントをChromaDBにインデックス化する関数
    """
    # データベース接続とエンベディングモデルを取得
    embedding_model = get_embedding_model()
    client = get_db_conn()

    # ドキュメントローダーを初期化
    loader = DirectoryLoader("/app/opt/docs")

    # テキストをチャンクに分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=10
    )
    split_texts = loader.load_and_split(text_splitter=text_splitter)

    # ChromaDBにドキュメントをインデックス化
    chroma_db = Chroma(
        collection_name="my_collection",
        embedding_function=embedding_model,  # エンベディング関数を直接指定
        client=client,
    )

    chroma_db.add_documents(documents=split_texts)
    print("インデックス化が完了しました")

if __name__ == "__main__":
    save()
