from flask import Flask, jsonify, request, Blueprint
from ..commands.create_route import CreateRoute
from ..commands.get_routes import GetRoutes
from ..commands.get_route import GetRoute
from ..commands.delete_route import DeleteRoute
from ..commands.authenticate import Authenticate
from ..commands.reset import Reset

routes_blueprint = Blueprint('routes', __name__)


@routes_blueprint.route('/routes', methods=['POST'])
def create():
    Authenticate(auth_token()).execute()

    route = CreateRoute(request.get_json()).execute()
    return jsonify(route), 201


@routes_blueprint.route('/routes', methods=['GET'])
def index():
    Authenticate(auth_token()).execute()

    routes = GetRoutes(request.args.to_dict()).execute()
    return jsonify(routes)


@routes_blueprint.route('/routes/<id>', methods=['GET'])
def show(id):
    Authenticate(auth_token()).execute()

    route = GetRoute(id).execute()
    return jsonify(route)


@routes_blueprint.route('/routes/<id>', methods=['DELETE'])
def destroy(id):
    Authenticate(auth_token()).execute()

    response = DeleteRoute(id).execute()
    return jsonify(response)


@routes_blueprint.route('/routes/ping', methods=['GET'])
def ping():
    return 'pong'


@routes_blueprint.route('/routes/reset', methods=['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})


def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization
