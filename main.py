import json

from flask import Flask, Response, request, abort, jsonify
from pymongo import MongoClient

from bson import ObjectId

from model import Product

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

client = MongoClient('localhost', 27017)
collection = client['test_db']['test']


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
        abort(Response('There is no product with this id', 404))
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
            abort(Response(""), 400)
        for sub_par in parameters:
            filt['.'.join(['parameters', sub_par])] = parameters[sub_par]
    product_objects = collection.find(filt)
    if not product_objects:
        abort(Response('There are no products with such characteristics', 404))
    products = [Product(product_obj['_id'], product_obj['title'], product_obj['description'],
                        product_obj['parameters']).json_format() for product_obj in product_objects]
    return jsonify(products)


@app.route('/test/api/products', methods=['POST'])
def create_product():
    if not request.json or 'title' not in request.json:
        abort(Response('Product must have "title"', 400))
    if 'parameters' in request.json and not isinstance(request.json['parameters'], dict):
        abort(Response('Product parameters must be set as list of key/value pairs.\
                        Example - "parameters": {first: f_value, second: s_value}', 400))
    product_id = collection.insert_one({'title': request.json['title'],
                                        'description': request.json.get('description', ''),
                                        'parameters': request.json.get('parameters', {})}).inserted_id
    return Response(json.dumps({'id': str(product_id)}), status=201)


if __name__ == '__main__':
    app.run(debug=True)
