from flask import render_template, redirect, url_for, flash, Blueprint, request
from webapp.main.forms import LuckyLosers
from webapp.main.utils import get_opposition

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def eredivisie():
    form = LuckyLosers(request.form)
    if request.method == 'POST' and form.validate():
        if form.data['position'] == '1e':
            result = get_opposition(form.data['qualified'],
                                    form.data['unqualified'])
        if form.data['position'] == '2e':
            result = 'Groepswinaar van Groep A.'
        if form.data['position'] == '3e':
            result = get_opposition(form.data['qualified'],
                                    form.data['unqualified'])
        if form.data['position'] == '4e':
            result = 'Uitgeschakeld!'
        return render_template('index.html', form=form, result=result)
    return render_template('index.html', form=form)