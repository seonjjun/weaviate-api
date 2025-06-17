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

# 🎯 Structure 컬렉션 연결
collection = client.collections.get("Structure")


# ✅ 1. 구조 저장 API
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


# ✅ 2. 유사도 검색 API
@app.route('/search', methods=['POST'])
def search():
    query = request.json.get("query")
    result = collection.query.near_text(query=query, limit=1)
    return jsonify(result.objects), 200


# ✅ 3. 저장된 구조 목록 API (우리가 입력한 id만)
@app.route('/list', methods=['GET'])
def list_structures():
    result = collection.query.fetch_objects(limit=100)
    ids = [
        obj.properties["id"]
        for obj in result.objects if "id" in obj.properties
    ]
    return jsonify(ids), 200


# ✅ 4. 구조 삭제 API (id 기준으로 삭제)
@app.route('/delete-structure', methods=['POST'])
def delete_structure():
    try:
        data = request.get_json()
        uuid = data.get("uuid")
        if not uuid:
            return jsonify({"status": "error", "message": "UUID is required"}), 400

        client.data_object.delete(uuid=uuid, class_name="Structure")
        return jsonify({"status": "ok", "message": f"Deleted {uuid}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


    result = collection.query.fetch_objects(limit=100)
    for obj in result.objects:
        if obj.properties.get("id") == structure_id:
            collection.data.delete_by_id(obj.uuid)
            return jsonify({"status": f"{structure_id} deleted"}), 200

    return jsonify({"error": f"{structure_id} not found"}), 404
