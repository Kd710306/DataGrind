from flask import request
from flask_restful import Resource
from ..service import createAlterSQLQueries


class relationGenerationServiceView(Resource):
    def post(self):
        data = request.get_json()
        sql_schemas=createAlterSQLQueries(data)
        return sql_schemas
