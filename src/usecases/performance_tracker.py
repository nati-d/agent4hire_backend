from infrastructure.performance_analyzer import PerformanceAnalyzer
from infrastructure.repositories.agent_repository import AgentRepository
from infrastructure.repositories.goal_repository import GoalRepository
from infrastructure.repositories.sub_goal_repository import SubGoalRepository
from infrastructure.repositories.workstream_repository import WorkstreamRepository


class PerformanceTracker:
    def __init__(self,agent_repository: AgentRepository, goal_repository: GoalRepository, sub_goal_repository: SubGoalRepository, workstream_repository: WorkstreamRepository, performance_analyzer: PerformanceAnalyzer):
        self.agent_repository = agent_repository
        self.goal_repository = goal_repository
        self.sub_goal_repository = sub_goal_repository
        self.workstream_repository = workstream_repository
        self.performance_analyzer = performance_analyzer

    def update_performance_data(self, workstream_id: str, modules_performance: list[dict]) -> None:
        workstream = self.workstream_repository.get_workstream(workstream_id)
        prev_workstream_performance_data = self.workstream_repository.get_performance_data(workstream_id)
        curr_workstream_performance_data = self.performance_analyzer.analyze_workstream_performance(workstream, modules_performance)
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        
        if prev_workstream_performance_data is not None:
            curr_workstream_performance_data = self.performance_analyzer.update_performance_data(prev_workstream_performance_data, curr_workstream_performance_data)
        
        print(curr_workstream_performance_data)
        self.workstream_repository.add_performance_data(workstream_id, curr_workstream_performance_data)

        sub_goal = self.sub_goal_repository.get_sub_goal(workstream.sub_goal_id)
        prev_sub_goal_performance_data = self.sub_goal_repository.get_performance_data(sub_goal.id)
        curr_sub_goal_performance_data = self.performance_analyzer.analyze_sub_goal_performance(sub_goal,workstream, curr_workstream_performance_data)

        if prev_sub_goal_performance_data is not None:
            curr_sub_goal_performance_data = self.performance_analyzer.update_performance_data(prev_sub_goal_performance_data, curr_sub_goal_performance_data)

        print(curr_sub_goal_performance_data)
        self.sub_goal_repository.add_performance_data(sub_goal.id, curr_sub_goal_performance_data)

        goal = self.goal_repository.get_goal(sub_goal.goal_id)
        prev_goal_performance_data = self.goal_repository.get_performance_data(goal.id)
        curr_goal_performance_data = self.performance_analyzer.analyze_goal_performance(goal, sub_goal, curr_sub_goal_performance_data)

        if prev_goal_performance_data is not None:
            curr_goal_performance_data = self.performance_analyzer.update_performance_data(prev_goal_performance_data, curr_goal_performance_data)
        
        print(curr_goal_performance_data)
        self.goal_repository.add_performance_data(goal.id, curr_goal_performance_data)
        
        agent = self.agent_repository.get_agent(goal.agent_id)
        prev_agent_performance_data = self.agent_repository.get_performance_data(agent.id)
        curr_agent_performance_data = self.performance_analyzer.analyze_agent_performance(agent, goal, curr_goal_performance_data)

        if prev_agent_performance_data is not None:
            curr_agent_performance_data = self.performance_analyzer.update_performance_data(prev_agent_performance_data, curr_agent_performance_data)

        print(curr_agent_performance_data)
        self.agent_repository.add_performance_data(agent.id, curr_agent_performance_data)