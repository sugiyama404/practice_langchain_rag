import os
import json

from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, PickleType, BLOB
from sqlalchemy.orm import declarative_base, Session
import pickle

# Mysqlz DB接続情報
db_user = os.environ['MYSQL_USER']
db_pwd = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = "db"

# SQLAlchemyのベースクラスを作成
Base = declarative_base()

# Vectorsモデルを定義
class Vectors(Base):
    __tablename__ = 'vectors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    metadata_info = Column(Text)
    embedding = Column(BLOB)

# embeddingモデルの読み込み
embedding_model = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large"
)

# PDFファイルの読み込み
data_dir = "/app/opt/docs"
files = []

# ディレクトリの読み込み
loader = DirectoryLoader(data_dir)

# テキストをチャンクに分割
split_texts = loader.load_and_split(
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=200, # 分割したチャンクごとの文字数
        chunk_overlap=50 # チャンク間で被らせる文字数
    )
)

engine = create_engine(f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}/{db_name}?charset=utf8')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

for t in split_texts:
    session = Session(engine)
    embed = embedding_model.embed_documents(t.page_content)
    embed_bytes = pickle.dumps(embed)
    session.add(Vectors(content=t.page_content, metadata_info=t.metadata["source"], embedding = embed_bytes))
    session.commit()
session.close()
