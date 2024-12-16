from infrastructure.repositories.goal_repository import GoalRepository

class GoalUsecase:
    def __init__(self, goal_repo: GoalRepository):
        self.goal_repo = goal_repo

    def create_goal(self, goal_data):   
        return self.goal_repo.create_goal(goal_data)
    
    def get_goal(self, goal_id):
        return self.goal_repo.get_goal(goal_id)
    
    def get_goals(self):
        return self.goal_repo.get_goals()