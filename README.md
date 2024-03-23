# sa-ms-py-calendar-mngr
Repositorio para realizar todo lo relacionado con la funcionalidad de Calendario


crear un entorno virtual
```
python3 -m venv venv
```

activar venv
```
source venv/bin/activate
```

generar archivo de dependencias
```
pip3 freeze > requirements.txt
```

instalar dependencias del archivo requirements.txt
```
pip3 install -r requirements.txt
```

correr tests con pytest
```
pytest
```

correr flask
```
export FLASK_APP=app/app.py
flask run
```