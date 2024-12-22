from google.cloud import firestore
from domain.models.trait import Traits

class TraitsRepository:
    def __init__(self):
        self.database = firestore.Client(database='agent-square')
        self._collection_name = "traits"

    def create_trait(self, trait: Traits) -> None:
        try:
            self.database.collection(self._collection_name).document(trait.id).set(trait.to_dict())
        except Exception as e:
            raise e

    def get_trait(self, trait_id: str) -> Traits:
        try:
            trait_doc = self.database.collection(self._collection_name).document(trait_id).get()
            if not trait_doc.exists:
                return None
            return Traits.from_dict(trait_doc.to_dict())
        except Exception as e:
            raise e

    def update_trait(self, trait: Traits) -> None:
        try:
            self.database.collection(self._collection_name).document(trait.id).update(trait.to_dict())
        except Exception as e:
            raise e

    def delete_trait(self, trait_id: str) -> None:
        try:
            self.database.collection(self._collection_name).document(trait_id).delete()
        except Exception as e:
            raise e

    def get_traits_by_agent_id(self, agent_id: str) -> list[Traits]:
        try:
            traits = self.database.collection(self._collection_name).where(
                 "agent_id", "==", agent_id).stream()
            return [Traits.from_dict(trait.to_dict()) for trait in traits]
        except Exception as e:
            raise e

    def get_all_traits(self) -> list[Traits]:
        try:
            traits = self.database.collection(self._collection_name).stream()
            print(traits, "traits from db")
            return [Traits.from_dict(trait.to_dict()) for trait in traits]
        except Exception as e:
            raise e

