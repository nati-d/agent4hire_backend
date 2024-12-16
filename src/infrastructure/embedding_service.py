import chromadb
from chromadb.utils import embedding_functions
import os
from typing import List, Dict, Any
import uuid
from collections import OrderedDict


class EmbeddingService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
            api_key=os.getenv('GEMINI_API_KEY')
        )
        print("Initialized EmbeddingService")
        
        # Create generic collections for APIs, goals, sub-goals, and workstreams
        self.collections = {
            "api_collection": self.client.get_or_create_collection(
                name="api_collection",
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            ),
            "goal_collection": self.client.get_or_create_collection(
                name="goal_collection",
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            ),
            "sub_goal_collection": self.client.get_or_create_collection(
                name="sub_goal_collection",
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            ),
            "workstream_collection": self.client.get_or_create_collection(
                name="workstream_collection",
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            )
        }
        print("Initialized collections for APIs, goals, sub-goals, and workstreams")

    def _add_entities(self, collection_name: str, entities: List[Dict[str, Any]]):
        """Generic method to add entities to a collection with deduplication."""
        print(f"Processing {len(entities)} entities for addition to {collection_name}")
        collection = self.collections[collection_name]
        
        # Fetch existing content to avoid duplicates
        existing_content = set()
        try:
            existing_results = collection.get()
            if existing_results and 'documents' in existing_results:
                existing_content = set(existing_results['documents'])
        except Exception as e:
            print(f"Warning: Could not fetch existing content: {e}")

        unique_entities = []
        seen_descriptions = set(existing_content)
        
        # Deduplicate based on the description content
        for entity in entities:
            description = entity["description"].strip()
            if description not in seen_descriptions:
                unique_entities.append(entity)
                seen_descriptions.add(description)
            else:
                print(f"Skipping duplicate entity: {entity.get('name', 'Unnamed')}")

        if not unique_entities:
            print("No new unique entities to add")
            return

        documents = []
        ids = []
        metadatas = []

        for entity in unique_entities:
            new_id = str(uuid.uuid4())
            documents.append(entity["description"])
            ids.append(new_id)
            metadatas.append({
                "name": entity.get("name"),
                "type": entity.get("type"),
                "hash": hash(description)  # Store content hash for future comparison
            })

        try:
            collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            print(f"Successfully added {len(unique_entities)} unique entities to {collection_name}")
        except Exception as e:
            print(f"Error adding entities: {e}")

    def add_entities(self, entities: List[Dict[str, Any]], entity_type: str):
        """Public method to add entities by type."""
        type_to_collection = {
            "api": "api_collection",
            "goal": "goal_collection",
            "sub_goal": "sub_goal_collection",
            "workstream": "workstream_collection"
        }
        
        collection_name = type_to_collection.get(entity_type.lower())
        if not collection_name:
            print(f"Invalid entity type: {entity_type}")
            return
        
        self._add_entities(collection_name, entities)

    def search_relevant_entities(self, query: str, entity_type: str, n_results: int = 30) -> List[Dict]:
        """Generic method to search for relevant entities with deduplication of results."""
        collection_name = {
            "api": "api_collection",
            "goal": "goal_collection",
            "sub_goal": "sub_goal_collection",
            "workstream": "workstream_collection"
        }.get(entity_type.lower())
        
        if not collection_name:
            print(f"Invalid entity type: {entity_type}")
            return []

        collection = self.collections[collection_name]

        try:
            results = collection.query(
                query_texts=[query],
                n_results=n_results * 2  # Request more results to account for potential duplicates
            )
            
            unique_results = OrderedDict()
            
            for metadata, document, id in zip(
                results['metadatas'][0],
                results['documents'][0],
                results['ids'][0]
            ):
                content_key = document.strip()
                
                if content_key not in unique_results:
                    unique_results[content_key] = {
                        "name": metadata['name'],
                        "description": document,
                        "type": metadata['type'],
                        "id": id
                    }
                    
                    if len(unique_results) >= n_results:
                        break
            
            return list(unique_results.values())
            
        except Exception as e:
            print(f"Error during search: {e}")
            return []

    def remove_duplicates(self, collection_name: str):
        """Remove duplicate entries from a specified collection based on content."""
        collection = self.collections.get(collection_name)
        if not collection:
            print(f"Invalid collection name: {collection_name}")
            return

        try:
            results = collection.get()
            if not results or 'documents' not in results:
                print("No documents found in collection")
                return

            seen_content = {}
            duplicate_ids = []

            for idx, (doc, id) in enumerate(zip(results['documents'], results['ids'])):
                content = doc.strip()
                if content in seen_content:
                    duplicate_ids.append(id)
                else:
                    seen_content[content] = id

            if duplicate_ids:
                for duplicate_id in duplicate_ids:
                    collection.delete(ids=[duplicate_id])
                print(f"Removed {len(duplicate_ids)} duplicate entries from {collection_name}")
            else:
                print("No duplicates found")

        except Exception as e:
            print(f"Error removing duplicates: {e}")

    def clear_collection(self, collection_name: str):
        """Clear a specified collection."""
        collection = self.collections.get(collection_name)
        if not collection:
            print(f"Invalid collection name: {collection_name}")
            return

        try:
            collection.delete(where={})
            print(f"{collection_name} cleared successfully")
        except Exception as e:
            print(f"Error clearing {collection_name}: {e}")

    def clear_all_collections(self):
        """Clear all collections."""
        for name, collection in self.collections.items():
            self.clear_collection(name)


class UserEmbeddingService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
            api_key=os.getenv('GEMINI_API_KEY')
        )
        print("Initialized UserEmbeddingService")
        
        self.collection = self.client.get_or_create_collection(
            name="user_descriptions",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )
        print("Initialized user_descriptions collection")

    def add_user_data(self, user_id: str, user_data: Dict[str, List[str]]):
        """
        Add user descriptions (persona and specifications) to the collection.
        
        :param user_id: Unique identifier for the user.
        :param user_data: Dictionary containing 'user_persona' and 'specific_needs'.
        """
        print(f"Adding data for user_id: {user_id}")
        
        documents = []
        ids = []
        metadatas = []
        
        # Add user persona
        persona_id = f"{user_id}_persona"
        persona_text = user_data['user_persona'].strip()
        documents.append(persona_text)
        ids.append(persona_id)
        metadatas.append({
            "type": "persona",
            "user_id": user_id,
            "content_key": persona_text
        })
        
        # Add specific needs
        for i, spec in enumerate(user_data['specific_needs']):
            spec_id = f"{user_id}_spec_{i}"
            spec_text = spec.strip()
            documents.append(spec_text)
            ids.append(spec_id)
            metadatas.append({
                "type": "specification",
                "user_id": user_id,
                "content_key": spec_text
            })
        
        try:
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            print(f"Successfully added data for user_id: {user_id}")
        except Exception as e:
            print(f"Error adding user data: {e}")

    def retrieve_user_info(self, query: str, user_id: str, n_results: int = 3) -> str:
        """
        Retrieve relevant user information based on the query.
        
        :param query: The user's query.
        :param user_id: Unique identifier for the user.
        :param n_results: Number of relevant pieces of information to retrieve.
        :return: A string containing the concatenated relevant user information.
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where={"user_id": user_id}
            )
            
            if results['documents']:
                relevant_texts = results['documents'][0]
                return "\n".join(relevant_texts)
            else:
                return ""
        except Exception as e:
            print(f"Error during retrieval: {e}")
            return ""

    def remove_user_data(self, user_id: str):
        """
        Remove all data associated with a specific user.
        
        :param user_id: Unique identifier for the user.
        """
        try:
            self.collection.delete(where={"user_id": user_id})
            print(f"Removed data for user_id: {user_id}")
        except Exception as e:
            print(f"Error removing user data: {e}")