from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

import chromadb
from chromadb.config import Settings

client = chromadb.HttpClient(
    host="db",
    port=8000,
    settings=Settings(allow_reset=True, anonymized_telemetry=False),
    )

embedding_model = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large"
)

data_dir = "/app/opt/docs"
files = []

loader = DirectoryLoader(data_dir)

# テキストをチャンクに分割
split_texts = loader.load_and_split(
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=200, # 分割したチャンクごとの文字数
        chunk_overlap=50 # チャンク間で被らせる文字数
    )
)

# ChromaDBにドキュメントをインデックス化
chroma_db = Chroma(
    collection_name="my_collection",
    embedding_function=embedding_model,  # エンベディング関数を直接指定
    client=client,
)

chroma_db.add_documents(
    documents=split_texts,
)

print("インデックス化が完了しました")
