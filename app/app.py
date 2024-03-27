from flask import Flask, render_template
import json

app=Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def health_check():
    response = {
        'status': 'OK'
    }
    return json.dumps(response), 200

if __name__=='__main__':
    app.run(debug=True, port=5001)