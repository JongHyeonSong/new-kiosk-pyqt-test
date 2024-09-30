import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import asyncio
import aiohttp
import sqlite3
import aiosqlite
import socketio

from functools import wraps

class AsyncioThread(QThread):
    __instance = None
    inited = False
    
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = QObject.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        super().__init__()

    def run(self):
        if self.inited:
            return
        else:
            self.inited = True
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
        

        # with qtimer hook one shot after 1second
        # self.timer = QTimer()
        QTimer.singleShot(3500, self.hook1)
        # self.timer.timeout.connect(self.hook1)
        
        # self.werwer = aiohttp.ClientSession()
    def hook1(self):
        a=3

        # self.werwer = aiohttp.ClientSession()

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



class Thr(QThread):
    message_received = pyqtSignal(str)
        
    def __init__(self):
        super().__init__()
        self.sio = socketio.Client()

    def run(self):
        print("WOWOWO!!!")

        @self.sio.event
        def connect():
            print("Connected to server")

        @self.sio.event
        def disconnect():
            print("Disconnected from server")

        @self.sio.event
        def message(data):
            print(f"Message from server: {data}")
            self.message_received.emit(data)

        self.sio.connect('http://localhost:3300')
        self.sio.wait()

class WebSocketManager(QObject):


    __instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = QObject.__new__(cls, *args, **kwargs)

        return cls.__instance

    def __init__(self):

        super().__init__()
        self.thread = AsyncioThread()
        self.thread.start() 
    

        # self.sio = socketio.AsyncSimpleClient()
        # self.sio.connect('http://localhost:3300')
        sio = socketio.Client()
        sio.connect('http://localhost:3300')




    def ggg(self, url, cb):
        asyncio.run_coroutine_threadsafe(self.wow(), self.thread.loop)

    async def wow(self):
        # async with socketio.AsyncSimpleClient() as sio:
        print("WOWOWO!!!")
        a=3 
        