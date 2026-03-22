from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    rating = db.Column(db.Integer)
    platform = db.Column(db.String(50))
    status = db.Column(db.String(50))
    note = db.Column(db.Text)

    image_url = db.Column(db.String(300))
    

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    performances = db.relationship('Performance', backref='game', lazy=True)


class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    graphics_setting = db.Column(db.String(20))
    fps = db.Column(db.Integer)
    resolution = db.Column(db.String(20))

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))