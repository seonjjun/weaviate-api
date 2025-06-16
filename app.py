from flask import Flask, request, jsonify
import weaviate
from weaviate.auth import AuthApiKey
import os

app = Flask(__name__)

# 🔐 Weaviate Cloud (WCS) 접속 설정
client = weaviate.connect_to_wcs(
    cluster_url=os.environ.get("WEAVIATE_URL"),
    auth_credentials=AuthApiKey(api_key=os.environ.get("WCS_API_KEY"))
)

# ✅ 구조 저장 API
@app.route('/store', methods=['POST'])
def store():
    data = request.json
    client.data_object.create(
        data_object={
            "name": data.get("name"),
            "content": data.get("content")
        },
        class_name="Structure"
    )
    return jsonify({"status": "stored"})

# ✅ 구조 유사도 검색 API
@app.route('/search', methods=['POST'])
def search():
    query = request.json.get("query")
    result = client.query.get("Structure", ["name", "content"])\
        .with_near_text({"concepts": [query]})\
        .with_limit(1).do()
    return jsonify(result)
