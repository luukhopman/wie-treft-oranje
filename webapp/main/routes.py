from flask import render_template, Blueprint, request
import pandas as pd
from webapp.main.forms import SenarioTester
from webapp.main.utils import (get_country,
                               get_current_information,
                               get_opposition)

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def current():
    position, best_third_places, opponent = get_current_information()
    best_third_places = ', '.join(sorted(best_third_places))

    form = SenarioTester(request.form)
    if request.method == 'POST' and form.validate():
        qualified = form.data['qualified']
        unqualified = form.data['unqualified']
        pos = int(form.data['position'][0])

        result = get_opposition(qualified, unqualified, pos=pos)

        return render_template('index.html',
                               position=position,
                               best_third_places=best_third_places,
                               opponent=opponent,
                               form=form,
                               result=result)

    return render_template('index.html',
                           position=position,
                           best_third_places=best_third_places,
                           opponent=opponent,
                           form=form)
