import os
from dotenv import load_dotenv
import sys
sys.path.append('/app')
from opt.load import similer_documents_search
from opt.utils.main import remove_duplicates

def question(query: str):
    load_dotenv()
    GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
    print(GOOGLE_API_KEY)

    results = similer_documents_search(query)
    # print(results['metadatas'])
    src = remove_duplicates(results['metadatas'])
    print(src)

if __name__ == "__main__":
    query = "黒（ヘイ）について教えてください"
    question(query)
