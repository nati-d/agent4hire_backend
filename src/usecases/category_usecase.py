from typing import List, Optional
from domain.models.category import Category, AGENT_CATEGORIES
import uuid
from infrastructure.llm.open_ai_llm import OpenAiLLMService

class CategoryUsecase:
    def __init__(self, category_repository, llm_service: OpenAiLLMService):
        self.category_repository = category_repository
        self.llm_service = llm_service

    def create_category(self, name: str, description: str, agent_id: Optional[str] = None) -> Category:
        """Create a new category with validation and business logic."""
        try:
            # Validate name uniqueness
            existing_categories = self.category_repository.get_all_categories()
            if any(cat.name.lower() == name.lower() for cat in existing_categories):
                raise ValueError(f"Category with name '{name}' already exists")

            # Validate description quality using LLM
            if not self._validate_description(name, description):
                raise ValueError("Description is not sufficiently descriptive or relevant to the category name")

            # Create and store category
            category = Category(
                id=uuid.uuid4().hex,
                name=name,
                description=description,
                agent_id=agent_id
            )
            self.category_repository.create_category(category)
            return category

        except Exception as e:
            raise RuntimeError(f"Error creating category: {str(e)}")

    def get_categories(self) -> List[Category]:
        """Get all categories with optional filtering and sorting."""
        try:
            return self.category_repository.get_all_categories()
        except Exception as e:
            raise RuntimeError(f"Error fetching categories: {str(e)}")

    def get_category(self, category_id: str) -> Optional[Category]:
        """Get a specific category by ID."""
        try:
            category = self.category_repository.get_category(category_id)
            if not category:
                raise ValueError(f"Category with ID '{category_id}' not found")
            return category
        except Exception as e:
            raise RuntimeError(f"Error fetching category: {str(e)}")

    def get_category_by_agent_id(self, agent_id: str) -> Optional[Category]:
        """Get the category associated with a specific agent."""
        try:
            return self.category_repository.get_category_by_agent_id(agent_id)
        except Exception as e:
            raise RuntimeError(f"Error fetching category for agent: {str(e)}")

    def _validate_description(self, name: str, description: str) -> bool:
        """Validate category description using LLM."""
        system_instruction = """You are an AI assistant designed to validate category descriptions for an AI agent system."""
        
        query = f"""Evaluate if this category description is sufficiently descriptive and relevant.
        
        Category Name: {name}
        Description: {description}
        
        Requirements:
        1. Description should clearly explain the category's purpose
        2. Description should be relevant to the category name
        3. Description should be specific enough to distinguish from other categories
        4. Description should be professional and well-written
        
        Return only 'true' if the description meets all requirements, or 'false' if it doesn't."""

        response = self.llm_service.generate_content(
            system_instruction=system_instruction,
            query=query
        )
        
        return response.strip().lower() == 'true'

    def suggest_description(self, name: str) -> str:
        """Generate a suggested description for a category name."""
        system_instruction = """You are an AI assistant designed to generate professional category descriptions."""
        
        query = f"""Generate a clear and professional description for this AI agent category.
        
        Category Name: {name}
        
        Requirements:
        1. Description should clearly explain the category's purpose
        2. Description should be relevant to the category name
        3. Description should be specific enough to distinguish from other categories
        4. Description should be concise (max 100 characters)
        
        Return only the description text."""

        return self.llm_service.generate_content(
            system_instruction=system_instruction,
            query=query
        ).strip()

    def initialize_default_categories(self) -> None:
        """Initialize the default categories if they don't exist."""
        try:
            existing_categories = self.category_repository.get_all_categories()
            if not existing_categories:
                for category_data in AGENT_CATEGORIES:
                    self.create_category(
                        name=category_data['name'],
                        description=category_data['description']
                    )
        except Exception as e:
            raise RuntimeError(f"Error initializing default categories: {str(e)}")

    def validate_category_exists(self, category_id: str) -> bool:
        """Validate that a category exists."""
        try:
            category = self.category_repository.get_category(category_id)
            return category is not None
        except Exception:
            return False
