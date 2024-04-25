from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from decimal import Decimal as D 
import sqlalchemy.types as types
from sqlalchemy.orm import relationship

class SqliteNumeric(types.TypeDecorator):     
    impl = types.String     
    def load_dialect_impl(self, dialect):         
        return dialect.type_descriptor(types.VARCHAR(100))     
    def process_bind_param(self, value, dialect):         
        return str(value)     
    def process_result_value(self, value, dialect):         
        return D(value)  


db = SQLAlchemy()

class TrainingSession(db.Model):
    __tablename__ = 'training_session'

    id = db.Column(db.String(255), primary_key=True)
    id_sport_user = db.Column(db.String(255))
    id_event  = db.Column(db.String(255))
    event_category = db.Column(db.String(50))
    sport_type = db.Column(db.String(50))
    session_date = db.Column(db.DateTime, default=datetime.now)
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
    session_event = db.Column(db.DateTime, default=datetime.now)
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