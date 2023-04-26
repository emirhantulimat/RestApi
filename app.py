from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Sample API', description='A sample API')

# Sample data
data = [
    {'id': 1, 'name': 'John'},
    {'id': 2, 'name': 'Jane'}
]

# Model for data
model = api.model('Data', {'id': fields.Integer, 'name': fields.String})

# Endpoints
@api.route('/data')
class DataList(Resource):
    @api.marshal_list_with(model)
    def get(self):
        '''List all data'''
        return data

    @api.expect(model)
    @api.marshal_with(model, code=201)
    def post(self):
        '''Create new data'''
        new_data = api.payload
        new_data['id'] = len(data) + 1
        data.append(new_data)
        return new_data, 201


@api.route('/data/<int:id>')
@api.response(404, 'Data not found')
class Data(Resource):
    @api.marshal_with(model)
    def get(self, id):
        '''Get data with given ID'''
        for d in data:
            if d['id'] == id:
                return d
        api.abort(404)

    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
        '''Update data with given ID'''
        for d in data:
            if d['id'] == id:
                d.update(api.payload)
                return d
        api.abort(404)

    @api.response(204, 'Data deleted')
    def delete(self, id):
        '''Delete data with given ID'''
        for i, d in enumerate(data):
            if d['id'] == id:
                data.pop(i)
                return '', 204
        api.abort(404)


if __name__ == '__main__':
    app.run(debug=True)
