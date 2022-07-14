""" Creating a database  and a table  PostgreSql v.13  Python v.3.8.7"""

import psycopg2
from psycopg2 import Error


def create_table(db_name, db_table):
    """  Creating a table """
    try:

        connection = psycopg2.connect(user="postgres", dbname=db_name, password="aa4401", host="127.0.0.1", port="5432", )
        cursor = connection.cursor()
        create_table_query = (f'create table if not exists {db_table}         ' +
                              '  (id SERIAL PRIMARY KEY,   ' +
                              '  email VARCHAR(100),  ' +
                              '  uuid  uuid);'
                              )
        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица успешно создана в PostgreSQL")
        if connection:
            cursor.close()
            connection.close()

    except (Exception, Error, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        print("Соединение с PostgreSQL закрыто")
    return ()


if __name__ == '__main__':

    create_table("fintech", "users")
