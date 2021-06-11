import azure.functions as func
import pymongo
import json
from bson.json_util import dumps


def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        # TODO: Update with appropriate MongoDB connection information
        url = 'mongodb://neighborlycosmos:DUfTgid0ve7kaAaAoj4cDnuPYj2RoYlPNALBCEZDkCpFbNkOXRZF7ptlzKJtuIoYd2H95abeGH9RMLINrQA7cQ==@neighborlycosmos.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@neighborlycosmos@'

        client = pymongo.MongoClient(url)
        database = client['neighborlydb']
        collection = database['advertisements']

        result = collection.find({})
        result = dumps(result)

        return func.HttpResponse(result, mimetype="application/json", charset='utf-8')
    except:
        print("could not connect to mongodb")
        return func.HttpResponse("could not connect to mongodb",
                                 status_code=400)
