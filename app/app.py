#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate

from models import HeroPower, Power, db, Hero

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
    # Retrieve a power from the database by ID
    power = Power.query.get(id)

    # Check if the power with the specified ID exists
    if power is None:
        # If not found, return a JSON response with a 404 (Not Found) status
        return jsonify({"error": "Power not found"}), 404

    # Retrieve the 'description' field from the JSON data in the request
    description = request.json.get('description')

    # Check if 'description' is provided in the request
    if description is not None:
        try:
            # Perform validation on the provided description
            Power.validate_description(power, 'description', description)
            
            # If validation is successful, update the power's description in the database
            power.description = description
            db.session.commit()  # Commit the changes to the database

            # Create a dictionary containing the updated power data
            power_data = {
                'id': power.id,
                'name': power.name,
                'description': power.description,
            }
            
            # Use jsonify to convert the response data to JSON format and return with a 200 (OK) status
            return jsonify(power_data), 200

        except ValueError as e:
            # If validation fails, return a JSON response with validation error(s) and a 400 (Bad Request) status
            return jsonify({"errors": [str(e)]}), 400

    # If 'description' is not provided in the request, return a JSON response with a 400 (Bad Request) status
    return jsonify({"error": "Description not provided"}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    # Get JSON data from the request
    data = request.get_json()
    
    # Extract 'strength', 'power_id', and 'hero_id' from the JSON data
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    # Check if any of the required fields is missing in the JSON data
    if hero_id is None or power_id is None or strength is None:
        response = {
            'errors': ['Missing required fields']
        }
        # Return a JSON response with a 400 (Bad Request) status
        return jsonify(response), 400

    # Retrieve the hero and power objects from the database
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    # Check if the hero or power is not found
    if hero is None or power is None:
        response = {
            'errors': ['Hero or power not found']
        }
        # Return a JSON response with a 404 (Not Found) status
        return jsonify(response), 404

    # Create a new HeroPower association and add it to the database
    hero_power = HeroPower(strength=strength, power=power, hero=hero)
    db.session.add(hero_power)
    db.session.commit()

    # Retrieve the updated data related to the hero
    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': [{'id': p.id, 'name': p.name, 'description': p.description}
                   for p in hero.powers]
    }

    # Create a JSON response with the updated hero data and return with a 200 (OK) status
    response = jsonify(hero_data)
    return response, 200

if __name__ == '__main__':
    app.run(port=5000)
