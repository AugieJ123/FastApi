from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings  # For production...

# Connect to the postgress database
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Start the database connection by the URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session for the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # Connecting to the database. If fail will return an error and wait for 2 seconds then it restart the connection.
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='FastAPI', user='postgres', password='', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connected!")
#         break
#     except (Exception, psycopg2.Error) as error:
#         print("Error while connecting to PostgreSQL", error)
#         print('Error:', error)
#         time.sleep(2)