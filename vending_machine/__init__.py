import os
import json
import markdown
from .vending import VendingMachine
from .session import Session
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
session = Session()

@app.route("/")
def index():
    """Present README docs"""
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        return markdown.markdown(markdown_file.read())

class Build(Resource):
    def get(self):
        args = request.args
        session.vm = VendingMachine(json.loads(args['param']))
        response = {i : {"unit" : "{0:.2f}".format(j/100), "amount" : k} for i, (j, k) in enumerate(session.vm.cash.items())}
        return jsonify({"data" : {"cash" : response}, "message" : "vending machine successfully built"})

class Inventory(Resource):
    def get(self):
        response = {i : {"name" : j.lower(), "price" : k} for i, (j, k) in session.vm.inventory.items()}
        return jsonify({"data" : {"inventory" : response}, "message" : "inventory items"})

class Cash(Resource):
    def get(self, option):
        response = {'total' : session.vm.sum_cash()}
        if option:
            response = {i : {'unit': "{0:.2f}".format(j/100), 'amount': k} for i, (j, k) in enumerate(session.vm.cash.items())}
        return jsonify({"data" : {"cash" : response}, "message" : "cash available to vending machine"})

class Collected(Resource):
    def get(self, option):
        response = {'total' : session.vm.sum_collected()}
        if option:
            response = {i : {'unit': "{0:.2f}".format(j/100), 'amount': k} for i, (j, k) in enumerate(session.vm.collected.items())}
        return jsonify({"data" : {"collected" : response}, "message" : "cash collected during transaction"})

class Terminate(Resource):
    def get(self):
        response = session.vm.terminate()
        return jsonify({"data" : {"terminate" : response}, "message" : "transaction terminated"})

class Add(Resource):
    def get(self, option):
        response = session.vm.insert_coin(option)
        return jsonify({"data" : {"add" : response}, "message" : "add coin to vending machine"})

class Select(Resource):
    def get(self, option):
        response = session.vm.select(option)
        return jsonify({"data" : {"select" : response}, "message" : "select item from vending machine"})

api.add_resource(Build, '/build')
api.add_resource(Inventory, '/inventory')
api.add_resource(Cash, '/cash/<int:option>')
api.add_resource(Collected, '/collected/<int:option>')
api.add_resource(Terminate, '/terminate')
api.add_resource(Add, '/add/<int:option>')
api.add_resource(Select, '/select/<int:option>')
