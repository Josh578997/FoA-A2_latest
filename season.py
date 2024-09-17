from __future__ import annotations
from data_structures.bset import BSet
from data_structures.referential_array import ArrayR
from data_structures.linked_list import LinkedList
from algorithms import mergesort
from dataclasses import dataclass
from team import Team
from typing import Generator, Union
from game_simulator import GameSimulator
from constants import TeamStats,GameResult,PlayerStats,PlayerPosition,Constants,ResultStats
from data_structures.array_sorted_list import ArraySortedList


@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html
    """
    home_team: Team = None
    away_team: Team = None


class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        """
        self.games: ArrayR[Game] = games
        self.week: int = week

    def get_games(self) -> ArrayR:
        """
        Returns the games in a given week.

        Returns:
            ArrayR: The games in a given week.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.games

    def get_week(self) -> int:
        """
        Returns the week number.

        Returns:
            int: The week number.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.week

    def __iter__(self):
        """
        Complexity:
        Best Case Complexity:
        Worst Case Complexity:
        """
        raise NotImplementedError

    def __next__(self):
        """
        Complexity:
        Best Case Complexity:
        Worst Case Complexity:
        """
        raise NotImplementedError


class Season:

    def __init__(self, teams: ArrayR[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams played in this season.

        Complexity:
            Best Case Complexity: O(S), S is the length of the schedule array
            Worst Case Complexity: O(N^2+S), N is the number of the teams in the season, S is the length of the schedule array
        """
        
        self.teams = teams
        self.leaderboard = ArraySortedList(len(teams))
        for team in teams:
            self.leaderboard.add(team)
        # for i in range(len(self.leaderboard)-1):
        #     for j in range(i+1,len(self.leaderboard)):
        #         if self.leaderboard[i].name > self.leaderboard[j].name:
        #             temp = self.leaderboard[i]
        #             self.leaderboard[i] = self.leaderboard[j]
        #             self.leaderboard[j] = temp
        self.schedule = LinkedList()
        schedule_array = self._generate_schedule()
        for week in schedule_array:
            self.schedule.append(week)
    def _generate_schedule(self) -> ArrayR[ArrayR[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:
            ArrayR[ArrayR[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        """
        num_teams: int = len(self.teams)
        weekly_games: list[ArrayR[Game]] = []
        flipped_weeks: list[ArrayR[Game]] = []
        games: list[Game] = []

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: list[Game] = []
            flipped_week: list[Game] = []
            used_teams: BSet = BSet()

            week_game_no: int = 0
            for game in games[:]:  # Iterate over a copy of the list
                if game.home_team.get_number() not in used_teams and game.away_team.get_number() not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.get_number())
                    used_teams.add(game.away_team.get_number())

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(ArrayR.from_list(current_week))
            flipped_weeks.append(ArrayR.from_list(flipped_week))
            week += 1

        return ArrayR.from_list(weekly_games + flipped_weeks)

    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
            Assume simulate_game is O(1)
            Remember to define your variables and their complexity.

            Best Case Complexity:
            Worst Case Complexity:
        """
        for week in self.schedule:
            for game in week:
                #updating results values
                results = GameSimulator.simulate(game.home_team,game.away_team)
                if results[ResultStats.HOME_GOALS.value]>results[ResultStats.AWAY_GOALS.value]:
                    game.home_team[TeamStats.WINS.value] = game.home_team.statistics[TeamStats.WINS.value] + 1
                    game.away_team[TeamStats.LOSSES.value] += 1
                elif results[ResultStats.HOME_GOALS.value]==results[ResultStats.AWAY_GOALS.value]:
                    game.home_team[TeamStats.DRAWS.value] += 1
                    game.away_team[TeamStats.DRAWS.value] += 1
                else:
                    game.home_team[TeamStats.LOSSES.value] += 1
                    game.away_team[TeamStats.WINS.value] += 1

                #updating goals for/against
                game.home_team[TeamStats.GOALS_FOR.value] += results[ResultStats.HOME_GOALS.value]
                game.home_team[TeamStats.GOALS_AGAINST.value] += results[ResultStats.AWAY_GOALS.value]
                game.away_team[TeamStats.GOALS_FOR.value] += results[ResultStats.AWAY_GOALS.value]
                game.away_team[TeamStats.GOALS_AGAINST.value] += results[ResultStats.HOME_GOALS.value]

                #updating games played
                game.home_team[TeamStats.GAMES_PLAYED.value] += 1
                game.away_team[TeamStats.GAMES_PLAYED.value] += 1 

                #updating player stats
                for player_list in [game.home_team.get_players(), game.away_team.get_players()]:
                    for player in player_list:
                        player.statistics[PlayerStats.GAMES_PLAYED.value] += 1
                        if results[ResultStats.GOAL_SCORERS.value] == None:
                            pass
                        elif player.name in results[ResultStats.GOAL_SCORERS.value]:
                            for player_name in results[ResultStats.GOAL_SCORERS.value]:
                                if player_name == player.name:
                                    player.statistics[PlayerStats.GOALS.value] += 1
                        if results[ResultStats.GOAL_ASSISTS.value] == None:
                            pass
                        elif player.name in results[ResultStats.GOAL_ASSISTS.value]:
                            for player_name in results[ResultStats.GOAL_ASSISTS.value]:
                                if player_name == player.name:
                                    player.statistics[PlayerStats.ASSISTS.value] += 1
                        if results[ResultStats.INTERCEPTIONS.value] == None:
                            pass
                        elif player.name in results[ResultStats.INTERCEPTIONS.value]:
                            for player_name in results[ResultStats.INTERCEPTIONS.value]:
                                if player_name == player.name:
                                    player.statistics[PlayerStats.INTERCEPTIONS.value] += 1
                        if results[ResultStats.TACKLES.value]==None:
                            pass
                        elif player.name in results[ResultStats.TACKLES.value]:
                            for player_name in results[ResultStats.TACKLES.value]:
                                if player_name == player.name:
                                    player.statistics[PlayerStats.TACKLES.value] += 1
                # re initialize leaderboard to get values in right order;
                temp_list = self.leaderboard
                self.leaderboard = ArraySortedList(len(self.teams))
                for team in temp_list:
                    self.leaderboard.add(team)

    def delay_week_of_games(self, orig_week: int, new_week: Union[int, None] = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (Union[int, None]): The new week to move the games to. If this is None, it moves the games to the end of the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(N), N is the length of the schedule linked list
        """
        temp = self.schedule[orig_week-1]
        if isinstance(new_week,int):
            self.schedule.delete_at_index(orig_week-1)
            self.schedule.insert(new_week-1,temp)
        elif new_week == None:
            self.schedule.delete_at_index(orig_week-1)
            self.schedule.append(temp)

    def get_next_game(self) -> Union[Generator[Game], None]:
        """
        Gets the next game in the season.

        Returns:
            Game: The next game in the season.
            or None if there are no more games left.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        iter(self.schedule)
        return next(self.schedule)

    def get_leaderboard(self) -> ArrayR[ArrayR[Union[int, str]]]:
        """
        Generates the final season leaderboard.

        Returns:
            ArrayR(ArrayR[ArrayR[Union[int, str]]]):
                Outer array represents each team in the leaderboard
                Inner array consists of 10 elements:
                    - Team name (str)
                    - Games Played (int)
                    - Points (int)
                    - Wins (int)
                    - Draws (int)
                    - Losses (int)
                    - Goals For (int)
                    - Goals Against (int)
                    - Goal Difference (int)
                    - Previous Five Results (ArrayR(str)) where result should be WIN LOSS OR DRAW

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        outer_array = ArrayR(len(self.leaderboard))
        team_stats_list = []
        for stat in TeamStats:
            team_stats_list.append(stat.value)
        for i in range(len(self.leaderboard)):
            team_array = ArrayR(len(TeamStats)+1)
            team_array[0] = self.leaderboard[i].get_name()
            for j in range(len(TeamStats)-1):
                team_array[j+1] = self.leaderboard[i].statistics[team_stats_list[j]]
            team_array[len(team_array)-1] = self.leaderboard[i].get_last_five_results()
            outer_array[i] = team_array
        return outer_array
        

    def get_teams(self) -> ArrayR[Team]:
        """
        Returns:
            PlayerPosition (ArrayR(Team)): The teams participating in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.teams

    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return len(self.teams)

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the season object.

        Complexity:
            Analysis not required.
        """
        return f'Schedule: {str(self.schedule)}'

    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return str(self)
