from flask import render_template, redirect, url_for, flash, Blueprint, request
from webapp.main.forms import LuckyLosers

main = Blueprint('main', __name__)


from itertools import combinations
from collections import Counter
groups = list('ABCDEF')
third_places_combinations = [''.join(i) for i in combinations(groups, 4)]
third_places_combinations

opponents = ['3D', '3E', '3F', '3E', '3F', '3F', '3D', '3D', '3F', '3F', '3D', '3D', '3E', '3E', '3E']

def get_opposition(QUALIFIED, UNQUALIFIED):
    result = ''
    
    opponent_list = []
    print(f"Qualified: {''.join(QUALIFIED)}\nUnqualified: {''.join(UNQUALIFIED)}")
    for third_places, opponent in zip(third_places_combinations, opponents):
        if all(i in third_places for i in QUALIFIED) and not any(i in third_places for i in UNQUALIFIED):
            opponent_list.append(opponent)

    opponent_counter = dict(Counter(opponent_list))
    total = sum(opponent_counter.values())
    for key in opponent_counter:
        opponent_counter[key] /= total

    for k, v in opponent_counter.items():
        result += f"{k}: {v:.1%}\n\n"
    return result

@main.route('/', methods=['GET', 'POST'])
def eredivisie():
    form = LuckyLosers(request.form)
    if request.method == 'POST' and form.validate():
        result = get_opposition(form.data['qualified'],
                                form.data['unqualified'])
        return render_template('index.html', form=form, result=result)
    return render_template('index.html', form=form)