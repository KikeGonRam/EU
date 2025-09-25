import random
from faker import Faker
from pymongo import MongoClient

# Configuración de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "demo_db"
COLLECTION_NAME = "personas"

# Inicializar Faker
fake = Faker()

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Generar y agregar un millón de registros
batch_size = 10000
num_records = 1_000_000

for i in range(0, num_records, batch_size):
    batch = []
    for _ in range(batch_size):
        persona = {
            "nombre": fake.first_name(),
            "apellido": fake.last_name(),
            "email": fake.email(),
            "edad": random.randint(18, 90),
            "direccion": fake.address(),
            "telefono": fake.phone_number(),
            "fecha_nacimiento": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
            "genero": random.choice(["M", "F"])
        }
        batch.append(persona)
    collection.insert_many(batch)
    print(f"Insertados {i + batch_size} registros...")

print("¡Un millón de registros insertados en MongoDB!")