# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import aiohttp
import asyncio
import json
import inspect
import threading
import weakref

class SharedObject:
    __slots__ = (
        'func', 'args', 'kwargs',
        'object',
        'users',
        'sync_lock', 'async_locks',
    )
    
    def __init__(self, func, /, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        
        self.sync_lock = threading.Lock()
        self.async_locks = weakref.WeakKeyDictionary()
        
        self.users = 0
    
    @property
    def async_lock(self, /):
        token = asyncio.get_running_loop()
        
        try:
            lock = self.async_locks[token]
        except KeyError:
            self.async_locks[token] = lock = asyncio.Lock()
        
        return lock
    
    def __enter__(self, /):
        object = None
        
        with self.sync_lock:
            if self.users == 0:
                object = self.func(*self.args, **self.kwargs)
                
                if hasattr(object, '__enter__'):
                    object = object.__enter__()
                
                self.object = object
            else:
                object = self.object
            
            self.users += 1
        
        return object
    
    def __exit__(self, /, *exc_info):
        result = None
        
        with self.sync_lock:
            self.users -= 1
            
            if self.users == 0:
                object = self.object
                
                if hasattr(object, '__exit__'):
                    result = object.__exit__(*exc_info)
                elif hasattr(object, 'close'):
                    object.close()
                
                del self.object
        
        return result
    
    async def __aenter__(self, /):
        object = None
        
        with self.sync_lock:
            async with self.async_lock:
                if self.users == 0:
                    object = self.func(*self.args, **self.kwargs)
                    
                    if inspect.isawaitable(object):
                        object = await object
                    
                    if hasattr(object, '__aenter__'):
                        object = await object.__aenter__()
                    elif hasattr(object, '__enter__'):
                        object = object.__enter__()
                    
                    self.object = object
                else:
                    object = self.object
                
                self.users += 1
        
        return object
    
    async def __aexit__(self, /, *exc_info):
        result = None
        
        with self.sync_lock:
            async with self.async_lock:
                self.users -= 1
                
                if self.users == 0:
                    object = self.object
                    
                    if hasattr(object, '__aexit__'):
                        result = await object.__aexit__(*exc_info)
                    elif hasattr(object, 'aclose'):
                        await object.aclose()
                    elif hasattr(object, 'close'):
                        if inspect.isawaitable(coro := object.close()):
                            await coro
                    elif hasattr(object, '__exit__'):
                        result = object.__exit__(*exc_info)
                    
                    del self.object
        
        return result



class AioSession:
    session = SharedObject(aiohttp.ClientSession)
    proxy = None
    
    @classmethod
    async def enter(cls, proxy = None, /):
        cls.proxy = proxy
        
        return await cls.session.__aenter__()
    
    @classmethod
    async def exit(cls, /, *exc_info):
        if not exc_info:
            exc_info = (None, None, None)
        
        return await cls.session.__aexit__(*exc_info)
    
    @classmethod
    async def creat_session(cls):
        """Creates a session
        Returns:
            aiohttp.ClientSession: The session instance.
        """
        cls.session = aiohttp.ClientSession()
        
        return cls.session
        
    @classmethod
    async def get_session(cls):
        """
        Returns the session instance, creating it if necessary.

        Returns:
            aiohttp.ClientSession: The session instance.
        """
        if cls.session is None:
            cls.session = aiohttp.ClientSession()
        return cls.session

    @classmethod
    async def close_session(cls):
        """
        Closes the session if it exists.
        """
        if cls.session is not None:
            await cls.session.close()
            cls.session = None

    '''@classmethod
    def session(cls):
        """
        Returns the current session instance.

        Returns:
            aiohttp.ClientSession: The current session instance, or None if the session is not created.
        """
        return cls.session'''

    @classmethod
    async def get(cls, url, headers=None, response_format='json', proxy=None, **kwargs):
        """
        Sends a GET request using the current session instance.

        Args:
            url (str): The URL to send the request to.
            headers (dict): Optional headers to include in the request.
            response_format (str): The format of the response data to return.
            **kwargs: Additional arguments to pass to the aiohttp GET method.

        Returns:
            Depends on the specified response format:
            - dict: for 'json' format;
            - str: for 'text' format;
            - bytes: for 'bytes' format.
        """
        async with cls.session as session:
            if not cls.proxy is None:
                proxy = cls.proxy
                
            try:
                async with session.get(url, headers=headers, proxy=proxy, **kwargs) as response:
                    data = await cls.process_response(response, response_format)
                    return data
            except Exception as e:
                print(f"Error during GET request: {e}")


    @classmethod
    async def post(cls, url, data=None, headers=None, response_format='json', proxy=None, **kwargs):
        """
        Sends a POST request using the current session instance.

        Args:
            url (str): The URL to send the request to.
            data: The data to send in the request body.
            headers (dict): Optional headers to include in the request.
            response_format (str): The format of the response data to return.
            **kwargs: Additional arguments to pass to the aiohttp POST method.

        Returns:
            Depends on the specified response format:
            - dict: for 'json' format;
            - str: for 'text' format;
            - bytes: for 'bytes' format.
        """
        if not cls.proxy is None:
            proxy = cls.proxy
                
        async with cls.session as session:
            try:
                async with session.post(url, data=data, headers=headers, proxy=proxy, **kwargs) as response:
                    data = await cls.process_response(response, response_format)
                    return data
            except Exception as e:
                print(f"Error during POST request: {e}")

    @classmethod
    async def request(cls, method, url, headers=None, response_format='json', proxy=None, **kwargs):
        """
        Sends a custom HTTP request using the current session instance.

        Args:
            method (str): The HTTP method to use (e.g., 'GET', 'POST').
            url (str): The URL to send the request to.
            headers (dict): Optional headers to include in the request.
            response_format (str): The format of the response data to return.
            **kwargs: Additional keyword arguments to pass to the request function.

        Returns:
            Depends on the specified response format:
            - dict: for 'json' format;
            - str: for 'text' format;
            - bytes: for 'bytes' format.
        """
        if not cls.proxy is None:
            proxy = cls.proxy
            
        async with cls.session as session:
            try:
                async with session.request(method, url, headers=headers, proxy=proxy, **kwargs) as response:
                    data = await cls.process_response(response, response_format)
                    return data
            except Exception as e:
                print(f"Error during custom request: {e}")
   
    
    @classmethod
    async def process_response(cls, response, response_format):
        """
        Processes the response result before returning it in the specified format.

        Args:
            response (aiohttp.ClientResponse): The response object from the server.
            response_format (str): The format of the response data to return.

        Returns:
            Depends on the specified response format:
            - dict: for 'json' format;
            - str: for 'text' format;
            - bytes: for 'bytes' format.
        """

        if response_format == 'json':
            try:
                return await response.json()
            except aiohttp.ContentTypeError:
                data = await response.text()
                return json.loads(data)
        elif response_format == 'text':
            return await response.text()
        elif response_format == 'bytes':
            return await response.read()
        else:
            raise ValueError("Unsupported response format. Supported formats are 'json', 'text', and 'bytes'.")
