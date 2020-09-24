from flask_restful import Resource
from outh import github

class Github(Resource):
    @classmethod
    def get(cls):
        return github.authorize(callback="http://localhost:5000/login/github/authorized")