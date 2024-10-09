# src/config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'stockflow')  
    SQLALCHEMY_DATABASE_URI = (
        '{dbms}://{username}:{password}@{server}:{port}/{database}'.format(
            dbms='mysql+mysqlconnector',
            username='root',
            password='admin',
            server='localhost',
            port='3306',
            database='sistema_reclamacoes'
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False