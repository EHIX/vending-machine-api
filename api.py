from vending_machine.vending import VendingMachine
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

class Session():
    '''Session class manages the state of the interactive elements in the session'''
    def __init__(self):
        self.vm = None

class Build(Resource):
    def get(self):
        args = request.args
        # build?param=[50, 50, 50, 50, 50, 20, 10, 5]
        session.vm = VendingMachine(json.loads(args['param']))
        out = {i : {"denomination" : "{0:.2f}".format(j/100), "amount" : k} for i, (j, k) in enumerate(session.vm.cash.items())}
        return jsonify({"data" : {"cash" : out}})

class Inventory(Resource):
    def get(self):
        out = {i : {"name" : j, "price" : k} for i, (j, k) in session.vm.inventory.items()}
        return jsonify({"data" : {"inventory" : out}})

class Cash(Resource):
    def get(self):
        out = {i : {'denomination': "{0:.2f}".format(j/100), 'amount': k} for i, (j, k) in enumerate(session.vm.cash.items())}
        return jsonify({"data" : {"cash" : out}})

class Collected(Resource):
    def get(self):
        out = {i : {'denomination': "{0:.2f}".format(j/100), 'amount': k} for i, (j, k) in enumerate(session.vm.collected.items())}
        return jsonify({"data" : {"collected" : out}})

class Terminate(Resource):
    def get(self):
        out, data = session.vm.terminate()
        return jsonify({"data" : {"returned" : {"coins": data}}})

class Add(Resource):
    def get(self, option):
        out = session.vm.insert_coin(option)
        return jsonify({"data" : {"added" : out}})

class Select(Resource):
    def get(self, option):
        out = session.vm.select(option)
        return jsonify({"data" : {"added" : out}})

# api.add_resource(Build, '/build/<denominations>')
api.add_resource(Build, '/build')
api.add_resource(Inventory, '/inventory')
api.add_resource(Cash, '/cash')
api.add_resource(Collected, '/collected')
api.add_resource(Terminate, '/terminate')
api.add_resource(Add, '/add/<int:option>')
api.add_resource(Select, '/select/<int:option>')

if __name__ == '__main__':
    session = Session()
    app.run(port='8080')
