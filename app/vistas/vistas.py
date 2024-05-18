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
error_training_session_msg = "No se encontró la sesión de entrenamiento"
error_sport_session_msg = "No se encontró la sesión deportiva"
url_training_plan_ms = 'http://lb-ms-py-training-mngr-157212315.us-east-1.elb.amazonaws.com/' #NOSONAR


def generate_uuid():
    uid = uuid.uuid4()
    parts = str(uid).split("-")
    return parts[0]


def calculate_total_time(instructions, repeats):
    total_time = 0
    for instruction in instructions:
        total_time += instruction["instruction_time"]
    total_time = total_time * repeats # Se multiplica por las repeticiones ej: 5 min * 3 repeticiones = 15 min
    return total_time


def create_objective_instruction(
    sport_session, objective, instructions, id_training_session
):
    objective_instructions = []
    for instruction in instructions:
        data_objective_instruction = {}
        data_objective_instruction["id"] = generate_uuid()
        data_objective_instruction["id_sport_session"] = sport_session.id
        data_objective_instruction["instruction_description"] = instruction["instruction_description"]
        data_objective_instruction["instruction_time"] = instruction["instruction_time"]
        data_objective_instruction["target_achieved"] = 0
        data_objective_instruction["createdAt"] = datetime.now()
        data_objective_instruction["updatedAt"] = datetime.now()
        objective_instruction = ObjectiveInstruction(**data_objective_instruction)
        objective_instructions.append(data_objective_instruction)
        db.session.add(objective_instruction)
        db.session.commit()
        data_objective_instruction["createdAt"] = datetime.now().isoformat()
        data_objective_instruction["updatedAt"] = datetime.now().isoformat()
    return objective_instructions


def create_sport_session(
    id_training_session, objective, instructions, new_name, week, day, data
):
    total_time = calculate_total_time(instructions, objective["repeats"])
    data_sport_session = {}
    data_sport_session["id"] = generate_uuid()
    data_sport_session["id_training_session"] = id_training_session
    data_sport_session["name"] = new_name
    data_sport_session["week"] = week
    data_sport_session["day"] = day
    data_sport_session["repeats"] = objective["repeats"]
    data_sport_session["location"] = data["location"]
    data_sport_session["total_time"] = total_time
    data_sport_session["session_event"] = datetime.strptime(
        data["session_event"], date_format
    )
    data_sport_session["qty_objectives_achived"] = 0
    data_sport_session["createdAt"] = datetime.now()
    data_sport_session["updatedAt"] = datetime.now()
    sport_session = SportsSession(**data_sport_session)
    db.session.add(sport_session)
    db.session.commit()
    data_sport_session["session_event"] = data["session_event"]
    data_sport_session["createdAt"] = (datetime.now().isoformat())  # Quitar el isoformat # TODO
    data_sport_session["updatedAt"] = (datetime.now().isoformat())  # Quitar el isoformat # TODO
    objective_instructions = create_objective_instruction(
        sport_session, objective, instructions, id_training_session
    )
    data_sport_session["objective_instructions"] = objective_instructions
    return data_sport_session


class VistaStatusCheck(Resource):
    def get(self):
        return {"message": "OK", "code": 200}, 200


class VistaTrainingSession(Resource):

    def post(self):
        data = request.get_json()
        if "id" not in data:
            data["id"] = generate_uuid()
        
        training_sessions = TrainingSession.query.filter(
            TrainingSession.id_sport_user == data["id_sport_user"],
            TrainingSession.id_event == data["id_event"],
        ).all()
        
        if training_sessions is not None and len(training_sessions) > 0:
            return {
                "message": "Ya existe una sesión de entrenamiento para este usuario y evento",
                "code": 400,
            }, 400
        
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
            return {
                "message": "No se encontró la sesión de entrenamiento del usuario"
            }, 404

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
            "content": training_session_schema.dump(training_sessions, many=True),
            "message": "Se encontró la sesión de entrenamiento exitosamente",
            "code": 200,
        }, 200

    def put(self, id):
        data = request.get_json()
        training_session = TrainingSession.query.filter(
            TrainingSession.id == id
        ).first()
        if training_session is None:
            return {"message": error_training_session_msg}, 404

        training_session.id_sport_user = data["id_sport_user"]
        training_session.id_event = data["id_event"]
        training_session.event_category = data["event_category"]
        training_session.sport_type = data["sport_type"]
        training_session.session_date = datetime.strptime(
            data["session_date"], date_format
        )
        training_session.updatedAt = datetime.now()
        db.session.commit()
        return {
            "message": "Sesión de Entrenamiento actualizada",
            "code": 200,
            "content": training_session_schema.dump(training_session),
        }, 200

    def delete(self, id):
        training_session = TrainingSession.query.filter(
            TrainingSession.id == id
        ).first()
        if training_session is None:
            return {"message": error_training_session_msg}, 404

        sport_sessions = SportsSession.query.filter(
            SportsSession.id_training_session == training_session.id
        )

        for sport_session in sport_sessions:
            objective_instructions = ObjectiveInstruction.query.filter(
                ObjectiveInstruction.id_sport_session == sport_session.id
            )
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
            week = data["week"]
            day = data["day"]

            if id_training_session is None or week is None or day is None or id_training_session == "" or week == "" or day == "":
                return {"message": "Faltan datos para crear la sesión deportiva", "code":400}, 400
            
            training_session = TrainingSession.query.filter(
                TrainingSession.id == id_training_session
            ).first()
            if training_session is None:
                return {"message": error_training_session_msg, "code":404}, 404

            if training_session.event_category != "plan_training":
                return {
                    "message": "La sesión de entrenamiento no es de la categoría de Plan de Entrenamiento", "code":400
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

            training_plan_rq = requests.get(
                url_training_plan_ms + f"training_plan/{training_session.id_event}"
            )
            if training_plan_rq.status_code != 200:
                return {"message": "No se encontró el plan de entrenamiento"}, 404
            training_plan_response = training_plan_rq.json()
            training_plan = training_plan_response["training_plan"]
            

            # Se debe obtener: id_training_plan, semana, dia y con esos datos se debe generar una sesion deportiva
            # a partir de eso se llama al servicio de training_plan para obtener los objetivos y las instrucciones segun el dia
            # y tambien se debe buscar en la bd local si ya existe una sesion deportiva con esos datos (id_training_plan, semana, dia)

            sport_sessions = SportsSession.query.filter(
                SportsSession.id_training_session == id_training_session,
                SportsSession.week == week,
                SportsSession.day == day,
            ).all()

            if sport_sessions is not None and len(sport_sessions) > 0:
                return {
                    "message": "Ya existe una sesión deportiva para este día",
                    "code": 400,
                }, 400
            


            sport_sessions = []

            name = training_plan["id"] + "-WK" + "_WEEK_" + "-D" + "_DAY_"
            new_name = name.replace("_WEEK_", str(week)).replace("_DAY_", str(day))
            
            objectives = training_plan["objectives"]

            
            
            
            
            for objective in objectives:
                if objective["day"] == day:
                    instructions = objective["instructions"]
                    print("Creando sesion deportiva")                    
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
            
            if len(sport_sessions) == 0:
                return {
                    "message": "No se encontraron objetivos para el día",
                    "code": 404,
                }, 404

            print(sport_sessions)
            return {
                "message": "Sesion Deportiva creada",
                "code": 201,
                "content": sport_sessions,
            }, 201
        except IntegrityError as e:
            return {"message": error_msg + str(e)}, 400
        except Exception as e:
            return {"message": error_msg + str(e)}, 500

    def get(self):
        try:
            sport_sessions = SportsSession.query.all()
            if sport_sessions is None or len(sport_sessions) == 0:
                return {"message": error_sport_session_msg}, 404

            sport_sessions_obj = []
            for sport_session in sport_sessions:
                objective_instructions = ObjectiveInstruction.query.filter(
                    ObjectiveInstruction.id_sport_session == sport_session.id
                )
                objective_instructions_obj = []
                if objective_instructions is not None:
                    #sport_session.objecive_instructions = objective_instructions
                    for instruction in objective_instructions:
                        objective_instructions_obj.append(objective_instruction_schema.dump(instruction))
                sport_session_obj = sports_session_schema.dump(sport_session)
                sport_session_obj["objective_instructions"] = objective_instructions_obj
                sport_sessions_obj.append(sport_session_obj)

            return {
                "message": "Lista de Sesiones Deportivas",
                "code": 200,
                "content": sport_sessions_obj,
            }, 200
        except IntegrityError as e:
            return {"message": error_msg + str(e)}, 400
        except Exception as e:
            return {"message": error_msg + str(e)}, 500

class VistaSportUserSession(Resource):
    def get(self, id):
        training_sessions = TrainingSession.query.filter(
            TrainingSession.id_sport_user == id,
            TrainingSession.event_category == "plan_training",
        ).all()
        if training_sessions is None:
            return {"message": "No se encontró la sesión de entrenamiento del usuario", "code": 404}, 404
        sport_sessions = []
        for training_session in training_sessions:
            sport_session = SportsSession.query.filter(
                SportsSession.id_training_session == training_session.id
            ).all()
            if sport_session is not None and len(sport_session) > 0:
                for sport_session in sport_session:
                    sport_s = sports_session_schema.dump(sport_session)
                    sport_sessions.append(sport_s)
        
        if len(sport_sessions) == 0:
            return {"message": "No se encontraron sesiones deportivas del usuario", "code": 404}, 404
        return {
            "message": "Lista de Sesiones Deportivas del Usuario",
            "code": 200,
            "content": sport_sessions,
        }, 200


class VistaSportSessionID(Resource):
    def get(self, id):
        sport_session = SportsSession.query.filter(SportsSession.id == id).first()
        if sport_session is None:
            return {"message": error_sport_session_msg}, 404

        objective_instruction = ObjectiveInstruction.query.filter(
            ObjectiveInstruction.id_sport_session == sport_session.id
        )
        if objective_instruction is None:
            return {"message": "No se encontró la instrucción de objetivo"}, 404

        objective_instructions = []
        for instruction in objective_instruction:
            objective_instructions.append(objective_instruction_schema.dump(instruction))
        sport_session_obj = sports_session_schema.dump(sport_session)
        sport_session_obj["objecive_instructions"] = objective_instructions
        return {
            "message": "Sesión Deportiva encontrada",
            "code": 200,
            "content": sport_session_obj,
        }, 200
    
    def put(self, id):
        sport_session = SportsSession.query.filter(SportsSession.id == id).first()
        if sport_session is None:
            return {"message": error_sport_session_msg, "code": 404}, 404

        objective_instructions = ObjectiveInstruction.query.filter(
            ObjectiveInstruction.id_sport_session == sport_session.id
        )
        objectives_achived = 0
        for objective_instruction in objective_instructions:
            if objective_instruction.target_achieved == 1:
                objectives_achived += 1
        sport_session.qty_objectives_achived = objectives_achived
        sport_session.updatedAt = datetime.now()
        db.session.commit()
        return {
            "message": "Sesión Deportiva actualizada",
            "code": 200,
            "content": sports_session_schema.dump(sport_session),
        }, 200
    
    def delete(self, id):
        sport_session = SportsSession.query.filter(SportsSession.id == id).first()
        if sport_session is None:
            return {"message": error_sport_session_msg, "code": 404}, 404

        objective_instructions = ObjectiveInstruction.query.filter(
            ObjectiveInstruction.id_sport_session == sport_session.id
        )
        for objective_instruction in objective_instructions:
            db.session.delete(objective_instruction)
        db.session.delete(sport_session)
        db.session.commit()
        return {"message": "Sesión Deportiva eliminada", "code": 200}, 200

class VistaSportSessionObjectiveID(Resource):
    def put(self, id):
        data = request.get_json()
        objective_instruction = ObjectiveInstruction.query.filter(
            ObjectiveInstruction.id == id
        ).first()
        if objective_instruction is None:
            return {"message": error_upd_msg}, 404

        objective_instruction.target_achieved = data["target_achieved"]
        objective_instruction.updatedAt = datetime.now()
        db.session.commit()
        return {
            "message": "Objetivo de Instrucción actualizado",
            "code": 200,
            "content": objective_instruction_schema.dump(objective_instruction),
        }, 200

    def delete(self, id):
        objective_instruction = ObjectiveInstruction.query.filter(
            ObjectiveInstruction.id == id
        ).first()
        if objective_instruction is None:
            return {"message": error_upd_msg}, 404

        db.session.delete(objective_instruction)
        db.session.commit()
        return {"message": "Objetivo de Instrucción eliminado", "code": 200}, 200

