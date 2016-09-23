#!/usr/bin/env python3

import json
from flask import Flask, Response

app = Flask(__name__)
r = None


@app.route('/<sport>/teams', methods=['GET'])
def teams(sport):
    json_data = r.get('%s:teams' % sport)
    resp = Response(response=json_data, status=200, mimetype='application/json')
    return resp


@app.route('/<sport>/seasons', methods=['GET'])
def seasons(sport):
    json_data = r.get('%s:seasons' % sport)
    resp = Response(response=json_data, status=200, mimetype='application/json')
    return resp


#@app.route('/<sport>/rounds/', defaults={'round': None}, methods=['GET'])
@app.route('/<sport>/rounds/<round>', methods=['GET'])
def rounds(sport, round):
    json_data = r.lindex('%s:rounds' % sport, round)
    resp = Response(response=json_data, status=200, mimetype='application/json')
    return resp


@app.route('/<sport>/games/<game>', methods=['GET'])
def games(sport, game):
    json_data = r.lindex('%s:games' % sport, game)
    resp = Response(response=json_data, status=200, mimetype='application/json')
    return resp


def listen(redis_handle):
    global r
    r = redis_handle
    app.run(host='0.0.0.0')
