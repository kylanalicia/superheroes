from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Column, String

db = SQLAlchemy()

# Define the Hero model
class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)

    # Define a relationship with the HeroPower model
    powers = db.relationship('HeroPower', back_populates='hero', overlaps='hero')

# Define the Power model
class Power(db.Model):
    __tablename__ = 'power'  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    # Validate the description attribute to ensure it has a minimum length
    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return description

    # Define a relationship with the HeroPower model
    heroes = db.relationship('HeroPower', back_populates='power', viewonly=True)

# Define the HeroPower model
class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    #  primary key columns and foreign keys
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), primary_key=True)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), primary_key=True)

    # Define relationships with the Hero and Power models
    hero = db.relationship('Hero', back_populates='powers', overlaps='powers')
    power = db.relationship('Power', back_populates='heroes', overlaps='heroes')

    # Define a constraint to check the validity of the strength attribute
    strength = db.Column(db.String(20), nullable=False)
    __table_args__ = (
        CheckConstraint(strength.in_(['Strong', 'Weak', 'Average']), name='check_strength'),
    )


