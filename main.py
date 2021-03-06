import json

from flask import Flask, Response, request, abort, jsonify
from pymongo import MongoClient

from bson import ObjectId

from model import Product

import constants

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

client = MongoClient('localhost', 27017)
collection = client['products_db']['product_list']


@app.route('/test/api/products', methods=['GET'])
def get_all():
    product_list = list(collection.find())
    products = [Product(pr['_id'], pr['title'], pr['description'], pr['parameters']).json_format()
                for pr in product_list]
    return json.dumps(products, indent=2)


@app.route('/test/api/products/<pr_id>', methods=['GET'])
def get_by_id(pr_id):
    product_object = collection.find_one({'_id': ObjectId(pr_id)})
    if not product_object:
        abort(Response(constants.ID_NOT_FOUND_MESSAGE, 404))
    product = Product(product_object['_id'], product_object['title'], product_object['description'],
                      product_object['parameters'])
    return jsonify(product.json_format())


@app.route('/test/api/products/find', methods=['GET'])
def get_by_filter():
    filt = {}
    if 'title' in request.json:
        filt['title'] = request.json['title']
    if 'parameters' in request.json:
        parameters = request.json['parameters']
        if not isinstance(parameters, dict):
            abort(Response(constants.INVALID_PARAMETERS_MESSAGE, 400))
        for sub_par in parameters:
            filt['.'.join(['parameters', sub_par])] = parameters[sub_par]
    product_objects = collection.find(filt)
    products = [Product(product_obj['_id'], product_obj['title'], product_obj['description'],
                        product_obj['parameters']).json_format() for product_obj in product_objects]
    if not products:
        abort(Response(constants.PRODUCTS_WITH_CHARS_NOT_FOUND_MESSAGE, 404))
    return jsonify(products)


@app.route('/test/api/products', methods=['POST'])
def create_product():
    if not request.json or 'title' not in request.json:
        abort(Response(constants.NO_TITLE_MESSAGE, 400))
    if 'parameters' in request.json and not isinstance(request.json['parameters'], dict):
        abort(Response(constants.INVALID_PARAMETERS_MESSAGE, 400))
    product_id = collection.insert_one({'title': request.json['title'],
                                        'description': request.json.get('description', ''),
                                        'parameters': request.json.get('parameters', {})}).inserted_id
    return Response(json.dumps({'id': str(product_id)}), status=201)


if __name__ == '__main__':
    app.run(debug=True)
