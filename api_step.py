from pydantic import BaseModel, EmailStr, UUID5, ValidationError
import json
import uuid
from uuid import UUID
from email_validator import validate_email, EmailNotValidError
# import aiohttp
from typing import Union
import requests
from requests import RequestException


class AllError(Exception):
    pass


class Client(AllError):
    pass


skip = '\n'


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class Model(BaseModel):
    uuid_id: UUID5
    e_mail_id: EmailStr
    test_api: Union[bool, None] = True


def validator_email(email):
    try:
        validate_email(email)
    except EmailNotValidError:
        return False
    return True


def test(dicts):
    try:

        response = requests.post('http://127.0.0.1:8000', json=dicts)

        print(response.status_code)
        result = response.json()

        return result
    except (ValueError, Client, ValidationError, GeneratorExit, RuntimeError, RequestException) as error:
        print(f'Error connection: {error}')
        pass
    finally:
        pass


def create(dicts):
    print(dicts)
    result = test(dicts)
    print(result)

    return


if __name__ == "__main__":

    send = {'uuid_id': "39182b61569f51e88eba714f06098c75", 'email_id': 'jurijs.01.satalovs@gmail.com', 'test_api': True}
    # send = {0: 125, 17: 754, 'test_api': None}
    create(send)
