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

training_session_schema = TrainingSessionSchema()
sports_session_schema = SportsSessionSchema()
objective_instruction_schema = ObjectiveInstructionSchema()

date_format = "%Y-%m-%d %H:%M:%S"


error_msg = "Error: "
error_upd_msg = "No se pudo Realizar la Actualización "


def generate_uuid():
    uid = uuid.uuid4()
    parts = str(uid).split("-")
    return parts[0]


def calculate_total_time(instructions):
    total_time = 0
    for instruction in instructions:
        total_time += instruction["time"]
    return total_time


def create_objective_instruction(sport_session, objective, instructions):
    objective_instructions = []
    for instruction in instructions:
        if instruction["id_objective"] == objective["id_objective"]:
            data_objective_instruction = {}
            data_objective_instruction["id"] = generate_uuid()
            data_objective_instruction["id_sport_session"] = sport_session.id
            data_objective_instruction["instruction_description"] = instruction[
                "description"
            ]
            data_objective_instruction["instruction_time"] = instruction["time"]
            data_objective_instruction["target_achieved"] = 0
            data_objective_instruction["createdAt"] = datetime.now().isoformat() # Quitar el isoformat # TODO
            data_objective_instruction["updatedAt"] = datetime.now().isoformat() # Quitar el isoformat # TODO
            objective_instruction = ObjectiveInstruction(**data_objective_instruction)
            # json_object = objective_instruction_schema.dump(objective_instruction)
            objective_instructions.append(data_objective_instruction)
            # print(objective_instructions)
            # db.session.add(objective_instruction) # TODO
            # db.session.commit() # TODO
    return objective_instructions


def create_sport_session(
    id_training_session, objective, instructions, new_name, week, day, data
):
    total_time = calculate_total_time(instructions)
    data_sport_session = {}
    data_sport_session["id"] = generate_uuid()
    data_sport_session["id_training_session"] = id_training_session
    data_sport_session["name"] = new_name + day
    data_sport_session["week"] = week
    data_sport_session["day"] = day
    data_sport_session["repeats"] = objective["repeats"]
    data_sport_session["location"] = data["location"]
    data_sport_session["total_time"] = total_time
    data_sport_session["session_event"] = data["session_event"]
    data_sport_session["qty_objectives_achived"] = 0
    data_sport_session["createdAt"] = datetime.now().isoformat() # Quitar el isoformat # TODO
    data_sport_session["updatedAt"] = datetime.now().isoformat() # Quitar el isoformat # TODO
    # print(data_sport_session)
    sport_session = SportsSession(**data_sport_session)
    # db.session.add(sport_session) # TODO
    # db.session.commit() # TODO
    objective_instructions = create_objective_instruction(
        sport_session, objective, instructions
    )
    # data['objecive_instructions'] = objective_instructions
    # json_sport_object = sports_session_schema.dump(sport_session)
    data_sport_session["objecive_instructions"] = objective_instructions
    # print(data_sport_session)
    return data_sport_session



class VistaStatusCheck(Resource):
    def get(self):
        return {"message": "OK", "code": 200}, 200


class VistaTrainingSession(Resource):

    def post(self):
        data = request.get_json()
        data["id"] = generate_uuid()
        data["session_date"] = datetime.strptime(data["session_date"], date_format)
        data["createdAt"] = datetime.now()
        data["updatedAt"] = datetime.now()
        training_session = TrainingSession(**data)
        db.session.add(training_session)
        db.session.commit()
        return {
            "message": "Sesion de Entrenamiento creada",
            "code": 201,
            "content": training_session_schema.dump(training_session),
        }, 201

    def get(self):
        training_session = TrainingSession.query.all()
        return {
            "message": "Lista de Sesiones De Entrenamiento",
            "code": 200,
            "content": training_session_schema.dump(training_session, many=True),
        }, 200


class VistaTrainingSessionID(Resource):
    # Filtrar la sesión de entrenamiento por id del deportista
    def get(self, id):
        training_sessions = TrainingSession.query.filter(
            TrainingSession.id_sport_user == id
        )
        if training_sessions is None:
            return {"message": "No se encontró la sesión de entrenamiento del usuario"}, 404

        for training_session in training_sessions:
            sport_sessions = SportsSession.query.filter(
                SportsSession.id_training_session == training_session.id
            )
            
            for sport_session in sport_sessions:
                objective_instructions = ObjectiveInstruction.query.filter(
                    ObjectiveInstruction.id_sport_session == sport_session.id
                )
                if objective_instructions is not None:
                    sport_session.objecive_instructions = objective_instructions
            
            if sport_sessions is not None:
                training_session.sport_sessions = sport_sessions

        return {
            "training_session": training_session_schema.dump(training_sessions, many=True),
            "message": "Se encontró la sesión de entrenamiento exitosamente",
            "code": 200,
        }, 200
    
    def put(self, id):
        data = request.get_json()
        training_session = TrainingSession.query.filter(TrainingSession.id == id).first()
        if training_session is None:
            return {"message": "No se encontró la sesión de entrenamiento"}, 404

        training_session.id_sport_user = data["id_sport_user"]
        training_session.id_event = data["id_event"]
        training_session.event_category = data["event_category"]
        training_session.sport_type = data["sport_type"]
        training_session.session_date = datetime.strptime(data["session_date"], date_format)
        training_session.updatedAt = datetime.now()
        db.session.commit()
        return {
            "message": "Sesión de Entrenamiento actualizada",
            "code": 200,
            "content": training_session_schema.dump(training_session),
        }, 200
    
    def delete(self, id):
        training_session = TrainingSession.query.filter(TrainingSession.id == id).first()
        if training_session is None:
            return {"message": "No se encontró la sesión de entrenamiento"}, 404
        
        sport_sessions = SportsSession.query.filter(SportsSession.id_training_session == training_session.id)

        for sport_session in sport_sessions:
            objective_instructions = ObjectiveInstruction.query.filter(ObjectiveInstruction.id_sport_session == sport_session.id)
            for objective_instruction in objective_instructions:
                db.session.delete(objective_instruction)
            db.session.delete(sport_session)

        db.session.delete(training_session)
        db.session.commit()
        return {"message": "Sesión de Entrenamiento eliminada", "code": 200}, 200


class VistaSportSession(Resource):

    def post(self):
        try:
            data = request.get_json()
            print(data)
            id_training_session = data["id_training_session"]
            if id_training_session != "id_test":
                training_session = TrainingSession.query.filter(
                    TrainingSession.id == id_training_session
                ).first()
                if training_session is None:
                    return {"message": "No se encontró la sesión de entrenamiento"}, 404

                if training_session.event_category != "plan_training":
                    return {
                        "message": "La sesión de entrenamiento no es de la categoría de Plan de Entrenamiento"
                    }, 400

            # se debe buscar
            # - con el id de evento se busca en la tabla training_plan: id_training_plan, name, weeks, enable days (lunes, martes, miercoles, jueves, viernes), sport
            # - con el id del training_plan se busca en la tabla objective: id_objective, day, repeticiones
            # - con el id del objective se busca en la tabla instruction: description, time

            """
                Se debe crear por semana:
                - Una sesión deportiva por día
                    name: nombre training_plan + week + day
                    week: week (de la tabla de training_plan)
                    day: day (de la tabla de objective)
                    repeats: las repeticiones del dia ( de la tabla de objective)
                    location: location que viene de request
                    total_time: suma de los tiempos de las instrucciones de los objetivos del dia (de la tabla de instruction)
                    session_event: fecha de la sesión deportiva viene del request
                    qty_objectives_achived: 0
                - Una instrucción de objetivo por cada objetivo del día
                    id_sport_session: id de la sesión deportiva creada
                    instruction_description: description (de la tabla de instruction)
                    instruction_time: time (de la tabla de instruction)
                    target_achieved: 0
            """

            # Esto serviria para traer un training_plan = requests.get(f"{config('URL_TRAINING_PLAN')}/training_plan/{data['id_event']}")
            # Esto serviria para traer un objective = requests.get(f"{config('URL_TRAINING_PLAN')}/objective/{training_plan['id_training_plan']}")
            # Esto serviria para traer un instruction = requests.get(f"{config('URL_TRAINING_PLAN')}/instruction/{objective['id_objective']}")

            training_plan = {
                "id_training_plan": "id_training_plan",
                "name": "Entrenamiento Test",
                "description": "Entrenamiento Test para realizar pruebas",
                "weeks": 1,
                "enable_days": ["lunes", "martes", "jueves"],
                "sport": "Atletismo",
            }

            objectives = [
                {
                    "id_training_plan": "id_training_plan",
                    "id_objective": "id_objective_1",
                    "day": "lunes",
                    "repeats": 3,
                    "type_objective": "training",
                },
                {
                    "id_training_plan": "id_training_plan",
                    "id_objective": "id_objective_2",
                    "day": "martes",
                    "repeats": 3,
                    "type_objective": "training",
                },
                {
                    "id_training_plan": "id_training_plan",
                    "id_objective": "id_objective_3",
                    "day": "jueves",
                    "repeats": 3,
                    "type_objective": "training",
                },
            ]

            instructions = [
                {
                    "id_objective": "id_objective_1",
                    "id_instruction": "id_instruction_1",
                    "description": "Caminar",
                    "time": 5,
                },
                {
                    "id_objective": "id_objective_1",
                    "id_instruction": "id_instruction_2",
                    "description": "Correr",
                    "time": 5,
                },
                {
                    "id_objective": "id_objective_2",
                    "id_instruction": "id_instruction_3",
                    "description": "Caminar",
                    "time": 5,
                },
                {
                    "id_objective": "id_objective_2",
                    "id_instruction": "id_instruction_4",
                    "description": "Correr",
                    "time": 5,
                },
                {
                    "id_objective": "id_objective_3",
                    "id_instruction": "id_instruction_5",
                    "description": "Caminar",
                    "time": 5,
                },
                {
                    "id_objective": "id_objective_3",
                    "id_instruction": "id_instruction_6",
                    "description": "Correr",
                    "time": 5,
                },
            ]

            name = training_plan["name"] + "_WEEK_"
            weeks = training_plan["weeks"]
            sport_sessions = []

            for i in range(weeks):
                new_name = name.replace("_WEEK_", str(i + 1))
                week = i + 1
                for day in training_plan["enable_days"]:
                    for objective in objectives:
                        if objective["day"] == day:
                            data_sport_session = create_sport_session(
                                id_training_session,
                                objective,
                                instructions,
                                new_name,
                                week,
                                day,
                                data,
                            )
                            sport_sessions.append(data_sport_session)

            print(sport_sessions)
            return {
                "message": "Sesiones Deportivas creadas",
                "code": 201,
                "content": sport_sessions,
            }, 201
        except IntegrityError as e:
            return {"message": error_msg + str(e)}, 400
        except Exception as e:
            return {"message": error_msg + str(e)}, 500

    def get(self):
        sport_session = SportsSession.query.all()
        return {
            "message": "Lista de Sesiones Deportivas",
            "code": 200,
            "content": sports_session_schema.dump(sport_session, many=True),
        }, 200


class VistaSportSessionID(Resource):
    def get(self, id):
        sport_session = SportsSession.query.filter(SportsSession.id == id).first()
        if sport_session is None:
            return {"message": "No se encontró la sesión deportiva"}, 404

        objective_instruction = ObjectiveInstruction.query.filter(
            ObjectiveInstruction.id_sport_session == sport_session.id
        )
        if objective_instruction is None:
            return {"message": "No se encontró la instrucción de objetivo"}, 404

        return {
            "sport_session": sports_session_schema.dump(sport_session),
            "objective_instruction": objective_instruction_schema.dump(
                objective_instruction
            ),
            "message": "Se encontró la sesión deportiva exitosamente",
            "code": 200,
        }, 200