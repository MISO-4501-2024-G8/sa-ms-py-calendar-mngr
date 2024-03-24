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

correr tests con pytest
```
pytest --cov=app/ --cov-report xml --junitxml=pytest-report.xml
coverage xml
coverage html -d coverage_report
```

correr flask
```
export FLASK_APP=app/app.py
flask run
```
