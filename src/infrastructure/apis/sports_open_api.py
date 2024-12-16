from espn_api.football import League
from espn_api.basketball import League as BasketballLeague
from espn_api.baseball import League as BaseballLeague
from espn_api.hockey import League as HockeyLeague
import os

class ESPNClient:
    def __init__(self, sport, year, league_id):
        """
        Initializes the ESPN client with the given sport, year, and league ID.
        :param sport: The sport type (e.g., "football", "basketball", "baseball", "hockey").
        :param year: The year of the league.
        :param league_id: The league ID provided by the user.
        """
        if sport == "football":
            self.league = League(league_id=league_id, year=year)
        elif sport == "basketball":
            self.league = BasketballLeague(league_id=league_id, year=year)
        elif sport == "baseball":
            self.league = BaseballLeague(league_id=league_id, year=year)
        elif sport == "hockey":
            self.league = HockeyLeague(league_id=league_id, year=year)
        else:
            raise ValueError(f"Unsupported sport type: {sport}")

    def get_top_headlines(self):
        """
        Fetch top sports headlines (for example, fantasy football league).
        :return: List of headlines
        """
        return self.league.teams

    def get_fantasy_football_data(self):
        """
        Fetch fantasy football league data.
        :return: JSON response with Fantasy Football data or error message
        """
        return self.league.teams

    def get_team_info(self):
        """
        Retrieve team information in a specific sports league.
        :return: Team information from the league
        """
        return self.league.teams

    def get_scoreboard(self):
        """
        Fetch the scoreboard, or latest matchups for the league.
        :return: Matchups or scoreboard data
        """
        return self.league.scoreboard()

    def get_player_stats(self, player_id):
        """
        Fetch player stats (example from football league).
        :param player_id: Player ID
        :return: Player stats
        """
        for team in self.league.teams:
            for player in team.roster:
                if player.playerId == player_id:
                    return player.stats
        return "Player not found"

    def get_league_standings(self):
        """
        Retrieve team standings for the league.
        :return: League standings
        """
        return sorted(self.league.teams, key=lambda x: x.standing)

    def get_event_info(self, event_id):
        """
        Retrieve event information (fantasy event example).
        :param event_id: Event ID
        :return: Event information
        """
        return f"Event info for {event_id}: This can be implemented for live events."

    def get_season_info(self):
        """
        Retrieve information about the league season.
        :return: Season information
        """
        return f"Season info: {self.league.year}"

    def get_live_game_data(self):
        """
        Fetch live game data for fantasy matchups.
        :return: Live game data
        """
        return self.league.scoreboard()

    def get_league_info(self):
        """
        Retrieve league information.
        :return: League information
        """
        return f"League info for {self.league.year}."

    def get_team_roster(self):
        """
        Retrieve the roster for each team.
        :return: Team rosters
        """
        team_rosters = {}
        for team in self.league.teams:
            team_rosters[team.team_name] = [player.name for player in team.roster]
        return team_rosters

    def get_player_career_stats(self, player_id):
        """
        Retrieve career stats for a specific player.
        :param player_id: Player ID
        :return: Career stats or None
        """
        for team in self.league.teams:
            for player in team.roster:
                if player.playerId == player_id:
                    return player.stats
        return "Player not found"

    def get_team_schedule(self):
        """
        Retrieve match schedule for the fantasy league teams.
        :return: Schedule data
        """
        return self.league.scoreboard()


