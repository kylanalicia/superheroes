#!/usr/bin/env python3

from flask import Flask, make_response,jsonify
from flask_migrate import Migrate

from models import db, Hero

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    # Retrieve a list of heroes from the database
    heroes = Hero.query.all()
    
    # Create a list of dictionaries containing hero data
    hero_data = [
        {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        }
        for hero in heroes
    ]
    
    # jsonify to convert the response data to JSON format and return with a 200 (OK) status
    return jsonify(hero_data), 200

@app.route('/heroes/<int:id>',methods=['GET'])
def hero_by_id(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({"error":"Hero not found"},404)
    
    powers = [
        {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        for power in hero.powers
    ]

    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }
    return jsonify(hero_data)


if __name__ == '__main__':
    app.run(port=5555)
