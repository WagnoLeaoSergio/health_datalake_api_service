from sqlalchemy_serializer import SerializerMixin
from sqlalchemy_utils import EmailType

from health_datalake_api_service.ext.database import db


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    price = db.Column(db.Numeric())
    description = db.Column(db.Text)


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(140))
    email = db.Column(EmailType, nullable=True)
    password = db.Column(db.String(512))
    latest_measure_date = db.Column(db.DateTime, nullable=True)
    measures = db.relationship('Measure', backref='users')


class Measure(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    measure_time = db.Column(db.DateTime, nullable=False)
    steps = db.Column(db.Integer, nullable=True)
    sleep = db.Column(db.Integer, nullable=True)
    heart_rate = db.Column(db.Integer, nullable=True)
    oxygen_saturation = db.Column(db.Integer, nullable=True)
    blood_pressure_high = db.Column(db.Integer, nullable=True)
    blood_pressure_low = db.Column(db.Integer, nullable=True)
