from google.cloud import firestore
from domain.models.skill import Skill

class SkillRepository:
    def __init__(self):
        self.database = firestore.Client(database='agent-square')
        self._collection_name = "skills"

    def create_skill(self, skill: Skill) -> None:
        try:
            self.database.collection(self._collection_name).document(skill.id).set(skill.to_dict())
        except Exception as e:
            raise e

    def get_skill(self, skill_id: str) -> Skill:
        try:
            skill_doc = self.database.collection(self._collection_name).document(skill_id).get()
            if not skill_doc.exists:
                return None
            return Skill.from_dict(skill_doc.to_dict())
        except Exception as e:
            raise e

    def update_skill(self, skill: Skill) -> None:
        try:
            self.database.collection(self._collection_name).document(skill.id).update(skill.to_dict())
        except Exception as e:
            raise e

    def delete_skill(self, skill_id: str) -> None:
        try:
            self.database.collection(self._collection_name).document(skill_id).delete()
        except Exception as e:
            raise e

    def get_skills_by_agent_id(self, agent_id: str) -> list[Skill]:
        try:
            skills = self.database.collection(self._collection_name).where(
                "agents", "array_contains", agent_id).stream()
            return [Skill.from_dict(skill.to_dict()) for skill in skills]
        except Exception as e:
            raise e

    def get_all_skills(self) -> list[Skill]:
        try:
            skills = self.database.collection(self._collection_name).stream()
            print(skills, "skills from db")
            return [Skill.from_dict(skill.to_dict()) for skill in skills]
        except Exception as e:
            raise e
        
