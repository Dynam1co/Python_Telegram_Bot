import psycopg2
import os
import sys

def get_telegram_token():
    return os.getenv('TELEGRAM_TOKEN')


def get_telegram_group_id():
    print ('TELEGRAM_GROUP_ID=' + os.getenv('TELEGRAM_GROUP_ID'))
    return os.getenv('TELEGRAM_GROUP_ID')


def get_connection_by_config():
    postgresql = {
        "host": os.getenv('POSTGRES_HOST'),
        "user": os.getenv('POSTGRES_USER'),
        "password": os.getenv('POSTGRES_PASSWORD'),
        "database": os.getenv('POSTGRES_DATABASE'),
        "port": "5432"
    }
    conn = psycopg2.connect(**postgresql)
    return conn
