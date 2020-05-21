from vending_machine.vending import VendingMachine
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)


class Session():
    '''Session class manages the state of the interactive elements in the session'''
    def __init__(self):
        self.vm = None

class Build(Resource):
    # def get(self, denominations):
    def get(self):
        standard = [50, 50, 50, 50, 50, 20, 10, 5]
        session.vm = VendingMachine(standard)
        out = {i : {"denomination" : j, "amount" : k} for i, (j, k) in enumerate(session.vm.cash.items())}
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
        out = session.vm.terminate()
        return jsonify({"data" : {"message" : out}})

class Add(Resource):
    def get(self):
        return 0

class Selection(Resource):
    def get(self):
        return 0

# api.add_resource(Build, '/build/<denominations>')
api.add_resource(Build, '/build')
api.add_resource(Inventory, '/inventory')
api.add_resource(Cash, '/cash')
api.add_resource(Collected, '/collected')
api.add_resource(Terminate, '/terminate')


if __name__ == '__main__':
    session = Session()
    app.run(port='8080')
