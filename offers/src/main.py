from dotenv import load_dotenv, find_dotenv
loaded = load_dotenv('.env.development')

from .errors.errors import ApiError
from .blueprints.offers import offers_blueprint
from .models.model import Base
from .session import Session, engine
from flask import Flask, jsonify


app = Flask(__name__)
app.register_blueprint(offers_blueprint)

Base.metadata.create_all(engine)


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "msg": err.description
    }
    return jsonify(response), err.code
