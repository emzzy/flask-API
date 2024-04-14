from flask import Flask,request,jsonify

from package import dapp

from .. import db, Observations, ObservationSchema

from sqlalchemy import IntegrityError

# Initialize Marshmallow schema
observation_schema = ObservationSchema()

observations_schema = ObservationSchema(many=True)





# Read route (Get all observations)
@dapp.route('/observations', methods=['GET'])
def get_observations():
    all_observations = Observations.query.all()
    result = observations_schema.dump(all_observations)
    return jsonify(result)

# Create route
@dapp.route('/observation', methods=['POST'])
def add_observation():
    data = request.json
    try:
        new_observation = Observations(**data)
        db.session.add(new_observation)
        db.session.commit()
        return observation_schema.jsonify(new_observation), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Observation already exists"}), 409
    
    # Read route (Get single observation)
@dapp.route('/observation/<date>', methods=['GET'])
def get_observation(date):
    observation = Observations.query.get(date)
    if observation:
        return observation_schema.jsonify(observation)
    else:
        return jsonify({"message": "Observation not found"}), 404
    
    # Update route
@dapp.route('/observation/<date>', methods=['PUT'])
def update_observation(date):
    observation = Observations.query.get(date)
    if observation:
        data = request.json
        for key, value in data.items():
            setattr(observation, key, value)
        db.session.commit()
        return observation_schema.jsonify(observation)
    else:
        return jsonify({"message": "Observation not found"}), 404
    
    # Delete route
@dapp.route('/observation/<date>', methods=['DELETE'])
def delete_observation(date):
    observation = Observations.query.get(date)
    if observation:
        db.session.delete(observation)
        db.session.commit()
        return jsonify({"message": "Observation deleted successfully"})
    else:
        return jsonify({"message": "Observation not found"}), 404



