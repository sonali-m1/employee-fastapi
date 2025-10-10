from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://sonusemail_db_user:bvumrTHDE0PfGyoZ@employee-practice.iunxpst.mongodb.net/?retryWrites=true&w=majority&appName=employee-practice"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.employee_db
collection = db["employee_data"]
