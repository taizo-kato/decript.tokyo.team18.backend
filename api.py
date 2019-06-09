from flask import Flask, jsonify, request, make_response
from tinydb import TinyDB, Query
from flask_cors import CORS

app = Flask(__name__)
db = TinyDB('comeon.json')
CORS(app)


def _get_table(table):
    return db.table(table)


def _jsonify_no_content():
    response = make_response('', 204)
    response.mimetype = app.config['JSONIFY_MIMETYPE']
    return response


@app.route("/events", methods=["GET"])
def events():
    table = _get_table('events')
    if request.args.get('userId') is not None:
        que = Query()
        event_data = table.search(que.userId == request.args.get('userId'))
    elif request.args.get('contractAddress') is not None:
        que = Query()
        event_data = table.search(que.contractAddress == request.args.get('contractAddress'))
    else:
        event_data = table.all()
    return jsonify(event_data)


@app.route("/events", methods=["POST"])
def create_event():
    request_data = request.json
    data = {
        'userId': request_data['userId'],
        'contractAddress': request_data['contractAddress'],
        'eventName': request_data['eventName'],
        'eventDescription': request_data['eventDescription'],
        'eventType': request_data['eventType'],
        'prizeType': request_data['prizeType'],
        'totalPrizeAmount': request_data['totalPrizeAmount'],
        'numberOfWinners': request_data['numberOfWinners'],
        'startDate': request_data['startDate'],
        'endDate': request_data['endDate'],
    }
    table = _get_table('events')
    table.insert(data)
    return _jsonify_no_content()


@app.route("/events/<eventAddress>", methods=["GET"])
def event_detail(eventAddress):
    que = Query()
    table = _get_table('events')
    event_data = table.search(que.contractAddress == eventAddress)
    return jsonify(event_data[0])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')


