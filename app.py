#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
import outgo as model
import json
import datetime
from util import ListConverter


app = Flask(__name__)
base = model.Base()
app.url_map.converters['list'] = ListConverter

@app.route('/')
def index():
    return "Hello, World!"

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

############################CREATE OUTGO###############################

@app.route('/api/v1.0/outgoes', methods = ['POST'])
def create_outgo():
    if not request.json or not 'description' in request.json or not 'cost' or not 'tags':
        abort(400)
    outgo_dic = {
        'description': request.json['description'],
        'cost': request.json.get('cost'),
        'tags': request.json.get('tags', [])
    }
    outgo_id = base.addOutgo(model.createOutgoFromDic(outgo_dic))
    return jsonify( { 'outgo': make_public_outgo(outgo_dic) } ), 201


#######################################################################



###########################GET OUTGO###################################

@app.route('/api/v1.0/outgo/get_outgo_by_id/<string:outgo_id>', methods = ['GET'])
def get_outgo_by_id(outgo_id):
    outgo = base.findById(outgo_id)
    if not outgo: abort(404)
    return jsonify( { 'outgo': make_public_outgo(outgo) } )

#######################################################################


###########################GET ALL OUTGO###############################

@app.route('/api/v1.0/outgo/get_outgoes', methods = ['GET'])
def get_outgoes():
    outgoes = base.findAll()
    if not outgoes: abort(404)
    return jsonify( { 'outgoes': map(make_public_outgo, outgoes) } )


#######################################################################

############################GET OUTGO BY DATE##########################

@app.route('/api/v1.0/outgo/get_outgoes_by_date/<list:params>', methods = ['GET'])
def get_outgoes_from_date(params):
    dic_date_start = json.loads(params[0])
    dic_date_end = json.loads(params[1])
    date_start = dic_to_datetime(dic_date_start)
    date_end = dic_to_datetime(dic_date_end)
    outgoes = base.findFromDate(date_start,date_end)
    return jsonify( { 'outgoes': map(make_public_outgo, outgoes) } )




if __name__ == '__main__':
    app.run(debug=True)