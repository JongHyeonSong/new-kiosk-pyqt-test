import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import asyncio
import aiohttp
import sqlite3
import aiosqlite

from functools import wraps

class AsyncioThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.loop = asyncio.get_event_loop()
        self.loop.run_forever()




class SqlManager(QObject):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = QObject.__new__(cls, *args, **kwargs)

        return cls.__instance

    def __init__(self):
        super().__init__()
        self.thread = AsyncioThread()
        self.thread.start() 

    def async_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            asyncio.run_coroutine_threadsafe(func(self, *args, **kwargs), self.thread.loop)
        return wrapper

    def with_connection_and_cursor(func):
        @wraps(func)
        async def wrapper(self, sql, cb, *args, **kwargs):
            async with aiosqlite.connect("sql.sqlite") as db:
                async with db.cursor() as cursor:
                    try:
                        result = await func(self, cursor, sql, *args, **kwargs)
                        await db.commit()
                        cb(result)
                    except aiosqlite.OperationalError as e:
                        cb(e)
                    return result
        return wrapper
    
    @async_decorator
    @with_connection_and_cursor
    async def select_list(self, cursor, sql):
        await cursor.execute(sql)
        result = await cursor.fetchall()
        return result

class ApiManager(QObject):
    def __init__(self):
        super().__init__()
        self.thread = AsyncioThread()
        self.thread.start()

    def async_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            asyncio.run_coroutine_threadsafe(func(self, *args, **kwargs), self.thread.loop)
        return wrapper

    def handle_http_response(func):
        @wraps(func)
        async def wrapper(self, url, cb, *args, **kwargs):
            async with aiohttp.ClientSession() as session:
                try:
                    async with await func(self, session, url, *args, **kwargs) as response:
                        status = response.status

                        # if status not 2XX then
                        if(status < 200 or status >= 300):
                            error_response = await response.text()

                            raise Exception(f"Error: !!! {status} {error_response}")

                        contentType = response.headers.get('Content-Type')
                        if(contentType.startswith("application/json")):
                            cb(await response.json())
                        else:
                            cb(await response.text())
                except Exception as e:
                    cb(e)

        return wrapper
    

    @async_decorator
    @handle_http_response
    async def post_request_json(self, session, url, data):
        return await session.post(url, json = data)


    @async_decorator
    @handle_http_response
    async def get_request(self, session, url):
        return await session.get(url)

    


    # def with_connection_and_cursor(func):
    #     @wraps(func)
    #     async def wrapper(self, sql, cb, *args, **kwargs):
    #         async with aiosqlite.connect("sql.sqlite") as db:
    #             async with db.cursor() as cursor:
    #                 try:
    #                     result = await func(self, cursor, sql, *args, **kwargs)
    #                     await db.commit()
    #                     cb(result)
    #                 except aiosqlite.OperationalError as e:
    #                     cb(e)
    #                 return result
    #     return wrapper
