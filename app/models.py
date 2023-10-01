from sqlalchemy.orm import validate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint,Column,String

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    super_name = db.Column(db.String(255),nullable=False)
    powers = db.relationship('HeroPower',back_populates='hero',overlaps='hero')

class Power(db.Model):
    __tablename__ = 'power'  # Replace 'power' with the actual table name in your database

    id = db.Column(db.Integer, primary_key=True)
    heroes = db.relationship('HeroPower', back_populates='power', viewonly=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    @validate('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return description

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    hero_id = db.Column(db.Integer,db.ForeignKey('hero.id'),primary_key=True)
    power_id = db.Column(db.Column(db.Integer,db.ForeignKey('power.id'),primary_key=True))
    hero = db.relationship('Hero',back_populates='powers',overlaps='powers')
    power = db.relationship('Power',back_populates='heroes',overlaps='heroes')
    strength = db.Column(db.String(20),nullable=False)

    __table_args__ = (
        CheckConstraint(strength.in_(['Strong','Weak','Average',]),name='check_strength'),
    )
# add any models you may need. 