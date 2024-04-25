from datetime import datetime
from decimal import Decimal as D 

from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import sqlalchemy.types as types
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class TrainingSession(db.Model):
    __tablename__ = 'training_session'

    id = db.Column(db.String(255), primary_key=True)
    id_sport_user = db.Column(db.String(255))
    id_event  = db.Column(db.String(255))
    event_category = db.Column(db.String(50))
    sport_type = db.Column(db.String(50))
    session_date = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)


class SportsSession(db.Model):
    __tablename__ = 'sports_session'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(50))
    week = db.Column(db.Integer)
    day = db.Column(db.String(50))
    repeats = db.Column(db.Integer)
    location = db.Column(db.String(50))
    total_time = db.Column(db.Integer)
    session_event = db.Column(db.DateTime)
    qty_objectives_achived = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

    id_training_session = db.Column(db.Integer, db.ForeignKey('training_session.id'))

class ObjectiveInstruction(db.Model):
    __tablename__ = 'objective_instruction'

    id = db.Column(db.String(255), primary_key=True)
    instruction_description = db.Column(db.String(50))
    instruction_time = db.Column(db.Integer)
    target_achieved = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

    id_sport_session = db.Column(db.Integer, db.ForeignKey('sports_session.id'))

class TrainingSessionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TrainingSession
        include_relationships = True
        load_instance = True

class SportsSessionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SportsSession
        include_relationships = True
        load_instance = True

class ObjectiveInstructionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ObjectiveInstruction
        include_relationships = True
        load_instance = True