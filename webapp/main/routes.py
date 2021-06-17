from flask import render_template, Blueprint, request
from webapp.main.forms import LuckyLosers
from webapp.main.utils import get_country, get_opposition, get_current_opponent

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
@main.route('/home', methods=['GET'])
def current():
    qualified, opponent = get_current_opponent()
    qualified = ', '.join(sorted(qualified))
    return render_template('index.html', qualified=qualified, opponent=opponent)


@main.route('/senario', methods=['GET', 'POST'])
def senario():
    form = LuckyLosers(request.form)
    if request.method == 'POST' and form.validate():
        qualified = form.data['qualified']
        unqualified = form.data['unqualified']

        if form.data['position'] == '1e':
            result = get_opposition(qualified, unqualified, pos=1)

        if form.data['position'] == '2e':
            result = f"Oranje moet in de achtste finale tegen de groepswinaar van Groep A. Dat is op dit moment {get_country('1A')}!"

        if form.data['position'] == '3e':
            if ('C' in qualified) or (len(qualified) < 4):
                result = get_opposition(qualified, unqualified, pos=3)
            else:
                result = 'Uitgeschakeld.'

        if form.data['position'] == '4e':
            result = 'Uitgeschakeld.'

        return render_template('senario.html', form=form, result=result)

    return render_template('senario.html', form=form)
