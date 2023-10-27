
from flask import request
from flask_restful import Resource
from ..service import parse_input_data,getJsonFormats,generateSqlQueries


class identifyJsonFormatView(Resource):
    def post(self):
        text_data = request.data.decode('utf-8')
        jsonlist=parse_input_data(text_data)
        return getJsonFormats(jsonlist)

class generateSQLQueriesView(Resource):
    def post(self):
        data = request.get_json()
        return generateSqlQueries(data)

