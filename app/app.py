from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from modelos.modelos import db
from vistas import VistaStatusCheck, VistaTrainingSession, VistaTrainingSessionID, VistaSportSession, VistaSportSessionID, VistaSportSessionObjectiveID, VistaSportUserSession
import uuid

from decouple import config

app=Flask(__name__) # NOSONAR

def generate_uuid():
    uid = uuid.uuid4()
    parts = str(uid).split('-')
    return parts[0]


DATABASE_URI = config('DATABASE_URL', default=f'sqlite:///calendar_{generate_uuid()}.db')
print(' * DATABASE_URI:', DATABASE_URI)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()
cors = CORS(app) # NOSONAR
api = Api(app)


api.add_resource(VistaStatusCheck, '/')
api.add_resource(VistaTrainingSession, '/training_session')
api.add_resource(VistaTrainingSessionID, '/training_session/<string:id>')
api.add_resource(VistaSportSession, '/sport_session')
api.add_resource(VistaSportSessionID, '/sport_session/<string:id>')
api.add_resource(VistaSportSessionObjectiveID, '/sport_session_objective/<string:id>')
api.add_resource(VistaSportUserSession, '/sport_user_session/<string:id>')

jwt = JWTManager(app)


print(' * CALENDAR MNGR corriendo ----------------')

if __name__=='__main__': 
    app.run(port=5001)