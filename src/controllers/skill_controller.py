# from flask import Blueprint, request, jsonify
# from usecases.skill_usecase import SkillUsecase
# from infrastructure.repositories.skill_repository import SkillRepository

# # Create a Blueprint for the skills
# skills_bp = Blueprint('skills', __name__)

# # Initialize the SkillRepository
# skill_repository = SkillRepository()

# # Initialize the SkillUsecase with the repository
# skill_usecase = SkillUsecase(skill_repository=skill_repository)

# @skills_bp.route('/skills', methods=['POST'])
# def create_skill():
#     try:
#         skill_data = request.json
#         skill = skill_usecase.create_skill(skill_data)
#         return jsonify(skill.to_dict()), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @skills_bp.route('/skills/<string:skill_id>', methods=['GET'])
# def get_skill(skill_id):
#     try:
#         skill = skill_usecase.get_skill(skill_id)
#         return jsonify(skill.to_dict()), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @skills_bp.route('/skills', methods=['GET'])
# def get_all_skills():
#     try:
#         skills = skill_usecase.get_all_skills()
#         return jsonify([skill.to_dict() for skill in skills]), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
