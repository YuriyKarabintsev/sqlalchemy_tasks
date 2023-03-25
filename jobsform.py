from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, DateTimeField, DateField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    id = IntegerField("ID", validators=[DataRequired()])
    team_leader = StringField("Капитан корабля", validators=[DataRequired()])
    job = StringField("Работа", validators=[DataRequired()])
    work_size = DateTimeField("Время работы", validators=[DataRequired()])
    collaborators = StringField("Список id участников", validators=[DataRequired()])
    start_date = DateField("Дата начала", validators=[DataRequired()])
    end_date = DateField("Дата окончания", validators=[DataRequired()])
    is_finished = BooleanField("Признак завершения", validators=[DataRequired()])
    submit = SubmitField('Submit')