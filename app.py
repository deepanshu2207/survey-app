from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from flask.json import JSONEncoder
import productdb as dbs
from security import authenticate,identity
from flask_jwt import JWT, jwt_required,current_identity
from flask_cors import CORS,cross_origin
from pymongo import MongoClient
app = Flask(__name__)
app.config['SECRET_KEY'] = 'app@123!'
jwt = JWT(app,authenticate,identity)
api = Api(app)
CORS(app)
cors=CORS(app, resources={r"/product": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
@cross_origin(origin='*',headers=['Content-Type'])

@app.route("/products")
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin']) 
def all_products():
    return jsonify({"products" :dbs.get_all_products()})

@app.route("/product", methods=['POST']) 
def products():
    request_data = request.get_json()
    # print(request_data)
    print(request_data.get('san',None))
    return jsonify({"products" :dbs.post_products(request_data.get('san'))})


@app.route("/addsection", methods=['POST']) 
def addsection():
    request_data = request.get_json()
    # print(request_data)
    print(request_data.get('sec',None))
    return jsonify({"products" :dbs.add_section(request_data.get('sec',None))})
        

@app.route("/query1",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def query1():
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
    {
        '$project': {
            '_id': 0, 
            'org': 1
        }
    }
    ])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)    

@app.route("/query2_1/<orgname>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def query2_1(orgname):
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
            {
                '$project': {
                    '_id': 0, 
                    'org': 1, 
                    'answers': 1
                }
            }, {
                '$match': {
                    'org': orgname
                }
            }, {
                '$unwind': {
                    'path': '$answers'
                }
            }, {
                '$project': {
                    'org': 1, 
                    'responses': '$answers.que1'
                }
            },
             {
                '$group': {
                    '_id': '$responses', 
                    'count': {
                        '$sum': 1
                    }
                }
            }
        ])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)     



@app.route("/query2_2/<orgname>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def query2_2(orgname):
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
            {
                '$project': {
                    '_id': 0, 
                    'org': 1, 
                    'answers': 1
                }
            }, {
                '$match': {
                    'org': orgname
                }
            }, {
                '$unwind': {
                    'path': '$answers'
                }
            }, {
                '$project': {
                    'org': 1, 
                    'responses': '$answers.que2'
                }
            }
            ,
            {
                '$project': {
                    'responses.extra': 0
                }
            }
            ,{
                '$group': {
                    '_id': '$responses', 
                    'count': {
                        '$sum': 1
                    }
                }
            }
        ])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)     



             
@app.route("/query2_3/<orgname>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def query2_3(orgname):
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
            {
                '$project': {
                    '_id': 0, 
                    'org': 1, 
                    'answers': 1
                }
            }, {
                '$match': {
                    'org': orgname
                }
            }, {
                '$unwind': {
                    'path': '$answers'
                }
            }, {
                '$project': {
                    'org': 1, 
                    'responses': '$answers.que3'
                }
            }, {
                '$group': {
                    '_id': '$responses', 
                    'count': {
                        '$sum': 1
                    }
                }
            }
        ])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)  

@app.route("/query3_1",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def query3_1():
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
            {
                '$project': {
                    '_id': 0, 
                    'org': 1, 
                    'answers': 1
                }
            }, {
                '$unwind': {
                    'path': '$answers'
                }
            }, {
                '$project': {
                    'org': 1, 
                    'responses': '$answers.que1'
                }
            }, {
                '$group': {
                    '_id': '$org', 
                    'Satisfactory': {
                        '$sum': {
                            '$cond': [
                                {
                                    '$eq': [
                                        '$responses.satisfactory', True
                                    ]
                                }, 1, 0
                            ]
                        }
                    }, 
                    'Need_Revamp': {
                        '$sum': {
                            '$cond': [
                                {
                                    '$eq': [
                                        '$responses.needRevamp', True
                                    ]
                                }, 1, 0
                            ]
                        }
                    }, 
                    'New_Program': {
                        '$sum': {
                            '$cond': [
                                {
                                    '$eq': [
                                        '$responses.newprogram', True
                                    ]
                                }, 1, 0
                            ]
                        }
                    }
                }
            }
            ])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst) 


@app.route("/query3_2",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def query3_2():
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
    {
        '$project': {
            '_id': 0, 
            'org': 1, 
            'answers': 1
        }
    }, {
        '$unwind': {
            'path': '$answers'
        }
    }, {
        '$project': {
            'org': 1, 
            'responses': '$answers.que2'
        }
    }, {
        '$group': {
            '_id': '$org', 
            'Administrative': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$responses.adm', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'Pedagogical': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$responses.peda', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'Other': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$responses.other', True
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    }
])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst) 



@app.route("/query3_3",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def query3_3():
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
    {
        '$project': {
            '_id': 0, 
            'org': 1, 
            'answers': 1
        }
    }, {
        '$unwind': {
            'path': '$answers'
        }
    }, {
        '$project': {
            'org': 1, 
            'responses': '$answers.que3'
        }
    }, {
        '$group': {
            '_id': '$org', 
            'Long': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$responses.long', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'Short': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$responses.short', True
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    }
])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)     
 
    

@app.route('/userinfo')
@jwt_required()
def protected():
    return '%s' % current_identity

@app.route("/all_data_q1",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def all_data_q1():
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
            {
                '$project': {
                    '_id': 0, 
                    'answers.que1': 1
                }
            }, {
                '$unwind': {
                    'path': '$answers'
                }
            }, {
                '$group': {
                    '_id': 'All Organizations', 
                    'Satisfactory': {
                        '$sum': {
                            '$cond': [
                                {
                                    '$eq': [
                                        '$answers.que1.satisfactory', True
                                    ]
                                }, 1, 0
                            ]
                        }
                    }, 
                    'Need_Revamp': {
                        '$sum': {
                            '$cond': [
                                {
                                    '$eq': [
                                        '$answers.que1.needRevamp', True
                                    ]
                                }, 1, 0
                            ]
                        }
                    }, 
                    'New_Program': {
                        '$sum': {
                            '$cond': [
                                {
                                    '$eq': [
                                        '$answers.que1.newprogram', True
                                    ]
                                }, 1, 0
                            ]
                        }
                    }
                }
            },
            {
             '$project': {
                '_id': 0
            }
    }
        ])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)

@app.route("/all_data_q2",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def all_data_q2():
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
            {
                '$project': {
                    '_id': 0, 
                    'answers.que2': 1
                }
            }, {
                '$unwind': {
                    'path': '$answers'
                }
            }, {
                '$group': {
                    '_id': 'All Organizations', 
                    'Administrative': {
                        '$sum': {
                            '$cond': [
                                {
                                    '$eq': [
                                        '$answers.que2.adm', True
                                    ]
                                }, 1, 0
                            ]
                        }
                    }, 
                    'Pedagogical': {
                        '$sum': {
                            '$cond': [
                                {
                                    '$eq': [
                                        '$answers.que2.peda', True
                                    ]
                                }, 1, 0
                            ]
                        }
                    }, 
                    'Other': {
                        '$sum': {
                            '$cond': [
                                {
                                    '$eq': [
                                        '$answers.que2.other', True
                                    ]
                                }, 1, 0
                            ]
                        }
                    }
                }
            },
            {
             '$project': {
                '_id': 0
            }
        }
        ])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)

@app.route("/all_data_q3",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def all_data_q3():
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
            {
                '$project': {
                    '_id': 0, 
                    'answers.que3': 1
                }
            }, {
                '$unwind': {
                    'path': '$answers'
                }
            }, {
                '$group': {
                    '_id': 'All Organizations', 
                    'Long': {
                        '$sum': {
                            '$cond': [
                                {
                                    '$eq': [
                                        '$answers.que3.long', True
                                    ]
                                }, 1, 0
                            ]
                        }
                    }, 
                    'Short': {
                        '$sum': {
                            '$cond': [
                                {
                                    '$eq': [
                                        '$answers.que3.short', True
                                    ]
                                }, 1, 0
                            ]
                        }
                    }
                }
            },
            {
             '$project': {
                '_id': 0
            }
        }
      ])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)


@app.route("/allsections",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def allsections():
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['questions']
    result = col.aggregate([
            {
                '$project': {
                    '_id': 0, 
                    'topicName': 1
                }
            }
        ])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)

@app.route("/<selectedsectionindex>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def allquesofsection(selectedsectionindex):
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['questions']
    result = col.aggregate([
    {
        '$project': {
            '_id': 0, 
            'data.ref': 1
        }
    }, {
        '$match': {
            'data.ref': {
                '$regex': selectedsectionindex+'.'
            }
        }
    }
])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)         


@app.route("/selectedsection_q1/<selectedsectionindex>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def selectedsection_q1(selectedsectionindex):
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
    {
        '$unwind': {
            'path': '$answers'
        }
    }, {
        '$match': {
            'answers.ref': {
                '$regex': selectedsectionindex+'.'
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'answers.que1': 1
        }
    }, {
        '$group': {
            '_id': 'All Organizations', 
            'Satisfactory': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que1.satisfactory', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'Need_Revamp': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que1.needRevamp', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'New_Program': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que1.newprogram', True
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    },
            {
             '$project': {
                '_id': 0
            }
        }
])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)  

@app.route("/selectedsection_q2/<selectedsection>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def selectedsection_q2(selectedsection):
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
    {
        '$unwind': {
            'path': '$answers'
        }
    }, {
        '$match': {
            'answers.ref': {
                '$regex': '1.'
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'answers.que2': 1
        }
    }, {
        '$group': {
            '_id': 'All Organizations', 
            'Administrative': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que2.adm', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'Pedagogical': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que2.peda', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'Other': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que2.other', True
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    },
            {
             '$project': {
                '_id': 0
            }
        }
])

    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)

@app.route("/selectedsection_q3/<selectedsection>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def selectedsection_q3(selectedsection):
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
    {
        '$unwind': {
            'path': '$answers'
        }
    }, {
        '$match': {
            'answers.ref': {
                '$regex': '1.'
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'answers.que3': 1
        }
    }, {
        '$group': {
            '_id': 'All Organizations', 
            'Long': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que3.long', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'Short': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que3.short', True
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    },
            {
             '$project': {
                '_id': 0
            }
        }
])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)


@app.route("/que1/<selectedque>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def selectedque_q1(selectedque):
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
    {
        '$unwind': {
            'path': '$answers'
        }
    }, {
        '$match': {
            'answers.ref': selectedque
        }
    }, {
        '$project': {
            '_id': 0, 
            'answers.que1': 1
        }
    }, {
        '$group': {
            '_id': 'All Organizations', 
            'Satisfactory': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que1.satisfactory', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'Need_Revamp': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que1.needRevamp', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'New_Program': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que1.newprogram', True
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    }, {
        '$project': {
            '_id': 0
        }
    }
])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst) 

@app.route("/que2/<selectedque>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def selectedque_q2(selectedque):
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
    {
        '$unwind': {
            'path': '$answers'
        }
    }, {
        '$match': {
            'answers.ref': selectedque
        }
    }, {
        '$project': {
            '_id': 0, 
            'answers.que2': 1
        }
    }, {
        '$group': {
            '_id': 'All Organizations', 
            'Administrative': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que2.adm', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'Pedagogical': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que2.peda', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'Other': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que2.other', True
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    }, {
        '$project': {
            '_id': 0
        }
    }
])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst) 


@app.route("/que3/<selectedque>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Access-Control-Allow-Origin'])
def selectedque_q3(selectedque):
    client = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')
    db = client["surveyapp_ques"]
    col = db['answers']
    result = col.aggregate([
    {
        '$unwind': {
            'path': '$answers'
        }
    }, {
        '$match': {
            'answers.ref': selectedque
        }
    }, {
        '$project': {
            '_id': 0, 
            'answers.que3': 1
        }
    }, {
        '$group': {
            '_id': 'All Organizations', 
            'Long': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que3.long', True
                            ]
                        }, 1, 0
                    ]
                }
            }, 
            'Short': {
                '$sum': {
                    '$cond': [
                        {
                            '$eq': [
                                '$answers.que3.short', True
                            ]
                        }, 1, 0
                    ]
                }
            }
        }
    }, {
        '$project': {
            '_id': 0
        }
    }
])
    lst = []
    for i in result:
        lst.append(i)
    return jsonify(lst)                


port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
 


