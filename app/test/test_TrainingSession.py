import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        self.assertEqual(
            json.loads(response.data), {"message": "Lista de Sesiones De Entrenamiento", "content": [], "code": 200}
        )

    def test_post_training_session(self):
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
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            json.loads(response.data)["message"], "Sesion de Entrenamiento creada"
        )
        self.assertEqual(json.loads(response.data)["code"], 201)

    def test_put_training_session(self):
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
    
    def test_post_sportsession(self):
        response_2 = self.app.post(
            "/sport_session",
            json={
                "id_training_session":"no_id",
                "location": "Manizales",
                "session_event":"2023-02-28 14:30:00"
            },
        )
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(
            json.loads(response_2.data)["message"], "No se encontró la sesión de entrenamiento"
        )
        response_3 = self.app.post(
            "/training_session",
            json={
                "id_sport_user": "e2f75148",
                "id_event": "59785783",
                "event_category": "evento",
                "sport_type": "Ciclismo",
                "session_date": "2024-05-28 14:30:00",
            },
        )
        id_trainning_session = json.loads(response_3.data)["content"]["id"]
        response_4 = self.app.post(
            "/sport_session",
            json={
                "id_training_session":id_trainning_session,
                "location": "Manizales",
                "session_event":"2023-02-28 14:30:00"
            },
        )
        self.assertEqual(response_4.status_code, 400)
        self.assertEqual(
            json.loads(response_4.data)["message"], "La sesión de entrenamiento no es de la categoría de Plan de Entrenamiento"
        )
        response = self.app.post(
            "/sport_session",
            json={
                "id_training_session":"id_test",
                "location": "Manizales",
                "session_event":"2023-02-28 14:30:00"
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            json.loads(response.data)["message"], "Sesiones Deportivas creadas"
        )
        self.assertEqual(json.loads(response.data)["code"], 201)
    
    def test_get_sportsession(self):
        response_2 = self.app.get("/sport_session")
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(
            json.loads(response_2.data)["message"], "No se encontró la sesión deportiva"
        )
        response_3 = self.app.post(
            "/sport_session",
            json={
                "id_training_session":"id_test",
                "location": "Manizales",
                "session_event":"2023-02-28 14:30:00"
            },
        )

        response = self.app.get("/sport_session")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data)["message"], "Lista de Sesiones Deportivas"
        )
    
    def test_get_sportsession_by_id(self):
        response = self.app.post(
            "/sport_session",
            json={
                "id_training_session":"id_test",
                "location": "Manizales",
                "session_event":"2023-02-28 14:30:00"
            },
        )
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
                "id_training_session":"id_test",
                "location": "Manizales",
                "session_event":"2023-02-28 14:30:00"
            },
        )
        id_sport_user = 'e2f75148'
        response = self.app.get(f"/training_session/{id_sport_user}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data)["message"], "Se encontró la sesión de entrenamiento exitosamente"
        )
        self.assertEqual(json.loads(response.data)["code"], 200)