import dbconfig as cdb

def get_all_products():
    client = cdb.dbConnection2()
    db = client["surveyapp_ques"]
    col = db['questions']
    finaldata = {
        'name':'',
        'organisation':'',
        'email':'',
        'mobile':'',
        'responsibility':'',
        'address':'',
        'survey':[]
    }
    allsections = []
    for x in col.find({}):
        allsections.append({'id':str(x['_id']),'topicId':x['topicId'],'topicName':x['topicName'],'data':x['data']})   
    finaldata['survey']= allsections
    return finaldata

def post_products(products):
    client = cdb.dbConnection2()
    db = client['surveyapp_ques']
    col = db['answers']
    # print(products)
    col.insert_one({'name':products['name'],'mobile':products['mobile'],'org':products['org'],'respr':products['respr'],'email':products['email'],'address':products['address'],'answers':products['answers']})
    return "data posted"


def add_section(products):
    client = cdb.dbConnection2()
    db = client["surveyapp_ques"]
    col = db['questions']
    # print(products)
    col.insert_one({'topicId':products['topicId'],'topicName':products['topicName'],'data':products['data']})
    return "section posted"