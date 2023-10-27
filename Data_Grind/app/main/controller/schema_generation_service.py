from flask import request
from flask_restful import Resource
from ..service import createSQLQueries

class createSQLSchemaView(Resource):
    def post(self):
        data = request.get_json()
        sql_schemas=createSQLQueries(data)
        return sql_schemas