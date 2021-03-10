from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)

db = client['users1003']
# db2 = client['users_copy']

users = db.users
books = db.books


# users.insert_one({
#                 "author": "Peter2",
#                "age" : '56',
#                "text": "is cool! Wildberry",
#                "tags": ['cool','hot','ice'],
#                "date": '14.06.1983'})

# users.insert_many([{"author": "John",
#                "age" : 29,
#                "text": "Too bad! Strawberry",
#                "tags": ['ice'],
#                "date": '04.08.1971'},
#                     {"author": "Anna",
#                "age" : 36,
#                "title": "Hot Cool!!!",
#                "text": "easy too!",
#                "date": '26.01.1995'},
#                    {"author": "Jane",
#                "age" : 43,
#                "title": "Nice book",
#                "text": "Pretty text not long",
#                "date": '08.08.1975',
#                "tags":['fantastic','criminal']}
#       ])



# result = users.find({'author':'Peter'},{'author': True, 'date':True, '_id':False})
# result = users.find({'age' : {'gt' : 40}},{'author': True, 'age':True, '_id':False})
# result = users.find({}).sort('author', -1)
# result = users.find({}).limit(3)
# result = users.find({'$or':[{'author':'Peter'}, {'age':43}]})

doc = {
    "author": "Petya",
               "age" : 28,
               "text": "is hot!",
               "date": '11.09.1991'}

# users.update_one({'author':'Peter'},{'$set':doc})
# users.update_many({'author':'Peter'},{'$set':doc})

# users.replace_one({'author':'Petya'}, doc)

# users.delete_one({'author':'Peter2'})
# users.delete_many({})


result = users.find({})

for user in result:
    pprint(user)

