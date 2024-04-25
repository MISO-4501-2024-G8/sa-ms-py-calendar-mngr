from dataclasses import dataclass

from datetime import datetime
import requests
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource

from modelos.modelos import (
    TrainingSession,
    SportsSession,
    ObjectiveInstruction,
    TrainingSessionSchema,
    SportsSessionSchema,
    ObjectiveInstructionSchema,
    db,
)

from pathlib import Path
from decouple import config
import json
import uuid

from sqlalchemy.exc import IntegrityError


def generate_uuid():
    uid = uuid.uuid4()
    parts = str(uid).split("-")
    return parts[0]


training_session_schema = TrainingSessionSchema()
sports_session_schema = SportsSessionSchema()
objective_instruction_schema = ObjectiveInstructionSchema()

date_format = "%Y-%m-%d %H:%M:%S"

error_msg = "Error: "
error_upd_msg = "No se pudo Realizar la Actualización "


class VistaStatusCheck(Resource):
    def get(self):
        return {"status": "ok"}


class VistaTrainingPlan(Resource):

    def post(self):
        try:
            session_date = datetime.strptime(request.json["session_date"], date_format)
            sport_session_date = datetime.strptime(
                request.json["sport_session_date"], date_format
            )
            training_session_id = generate_uuid()
            sport_session_id = generate_uuid()
            objective_instruction_id = generate_uuid()
            training_session = TrainingSession(
                id=training_session_id,
                id_sport_user=request.json["id_sport_user"],
                id_event=request.json["id_event"],
                event_category=request.json["event_category"],
                sport_type=request.json["sport_type"],
                session_date=session_date,
                createdAt=datetime.now(),
                updatedAt=datetime.now(),
            )

            db.session.add(training_session)
            db.session.commit()

            sports_session = SportsSession(
                id=sport_session_id,
                id_training_session=training_session.id,
                name=request.json["name"],
                week=request.json["week"],
                day=request.json["day"],
                repeats=request.json["repeats"],
                location=request.json["location"],
                total_time=request.json["total_time"],
                session_event=sport_session_date,
                qty_objectives_achived=request.json["objectives_achived"],
                createdAt=datetime.now(),
                updatedAt=datetime.now(),
            )

            db.session.add(sports_session)
            db.session.commit()

            objective_instruction = ObjectiveInstruction(
                id=objective_instruction_id,
                id_sport_session=sports_session.id,
                instruction_description=request.json["instruction_description"],
                instruction_time=request.json["instruction_time"],
                target_achieved=request.json["target_achieved"],
                createdAt=datetime.now(),
                updatedAt=datetime.now(),
            )

            db.session.add(objective_instruction)
            db.session.commit()
            return {
                "message": "Se pudo crear el plan de entrenamiento exitosamante"
            }, 200

        except IntegrityError as e:
            print(error_msg, e)
            db.session.rollback()
            return {"message": "No se pudo crear el plan de entrenamiento"}, 500
        except Exception as e:
            print(error_msg, e)
            db.session.rollback()
            return {"message": "No se pudo crear el plan de entrenamiento"}, 500

    def put(self):
        def get_request_data(self):
            return {
                "name": request.json["name"],
                "day": request.json["day"],
                "id_event": request.json["id_event"],
                "session_date": datetime.strptime(
                    request.json["session_date"], date_format
                ),
                "sport_session_date": datetime.strptime(
                    request.json["sport_session_date"], date_format
                ),
                "event_category": request.json["event_category"],
                "sport_type": request.json["sport_type"],
                "week": request.json["week"],
                "repeats": request.json["repeats"],
                "location": request.json["location"],
                "total_time": request.json["total_time"],
                "qty_objectives_achived": request.json["objectives_achived"],
                "instruction_description": request.json["instruction_description"],
                "instruction_time": request.json["instruction_time"],
                "target_achieved": request.json["target_achieved"],
            }

        def update_training_session(self, training_session, data):
            training_session.event_category = data["event_category"]
            training_session.sport_type = data["sport_type"]
            training_session.session_date = data["session_date"]
            training_session.updatedAt = datetime.now()

        def update_sport_session(self, sport_session, data):
            sport_session.week = data["week"]
            sport_session.repeats = data["repeats"]
            sport_session.location = data["location"]
            sport_session.total_time = data["total_time"]
            sport_session.session_event = data["sport_session_date"]
            sport_session.qty_objectives_achived = data["qty_objectives_achived"]
            sport_session.updatedAt = datetime.now()

        def update_objective_instruction(self, objective_instruction, data):
            objective_instruction.instruction_description = data[
                "instruction_description"
            ]
            objective_instruction.instruction_time = data["instruction_time"]
            objective_instruction.target_achieved = data["target_achieved"]
            objective_instruction.updatedAt = datetime.now()

        try:
            data = get_request_data(self)

            sport_session = SportsSession.query.filter(
                SportsSession.name == data["name"]
            ).first()
            if sport_session is None:
                return {"message": "La sesion deportiva buscada no Existe"}, 404

            training_session = TrainingSession.query.filter(
                TrainingSession.id_event == data["id_event"]
            ).first()
            if training_session is None:
                return {"message": error_upd_msg, "code": 400}, 400

            objective_instruction = ObjectiveInstruction.query.filter(
                ObjectiveInstruction.id_sport_session == sport_session.id
            ).first()
            if objective_instruction is None:
                return {"message": error_upd_msg, "code": 400}, 400

            update_training_session(self, training_session, data)
            update_sport_session(self, sport_session, data)
            update_objective_instruction(self, objective_instruction, data)

            db.session.commit()

            return {
                "message": "Se actualizaron correctamente los campos",
                "training_session": training_session_schema.dump(training_session),
                "sport_session": sports_session_schema.dump(sport_session),
                "objective_instruction": objective_instruction_schema.dump(
                    objective_instruction
                ),
                "code": 200,
            }, 200

        except IntegrityError as e:
            db.session.rollback()
            print(error_msg, e)
            return {"message": error_upd_msg}, 500
        except Exception as e:
            print(error_msg, e)
            db.session.rollback()
            return {"message": error_upd_msg}, 500

    # def put_2(self):
    #     try:
    #         name = request.json["name"]
    #         day = request.json["day"]
    #         id_event = request.json["id_event"]

    #         session_date = datetime.strptime(request.json["session_date"], date_format)
    #         sport_session_date = datetime.strptime(
    #             request.json["sport_session_date"], date_format
    #         )
    #         event_category = request.json["event_category"]
    #         sport_type = request.json["sport_type"]
    #         week = request.json["week"]
    #         repeats = request.json["repeats"]
    #         location = request.json["location"]
    #         total_time = request.json["total_time"]
    #         qty_objectives_achived = request.json["objectives_achived"]
    #         instruction_description = request.json["instruction_description"]
    #         instruction_time = request.json["instruction_time"]
    #         target_achieved = request.json["target_achieved"]

    #         sport_session = SportsSession.query.filter(
    #             SportsSession.name == name
    #         ).first()
    #         if sport_session is None:
    #             return {"message": "La sesion deportiva buscada no Existe"}, 404
    #         else:
    #             # print("sport_session::", str(sport_session))
    #             training_session = TrainingSession.query.filter(
    #                 TrainingSession.id_event == id_event
    #             ).first()
    #             if training_session is not None:
    #                 objective_instruction = ObjectiveInstruction.query.filter(
    #                     ObjectiveInstruction.id_sport_session == sport_session.id
    #                 ).first()
    #                 if objective_instruction is not None:
    #                     (
    #                         training_session.event_category
    #                         if training_session.event_category == event_category
    #                         else event_category
    #                     )
    #                     (
    #                         training_session.sport_type
    #                         if training_session.sport_type == sport_type
    #                         else sport_type
    #                     )
    #                     (
    #                         training_session.session_date
    #                         if training_session.session_date == session_date
    #                         else session_date
    #                     )
    #                     sport_session.week if sport_session.week == week else week
    #                     (
    #                         sport_session.repeats
    #                         if sport_session.repeats == repeats
    #                         else repeats
    #                     )
    #                     (
    #                         sport_session.location
    #                         if sport_session.location == location
    #                         else location
    #                     )
    #                     (
    #                         sport_session.total_time
    #                         if sport_session.total_time == total_time
    #                         else total_time
    #                     )
    #                     (
    #                         sport_session.session_event
    #                         if sport_session.session_event == sport_session_date
    #                         else sport_session_date
    #                     )
    #                     (
    #                         sport_session.qty_objectives_achived
    #                         if sport_session.qty_objectives_achived
    #                         == qty_objectives_achived
    #                         else qty_objectives_achived
    #                     )
    #                     (
    #                         objective_instruction.instruction_description
    #                         if objective_instruction.instruction_description
    #                         == instruction_description
    #                         else instruction_description
    #                     )
    #                     (
    #                         objective_instruction.instruction_time
    #                         if objective_instruction.instruction_time
    #                         == instruction_time
    #                         else instruction_time
    #                     )
    #                     (
    #                         objective_instruction.target_achieved
    #                         if objective_instruction.target_achieved == target_achieved
    #                         else target_achieved
    #                     )
    #                     training_session.updatedAt = datetime.now()
    #                     sport_session.updatedAt = datetime.now()
    #                     objective_instruction.updatedAt = datetime.now()
    #                     db.session.commit()

    #                     return {
    #                         "message": "Se actualizaron correctmente los campos",
    #                         "training_session": training_session_schema.dump(
    #                             training_session
    #                         ),
    #                         "sport_session": sports_session_schema.dump(sport_session),
    #                         "objective_instruction": objective_instruction_schema.dump(
    #                             objective_instruction
    #                         ),
    #                         "code": 200,
    #                     }, 200
    #                 else:
    #                     return {
    #                         "message": error_upd_msg,
    #                         "code": 400,
    #                     }, 400
    #             else:
    #                 return {
    #                     "message": error_upd_msg,
    #                     "code": 400,
    #                 }, 400
    #     except IntegrityError as e:
    #         db.session.rollback()
    #         print(error_msg, e)
    #         return {"message": error_upd_msg}, 500
    #     except Exception as e:
    #         print(error_msg, e)
    #         db.session.rollback()
    #         return {"message": error_upd_msg}, 500
