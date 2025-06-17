from weaviate import connect_to_weaviate_cloud
from weaviate.auth import AuthApiKey
from weaviate.classes.config import Property, DataType
import os

client = connect_to_weaviate_cloud(
    cluster_url=os.environ.get("WEAVIATE_URL"),
    auth_credentials=AuthApiKey(os.environ.get("WCS_API_KEY")),
    headers={
        "X-Openai-Api-Key": os.environ.get("OPENAI_API_KEY")
    }
)

collection = client.collections.get("Structure")
schema = collection.config.properties
existing_fields = [prop.name for prop in schema]

if "id" not in existing_fields:
    collection.config.add_property(
        Property(name="id", data_type=DataType.TEXT)
    )
    print("✅ 'id' 필드 추가 완료!")
else:
    print("ℹ️ 'id' 필드는 이미 존재합니다.")
