from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import json
import methods

app = Flask(__name__)
CORS(app, orgins="*")
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('school', type=str, required=True)
parser.add_argument('interests', type=str, required=True)

class Test(Resource):
    def get(self):
        return {'about': 'whatup'}

class GetCourses(Resource):
    def __init__(self):
        self.school = parser.parse_args().get('school','None')
        self.interests = parser.parse_args().get('interests','None').lower()
    def get(self):
        relevantCourses = methods.getRelevantCourses(self.school, self.interests)
        return {'courses': relevantCourses}

api.add_resource(Test,'/test/')
api.add_resource(GetCourses, '/getcourses/')

if __name__ == '__main__':
    app.run(debug=True)
