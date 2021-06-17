from itertools import combinations
from collections import Counter
import pandas as pd

groups = list('ABCDEF')
third_places_combinations = [''.join(i) for i in combinations(groups, 4)]
opponents = ['3D', '3E', '3F', '3E', '3F', '3F', '3D', '3D',
             '3F', '3F', '3D', '3D', '3E', '3E', '3E']

def convert_to_text(opponent):
    position, group = opponent[0], opponent[1]
    return f"{position}e van Group {group}"

def get_opposition(QUALIFIED, UNQUALIFIED):
    result = ''
    
    opponent_list = []

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
    return df.to_html(formatters={'Kans': '{:,.2%}'.format},
                      classes=["table table-hover text-center"],
                      table_id="standings",
                      border=0, 
                      justify="center",
                      escape=False)