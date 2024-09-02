import motor.motor_asyncio

class MongoDB:
    def __init__(self):
        self.client = None
        self.database = None
        self.collections = {}

    async def connect(self, uri: str, db_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)   
        self.database = self.client[db_name]
        collection_names = ['admin', 'course', 'teacher', 'event', 'student', 'attendance', 'hof', 'feedback','school','class','calendar','assignment']
        self.collections = {name: self.database[name] for name in collection_names}
        print("MongoDB connected")

    async def close(self):
        self.client.close()
        print("MongoDB connection closed")

# MongoDB connection details
MONGO_URI = 'mongodb+srv://Sarpit07:Sarpit07@cluster.nvjypyg.mongodb.net/'
DATABASE_NAME = 'Workshop'

mongodb = MongoDB()
