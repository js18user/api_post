""" api_post.py      Python v.3.8.7  FastAPI  Postgresql v.13  os.environ FastAPI_asyncpg     js18.user """

import os
from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr, UUID5, ValidationError
from fastapi_asyncpg import configure_asyncpg
from asyncpg import PostgresError, ProtocolError
import uuid
from typing import Union
from email_validator import validate_email, EmailNotValidError


class ModelIn(BaseModel):
    uuid_id: UUID5
    email_id: EmailStr
    test_api: Union[bool, None] = None


skip = '\n'


async def validator_email(email):
    """ For next scripts """
    try:
        validate_email(email)
    except EmailNotValidError:
        return False
    return True


async def db_connection():
    """ For next scripts """

    conn_environ = configure_asyncpg(app, 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        name=os.environ['DB_NAME']))
    return conn_environ


async def db_operation(email_id, uuid_id, connection):

    q_insert, q_select = 'insert into users (email, uuid) values ( $1, $2 )', \
                                         'select * from users where (email = $1 and uuid = $2 )  '
    async with connection.transaction():

        row_record = await connection.fetchrow(q_select, email_id, uuid_id)
        if row_record is not None:
            pass

        else:
            await connection.executemany(q_insert, [(email_id, uuid_id), ])
            row_record = await connection.fetchrow(q_select, email_id, uuid_id)

    return row_record[0]


def counter(fu):
    """ For next scripts """
    def inner(*a, **kw):
        inner.count += 1
        return fu(*a, **kw)

    inner.count = 0
    return inner


@counter
async def test():
    pass
    return


app = FastAPI()

conn = configure_asyncpg(app, 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user='postgres',
        name='fintech',
        password='aa4401',
        host='localhost',
        port=5432))


@conn.on_init
async def init(db_initial):
    await db_initial.execute("SELECT 0")


@app.post("/")
async def post(model: ModelIn, connection=Depends(conn.connection)):  # (conn.atomic)

    try:
        if validator_email(model.email_id) is False:
            return {"Message": "e-mail address does not meet the standard"}
        else:
            pass
        if model.uuid_id != uuid.uuid5(uuid.NAMESPACE_URL, model.email_id):
            return {"Message": "Only uuid.uuid5 is allowed"}
        else:
            pass

        user_id = 12345
        if model.test_api is not True:
            user_id = await db_operation(model.email_id, model.uuid_id, connection)
        else:
            pass

        return {'id': user_id, 'uuid': model.uuid_id, 'email': model.email_id}

    except (ValueError, ValidationError) as error:
        return {'Message': error}

    except (PostgresError, ProtocolError) as error:
        print('Error into @app.post: ', error)
        return {'Message': 'Technical preventive maintenance on the site'}
    finally:
        pass
