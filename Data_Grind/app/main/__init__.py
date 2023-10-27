from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/mydb'
    api = Api(app)
    db.init_app(app)
    from ..main.controller import identifyJsonFormatView,createSQLSchemaView,relationGenerationServiceView,generateSQLQueriesView
    api.add_resource(identifyJsonFormatView, '/identify_json_formats/')
    api.add_resource(createSQLSchemaView, '/create_schemas/')
    api.add_resource(relationGenerationServiceView, '/create_relations/')
    api.add_resource(generateSQLQueriesView, '/generate_sql_queries/')
    return app