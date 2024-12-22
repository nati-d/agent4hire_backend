from google.cloud import firestore
from domain.models.tag import Tags

class TagsRepository:
    def __init__(self):
        self.database = firestore.Client(database='agent-square')
        self._collection_name = "tags"

    def create_tag(self, tag: Tags) -> None:
        try:
            self.database.collection(self._collection_name).document(tag.id).set(tag.to_dict())

        except Exception as e:
            raise e

    def get_tag(self, tag_id: str) -> Tags:
        try:
            tag_doc = self.database.collection(self._collection_name).document(tag_id).get()
            if not tag_doc.exists:
                return None
            return Tags.from_dict(tag_doc.to_dict())
        except Exception as e:
            raise e

    def update_tag(self, tag: Tags) -> None:
        try:
            self.database.collection(self._collection_name).document(tag.id).update(tag.to_dict())
        except Exception as e:
            raise e

    def delete_tag(self, tag_id: str) -> None:
        try:
            self.database.collection(self._collection_name).document(tag_id).delete()
        except Exception as e:
            raise e

    def get_tags_by_agent_id(self, agent_id: str) -> list[Tags]:
        try:
            tags = self.database.collection(self._collection_name).where(
                "agent_id", "==", agent_id).stream()
            return [Tags.from_dict(tag.to_dict()) for tag in tags]
        except Exception as e:
            raise e

    def get_all_tags(self) -> list[Tags]:
        try:
            tags = self.database.collection(self._collection_name).stream()
            print(tags, "tags from db")
            return [Tags.from_dict(tag.to_dict()) for tag in tags]
        except Exception as e:
            raise e
