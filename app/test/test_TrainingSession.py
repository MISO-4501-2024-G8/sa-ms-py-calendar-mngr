import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch
from app import app
import json
import random
import string
from flask_restful import Api
from flask import Flask
from flask_restful import Resource
from modelos.modelos import db
from urllib.parse import urlparse
from datetime import datetime


class TestVistaHealthCheck(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app = app.test_client()

    def test_health_check(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "OK", "code": 200})


class TestVistaTrainingSession(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app = app.test_client()

    def test_get_training_session(self):
        response = self.app.get("/training_session")
        self.assertEqual(response.status_code, 200)

    def test_put_training_session(self):
        response = self.app.post(
            "/training_session",
            json={
                "id_sport_user": "e2f75148",
                "id_event": "597857453",
                "event_category": "evento",
                "sport_type": "Ciclismo",
                "session_date": "2024-05-28 14:30:00",
            },
        )
        id_trainning_session = json.loads(response.data)["content"]["id"]
        response = self.app.put(
            f"/training_session/{id_trainning_session}",
            json={
                "id_sport_user": "e2f75148",
                "id_event": "59785783",
                "event_category": "evento",
                "sport_type": "Atletismo",
                "session_date": "2024-05-28 14:30:00",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data)["message"], "Sesión de Entrenamiento actualizada"
        )
        self.assertEqual(json.loads(response.data)["code"], 200)

    def test_delete_training_session(self):
        response = self.app.post(
            "/training_session",
            json={
                "id_sport_user": "e2f75148",
                "id_event": "59785783",
                "event_category": "evento",
                "sport_type": "Ciclismo",
                "session_date": "2024-05-28 14:30:00",
            },
        )
        id_trainning_session = json.loads(response.data)["content"]["id"]
        response = self.app.delete(f"/training_session/{id_trainning_session}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data)["message"], "Sesión de Entrenamiento eliminada"
        )
        self.assertEqual(json.loads(response.data)["code"], 200)

    @patch("requests.get")
    def test_delete_training_session_with_sportsessions(self, mock_get):
        self.app.delete("/training_session/no_id")
        response = self.app.post(
            "/training_session",
            json={
                "id_sport_user": "e2f75148",
                "id_event": "59785746543",
                "event_category": "plan_training",
                "sport_type": "Ciclismo",
                "session_date": "2024-05-28 14:30:00",
            },
        )
        id_trainning_session = json.loads(response.data)["content"]["id"]
        print("id_trainning_session: ", id_trainning_session)
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": "Se Encontro el plan de entranamiento buscado",
            "training_plan": {
                "id": "ae18e584",
                "name": "Plan de correr moderado",
                "description": "Plan para correr de manera moderada",
                "weeks": 1,
                "lunes_enabled": 1,
                "martes_enabled": 0,
                "miercoles_enabled": 0,
                "jueves_enabled": 0,
                "viernes_enabled": 1,
                "typePlan": "intermedio",
                "sport": "Atletismo",
                "id_eating_routine": "90bbac87",
                "id_rest_routine": "6ada8af4",
                "createdAt": "2024-05-16T03:54:35",
                "updatedAt": "2024-05-16T03:54:35",
                "objectives": [
                    {
                        "id": "339b2061",
                        "id_routine": "ae18e584",
                        "day": "Viernes",
                        "repeats": 1,
                        "type_objective": "1",
                        "createdAt": "2024-05-16T03:54:36",
                        "updatedAt": "2024-05-16T03:54:36",
                        "instructions": [
                            {
                                "id": "6b0101ad",
                                "id_objective": "339b2061",
                                "instruction_description": "correr",
                                "instruction_time": 1,
                                "createdAt": "2024-05-16T03:54:36",
                                "updatedAt": "2024-05-16T03:54:36",
                            }
                        ],
                    },
                    {
                        "id": "46ad261f",
                        "id_routine": "ae18e584",
                        "day": "Lunes",
                        "repeats": 1,
                        "type_objective": "1",
                        "createdAt": "2024-05-16T03:54:35",
                        "updatedAt": "2024-05-16T03:54:35",
                        "instructions": [
                            {
                                "id": "71e76237",
                                "id_objective": "46ad261f",
                                "instruction_description": "correr",
                                "instruction_time": 1,
                                "createdAt": "2024-05-16T03:54:36",
                                "updatedAt": "2024-05-16T03:54:36",
                            }
                        ],
                    },
                ],
                "risk_alerts": {
                    "training_plan_id": "ae18e584",
                    "stop_training": 0,
                    "notifications": 0,
                    "enable_phone": 0,
                    "createdAt": "2024-05-16T03:54:36",
                    "updatedAt": "2024-05-16T03:54:36",
                },
                "eating_routine": {
                    "id": "90bbac87",
                    "name": "Rutina Alimentacion Proteina",
                    "description": "Esta es una rutina de alimentacion basada en alto consumo de proteina",
                    "weeks": 1,
                    "max_weight": 100.0,
                    "min_weight": 60.0,
                    "createdAt": "2024-05-10T23:36:41",
                    "updatedAt": "2024-05-10T23:36:41",
                },
                "rest_routine": {
                    "id": "6ada8af4",
                    "name": "Rutina Descanso 10 min",
                    "description": "Es una rutina creada para realizar un descanso optimo en 10 min",
                    "createdAt": "2024-05-10T23:13:20",
                    "updatedAt": "2024-05-10T23:13:20",
                },
            },
            "code": 200,
        }
        response = self.app.post(
            "/sport_session",
            json={
                "id_training_session": id_trainning_session,
                "week": 1,
                "day": "Lunes",
                "location": "Manizales",
                "session_event": "2023-02-28 14:30:00",
            },
        )
        print("response delete ts: ", response.data)

        response = self.app.delete(f"/training_session/{id_trainning_session}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data)["message"], "Sesión de Entrenamiento eliminada"
        )
        self.assertEqual(json.loads(response.data)["code"], 200)

    @patch("requests.get")
    def test_post_sportsession(self, mock_get):
        self.app.post(
            "/sport_session",
            json={
                "id_training_session": "no_id",
                "week": 1,
                "day": "",
                "location": "Manizales",
                "session_event": "2023-02-28 14:30:00",
            },
        )
        response_2 = self.app.post(
            "/sport_session",
            json={
                "id_training_session": "no_id",
                "week": 1,
                "day": "Lunes",
                "location": "Manizales",
                "session_event": "2023-02-28 14:30:00",
            },
        )
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(
            json.loads(response_2.data)["message"],
            "No se encontró la sesión de entrenamiento",
        )
        response_3 = self.app.post(
            "/training_session",
            json={
                "id_sport_user": "e2f75148",
                "id_event": "597857878",
                "event_category": "evento",
                "sport_type": "Ciclismo",
                "session_date": "2024-05-28 14:30:00",
            },
        )
        response_33 = self.app.post(
            "/training_session",
            json={
                "id_sport_user": "e2f75148",
                "id_event": "597857879",
                "event_category": "plan_training",
                "sport_type": "Ciclismo",
                "session_date": "2024-05-28 14:30:00",
            },
        )
        print("response_3: ", response_3)
        id_trainning_session = json.loads(response_3.data)["content"]["id"]
        id_true_training_session = json.loads(response_33.data)["content"]["id"]
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": "Se Encontro el plan de entranamiento buscado",
            "training_plan": {
                "id": "ae18e584",
                "name": "Plan de correr moderado",
                "description": "Plan para correr de manera moderada",
                "weeks": 1,
                "lunes_enabled": 1,
                "martes_enabled": 0,
                "miercoles_enabled": 0,
                "jueves_enabled": 0,
                "viernes_enabled": 1,
                "typePlan": "intermedio",
                "sport": "Atletismo",
                "id_eating_routine": "90bbac87",
                "id_rest_routine": "6ada8af4",
                "createdAt": "2024-05-16T03:54:35",
                "updatedAt": "2024-05-16T03:54:35",
                "objectives": [
                    {
                        "id": "339b2061",
                        "id_routine": "ae18e584",
                        "day": "Viernes",
                        "repeats": 1,
                        "type_objective": "1",
                        "createdAt": "2024-05-16T03:54:36",
                        "updatedAt": "2024-05-16T03:54:36",
                        "instructions": [
                            {
                                "id": "6b0101ad",
                                "id_objective": "339b2061",
                                "instruction_description": "correr",
                                "instruction_time": 1,
                                "createdAt": "2024-05-16T03:54:36",
                                "updatedAt": "2024-05-16T03:54:36",
                            }
                        ],
                    },
                    {
                        "id": "46ad261f",
                        "id_routine": "ae18e584",
                        "day": "Lunes",
                        "repeats": 1,
                        "type_objective": "1",
                        "createdAt": "2024-05-16T03:54:35",
                        "updatedAt": "2024-05-16T03:54:35",
                        "instructions": [
                            {
                                "id": "71e76237",
                                "id_objective": "46ad261f",
                                "instruction_description": "correr",
                                "instruction_time": 1,
                                "createdAt": "2024-05-16T03:54:36",
                                "updatedAt": "2024-05-16T03:54:36",
                            }
                        ],
                    },
                ],
                "risk_alerts": {
                    "training_plan_id": "ae18e584",
                    "stop_training": 0,
                    "notifications": 0,
                    "enable_phone": 0,
                    "createdAt": "2024-05-16T03:54:36",
                    "updatedAt": "2024-05-16T03:54:36",
                },
                "eating_routine": {
                    "id": "90bbac87",
                    "name": "Rutina Alimentacion Proteina",
                    "description": "Esta es una rutina de alimentacion basada en alto consumo de proteina",
                    "weeks": 1,
                    "max_weight": 100.0,
                    "min_weight": 60.0,
                    "createdAt": "2024-05-10T23:36:41",
                    "updatedAt": "2024-05-10T23:36:41",
                },
                "rest_routine": {
                    "id": "6ada8af4",
                    "name": "Rutina Descanso 10 min",
                    "description": "Es una rutina creada para realizar un descanso optimo en 10 min",
                    "createdAt": "2024-05-10T23:13:20",
                    "updatedAt": "2024-05-10T23:13:20",
                },
            },
            "code": 200,
        }
        response_4 = self.app.post(
            "/sport_session",
            json={
                "id_training_session": id_trainning_session,
                "week": 1,
                "day": "Lunes",
                "location": "Manizales",
                "session_event": "2023-02-28 14:30:00",
            },
        )
        print("response_4: ", response_4.data)
        self.assertEqual(response_4.status_code, 400)
        self.assertEqual(
            json.loads(response_4.data)["message"],
            "La sesión de entrenamiento no es de la categoría de Plan de Entrenamiento",
        )
        response = self.app.post(
            "/sport_session",
            json={
                "id_training_session": id_true_training_session,
                "week": 1,
                "day": "Lunes",
                "location": "Manizales",
                "session_event": "2023-02-28 14:30:00",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            json.loads(response.data)["message"], "Sesion Deportiva creada"
        )
        self.assertEqual(json.loads(response.data)["code"], 201)

        self.app.get("/sport_user_session/no_id")
        user_sport_session_response = self.app.get("/sport_user_session/e2f75148")
        self.assertEqual(user_sport_session_response.status_code, 200)

        objective_id = json.loads(response.data)["content"][0]["objective_instructions"][0]["id"]
        self.app.put(
            "/sport_session_objective/no_id",
            json={
                "target_achieved": 1,
            },
        )
        response_objective = self.app.put(
            f"/sport_session_objective/{objective_id}",
            json={
                "target_achieved": 1,
            },
        )
        self.assertEqual(response_objective.status_code, 200)

        self.app.put(
            "/sport_session/no_id",
            json={
                "id_training_session": id_true_training_session,
                "week": 1,
                "day": "Lunes",
                "location": "Manizales",
                "session_event": "2023-02-28 14:30:00",
            },
        )
        sport_session_id = json.loads(response.data)["content"][0]["id"]
        response_put = self.app.put(
            f"/sport_session/{sport_session_id}",
            json={
                "id_training_session": id_true_training_session,
                "week": 1,
                "day": "Lunes",
                "location": "Manizales",
                "session_event": "2023-02-28 14:30:00",
                "total_time": 1,
            },
        )
        self.assertEqual(response_put.status_code, 200)
        self.app.delete("/sport_session_objective/no_id")
        delete_response = self.app.delete(f"/sport_session_objective/{objective_id}")
        self.assertEqual(delete_response.status_code, 200)
        self.app.delete("/sport_session/no_id")
        delete_response = self.app.delete(f"/sport_session/{sport_session_id}")
        self.assertEqual(delete_response.status_code, 200)

    @patch("requests.get")
    def test_get_sportsession(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": "Se Encontro el plan de entranamiento buscado",
            "training_plan": {
                "id": "ae18e584",
                "name": "Plan de correr moderado",
                "description": "Plan para correr de manera moderada",
                "weeks": 1,
                "lunes_enabled": 1,
                "martes_enabled": 0,
                "miercoles_enabled": 0,
                "jueves_enabled": 0,
                "viernes_enabled": 1,
                "typePlan": "intermedio",
                "sport": "Atletismo",
                "id_eating_routine": "90bbac87",
                "id_rest_routine": "6ada8af4",
                "createdAt": "2024-05-16T03:54:35",
                "updatedAt": "2024-05-16T03:54:35",
                "objectives": [
                    {
                        "id": "339b2061",
                        "id_routine": "ae18e584",
                        "day": "Viernes",
                        "repeats": 1,
                        "type_objective": "1",
                        "createdAt": "2024-05-16T03:54:36",
                        "updatedAt": "2024-05-16T03:54:36",
                        "instructions": [
                            {
                                "id": "6b0101ad",
                                "id_objective": "339b2061",
                                "instruction_description": "correr",
                                "instruction_time": 1,
                                "createdAt": "2024-05-16T03:54:36",
                                "updatedAt": "2024-05-16T03:54:36",
                            }
                        ],
                    },
                    {
                        "id": "46ad261f",
                        "id_routine": "ae18e584",
                        "day": "Lunes",
                        "repeats": 1,
                        "type_objective": "1",
                        "createdAt": "2024-05-16T03:54:35",
                        "updatedAt": "2024-05-16T03:54:35",
                        "instructions": [
                            {
                                "id": "71e76237",
                                "id_objective": "46ad261f",
                                "instruction_description": "correr",
                                "instruction_time": 1,
                                "createdAt": "2024-05-16T03:54:36",
                                "updatedAt": "2024-05-16T03:54:36",
                            }
                        ],
                    },
                ],
                "risk_alerts": {
                    "training_plan_id": "ae18e584",
                    "stop_training": 0,
                    "notifications": 0,
                    "enable_phone": 0,
                    "createdAt": "2024-05-16T03:54:36",
                    "updatedAt": "2024-05-16T03:54:36",
                },
                "eating_routine": {
                    "id": "90bbac87",
                    "name": "Rutina Alimentacion Proteina",
                    "description": "Esta es una rutina de alimentacion basada en alto consumo de proteina",
                    "weeks": 1,
                    "max_weight": 100.0,
                    "min_weight": 60.0,
                    "createdAt": "2024-05-10T23:36:41",
                    "updatedAt": "2024-05-10T23:36:41",
                },
                "rest_routine": {
                    "id": "6ada8af4",
                    "name": "Rutina Descanso 10 min",
                    "description": "Es una rutina creada para realizar un descanso optimo en 10 min",
                    "createdAt": "2024-05-10T23:13:20",
                    "updatedAt": "2024-05-10T23:13:20",
                },
            },
            "code": 200,
        }
        response_2 = self.app.get("/sport_session")
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(
            json.loads(response_2.data)["message"], "No se encontró la sesión deportiva"
        )
        response_post_training_session = self.app.post(
            "/training_session",
            json={
                "id_sport_user": "e2f75148",
                "id_event": "59785783",
                "event_category": "plan_training",
                "sport_type": "Ciclismo",
                "session_date": "2024-05-28 14:30:00",
            },
        )
        response = json.loads(response_post_training_session.data)["content"]
        # print("post training session: ", response)
        # print(response["id"])
        response_3 = self.app.post(
            "/sport_session",
            json={
                "id_training_session": response["id"],
                "week": 1,
                "day": "Lunes",
                "location": "Manizales",
                "session_event": "2023-02-28 14:30:00",
            },
        )
        response_3_rslt = json.loads(response_3.data)["message"]
        # print("post sport session: ", response_3_rslt)

        response = self.app.get("/sport_session")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data)["message"], "Lista de Sesiones Deportivas"
        )

    @patch("requests.get")
    def test_get_sportsession_by_id(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": "Se Encontro el plan de entranamiento buscado",
            "training_plan": {
                "id": "ae18e584",
                "name": "Plan de correr moderado",
                "description": "Plan para correr de manera moderada",
                "weeks": 1,
                "lunes_enabled": 1,
                "martes_enabled": 0,
                "miercoles_enabled": 0,
                "jueves_enabled": 0,
                "viernes_enabled": 1,
                "typePlan": "intermedio",
                "sport": "Atletismo",
                "id_eating_routine": "90bbac87",
                "id_rest_routine": "6ada8af4",
                "createdAt": "2024-05-16T03:54:35",
                "updatedAt": "2024-05-16T03:54:35",
                "objectives": [
                    {
                        "id": "339b2061",
                        "id_routine": "ae18e584",
                        "day": "Viernes",
                        "repeats": 1,
                        "type_objective": "1",
                        "createdAt": "2024-05-16T03:54:36",
                        "updatedAt": "2024-05-16T03:54:36",
                        "instructions": [
                            {
                                "id": "6b0101ad",
                                "id_objective": "339b2061",
                                "instruction_description": "correr",
                                "instruction_time": 1,
                                "createdAt": "2024-05-16T03:54:36",
                                "updatedAt": "2024-05-16T03:54:36",
                            }
                        ],
                    },
                    {
                        "id": "46ad261f",
                        "id_routine": "ae18e584",
                        "day": "Lunes",
                        "repeats": 1,
                        "type_objective": "1",
                        "createdAt": "2024-05-16T03:54:35",
                        "updatedAt": "2024-05-16T03:54:35",
                        "instructions": [
                            {
                                "id": "71e76237",
                                "id_objective": "46ad261f",
                                "instruction_description": "correr",
                                "instruction_time": 1,
                                "createdAt": "2024-05-16T03:54:36",
                                "updatedAt": "2024-05-16T03:54:36",
                            }
                        ],
                    },
                ],
                "risk_alerts": {
                    "training_plan_id": "ae18e584",
                    "stop_training": 0,
                    "notifications": 0,
                    "enable_phone": 0,
                    "createdAt": "2024-05-16T03:54:36",
                    "updatedAt": "2024-05-16T03:54:36",
                },
                "eating_routine": {
                    "id": "90bbac87",
                    "name": "Rutina Alimentacion Proteina",
                    "description": "Esta es una rutina de alimentacion basada en alto consumo de proteina",
                    "weeks": 1,
                    "max_weight": 100.0,
                    "min_weight": 60.0,
                    "createdAt": "2024-05-10T23:36:41",
                    "updatedAt": "2024-05-10T23:36:41",
                },
                "rest_routine": {
                    "id": "6ada8af4",
                    "name": "Rutina Descanso 10 min",
                    "description": "Es una rutina creada para realizar un descanso optimo en 10 min",
                    "createdAt": "2024-05-10T23:13:20",
                    "updatedAt": "2024-05-10T23:13:20",
                },
            },
            "code": 200,
        }
        response_post_training_session = self.app.post(
            "/training_session",
            json={
                "id_sport_user": "e2f75148",
                "id_event": "59785785",
                "event_category": "plan_training",
                "sport_type": "Ciclismo",
                "session_date": "2024-05-28 14:30:00",
            },
        )
        response_t = json.loads(response_post_training_session.data)["content"]
        # print("response training session: ", response_t)
        response = self.app.post(
            "/sport_session",
            json={
                "id_training_session": response_t["id"],
                "week": 1,
                "day": "Lunes",
                "location": "Manizales",
                "session_event": "2023-02-28 14:30:00",
            },
        )
        # print("response sport_session: ", response)
        id_sport_session = json.loads(response.data)["content"][0]["id"]
        response = self.app.get(f"/sport_session/{id_sport_session}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data)["message"], "Sesión Deportiva encontrada"
        )
        self.assertEqual(json.loads(response.data)["code"], 200)

    def test_get_training_session_by_id(self):
        self.app.post(
            "/training_session",
            json={
                "id": "id_test",
                "id_sport_user": "e2f75148",
                "id_event": "59785783",
                "event_category": "Plan de Entrenamiento",
                "sport_type": "Ciclismo",
                "session_date": "2024-05-28 14:30:00",
            },
        )
        self.app.post(
            "/sport_session",
            json={
                "id_training_session": "id_test",
                "week": 1,
                "day": "Lunes",
                "location": "Manizales",
                "session_event": "2023-02-28 14:30:00",
            },
        )
        id_sport_user = "e2f75148"
        response = self.app.get(f"/training_session/{id_sport_user}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data)["message"],
            "Se encontró la sesión de entrenamiento exitosamente",
        )
        self.assertEqual(json.loads(response.data)["code"], 200)
