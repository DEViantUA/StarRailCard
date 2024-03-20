# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import aiohttp
import asyncio
import json

class AioSession:
    _session = None
    _semaphore = asyncio.Semaphore(5)
    
    @classmethod
    async def get_session(cls):
        """
        Returns the session instance, creating it if necessary.

        Returns:
            aiohttp.ClientSession: The session instance.
        """
        if cls._session is None:
            cls._session = aiohttp.ClientSession()
        return cls._session

    @classmethod
    async def close_session(cls):
        """
        Closes the session if it exists.
        """
        if cls._session is not None:
            await cls._session.close()
            cls._session = None

    @classmethod
    def session(cls):
        """
        Returns the current session instance.

        Returns:
            aiohttp.ClientSession: The current session instance, or None if the session is not created.
        """
        return cls._session

    @classmethod
    async def get(cls, url, headers=None, response_format='json'):
        """
        Sends a GET request using the current session instance.

        Args:
            url (str): The URL to send the request to.
            headers (dict): Optional headers to include in the request.
            response_format (str): The format of the response data to return.

        Returns:
            Depends on the specified response format:
            - dict: for 'json' format;
            - str: for 'text' format;
            - bytes: for 'bytes' format.
        """
        response = None
        try:
            if cls._session is not None:
                async with cls._session.get(url, headers=headers) as response:
                    data = await cls.process_response(response, response_format)
                    return data
        except Exception as e:
            print(f"Error during GET request: {e}")
        finally:
            if response:
                await response.release()

    @classmethod
    async def post(cls, url, data=None, headers=None, response_format='json'):
        """
        Sends a POST request using the current session instance.

        Args:
            url (str): The URL to send the request to.
            data: The data to send in the request body.
            headers (dict): Optional headers to include in the request.
            response_format (str): The format of the response data to return.

        Returns:
            Depends on the specified response format:
            - dict: for 'json' format;
            - str: for 'text' format;
            - bytes: for 'bytes' format.
        """
        response = None
        try:
            if cls._session is not None:
                async with cls._session.post(url, data=data, headers=headers) as response:
                    data = await cls.process_response(response, response_format)
                    return data
        except Exception as e:
            print(f"Error during POST request: {e}")
        finally:
            if response:
                await response.release()

    @classmethod
    async def request(cls, method, url, headers=None, response_format='json', **kwargs):
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
        response = None
        try:
            if cls._session is not None:
                async with cls._session.request(method, url, headers=headers, **kwargs) as response:
                    data = await cls.process_response(response, response_format)
                    return data
        except Exception as e:
            print(f"Error during custom request: {e}")
        finally:
            if response:
                await response.release()
   
    
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
