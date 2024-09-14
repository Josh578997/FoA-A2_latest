from enum import Enum
import math
class PlayerStats(Enum):
    GAMES_PLAYED = "Games Played"
    GOALS = "Goals"
    ASSISTS = "Assists"
    TACKLES = "Tackles"
    INTERCEPTIONS = "Interceptions"
    STAR_SKILL = "Star Skill"
    WEAK_FOOT_ABILITY = "Weak Foot Ability"
    WEIGHT = "Weight"
    HEIGHT = "Height"

for key in PlayerStats:
    step = 0
    hash_base = 53
    offset = 89
    key = key.value
    table_size  =13
    for i,char in enumerate(key):
        step+= ((ord(char)+len(key))*(hash_base**i))%offset*4
        step%=table_size
    if step >= 5:
        step%= 5

    print(f'{key}: {step}')