from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired


class ReportForm(FlaskForm):
    file = FileField('Upload file for analyses', validators=[FileRequired(), FileAllowed(['pdf'], 'PDF only allowed!')])
    submit = SubmitField('Analyse file')
