from flask import Flask
from flask_restful import Resource, Api
import json


app = Flask(__name__)
api = Api(app)

'''
TEST ENDPOINT
***
This endpoint is used to test that the server is up and running.
'''
class Test(Resource):
    def get(self):
        return {'msg': '[SUCCESS] The Test endpoint is up and running!'}

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
                return {'msg': '[ERROR] There was an error parsing the questionnaire responses.'}

api.add_resource(Test, '/')
api.add_resource(RecChannel, '/recchannel')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
