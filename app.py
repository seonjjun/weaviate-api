from flask import Flask, request, jsonify
import weaviate
from weaviate.auth import AuthApiKey
import os

app = Flask(__name__)

# ✅ 최신 방식: connect_to_weaviate_cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.environ.get("WEAVIATE_URL"),
    auth_credentials=AuthApiKey(api_key=os.environ.get("WCS_API_KEY")),
    headers={
        "X-Openai-Api-Key": os.environ.get("OPENAI_API_KEY")
    }
)

collection = client.collections.get("Structure")

@app.route('/store', methods=['POST'])
def store():
    data = request.json
    collection.data.insert({
        "name": data.get("name"),
        "content": data.get("content")
    })
    return jsonify({"status": "stored"})

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get("query")
    result = collection.query.near_text(query=query, limit=1)
    return jsonify(result.objects)
