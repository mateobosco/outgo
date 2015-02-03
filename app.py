#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
import outgo as model
import json
import datetime

app = Flask(__name__)
base = model.Base()

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

############################GET OUTGO BY DATE##############################

@app.route('/api/v1.0/outgo/get_outgoes_by_date', methods = ['GET'])
def get_outgoes_from_date():
    print request.args.keys()
    print request.args.get("start")
    print request.args.get("end")
    json_from = request.args.get("start")
    json_to = request.args.get("end")
    #date_from = datetime.datetime.strptime(json_from,"%Y-%m-%d %H:%M:%S.%f")
    #date_to = datetime.datetime.strptime(json_to,"%Y-%m-%d %H:%M:%S.%f")
    date_from = json.loads(json_from)
    date_to = json.loads(json_to)

    print date_from
    print date_to
    #outgo = base.findById(outgo_id)
    #if not outgo: abort(404)
    #return jsonify( { 'outgo': make_public_outgo(outgo) } )
    return "bla"



if __name__ == '__main__':
    app.run(debug=True)