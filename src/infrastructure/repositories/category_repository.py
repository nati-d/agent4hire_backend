from google.cloud import firestore
from domain.models.category import Category, AGENT_CATEGORIES
import uuid

class CategoryRepository:
    def __init__(self):
        self.database = firestore.Client(database='agent-square')
        self._collection_name = "categories"
        self._initialize_categories()

    def _initialize_categories(self):
        """Initialize predefined categories if they don't exist."""
        try:
            existing_categories = list(self.database.collection(self._collection_name).stream())
            if not existing_categories:
                for category in AGENT_CATEGORIES:
                    self.create_category(Category(
                        id=uuid.uuid4().hex,
                        name=category['name'],
                        description=category['description'],
                        agent_id=None
                    ))
        except Exception as e:
            raise e

    def create_category(self, category: Category) -> None:
        try:
            self.database.collection(self._collection_name).document(category.id).set(category.to_dict())
        except Exception as e:
            raise e

    def get_category(self, category_id: str) -> Category:
        try:
            category_doc = self.database.collection(self._collection_name).document(category_id).get()
            if not category_doc.exists:
                return None
            return Category.from_dict(category_doc.to_dict())
        except Exception as e:
            raise e

    def get_all_categories(self) -> list[Category]:
        try:
            categories = self.database.collection(self._collection_name).stream()
            return [Category.from_dict(category.to_dict()) for category in categories]
        except Exception as e:
            raise e

    def get_category_by_agent_id(self, agent_id: str) -> Category:
        try:
            categories = self.database.collection(self._collection_name).where("agent_id", "==", agent_id).stream()
            category_list = [Category.from_dict(category.to_dict()) for category in categories]
            return category_list[0] if category_list else None
        except Exception as e:
            raise e
