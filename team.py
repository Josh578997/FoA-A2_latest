from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.hash_table import LinearProbeTable
from data_structures.linked_stack import LinkedStack
from data_structures.linked_list import LinkedList
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining
from data_structures.linked_queue import LinkedQueue
from constants import GameResult, PlayerPosition, PlayerStats, TeamStats, Constants
from player import Player
from typing import Collection, Union, TypeVar

T = TypeVar("T")


class Team:
    count = 0
    def __init__(self, team_name: str, players: ArrayR[Player]) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            players (ArrayR[Player]): The players of the team

        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        
        self.initial_player_states = players
        Team.count += 1             #increments the class count by 1 every time an instance of the Team object 
        self.number = Team.count    #is initialised and assigns it to that initialisation.
        self.name = team_name
        self.statistics = LinearProbeTable()
        for stat in TeamStats:
            self.statistics[stat.value] = 0
        self.statistics[TeamStats.LAST_FIVE_RESULTS.value] = LinkedQueue()
        self.players = HashTableSeparateChaining()
        for position in PlayerPosition:
            self.players[position.value] = LinkedList()
        for player in players:
            self.add_player(player)

    def reset_stats(self) -> None:
        """
        Resets all the statistics of the team to the values they were during init.

        Complexity:
            Best Case Complexity: O(1), only 1 statistic
            Worst Case Complexity: O(n), where n is the number of teamStats in the TeamStats Enum class
        """
        for stat in TeamStats:
            self.statistics[stat.value] = 0
        self.statistics[TeamStats.LAST_FIVE_RESULTS.value] = LinkedQueue()


    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(n), n is the number of elements in the players hash table
        """
        self.players[player.position.value].append(player)

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(n), n is the length of the linkedlit in the hashtable position
        """
        playerpos = player.position.value
        player_ind_in_lst = self.players[playerpos].index(player)
        self.players[playerpos].delete_at_index(player_ind_in_lst)
        return None

    def get_number(self) -> int:
        """
        Returns the number of the team.

        Complexity:
            Analysis not required.
        """
        return self.number

    def get_name(self) -> str:
        """
        Returns the name of the team.

        Complexity:
            Analysis not required.
        """
        return self.name

    def get_players(self, position: Union[PlayerPosition, None] = None) -> Union[Collection[Player], None]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (Union[PlayerPosition, None]): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder this includes the ArrayR
            which was previously prohibited.

            None: When no players match the criteria / team has no players

        Complexity:
            Best Case Complexity: O(p), where p is the number of player positions
            Worst Case Complexity: O(p*players), where p is the number of player positions and players is the number of players
        """

        if len(self) == 0:
            return None
        output = LinkedList()
        if position == None:
            for pos in PlayerPosition:
                for player in self.players[pos.value]:
                    output.append(player)
        else:
            for player in self.players[position.value]:
                    output.append(player)
        if len(output) == 0:
            return None
        return output

    def get_statistics(self):
        """
        Get the statistics of the team

        Returns:
            statistics: The teams' statistics

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.statistics

    def get_last_five_results(self) -> Union[Collection[GameResult], None]:
        """
        Returns the last five results of the team.
        If the team has played less than five games,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the array should be an array of size 4
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        **Important Note:**
        If this method is called before the team has played any games,
        return None the reason for this is explained in the specefication.

        Returns:
            Collection[GameResult]: The last five results of the team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(r), r is the length of results
        """
        output = LinkedList()
        results = self.statistics[TeamStats.LAST_FIVE_RESULTS.value]
        results_clone = LinkedQueue()   
        while len(results) > 0:
            served = results.serve()
            results_clone.append(served)
            output.append(served)
        self.statistics[TeamStats.LAST_FIVE_RESULTS.value] = results_clone
        if len(output) > 0:
            return output
        else:
            return None
        

    def get_top_x_players(self, player_stat: PlayerStats, num_players: int) -> list[tuple[int, str, Player]]:
        """
        Note: This method is only required for FIT1054 students only!

        Args:
            player_stat (PlayerStats): The player statistic to use to order the top players
            num_players (int): The number of players to return from this team

        Return:
            list[tuple[int, str, Player]]: The top x players from this team
        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        raise NotImplementedError

    def __setitem__(self, statistic: TeamStats, value: int) -> None:
        """
        Updates the team's statistics.

        Args:
            statistic (TeamStats): The statistic to update
            value (int): The new value of the statistic

        Complexity:
            Best Case Complexity: O(comp), comp is cost of comparison
            Worst Case Complexity: O(comp^2), comp is cost of comparison
        """
        self.statistics[statistic] = value
        if statistic in [TeamStats.WINS.value,TeamStats.DRAWS.value,TeamStats.LOSSES.value]:
            if statistic == TeamStats.WINS.value:
                self.statistics[TeamStats.POINTS.value] +=  GameResult.WIN.value
                self.statistics[TeamStats.LAST_FIVE_RESULTS.value].append(GameResult.WIN)
            elif statistic == TeamStats.DRAWS.value:
                self.statistics[TeamStats.POINTS.value] += GameResult.DRAW.value
                self.statistics[TeamStats.LAST_FIVE_RESULTS.value].append(GameResult.DRAW)
            elif statistic == TeamStats.LOSSES.value:
                self.statistics[TeamStats.POINTS.value] += GameResult.LOSS.value
                self.statistics[TeamStats.LAST_FIVE_RESULTS.value].append(GameResult.LOSS)
        if len(self.statistics[TeamStats.LAST_FIVE_RESULTS.value]) > 5:
            self.statistics[TeamStats.LAST_FIVE_RESULTS.value].serve()
        #if statistic in [TeamStats.GOALS_FOR,TeamStats.GOALS_AGAINST]:
        self.statistics[TeamStats.GOALS_DIFFERENCE.value] = self.statistics[TeamStats.GOALS_FOR.value] - self.statistics[TeamStats.GOALS_AGAINST.value]

    def __getitem__(self, statistic: TeamStats) -> int:
        """
        Returns the value of the specified statistic.

        Args:
            statistic (TeamStats): The statistic to return

        Returns:
            int: The value of the specified statistic

        Raises:
            ValueError: If the statistic is invalid

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.statistics[statistic]

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
            Best Case Complexity: O(1), only one player position
            Worst Case Complexity: O(pos), pos is the number of player positions
        """

        # get number of players not this
        totallength = 0
        for position in self.players.values():
            totallength += len(position)
        return totallength
    def __lt__(self,other:Team) -> bool:
        conditions = [TeamStats.POINTS.value, TeamStats.GOALS_DIFFERENCE.value,TeamStats.GOALS_FOR.value]
        for cond in conditions:
            if self.statistics[cond] != other.statistics[cond]:
                return not (self.statistics[cond] < other.statistics[cond])
        return (self.name < other.name)
    def __gt__(self,other:Team)->bool:
        conditions = [TeamStats.POINTS.value, TeamStats.GOALS_DIFFERENCE.value,TeamStats.GOALS_FOR.value]
        for cond in conditions:
            if self.statistics[cond] != other.statistics[cond]:
                return not (self.statistics[cond] > other.statistics[cond])
        return (self.name > other.name)
    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity:
            Analysis not required.
        """
        return f"{self.name}"

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure."""
        return str(self)

    ## FOR TESTING

if __name__ == "__main__":
    sample_players = [
        Player("Alexey", PlayerPosition.STRIKER, 22),
        Player("Maria", PlayerPosition.MIDFIELDER, 22),
        Player("Brendon", PlayerPosition.DEFENDER, 22),
        Player("Saksham", PlayerPosition.GOALKEEPER, 22),
        Player("Rupert", PlayerPosition.GOALKEEPER, 45),
    ]
    sample_team = Team("Sample Team", ArrayR.from_list(sample_players))
    sample_team[TeamStats.WINS] += 1
    sample_team[TeamStats.LOSSES] += 1
    print('length', len(sample_team.statistics[TeamStats.LAST_FIVE_RESULTS.value]))
    last5 = sample_team.get_last_five_results()
    for item in last5:
        print(item)
