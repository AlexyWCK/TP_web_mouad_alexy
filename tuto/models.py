from .app import db

from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, SubmitField, PasswordField
from wtforms. validators import DataRequired,EqualTo

from flask_login import UserMixin,current_user



class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return "<Author (%d) %s>" % (self.id, self.name)



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author',
    backref=db.backref('books', lazy='dynamic'))
    def __repr__(self ):
        return "<Book (%d) %s>" % (self.id, self.title)
    
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) 



class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S’inscrire')


class LoginForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')



def get_sample():
    return Book.query.all()

def get_author(id):
    return Author.query.get(id)
