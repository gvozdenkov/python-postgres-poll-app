import configparser
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2 import Error

def config(filename = 'database.ini', section = 'postgresql'):
    parser = configparser.RawConfigParser()
    parser.read(filename)
    parser.has_section(section)
    # print(parser.items(section))

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
            # print(f"{param[0]} = {param[1]}")
    else:
        raise Exception('section {0} not found in the {1} file'.format(section, filename))
        
    return db

postgresSQLparams = config('database.ini', 'postgresql')

print(f"Connecting to the PostgreSQL database '{postgresSQLparams['database']}'...\n")

try:
    postgresql_pool = SimpleConnectionPool(1, 20, **postgresSQLparams)
    if postgresql_pool:
        print("Пул соединений создан успешно")
except (Exception, Error) as error :
  print ("Ошибка при подключении к PostgreSQL", error)

