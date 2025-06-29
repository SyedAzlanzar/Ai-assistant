from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.db_name]
print(db.name, 'Mongodb Connected succuessfully')  # This will print the name of the database to confirm connection
