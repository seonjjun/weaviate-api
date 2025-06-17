from flask import Flask, request, jsonify
import weaviate
from weaviate.auth import AuthApiKey
import os

app = Flask(__name__)

# 🔐 Weaviate 클라이언트 연결 (Cloud 버전)
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.environ.get("WEAVIATE_URL"),
    auth_credentials=AuthApiKey(api_key=os.environ.get("WCS_API_KEY")),
    headers={
        "X-Openai-Api-Key": os.environ.get("OPENAI_API_KEY")
    }
)

# 🎯 'Structure'라는 컬렉션 불러오기
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


# ✅ 유사 검색 API
@app.route('/search', methods=['POST'])
def search():
    query = request.json.get("query")
    result = collection.query.near_text(query=query, limit=1)
    return jsonify(result.objects), 200


# ✅ 저장된 구조 리스트 API
@app.route('/list', methods=['GET'])
def list_structures():
    result = collection.query.fetch_objects(limit=100)
    ids = [obj.properties.get("id", obj.uuid) for obj in result.objects]
    return jsonify(ids), 200


# ✅ Render용 (app:app)
# (주의: 절대 app.run() 쓰지 말 것)
