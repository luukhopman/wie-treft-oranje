from flask import render_template, Blueprint, request
from webapp.main.forms import LuckyLosers
from webapp.main.utils import get_opposition, get_current_opponent

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
@main.route('/home', methods=['GET'])
def current():
    opponent = get_current_opponent()
    return render_template('index.html', opponent=opponent)


@main.route('/custom', methods=['GET', 'POST'])
def custom():
    form = LuckyLosers(request.form)
    if request.method == 'POST' and form.validate():
        qualified = form.data['qualified']
        unqualified = form.data['unqualified']

        if form.data['position'] == '1e':
            result = get_opposition(qualified, unqualified, pos=1)

        if form.data['position'] == '2e':
            result = 'Oranje moet in de achtste finale tegen de groepswinaar van Groep A! Dat is op dit moment Italië.'

        if form.data['position'] == '3e':
            if ('C' in qualified) or (len(qualified) < 4):
                result = get_opposition(qualified, unqualified, pos=3)
            else:
                result = 'Oranje in uitgeschakeld... 😭'

        if form.data['position'] == '4e':
            result = 'Oranje in uitgeschakeld... 😭'

        return render_template('custom.html', form=form, result=result)

    return render_template('custom.html', form=form)
