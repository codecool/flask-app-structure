import os


DEBUG = True
CSRF_TOKEN = True
SECRET_KEY = 'mysecretkey'
DB_USER = ''
DB_PASSWORD = ''
DB_NAME = ''
DB_PORT = 5432

DATABASE_URI_FMT = "postgresql+psycopg2://%(db_user)s:%(db_password)s@localhost:%(db_port)s/%(db_name)s"
DATABASE_URI = DATABASE_URI_FMT % {'db_user': DB_USER,
                                    'db_password': DB_PASSWORD,
                                    'db_port': DB_PORT,
                                    'db_name': DB_NAME}

LOG_LOCATION = ''