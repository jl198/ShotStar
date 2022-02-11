from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, IntegerField, DateField, RadioField, \
    SelectField, FileField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class GameForm(FlaskForm):
    date_played = DateField('What was the date:', validators=[DataRequired()])
    score = IntegerField('What was the score:', validators=[DataRequired()])
    submit = SubmitField('Submit')

    # def validate_date_played(self, date_played):
    #     entered_date = date_played.data
    #     if entered_date is not None:
    #         raise ValidationError(f'Incorrect Date Format. Entered: {entered_date}')


class ScoreGameForm(FlaskForm):
    date_played = DateField(validators=[DataRequired()])
    number_of_players = RadioField('How many players?', choices=[1, 2, 3, 4, 5], validators=[DataRequired()])
    starting_position = RadioField('Which station will you start at?', choices=[1, 2, 3, 4, 5], coerce=IntegerField,
                                   validators=[DataRequired()])
    other_positions = SelectMultipleField('What other stations are occupied?', choices=[('1',1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)],
                                          coerce=IntegerField, validators=[])
    auto_or_manual = RadioField('Auto Score or Manual Score?', choices=['Auto', 'Manual'], validators=[DataRequired()])
    file_name = FileField()
    submit = SubmitField('Submit')
