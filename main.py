from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create/access database
db = client["testdb"]

# Create/access collection
collection = db["ems"]

# Dummy employee data
employees = [
    {
        "employee_id": 1001,
        "name": "Han Lee",
        "department": "Engineering",
        "salary": 95000,
        "email": "han@example.com"
    },
    {
        "employee_id": 1002,
        "name": "Alice Kim",
        "department": "HR",
        "salary": 72000,
        "email": "alice@example.com"
    },
    {
        "employee_id": 1003,
        "name": "John Park",
        "department": "Finance",
        "salary": 81000,
        "email": "john@example.com"
    }
]

# Insert many documents
result = collection.insert_many(employees)

print("Inserted IDs:")
print(result.inserted_ids)

print("\nEmployees:\n")

# Read documents
for emp in collection.find():
    print(emp)