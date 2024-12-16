import json
from google.cloud import firestore
from typing import Optional

from domain.models.function_meta_data import FunctionMetadata


class FunctionMetadataRepository:
    def __init__(self):
        self.database = firestore.Client()
        self._collection_name = "function_metadata"

    def add_function_metadata(self, metadata: FunctionMetadata) -> bool:
        """Adds function metadata if it doesn’t already exist."""
        doc_ref = self.database.collection(self._collection_name).document(metadata.name)
        if not doc_ref.get().exists:
            doc_ref.set(metadata.to_dict())
            return True
        return False  # Metadata with this function name already exists

    def get_function_metadata(self, name: str) -> Optional[FunctionMetadata]:
        """Retrieves metadata for a specific function by name."""
        doc = self.database.collection(self._collection_name).document(name).get()
        if doc.exists:
            return FunctionMetadata.from_dict(doc.to_dict())
        return None

    def get_all_function_metadata(self) -> list:
        """Retrieves all function metadata."""
        docs = self.database.collection(self._collection_name).stream()
        return [FunctionMetadata.from_dict(doc.to_dict()) for doc in docs]

    def update_function_metadata(self, metadata: FunctionMetadata) -> bool:
        """Updates existing function metadata if it exists."""
        doc_ref = self.database.collection(self._collection_name).document(metadata.name)
        if doc_ref.get().exists:
            doc_ref.update(metadata.to_dict())
            return True
        return False  # Metadata not found

    def delete_function_metadata(self, name: str) -> bool:
        """Deletes function metadata if it exists."""
        doc_ref = self.database.collection(self._collection_name).document(name)
        if doc_ref.get().exists:
            doc_ref.delete()
            return True
        return False  # Metadata not found
