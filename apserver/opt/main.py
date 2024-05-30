import os
from dotenv import load_dotenv
import google.generativeai as genai

import sys
sys.path.append('/app')
from opt.load import similer_documents_search
from opt.utils.main import remove_duplicates

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
GEMINI_MODEL = os.getenv('GEMINI_MODEL')

def question(query: str)->str:
    results = similer_documents_search(query)
    references = remove_duplicates(results['metadatas'])

    prompt = f"""
    [参考情報]に基づき100字以内で[質問]に答えてください。
    [質問]
    {query}
    [参考情報]
    {results['documents']}
    """

    gemini_pro = genai.GenerativeModel(GEMINI_MODEL)
    response = gemini_pro.generate_content(prompt)
    result = response.text + "\n" + references
    return result

if __name__ == "__main__":
    query = "黒（ヘイ）について教えてください"
    res = question(query)
    print(f"[質問]\n{query}\n[回答]\n{res}")
