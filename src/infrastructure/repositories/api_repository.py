from google.cloud import firestore
from domain.models.api import API

class APIRepository:
    def __init__(self):
        self.database = firestore.Client(database='agent-square')
        self._collection_name = "apis"

    def get_all_apis(self) -> list[API]:
        try:
            apis = self.database.collection(self._collection_name).stream()
            res = [API.from_dict(api.to_dict()) for api in apis]
            return res
        except Exception as e:
            raise e