import pymongo as pymongo

client = pymongo.MongoClient("mongodb+srv://bobjoe:abc@cluster0.j9y1e.mongodb.net/test?retryWrites=true&w=majority")
db2 = client.test

post = {"mmr": "800"}
# db.ian.insert_one(post)
# delete_many = db.ian.delete_many({})
names = ["ian", "liam", "will", "nicky", "steve", "vevey", "yuuki", "aaron", "erik", "cam"]
def add_user(name, db):
    col = db[name]
    col.insert_one(post)

def add_collections(db):
    for i in names:
        col = db[i]
        col.insert_one(post)

def delete_documents_in_all(db):
    for i in names:
        col = db[i]
        col.delete_many({})

def find_docs(db):
    for i in db.ian.find():
        print(i)

def find_last_document(db, col):
    sorted_list = db[col].find().sort("_id", -1).limit(1)

    #print(int(sorted_list[0]["mmr"]) + 3)
    return sorted_list

    # for i in sorted_list:
    #     print(i)

#add_collections(client.mmr)
#delete_documents_in_all(client.mmr)