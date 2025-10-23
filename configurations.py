from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()


uri = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.employee_management_db
employee_coll = db["employee_data"]
dept_coll = db["department_data"]
attendance_coll = db["attendance_data"]
