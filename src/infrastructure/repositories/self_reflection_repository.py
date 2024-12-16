from google.cloud import firestore
from domain.models.self_reflection import SelfReflection


class SelfReflectionRepository:
    def __init__(self):
        self.database = firestore.Client(database="agent-square")
        self._collection_name = "self_reflection"

    def create_self_reflection(self, self_reflection_data: SelfReflection) -> None:
        try:
            self.database.collection(self._collection_name).document(
                self_reflection_data.id
            ).set(self_reflection_data.to_dict())
        except Exception as e:
            raise e

    def get_self_reflection(self, self_reflection_id: str) -> SelfReflection:
        try:
            self_reflection = (
                self.database.collection(self._collection_name)
                .document(self_reflection_id)
                .get()
            )
            return SelfReflection.from_dict(self_reflection.to_dict())
        except Exception as e:
            raise e

    def update_self_reflection(self, self_reflection_data: SelfReflection) -> None:
        try:
            self.database.collection(self._collection_name).document(
                self_reflection_data.id
            ).update(self_reflection_data.to_dict())
        except Exception as e:
            raise e
