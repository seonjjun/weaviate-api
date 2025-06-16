from flask import Flask, request, jsonify
import weaviate
from weaviate.auth import AuthApiKey
import os

app = Flask(__name__)

# ✅ Weaviate Cloud 연결
client = weaviate.connect_to_wcs(
    cluster_url=os.environ.get("WEAVIATE_URL"),
    auth_credentials=AuthApiKey(api_key=os.environ.get("WCS_API_KEY"))
)

# ✅ Structure 컬렉션 객체 획득
collection = client.collections.get("Structure")

# ✅ 구조 저장 API
@app.route('/store', methods=['POST'])
def store():
    data = request.json
    collection.data.insert({
        "name": data.get("name"),
        "content": data.get("content")
    })
    return jsonify({"status": "stored"})

# ✅ 유사 구조 검색 API
@app.route('/search', methods=['POST'])
def search():
    query = request.json.get("query")
    result = collection.query.near_text(query=query, limit=1)
    return jsonify(result.objects)
