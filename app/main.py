
from http import HTTPStatus
from datetime import datetime

from flask import Flask, request, abort, render_template, jsonify, Response
from flask_cors import CORS

from defaultLogger import defaultLogger
from ConfigManager import ConfigManager

# -- Flask setup  --------
CONTAINER_ID = open('/etc/hostname').read().strip()
VERSION = open('/app/version').read().strip()

app = Flask(__name__)
cors = CORS(app)

log = defaultLogger('info')

cfgmgr = ConfigManager(log=log)

birth_time = datetime.now()

# -- Routes --------
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', version=VERSION)

@app.route('/schema/<schema>', methods=['GET'])
def getSchema(schema):
    status, data =  cfgmgr.getFile(schema, path='schema')
    if status != HTTPStatus.OK:
        return abort(status, data)

    return data

@app.route('/load/<config>', methods=['GET'])
def getConfig(config):
    status, data =  cfgmgr.getFile(config, path='data')
    if status != HTTPStatus.OK:
        return abort(status, data)

    return data

@app.route('/save/<config>', methods=['POST'])
def saveConfig(config):
    status, msg = cfgmgr.saveConfig(request, config)
    if status != HTTPStatus.OK:
        return abort(status, msg)

    return jsonify(msg)

@app.route('/liveness', methods=['GET'])
def liveness():
    uptime = datetime.now() - birth_time
    data = jsonify(dict(uptime=uptime))
    mystatus = HTTPStatus.OK # Use 5xxx if we have issues
    response = Response(data, status=mystatus, mimetype='application/json')
    return response

@app.route('/readiness', methods=['GET'])
def readiness():
    uptime = datetime.now() - birth_time
    data = jsonify(dict(uptime=uptime))
    mystatus = 200 # Use 5xxx if we have issues
    response = Response(data, status=mystatus, mimetype='application/json')
    return response

@app.route('/health', methods=['GET'])
def health():
    uptime = datetime.now() - birth_time
    return render_template('health.html', uptime=uptime)

@app.route('/version', methods=['GET'])
def show_version():
    return VERSION


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

