from flask import Flask
from flask_restful import reqparse, abort,Resource, Api
from covid19 import COVID19

app = Flask(__name__)
api = Api(app)

# cria a classe a ser trabalhada

covid19 = COVID19() # muito demorado pois você baixa, e extrai um arquivo rar!!!

parser = reqparse.RequestParser()
parser.add_argument('task')
raw_data = covid19.get_raw_data()


class Raw_data_covid19(Resource):
    def get(self):
        return raw_data.head(10).to_json(orient="split")

    
class Filter_raw_data_covid19(Resource):
    def get(self, column_id):
        return raw_data[column_id].head(10).to_json(orient="split"), 201
        
class Filter_data_covid19(Resource):

    def get(self, UF_id, city_id):
        return covid19.data_analysis(UF_id, city_id).head(10).to_json(orient='split')
 
    
api.add_resource(Raw_data_covid19, '/raw_data')
api.add_resource(Filter_raw_data_covid19, '/raw_data/<column_id>')
api.add_resource(Filter_data_covid19, '/covid19_filter_data/<UF_id>/<city_id>')

if __name__ == '__main__':
    app.run(debug=True)
