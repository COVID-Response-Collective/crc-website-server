from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import json
from datetime import datetime
from database import Database, Role, Status

app = Flask(__name__)
CORS(app)
api = Api(app)

'''
TEST ENDPOINT
***
This endpoint is used to test that the server is up and running.
'''
class Test(Resource):
    def get(self):
        return {'msg': '[SUCCESS] The server is up and running!'}

'''
RECCHANNEL ENDPOINT
***
This endpoint reads in the user's response to the questionnaire
and returns a list of Discord channel recommendations, grouped
by category.
'''
class RecChannel(Resource):
    def get(self):
        return {'msg': '[SUCCESS] This endpoint is up and running!'}

    def post(self):
        recommendedChannels = dict()
        responses = request.form.get('responses')
        with open('utils/questionnaire_map.json') as f:
            questionnaireMap = json.load(f)
        for resp in responses:
            try:
                qResponse = next(q for q in questionnaireMap if q['question'] == resp['question'])
                answer = next(o for o in qResponse['options'] if o['answer'] == resp['answer'])
                channels = answer['channels']
                for ch in channels:
                    if ch['name'] in recommendedChannels.keys():
                        recommendedChannels[ch['name']] += ch['weight']
                    else:
                        recommendedChannels[ch['name']] = ch['weight']
            except Exception:
                returned_data = {'msg': '[ERROR] There was an error parsing the questionnaire responses.'}
                return 
        returned_data = {
            'msg': '[SUCCESS] Returned recommended channels.',
            'channels': recommendedChannels.keys()
        }
        return json.dumps(returned_data), 201

'''
CREATEREQUEST ENDPOINT
***
This endpoint reads in a resource request and creates a record for
the request in the database, officially opening the request..
'''
class CreateRequest(Resource):
    def get(self):
        return {'msg': '[SUCCESS] This endpoint is up and running!'}

    def post(self):
        name = request.form.get('name')
        roleValue = request.form.get('role')
        email = request.form.get('email')
        phoneValue = request.form.get('phone')
        req = request.form.get('request')

        if email == '':
            email = None
        if phoneValue == '':
            phone = None
        else:
            phone = phoneValue
        if roleValue == 1:
            role = Role.COMM
        else:
            role = Role.EMAUTH
        status = Status.OPEN
        dateOpened = datetime.now()

        db = Database()
        db.cursor.execute("INSERT INTO requests (name, role, email, phone, request, status, dateOpened) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING rID", (name, role, email, phone, req, status, dateOpened))
        db.conn.commit()
        
        results = db.cursor.fetchall()
        for row in results:
            rID = row.pop()
            print("New request ID: %s" % (rID))
        return {'msg': '[SUCCESS] The request has been recorded! rID = %s' % rID}

'''
FULFILLREQUEST ENDPOINT
***
This endpoint reads in the ID of a resource request and marks it
as fulfilled, officially closing the request..
'''
class FulfillRequest(Resource):
    def get(self):
        return {'msg': '[SUCCESS] This endpoint is up and running!'}

    def post(self):
        rID = int(request.form.get('rID'))
        db = Database()
        db.cursor.execute("UPDATE requests SET status = %s, dateFulfilled = %s WHERE rID = %s", (Status.FULFILLED, datetime.now(), rID))
        db.conn.commit()
        return {'msg': '[SUCCESS] The request with rID = %s has been fulfilled!' %s rID}

api.add_resource(Test, '/')
api.add_resource(RecChannel, '/connect/rec-channel')
api.add_resource(CreateRequest, '/request/create')
api.add_resource(FulfillRequest, '/request/fulfill')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
