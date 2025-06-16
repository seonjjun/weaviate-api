from flask import Flask, request, jsonify
import weaviate, os

app = Flask(__name__)

client = weaviate.Client(
    url=os.environ.get("WEAVIATE_URL"),
    additional_headers={"X-OpenAI-Api-Key": os.environ.get("OPENAI_API_KEY")}
)

@app.route('/store', methods=['POST'])
def store():
    data = request.json
    client.data_object.create(
        data_object={"name": data.get("name"), "content": data.get("content")},
        class_name="Structure"
    )
    return jsonify({"status": "stored"})

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get("query")
    result = client.query.get("Structure", ["name", "content"])\
        .with_near_text({"concepts": [query]})\
        .with_limit(1).do()
    return jsonify(result)
