#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate

from models import Power, db, Hero

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

@app.route('/heroes/<int:id>', methods=['GET'])
def hero_by_id(id):
    # Retrieve a hero from the database by ID
    hero = Hero.query.get(id)

    # Check if the hero with the specified ID exists
    if hero is None:
        # If not found, return a JSON response with a 404 (Not Found) status
        return jsonify({"error": "Hero not found"}, 404)

    # Create a list of powers associated with the hero
    powers = [
        {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        for power in hero.powers
    ]

    # Create a dictionary containing hero data and associated powers
    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }

    # Use jsonify to convert the response data to JSON format and return with a default 200 (OK) status
    return jsonify(hero_data)


@app.route('/powers', methods=['GET'])
def get_powers():
    # Retrieve a list of powers from the database
    powers = Power.query.all()

    # Create a list of dictionaries containing power data
    power_data = [
        {
            'id': power.id,
            'name': power.name,
            'description': power.description,
        }
        for power in powers
    ]

    # Use jsonify to convert the response data to JSON format and return with a default 200 (OK) status
    return jsonify(power_data)

@app.route('/powers/<int:id>', methods=['GET'])
def power_by_id(id):
    # Retrieve a power from the database by ID
    power = Power.query.get(id)

    # Check if the power with the specified ID exists
    if power is None:
        # If not found, return a JSON response with a 404 (Not Found) status
        return jsonify({"error": "Power not found"}, 404)

    # Create a dictionary containing power data
    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description,
    }

    # Use jsonify to convert the response data to JSON format and return with a default 200 (OK) status
    return jsonify(power_data)

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    description = request.json.get('description')
    if description is not None:
        # Perform validation on power.description
        try:
            # Assuming Power.validate_description is a method to validate the description
            Power.validate_description(power, 'description', description)
            # If validation is successful, update the power's description
            power.description = description
            db.session.commit()  # Commit the changes to the database

            power_data = {
                'id': power.id,
                'name': power.name,
                'description': power.description,
            }
            return jsonify(power_data), 200  # Return with a 200 (OK) status
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400

    # If description is not provided in the request, return a 400 (Bad Request) status
    return jsonify({"error": "Description not provided"}), 400


if __name__ == '__main__':
    app.run(port=5555)
