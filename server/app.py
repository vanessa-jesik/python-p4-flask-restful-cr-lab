#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        plants_dict = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(plants_dict, 200)

    def post(self):
        plant_json = request.get_json()
        plant = Plant()
        for key in plant_json:
            if hasattr(plant, key):
                setattr(plant, key, plant_json[key])
        db.session.add(plant)
        db.session.commit()
        return make_response(plant.to_dict(), 201)


class PlantByID(Resource):
    def get(self, id):
        plant_dict = db.session.get(Plant, id).to_dict()
        return make_response(plant_dict, 200)


api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
