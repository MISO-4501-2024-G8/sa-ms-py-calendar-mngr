# sa-ms-py-calendar-mngr
Repositorio para realizar todo lo relacionado con la funcionalidad de Calendario



generar archivo de dependencias
```
pip3 freeze > requirements.txt
```

## Instrucciones para correr el proyecto

crear un entorno virtual
```
python3 -m venv venv
```
activar venv
```
source venv/bin/activate
```
instalar dependencias del archivo requirements.txt
```
pip3 install -r requirements.txt
```

correr flask
```
export FLASK_APP=app/app.py
export DATABASE_URL=mysql+pymysql://admin:c5d5e19030104ba38e131c2ee8e76dec@dbsportapprestore.cvweuasge1pc.us-east-1.rds.amazonaws.com/db_training_session
flask run -p 5001
```

correr tests con pytest
```
export DATABASE_URL=
unset DATABASE_URL
pytest --cov=app/ --cov-report xml --junitxml=pytest-report.xml
pytest --cov=app/ --cov-report xml --junitxml=pytest-report.xml -s
coverage xml
coverage html -d coverage_report
```

Generar imagen de docker
```
docker build -t calendar-mngr .
```

Correr imagen de docker local
```
docker run -e DATABASE_URL=mysql+pymysql://admin:c5d5e19030104ba38e131c2ee8e76dec@dbsportapprestore.cvweuasge1pc.us-east-1.rds.amazonaws.com/db_training_session -p 5001:5001 calendar-mngr

docker run -p 5001:5001 calendar-mngr
```

remover db de prueba
```
sudo rm -rf /Users/juansanchez/Documents/Github/MISO/sa-ms-py-calendar-mngr/app/instance/*
```