from flask import Blueprint, abort, jsonify,request,Response

from data import Pet
from get_session import get_session

#pet API
pets = Blueprint('pets', __name__)
@pets.route('')
def list_pets():
    session = get_session()
    pets = session.query(Pet).all()
    result = [p.asdict() for p in pets]
    return jsonify(result)

@pets.route('/<int:id>')
def get_pets(id):
    session = get_session()
    pet = session.query(Pet).filter(Pet.id == id).first()
    if pet is None :
        abort(404, "There's no such pet id")
    return jsonify(pet.asdict())

@pets.route('/', methods=['POST'])
def create_pet():
    pet_j = request.get_json()
    if "id" in pet_j:
        abort(422)
    session = get_session()
    try:
        pet = Pet.from_dict(pet_j)
        session.add(pet)
        session.commit()
    except (AttributeError, TypeError, DataError, IntegrityError) as err:
        abort(422, err)
    return jsonify(pet.asdict()), 201


@pets.route('/', methods=['PUT'])
def update_pet():

    pet_j = request.get_json()
    if "id" not in pet_j:
        abort(422, "There's no such id")
    session = get_session()
    pet = session.query(Pet).get(pet_j["id"])
    if pet is None:
        abort(404, "Pet's id is wrong")
    try:
        pet.update(pet_j)
    except (AttributeError, TypeError, DataError, IntegrityError) as err:
        abort(422, err)
    session.commit()
    return jsonify(pet.asdict()), 200


@pets.route('/<int:id>', methods=['DELETE'])
def delete_pet(id):
    session = get_session()
    pet = session.query(Pet).get(id)
    if pet is None :
        abort(404, "Pet's id is wrong")
    session.delete(pet)
    session.commit()
    return Response('', status=200, mimetype='application/json')