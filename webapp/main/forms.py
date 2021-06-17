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
            self.qualified.errors.append('Please select no more than 4 groups')  
            return False
        
        if len(self.unqualified.data) > 2:
            self.qualified.errors.append('Please select no more than 2 groups')  
            return False
        
        if len(list(set(self.qualified.data) & set(self.unqualified.data))):
            self.qualified.errors.append('Error')  
            return False

        return True