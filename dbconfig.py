from pymongo import MongoClient

# client = MongoClient('mongodb+srv://dbuser:dbuser@cluster0.qemcw.mongodb.net/productdb?retryWrites=true&w=majority')

client = MongoClient("mongodb+srv://dbuser:dbuser@cluster0.gurpd.mongodb.net/productdb?retryWrites=true&w=majority")

client1 = MongoClient('mongodb+srv://deepanshu:deepanshu@cluster0.tjz0w.mongodb.net/survey?retryWrites=true&w=majority')

def dbConnection():
    # print(client)
    return client 

def dbConnection2():
    return client1
