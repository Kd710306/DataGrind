from ..service.constants import data_type_mapping
from collections import defaultdict
from app.main import db


def provideSchemasQueries(table_data):
    sql_queries = []
    sql_schemas={}
    for table_name, columns in table_data.items():
        create_table_query = f"CREATE TABLE {table_name} ("
        if "id" not in [column[0] for column in columns]:
            columns.insert(0,["id", "<class 'int'>"])
        columns_details={}
        for column_name, python_data_type in columns:
            sql_data_type = data_type_mapping.get(python_data_type, "VARCHAR(255)")
            columns_details[column_name]=sql_data_type
            create_table_query += f"{column_name} {sql_data_type}, "

        create_table_query = create_table_query[:-2]
        sql_schemas[table_name]=columns_details
        create_table_query += ");"
        sql_queries.append(create_table_query)
    return sql_queries,sql_schemas
    
def createRelationships(relationships,table_data):
    sql_queries=[]
    sql_schemas={}
    sql_schemas['relationships']={}
    for key, val in relationships.items():
        table1,column1 = key.split(".")
        table2,column2 = val.split(".")
        if column1 not in [i[0] for i in table_data[table1]]:
            continue
        primary_key_query = f"ALTER TABLE {table1} ADD PRIMARY KEY ({column1});"
        foreign_key_query = f"ALTER TABLE {table2} ADD FOREIGN KEY ({column2}) REFERENCES {table1}({column1});"
        sql_queries.append(foreign_key_query)
        sql_queries.append(primary_key_query)
        sql_schemas['relationships'][key]=val
    return sql_queries,sql_schemas

def createAlterSQLQueries(data,execute=True):
    table_data = defaultdict(list)
    find_entities(data['json'],table_data, "base")
    alter_sql_queries=[]
    alter_sql_schemas={}
    if "relationships" in data.keys():          
            relationships = data['relationships']
            alter_sql_queries,alter_sql_schemas=createRelationships(relationships, table_data)
    else:
        return {}
    if execute:
        sql_string = "\n".join(alter_sql_queries)
        formatted_sql_string = f'"""\n{sql_string}\n"""'

        #the below code needs o be updated with proper connection param
        # with db.engine.connect() as connection:
        #     connection.execute(formatted_sql_string)
        return alter_sql_schemas
    else:
        return alter_sql_queries
    
def createSQLQueries(data, execute=True):
    table_data = defaultdict(list)
    find_entities(data['json'],table_data, "base")
    sql_queries,sql_schemas = provideSchemasQueries(table_data)
    if execute:
        sql_string = "\n".join(sql_queries)
        formatted_sql_string = f'"""\n{sql_string}\n"""'
        #the below code needs o be updated with proper connection param
        # with db.engine.connect() as connection:
        #     connection.execute(formatted_sql_string)
        return sql_schemas
    else:
        return sql_queries

def generateSqlQueries(data):
    sql_queries=createSQLQueries(data,False)
    alter_sql_queries=createAlterSQLQueries(data,False)
    sql_queries.extend(alter_sql_queries)
    return sql_queries

def find_entities(data,sol, key_val):
    table_data=[]
    for key, val in data.items():
        if type(val) == list and len(val) and type(val[0])==dict:
            find_entities(val[0], sol, key)
            continue
        if type(val)==dict:
            find_entities(val,sol, key)
            continue
        table_data.append([key,str(type(val))])
    sol[key_val]=table_data