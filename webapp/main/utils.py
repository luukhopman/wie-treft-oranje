from itertools import combinations
from collections import Counter
import pandas as pd
from datetime import datetime

# All the combinations of lucky losers (4 best number threes)
THIRD_PLACE_COMBINATIONS = [''.join(i)
                            for i in combinations(list('ABCDEF'), 4)]

# Opponents if the Netherlands ends first in Group C
OPPONENTS_1ST = ['3D', '3E', '3F', '3E', '3F', '3F', '3D', '3D',
                 '3F', '3F', '3D', '3D', '3E', '3E', '3E']

# Opponents if the Netherlands ends third in Group C
OPPONENTS_3RD = ['1F', '1F', '1F', 'X', 'X', 'X', '1E', '1E',
                 '1E', 'X', '1F', '1E', '1E', 'X', '1F']

# Scrape all Wikipedia tables
TABLES = pd.read_html(
    'https://nl.wikipedia.org/wiki/Europees_kampioenschap_voetbal_2020'
)

LAST_SCRAPE = datetime.now()

# Group standings table mapping to Wikipedia table number
GROUP_MAPPING = {'A': 12, 'B': 19, 'C': 26, 'D': 33, 'E': 40, 'F': 47}


def refresh_data(first=False):
    global LAST_SCRAPE
    global TABLES

    # Scrape all Wikipedia tables
    if (((datetime.now() - LAST_SCRAPE).seconds > 60) or first):
        TABLES = pd.read_html(
            'https://nl.wikipedia.org/wiki/Europees_kampioenschap_voetbal_2020'
        )
        LAST_SCRAPE = datetime.now()


refresh_data(first=True)


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


def get_opposition(qualified, unqualified, pos=1):
    opponent_list = []

    if pos == 1:
        opponents = OPPONENTS_1ST
    elif pos == 3:
        opponents = OPPONENTS_3RD

    for third_places, opponent in zip(THIRD_PLACE_COMBINATIONS, opponents):
        if (all(i in third_places for i in qualified)
                and not any(i in third_places for i in unqualified)):
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


def get_position(group, country):
    group_table = TABLES[GROUP_MAPPING[group]]
    return (group_table
            .loc[group_table['Team'].str.contains(country), 'Pos']
            .iloc[0])


def get_country(identifier):
    pos, group = int(identifier[0]), identifier[1]
    country = TABLES[GROUP_MAPPING[group]].loc[pos-1, 'Team']
    return country.split('(')[0].strip()


def third_place_opponent(best_third_places, position):
    if position == 1:
        opponents = OPPONENTS_1ST
    elif position == 3:
        opponents = OPPONENTS_3RD

    for third_places, opponent in zip(THIRD_PLACE_COMBINATIONS, opponents):
        if all(c in third_places for c in best_third_places):
            return get_country(opponent)


def get_current_information():
    refresh_data()
    position = get_position('C', 'Nederland')

    third_places = TABLES[54]
    best_third_places = third_places['Grp'].to_list()[0:4]

    if position == 1:
        opponent = third_place_opponent(best_third_places, position)
    elif position == 2:
        opponent = get_country('1A')
    elif position == 3:
        if 'C' in best_third_places:
            opponent = 'Uitgeschakeld'
        else:
            opponent = third_place_opponent(best_third_places, position)
    else:
        opponent = 'Uitgeschakeld'

    return position, best_third_places, opponent
