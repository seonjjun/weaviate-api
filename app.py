from flask import Flask, request, jsonify
import weaviate
from weaviate.auth import AuthApiKey
import os

app = Flask(__name__)

# ✅ Weaviate Cloud 연결
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.environ.get("WEAVIATE_URL"),
    auth_credentials=AuthApiKey(api_key=os.environ.get("WCS_API_KEY")),
    headers={
        "X-Openai-Api-Key": os.environ.get("OPENAI_API_KEY")
    }
)

# 🔍 Structure 컬렉션 가져오기
collection = client.collections.get("Structure")


# ✅ 구조 저장 API
@app.route('/store', methods=['POST'])
def store():
    data = request.json
    collection.data.insert({
        "id": data.get("id"),
        "symbol": data.get("symbol"),
        "timeframes": data.get("timeframes"),
        "description": data.get("description"),
        "indicators": data.get("indicators"),
        "price_zone": data.get("price_zone"),
        "labels": data.get("labels"),
        "notes": data.get("notes"),
        "entry_price": data.get("entry_price"),
        "exit_price": data.get("exit_price"),
        "success": data.get("success"),
        "source": data.get("source")
    })
    return jsonify({"status": "stored"}), 200


# ✅ 유사 구조 검색 API
@app.route('/search', methods=['POST'])
def search():
    query = request.json.get("query")
    result = collection.query.near_text(query=query, limit=1)
    return jsonify(result.objects), 200


# ✅ 저장된 구조 ID 목록 API (우리가 저장한 id만 반환)
@app.route('/list', methods=['GET'])
def list_structures():
    result = collection.query.fetch_objects(limit=100)
    ids = [
        obj.properties["id"]
        for obj in result.objects if "id" in obj.properties
    ]
    return jsonify(ids), 200
