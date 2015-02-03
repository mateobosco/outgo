#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
import outgo as model

app = Flask(__name__)
base = model.Base()

@app.route('/')
def index():
    base = model.Base()
    return "Hello, World!"


def make_public_outgo(outgo):
    new_outgo = {}
    for field in outgo:
        if field == '_id':
            new_outgo['uri'] = url_for('get_outgo', outgo_id = outgo['_id'], _external = True)
        else:
            new_outgo[field] = outgo[field]
    return new_outgo

@app.route('/api/v1.0/outgoes', methods = ['POST'])
def create_outgo():
    print request.json
    if not request.json or not 'description' in request.json or not 'cost' or not 'tags':
        abort(400)
    outgo_dic = {
        'description': request.json['description'],
        'cost': request.json.get('cost'),
        'tags': request.json.get('tags', [])
    }
    outgo_id = base.addOutgo(model.createOutgoFromDic(outgo_dic))
    # outgo_dic['_id'] = base.addOutgo(createOutgoFromDic(outgo_dic)
    # outgo_dic.update('_id':outgo_id)
    print type(outgo_dic)
    return jsonify( { 'outgo': make_public_outgo(outgo_dic) } ), 201

if __name__ == '__main__':
    app.run(debug=True)