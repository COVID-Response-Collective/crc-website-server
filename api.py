from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import json
from datetime import datetime
from database import Database, Region, Role, RequestType, Status

app = Flask(__name__)
CORS(app)
api = Api(app)
db = Database()

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
        regionValue = request.form.get('region')
        roleValue = request.form.get('role')
        email = request.form.get('email')
        phone = request.form.get('phone')
        requestTypeValue = request.form.get('type')
        details = request.form.get('details')
        neededBy = request.form.get('neededBy')
        public = int(request.form.get('public'))

        regions = [e for e in Region]
        roles = [e for e in Role]
        requestTypes = [e for e in RequestType]

        if email == '':
            email = None

        if phone == '':
            phone = None

        region = [r for r in regions if r == regionValue].pop()
        role = [r for r in roles if r == roleValue].pop()
        requestType = [r for r in requestTypes if r == requestTypeValue].pop()

        status = Status.OPEN
        dateOpened = datetime.now()

        db.cursor.execute("INSERT INTO request (name, region, role, title, agency, jurisdiction, email, phone, request_type, details, neededBy, public, status, dateOpened) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %d, %s, %s) RETURNING rID", (name, region, role, title, agency, jurisdiction, email, phone, requestType, details, neededBy, public, status, dateOpened))
        db.conn.commit()

        results = db.cursor.fetchall()
        for row in results:
            rID = row.pop()
            print("New request ID: %s" % (rID))

        return {
            'console_msg': '[SUCCESS] The request has been recorded! rID = %s' % (rID),
            'msg': 'Thanks for reaching out! Your request has been submitted!',
        }

'''
ADDVOLUNTEERTOREQUEST ENDPOINT
***
This endpoint reads in the ID of a resource request and the name
of a volunteer who has decided to take on the request, and adds
their name to the list of volunteers taking on the request.
'''
class AddVolunteerToRequest(Resource):
    def get(self):
        return {'msg': '[SUCCESS] This endpoint is up and running!'}

    def post(self):
        rID = int(request.form.get('rID'))
        name = request.form.get('name')
        db.cursor.execute("SELECT volunteers FROM requests WHERE rID = %s", (rID))
        db.conn.commit()
        results = db.cursor.fetchall()
        for row in results:
            volunteers = row.pop()
            if volunteers is None:
                volunteers = ''
            else:
                volunteers = volunteers[1:-1]
        volunteerList = volunteers.split(', ')
        volunteerList.append(name)
        volunteers = ''.join(', ')
        db.cursor.execute("UPDATE requests SET volunteers = %s WHERE rID = %s", (volunteers, rID))
        db.conn.commit()
        return {'msg': '[SUCCESS] Added %s to the list of volunteers for the request with rID = %s' % (name, rID)}


'''
STARTREQUEST ENDPOINT
***
This endpoint reads in the ID of a resource request and marks it
as started, changing the status of the request to "in progress."
'''
class StartRequest(Resource):
    def get(self):
        return {'msg': '[SUCCESS] This endpoint is up and running!'}

    def post(self):
        rID = int(request.form.get('rID'))
        db.cursor.execute("UPDATE requests SET status = %s, dateStarted = %s WHERE rID = %s", (Status.IN_PROGRESS, datetime.now(), rID))
        db.conn.commit()
        return {'msg': '[SUCCESS] The request with rID = %s has been started!' %s (rID)}

'''
FULFILLREQUEST ENDPOINT
***
This endpoint reads in the ID of a resource request and marks it
as fulfilled, officially closing the request.
'''
class FulfillRequest(Resource):
    def get(self):
        return {'msg': '[SUCCESS] This endpoint is up and running!'}

    def post(self):
        rID = int(request.form.get('rID'))
        db.cursor.execute("UPDATE requests SET status = %s, dateFulfilled = %s WHERE rID = %s", (Status.FULFILLED, datetime.now(), rID))
        db.conn.commit()
        return {'msg': '[SUCCESS] The request with rID = %s has been fulfilled!' %s (rID)}

api.add_resource(Test, '/test')
api.add_resource(RecChannel, '/connect/rec-channel')
api.add_resource(CreateRequest, '/request/create')
api.add_resource(AddVolunteerToRequest, '/request/add-volunteer')
api.add_resource(StartRequest, '/request/start')
api.add_resource(FulfillRequest, '/request/fulfill')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
