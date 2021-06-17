from flask import render_template, Blueprint, request
from webapp.main.forms import SenarioTester
from webapp.main.utils import (get_country,
                               get_current_information,
                               get_opposition)

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def current():
    netherlands_pos, qualified, opponent = get_current_information()
    qualified = ', '.join(sorted(qualified))

    form = SenarioTester(request.form)
    if request.method == 'POST' and form.validate():
        qualified = form.data['qualified']
        unqualified = form.data['unqualified']

        if form.data['position'].startswith('1'):
            result = get_opposition(qualified, unqualified, pos=1)

        if form.data['position'].startswith('2'):
            result = f"Oranje moet in de achtste finale tegen de groepswinaar van Groep A. Dat is op dit moment {get_country('1A')}!"

        if form.data['position'] .startswith('3'):
            if ('C' in qualified) or (len(qualified) < 4):
                result = get_opposition(qualified, unqualified, pos=3)
            else:
                result = 'Uitgeschakeld.'

        if form.data['position'].startswith('4'):
            result = 'Uitgeschakeld.'

        return render_template('index.html',
                               netherlands_pos=netherlands_pos,
                               qualified=qualified,
                               opponent=opponent,
                               form=form,
                               result=result)

    return render_template('index.html',
                           netherlands_pos=netherlands_pos,
                           qualified=qualified,
                           opponent=opponent,
                           form=form)
