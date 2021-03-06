#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for, current_app
import outgo as model
import json
import datetime
from util import ListConverter
from datetime import timedelta
from functools import update_wrapper


app = Flask(__name__)
base = model.Base()
app.url_map.converters['list'] = ListConverter

@app.route('/')
def index():
    return "Hello, World!"

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def make_public_outgo(outgo):
    new_outgo = {}
    for field in outgo:
        if field == '_id':
            new_outgo['uri'] = url_for('get_outgo_by_id', outgo_id = outgo['_id'], _external = True)
        else:
            new_outgo[field] = outgo[field]
    return new_outgo


def datetime_to_dic(date):
    dic = {}
    dic["year"] = date.year
    dic["month"] = date.month
    dic["day"] = date.day
    dic["hour"] = date.hour
    dic["minute"] = date.minute
    dic["second"] = date.second
    dic["microsecond"] = date.microsecond
    dic["tzinfo"] = date.tzinfo
    return dic

def dic_to_datetime(dic):
    return datetime.datetime(dic.get("year"),
                             dic.get("month"),
                              dic.get("day"),
                               dic.get("hour"),
                                dic.get("minute"),
                                dic.get("second"),
                                dic.get("microsecond"),
                                 dic.get("tzinfo"))

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


############################CREATE OUTGO###############################

@app.route('/api/v1.0/outgo', methods = ['POST'])
@crossdomain(origin='*')
def create_outgo():
    if not request.json or not 'description' in request.json or not 'cost' or not 'tags':
        abort(400)
    outgo_dic = {
        'description': request.json['description'],
        'cost': request.json.get('cost'),
        'tags': request.json.get('tags', []),
        'date': request.json.get('date',datetime.datetime.now())
    }
    outgo_id = base.addOutgo(model.createOutgoFromDic(outgo_dic))
    return jsonify( { 'outgo': make_public_outgo(outgo_dic) } ), 201

#######################################################################


###########################GET OUTGO BY ID##############################

@app.route('/api/v1.0/outgo/get_outgo_by_id/<string:outgo_id>', methods = ['GET'])
@crossdomain(origin='*')
def get_outgo_by_id(outgo_id):
    outgo = base.findById(outgo_id)
    if not outgo: abort(404)
    return jsonify( { 'outgo': make_public_outgo(outgo) } )

#######################################################################


###########################GET ALL OUTGOES#############################

@app.route('/api/v1.0/outgo/get_outgoes', methods = ['GET'])
@crossdomain(origin='*')
def get_outgoes():
    outgoes = base.findAll()
    if not outgoes: abort(404)
    return jsonify( { 'outgoes': map(make_public_outgo, outgoes) } )

#######################################################################


############################GET OUTGOES BY DATE########################

@app.route('/api/v1.0/outgo/get_outgoes_by_date/<list:params>', methods = ['GET'])
@crossdomain(origin='*')
def get_outgoes_from_date(params):
    dic_date_start = json.loads(params[0])
    dic_date_end = json.loads(params[1])
    date_start = dic_to_datetime(dic_date_start)
    date_end = dic_to_datetime(dic_date_end)
    outgoes = base.findFromDate(date_start,date_end)
    return jsonify( { 'outgoes': map(make_public_outgo, outgoes) } )

######################################################################


############################GET OUTGOES IN TAGS#######################

@app.route('/api/v1.0/outgo/get_outgoes_in_tags/<list:tags>', methods = ['GET'])
@crossdomain(origin='*')
def get_outgoes_in_tags(tags):
    outgoes = base.findInTags(tags)
    return jsonify( { 'outgoes': map(make_public_outgo, outgoes) } ) 

######################################################################


############################GET OUTGOES WITH TAGS#####################

@app.route('/api/v1.0/outgo/get_outgoes_with_tags/<list:tags>', methods = ['GET'])
@crossdomain(origin='*')
def get_outgoes_with_tags(tags):
    outgoes = base.findWithTags(tags)
    return jsonify( { 'outgoes': map(make_public_outgo, outgoes) } ) 

######################################################################


#######################UPDATE OUTGO BY ID#############################

@app.route('/api/v1.0/outgo/<string:outgo_id>', methods = ['PUT'])
@crossdomain(origin='*')
def update_outgo(outgo_id):
    outgo = base.findById(outgo_id)
    if not outgo: abort(404)
    if not request.json: abort(400)
    if 'cost' in request.json and type(request.json['cost']) != int:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'tags' in request.json and type(request.json['tags']) is not list:
        abort(400)
    if 'date' in request.json and type(request.json['tags']) is not datetime.datetime:
        abort(400)

    outgo['cost'] = request.json.get('cost', outgo['cost'])
    outgo['description'] = request.json.get('description', outgo['description'])
    outgo['tags'] = request.json.get('tags', outgo['tags'])
    outgo['date'] = request.json.get('date', outgo['date'])
    base.updateById(outgo)

    return jsonify( { 'outgo': make_public_outgo(outgo) } )

######################################################################


#####################DELETE OUTGO BY ID###############################

@app.route('/api/v1.0/outgo/<string:outgo_id>', methods = ['DELETE'])
@crossdomain(origin='*')
def delete_outgo(outgo_id):
    outgo = base.findById(outgo_id)
    if not outgo: abort(404)
    base.removeById(outgo)
    return jsonify( { 'result': True } )

######################################################################


if __name__ == '__main__':
    app.run(debug=True)