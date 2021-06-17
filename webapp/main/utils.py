from itertools import combinations
from collections import Counter
import pandas as pd
from datetime import datetime

groups = list('ABCDEF')
third_places_combinations = [''.join(i) for i in combinations(groups, 4)]
opponents_1st = ['3D', '3E', '3F', '3E', '3F', '3F', '3D', '3D',
                 '3F', '3F', '3D', '3D', '3E', '3E', '3E']
opponents_3rd = ['1F', '1F', '1F', 'X', 'X', 'X', '1E', '1E',
                 '1E', 'X', '1F', '1E', '1E', 'X', '1F']


def convert_to_text(opponent):
    if opponent == 'X':
        return "Uitgeschakeld"
    else:
        position, group = opponent[0], opponent[1]
        if int(position) == 1:
            return (f"Winnaar van Group {group} "
                    f"(nu {get_country(opponent)})")
        else:
            return (f"{position}e van Group {group} "
                    f"(nu {get_country(opponent)})")


def get_opposition(QUALIFIED, UNQUALIFIED, pos=1):
    opponent_list = []

    if pos == 1:
        opponents = opponents_1st
    elif pos == 3:
        opponents = opponents_3rd

    for third_places, opponent in zip(third_places_combinations, opponents):
        if (all(i in third_places for i in QUALIFIED)
                and not any(i in third_places for i in UNQUALIFIED)):
            opponent_list.append(convert_to_text(opponent))

    opponent_counter = dict(Counter(opponent_list))
    total = sum(opponent_counter.values())
    for key in opponent_counter:
        opponent_counter[key] /= total

    df = pd.DataFrame.from_dict(data=opponent_counter, orient='index')
    df.columns = ['Kans']
    df = df.sort_values('Kans', ascending=False)
    return df.to_html(formatters={'Kans': '{:,.1%}'.format},
                      classes=["table table-hover text-center"],
                      table_id="standings",
                      border=0,
                      justify="center",
                      escape=False)


GROUP_TABLES = {'A': 12, 'B': 19, 'C': 26, 'D': 33, 'E': 40, 'F': 47}


tables = pd.read_html(
    'https://nl.wikipedia.org/wiki/Europees_kampioenschap_voetbal_2020'
)


def get_netherlands_pos():
    group_netherlands = tables[GROUP_TABLES['C']]
    return group_netherlands[group_netherlands['Team'].str.contains('Nederland')].iloc[0]['Pos']


def get_country(identifier):
    pos, group = int(identifier[0]), identifier[1]
    country = tables[GROUP_TABLES[group]].loc[pos-1, 'Team']
    return country.split('(')[0].strip()


def third_place_opponent(best_third_places, position):
    if position == 1:
        opponents = opponents_1st
    elif position == 3:
        opponents = opponents_3rd

    for third_places, opponent in zip(third_places_combinations, opponents):
        if all(c in third_places for c in best_third_places):
            return get_country(opponent)


def get_current_information():
    netherlands_pos = get_netherlands_pos()

    best_third_places = tables[54]
    qualified = best_third_places['Grp'].to_list()[0:4]

    if netherlands_pos == 1:
        opponent = third_place_opponent(qualified, netherlands_pos)
    elif netherlands_pos == 2:
        opponent = get_country('1A')
    elif netherlands_pos == 3:
        if 'C' in best_third_places:
            opponent = 'Uitgeschakeld'
        else:
            opponent = third_place_opponent(qualified, netherlands_pos)
    else:
        opponent = 'Uitgeschakeld'

    return netherlands_pos, qualified, opponent
