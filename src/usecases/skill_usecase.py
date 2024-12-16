from domain.models.skill import Skill
from infrastructure.repositories.skill_repository import SkillRepository

class SkillUsecase:
    def __init__(self, skill_repository: SkillRepository):
        self.skill_repository = skill_repository

    def create_skill(self, skill_data: dict) -> Skill:
        skill = Skill.from_dict(skill_data)
        self.skill_repository.create_skill(skill)
        return skill

    def update_skill(self, skill_id: str, skill_data: dict) -> Skill:
        skill = self.skill_repository.get_skill(skill_id)
        if not skill:
            raise ValueError("Skill not found")
        skill.name = skill_data.get('name', skill.name)
        self.skill_repository.update_skill(skill)
        return skill

    def delete_skill(self, skill_id: str) -> None:
        self.skill_repository.delete_skill(skill_id)

    def get_skill(self, skill_id: str) -> Skill:
        skill = self.skill_repository.get_skill(skill_id)
        if not skill:
            raise ValueError("Skill not found")
        return skill

    def get_all_skills(self) -> list[Skill]:
        """Retrieve all skills from the repository."""
        return self.skill_repository.get_all_skills()
