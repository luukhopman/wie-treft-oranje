from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms import widgets, SelectMultipleField


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label='')
    option_widget = widgets.CheckboxInput()


class LuckyLosers(FlaskForm):
    groups = list('ABCDEF')
    choices = [(g, f'Group {g}') for g in groups]
    position = SelectField(label='State', choices=['1e', '2e', '3e', '4e'])
    qualified = MultiCheckboxField('Qualified', choices=choices)
    unqualified = MultiCheckboxField('Unqualified', choices=choices)

    def validate(self):
        rv = FlaskForm.validate(self)

        if not rv:
            return False

        if len(self.qualified.data) > 4:
            self.qualified.errors.append(
                'Selecteer maximaal 4 beste nummers 3')
            return False

        if len(self.unqualified.data) > 2:
            self.qualified.errors.append(
                'Selecteer maximaal 2 slechtse nummers 3')
            return False

        if len(list(set(self.qualified.data) & set(self.unqualified.data))):
            self.qualified.errors.append(
                'Een groep kan niet zowel de beste als slechte nummers drie bevatten.')
            return False

        return True
