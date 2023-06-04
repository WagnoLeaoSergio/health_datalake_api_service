from flask import Blueprint
from flask_restful import Api

from .resources import UserResource, MeasureResource

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app):
    api.add_resource(UserResource, "/user/<user_name>")
    api.add_resource(MeasureResource, "/measure/<user_name>")
    app.register_blueprint(bp)
