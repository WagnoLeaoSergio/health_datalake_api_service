from datetime import datetime
from flask import abort, jsonify, request
from flask_restful import Resource
from flask_simplelogin import login_required
from sqlalchemy import desc

from health_datalake_api_service.models import Product, Measure, User, db


class UserResource(Resource):
    def get(self, user_name: str):
        user = User.query.filter_by(username=user_name).first() or abort(204)
        return {
            "username": user.username,
            "email": user.email,
            "latest_data_request": user.latest_data_request
        }


class MeasureResource(Resource):
    def get(self, user_name: str):

        user = User.query.filter_by(username=user_name).first() or abort(204)

        oldest_measure = Measure.query.order_by(
            Measure.measure_time
        ).first()
        latest_measure = Measure.query.order_by(
            desc(Measure.measure_time)
        ).first()

        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        if start_date is not None:
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        else:
            start_date = oldest_measure.measure_time

        if end_date is not None:
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        else:
            end_date = latest_measure.measure_time

        if not start_date and not end_date:
            return {}

        measures_range = Measure.query.filter(
            Measure.measure_time >= start_date,
            Measure.measure_time <= end_date
        ).all()

        measures = []

        if len(measures_range) != 0:
            measures = [
                {
                    "id": measure.id,
                    "user": measure.user,
                    "date": str(measure.measure_time),
                    "steps": measure.steps,
                    "sleep": measure.sleep,
                    "heart": measure.heart_rate,
                    "preassure_high": measure.blood_pressure_high,
                    "preassure_low": measure.blood_pressure_low,
                    "oxygen": measure.oxygen_saturation
                }
                for measure in measures_range
            ]

            user.latest_data_request = Measure.query.order_by(
                desc(Measure.measure_time)
            ).first().measure_time

            db.session.commit()

        return {
            "user_id": user.id,
            "email": user.email,
            "measures": measures
        }

    def post(self, user_name: str):

        user = User.query.filter_by(username=user_name).first() or abort(204)
        batch_file = request.files.get("batch_file")
        measures = request.get_json()

        print(measures)

        if batch_file is not None:
            return {"OK": True}

        if measures is None:
            return {"Error": "No measures provided"}, 400

        measures_bulk = []

        for measure in measures:
            m_date = measure["date"]
            m_date = datetime.strptime(m_date, "%Y-%m-%d %H:%M:%S")

            m_steps = int(measure["steps"]) or -1
            m_sleep = int(measure["sleep"]) or -1
            m_heart = int(measure["heart"]) or -1
            m_pressure_high = int(measure["pressure_high"]) or -1
            m_pressure_low = int(measure["pressure_low"]) or -1
            m_oxygen = int(measure["oxygen"]) or -1

            measures_bulk.append(Measure(
                user=user.id,
                measure_time=m_date,
                steps=m_steps,
                sleep=m_sleep,
                heart_rate=m_heart,
                oxygen_saturation=m_oxygen,
                blood_pressure_high=m_pressure_high,
                blood_pressure_low=m_pressure_low
            ))

        db.session.add_all(measures_bulk)
        db.session.commit()

        return {"OK": True}
