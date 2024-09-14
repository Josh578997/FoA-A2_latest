from data_structures.linked_list import LinkedList
from team import Team
from data_structures.referential_array import ArrayR
from player import Player
from constants import PlayerPosition

sample_players = [
        Player("Alexey", PlayerPosition.STRIKER, 22),
        Player("Maria", PlayerPosition.MIDFIELDER, 22),
        Player("Brendon", PlayerPosition.DEFENDER, 22),
        Player("Saksham", PlayerPosition.GOALKEEPER, 22),
        Player("Rupert", PlayerPosition.GOALKEEPER, 45),
    ]
players = ArrayR(len(sample_players))
for i in range(len(sample_players)):
    players[i] = sample_players[i]

leaderboard = LinkedList()

team1 = Team('Manchester',players)
team2 = Team('Liverpool',players)
team3 = Team('Real Madrid',players)
team4 = Team('Barcelona',players)

teams_list = [team1, team2, team3, team4]
teams = ArrayR(len(teams_list))

for t in range(len(teams_list)):
    teams[i] = teams_list[t]

for team in teams:
    leaderboard.append(team)
for i in range(len(leaderboard)-1):
    for j in range(i+1,len(leaderboard)):
        if leaderboard[i] > leaderboard[j]:
            temp = leaderboard[i]
            leaderboard[i] = leaderboard[j]
            leaderboard[j] = temp

print(str(leaderboard))