""" api_test.py  Python v.3.8.7,  asyncio/await, AioHTTP , uuid.UUID ,  UUIDEncoder/json.JSONEncoder     js18.user   """

import asyncio
import aiohttp
import time
import uuid
import datetime
from uuid import UUID
import json
from typing import Union
from pydantic import BaseModel, EmailStr, UUID5, ValidationError
# from aiohttp import ClientError


class AllError(Exception):
    pass


class Client(AllError):
    pass


class Model(BaseModel):
    uuid_id: UUID5
    email_id: EmailStr
    test_api: Union[bool, None] = None


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


skip = '\n'


async def test(task_number, connection_number, mail_name, api_only):

    try:
        print(f'Start async task_number:({task_number}), {datetime.datetime.now()}')

        async with aiohttp.ClientSession(read_bufsize=2 ** 12, ) as session:

            for connect in range(connection_number):
                email = ''.join((mail_name, str(task_number), str(connect), '@test.com'), )

                async with session.post('http://127.0.0.1:8000',
                                        json=json.loads(json.dumps(
                                            Model(uuid_id=uuid.uuid5(uuid.NAMESPACE_URL, email),
                                                  email_id=email, test_api=api_only).dict(), cls=UUIDEncoder), )) as response:
                    await response.json()

                    if response.status != 200:
                        print(f' error test, response.status is: {response.status}', skip,
                              f'email is: {email}',
                              )

                    # print(f'Transaction: task {task_number} connection {connect}')
                    """  Print for control every transaction"""

                    await asyncio.sleep(0.0)
                await asyncio.sleep(0.0)
            await asyncio.sleep(0.0)
        await asyncio.sleep(0.0)

        print(f'End   async task_number:({task_number}), {datetime.datetime.now()}')

    except (ValueError, Client, ValidationError, GeneratorExit, RuntimeError) as error:
        print(f'Error connection: task {task_number} connection {connection_number}  ', skip,
              f'Error:{error}')
        pass

    except KeyboardInterrupt:
        pass
    finally:
        await session.close()
        pass

    return()


async def asynchronous(t_numbers, n_connections, mail_name, api_only):

    futures = [test(task_number, n_connections, mail_name, api_only)
               for task_number in range(t_numbers)
               ]
    for i, future in enumerate(asyncio.as_completed(futures)):
        await future


def main(t_numbers, n_connections, mail_name, api_only):
    try:
        message = '(only API)'
        if api_only is None:
            message = '(include DB)'

        print(skip,
              f'***** Test {message} ******', skip,
              f'Number_of_tasks is: {t_numbers}', skip,
              f'Number_of_connections into task is:  {n_connections}', skip,
              f'Number_of_connections in test is:   {t_numbers * n_connections}', skip,
              )

        start_time = time.time()

        asyncio.get_event_loop().run_until_complete(asynchronous(t_numbers, n_connections, mail_name, api_only))

        print(skip,
              f'The medium time of one  connection is: ',
              f'{round((time.time() - start_time) * 1000 / (t_numbers * n_connections))} ms',
              )

        print(skip,
              '************** Test end **************', skip
              )

    except (Client, GeneratorExit) as error:

        print('error : ', error)
        pass
    except (KeyboardInterrupt, ):
        pass
    finally:
        pass
    return ()


if __name__ == "__main__":

    number_of_tasks = 10
    """ number of concurrent tasks """

    number_of_connections_in_task = 1000
    """ number of calls to api in one task """

    prefix_of_mail = 'Test.1203'
    """ initial characters in the email address name field """

    test_api_only = None
    """ True - without db connecting, only api, else: None - with db connecting"""

    main(number_of_tasks, number_of_connections_in_task, prefix_of_mail, test_api_only)
