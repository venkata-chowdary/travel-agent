from langsmith import Client
import os

_client = None

def get_langsmith_client() -> Client:
    global _client
    if _client is None:
        _client = Client(
            api_key=os.getenv("LANGSMITH_API_KEY")
        )
    return _client