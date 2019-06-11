from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class PcCreatorForm(FlaskForm):
    races = {
        ('human', 'Human'),
        ('gnome', 'Gnome'),
        ('dwarf', 'Dwarf'),
        ('tiefling', 'Tiefling'),
    }
    vocations = {
        ('cleric', 'Cleric'),
        ('rogue', 'Rogue'),
        ('ranger', 'Ranger'),
    }
    backgrounds = {
        ('noble', 'Noble'),
        ('sage', 'Sage'),
        ('criminal', 'Criminal'),
    }

    name = StringField('Name', validators=[DataRequired()])

    race = SelectField('Race', choices=races, validators=[DataRequired()])
    vocation = SelectField('Vocation', choices=vocations, validators=[DataRequired()])
    background = SelectField('Background', choices=backgrounds, validators=[DataRequired()])

    submit = SubmitField('Create Your Character!')
