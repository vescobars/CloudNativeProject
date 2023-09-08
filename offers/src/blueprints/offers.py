from flask import Flask, jsonify, request, Blueprint
from ..commands.create_offer import CreateOffer
from ..commands.get_offer import GetOffer
from ..commands.get_offers import GetOffers
from ..commands.delete_offer import DeleteOffer
from ..commands.authenticate import Authenticate
from ..commands.reset import Reset

offers_blueprint = Blueprint('offers', __name__)


@offers_blueprint.route('/offers', methods=['POST'])
def create():
    auth_info = Authenticate(auth_token()).execute()
    offer = CreateOffer(request.get_json(), auth_info['id']).execute()
    return jsonify(offer), 201


@offers_blueprint.route('/offers', methods=['GET'])
def index():
    auth_info = Authenticate(auth_token()).execute()
    offers = GetOffers(request.args.to_dict(), auth_info['id']).execute()
    return jsonify(offers)


@offers_blueprint.route('/offers/<id>', methods=['GET'])
def show(id):
    Authenticate(auth_token()).execute()
    offer = GetOffer(id).execute()
    return jsonify(offer)


@offers_blueprint.route('/offers/<id>', methods=['DELETE'])
def destroy(id):
    Authenticate(auth_token()).execute()
    response = DeleteOffer(id).execute()
    return jsonify(response)


@offers_blueprint.route('/offers/ping', methods=['GET'])
def ping():
    return 'pong'


@offers_blueprint.route('/offers/reset', methods=['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})


def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization
