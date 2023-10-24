"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Planets, Characters
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters()
    characters = characters.query.all()
    result = []

    for char in characters:
        result.append(char.serialize())
   


    return jsonify(result), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets()
    planets = planets.query.all()
    response_body = []
    for planet in planets:
        response_body.append(planet.serialize())

    return jsonify(response_body), 200

@app.route('/characters/<int:id>', methods=['GET'])
def get_one_character(id=None):
    character_to_return = Characters()
    character_to_return = character_to_return.query.get(id)
    if id is None:
        return jsonify({"error in request, id needed"}), 400
    if character_to_return is None:
        return jsonify({"error in request, character not found"}), 404

    return jsonify(character_to_return.serialize()), 200

@app.route('/planets/<int:id>')
def get_one_planet(id=None):
    planet_to_return = Planets()
    planet_to_return = planet_to_return.query.get(id)
    if id is None:
        return jsonify({"error in request, id needed"}), 400
    if planet_to_return is None:
        return jsonify({"error in request, planet not found"}), 404
    return jsonify(planet_to_return.serialize())
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
