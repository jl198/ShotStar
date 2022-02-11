from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, IntegerField, DateField
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
