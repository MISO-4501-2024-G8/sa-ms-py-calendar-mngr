import sqlalchemy
import json
from unittest import TestCase
from faker import Faker
from faker.generator import random
from app import app


class TestTrainingPlan(TestCase):
    
    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

    def test_post_not_None(self):
        nuevo_training_plan_fake = {
            "id_sport_user": self.data_factory.name(),
            "id_event": self.data_factory.word(),
            "event_category": self.data_factory.name(),
            "sport_type": self.data_factory.word(),
            "session_date":"2023-02-28 14:30:00",
            "name": self.data_factory.word(),
            "week": self.data_factory.name(),
            "day": self.data_factory.word(),
            "repeats": self.data_factory.word(),
            "session_date":"2023-02-28 14:30:00",
            "location": self.data_factory.word(),
            "total_time": self.data_factory.name(),
            "sport_session_date":"2023-02-28 14:30:00",
            "objectives_achived": self.data_factory.word(),
            "instruction_description": self.data_factory.word(),
            "instruction_time": self.data_factory.word(),
            "target_achieved": self.data_factory.name()
        }
        endpoint = "/create_training_plan"
        solicitud_crear_planEntrenamiento = self.client.post(endpoint,
                                                             data = json.dumps(nuevo_training_plan_fake),
                                                             headers={'Content-Type': 'application/json'}).get_data().decode("utf-8")
        self.assertIsNotNone(solicitud_crear_planEntrenamiento)

    def test_post_succes(self):
        nuevo_training_plan_fake = {
            "id_sport_user": self.data_factory.name(),
            "id_event": self.data_factory.word(),
            "event_category": self.data_factory.name(),
            "sport_type": self.data_factory.word(),
            "session_date":"2023-02-28 14:30:00",
            "name": self.data_factory.word(),
            "week": self.data_factory.name(),
            "day": self.data_factory.word(),
            "repeats": self.data_factory.word(),
            "session_date":"2023-02-28 14:30:00",
            "location": self.data_factory.word(),
            "total_time": self.data_factory.name(),
            "sport_session_date":"2023-02-28 14:30:00",
            "objectives_achived": self.data_factory.word(),
            "instruction_description": self.data_factory.word(),
            "instruction_time": self.data_factory.word(),
            "target_achieved": self.data_factory.name()
        }
        endpoint = "/create_training_plan"
        solicitud_crear_planEntrenamiento = self.client.post(endpoint,
                                                          data = json.dumps(nuevo_training_plan_fake),
                                                          headers={'Content-Type': 'application/json'}).get_data().decode("utf-8")
     
        self.assertFalse(str.__contains__(solicitud_crear_planEntrenamiento[0], "Se pudo crear el plan de entrenamiento exitosamante"))
 
    def test_put_not_None(self):
        nuevo_training_plan_fake = {
            "id_sport_user": self.data_factory.name(),
            "id_event": self.data_factory.word(),
            "event_category": self.data_factory.name(),
            "sport_type": self.data_factory.word(),
            "session_date":"2023-02-28 14:30:00",
            "name": self.data_factory.word(),
            "week": self.data_factory.name(),
            "day": self.data_factory.word(),
            "repeats": self.data_factory.word(),
            "session_date":"2023-02-28 14:30:00",
            "location": self.data_factory.word(),
            "total_time": self.data_factory.name(),
            "sport_session_date":"2023-02-28 14:30:00",
            "objectives_achived": self.data_factory.word(),
            "instruction_description": self.data_factory.word(),
            "instruction_time": self.data_factory.word(),
            "target_achieved": self.data_factory.name()
        }
        endpoint_carreras = "/create_training_plan"
        solicitud_put_planEntrenamiento = self.client.put(endpoint_carreras,
                                                          data = json.dumps(nuevo_training_plan_fake),
                                                          headers={'Content-Type': 'application/json'}).get_data().decode("utf-8")
        self.assertIsNotNone(solicitud_put_planEntrenamiento)

    def test_put_succes(self):
        nuevo_training_plan_fake = {
            "id_sport_user": self.data_factory.name(),
            "id_event": self.data_factory.word(),
            "event_category": self.data_factory.name(),
            "sport_type": self.data_factory.word(),
            "session_date":"2023-02-28 14:30:00",
            "name": self.data_factory.word(),
            "week": self.data_factory.name(),
            "day": self.data_factory.word(),
            "repeats": self.data_factory.word(),
            "session_date":"2023-02-28 14:30:00",
            "location": self.data_factory.word(),
            "total_time": self.data_factory.name(),
            "sport_session_date":"2023-02-28 14:30:00",
            "objectives_achived": self.data_factory.word(),
            "instruction_description": self.data_factory.word(),
            "instruction_time": self.data_factory.word(),
            "target_achieved": self.data_factory.name()
        }
        endpoint_carreras = "/create_training_plan"
        solicitud_put_planEntrenamiento = self.client.post(endpoint_carreras,
                                                          data = json.dumps(nuevo_training_plan_fake),
                                                          headers={'Content-Type': 'application/json'}).get_data().decode("utf-8")
        self.assertFalse(solicitud_put_planEntrenamiento[0] == "Se actualizaron correctmente los campos")
