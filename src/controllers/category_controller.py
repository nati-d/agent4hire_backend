from flask import jsonify, request
from domain.models.category import Category

class CategoryController:
    def __init__(self, category_usecase):
        self.category_usecase = category_usecase

    def create_category(self):
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(key in data for key in ['name', 'description']):
                return jsonify({
                    'error': 'Missing required fields. Need name and description'
                }), 400

            # Create category using usecase
            category = self.category_usecase.create_category(
                name=data['name'],
                description=data['description'],
                agent_id=data.get('agent_id')
            )

            return jsonify({
                'message': 'Category created successfully',
                'category': category.to_dict()
            }), 201

        except ValueError as e:
            return jsonify({
                'error': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'error': str(e)
            }), 500

    def get_categories(self):
        try:
            categories = self.category_usecase.get_categories()
            return jsonify([category.to_dict() for category in categories]), 200
        except Exception as e:
            return jsonify({
                'error': str(e)
            }), 500

    def get_category(self, category_id):
        try:
            category = self.category_usecase.get_category(category_id)
            if not category:
                return jsonify({
                    'error': 'Category not found'
                }), 404
            return jsonify(category.to_dict()), 200
        except ValueError as e:
            return jsonify({
                'error': str(e)
            }), 404
        except Exception as e:
            return jsonify({
                'error': str(e)
            }), 500

    def suggest_description(self):
        try:
            data = request.get_json()
            if 'name' not in data:
                return jsonify({
                    'error': 'Missing required field: name'
                }), 400

            description = self.category_usecase.suggest_description(data['name'])
            return jsonify({
                'suggested_description': description
            }), 200
        except Exception as e:
            return jsonify({
                'error': str(e)
            }), 500
