# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.


import aiohttp
import base64

from io import BytesIO
from .src.model import utils_model
from contextlib import AsyncExitStack


import_magic = False

try:
    import magic
except ImportError:
    import_magic = True
    import imghdr

IMAGE_TYPES = {
    'image/jpeg',
    'image/png',
    'image/gif'
}


async def get_character(lang = "en"):
    url = f"https://hsr.yatta.top/{lang}/archive/avatar"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def get_name(character_id = None, lang = "en"):
    avatar_data = await get_character(lang)
    if avatar_data.get("response") != 200:
        print("An error occurred while receiving data")
        return 
    data = {}
    for key in avatar_data.get("data", {}).get("items", {}):
        if not character_id is None:
            if int(key) == int(character_id):
                return {key: avatar_data["data"]["items"][key].get("name")}
        data[key] = avatar_data["data"]["items"][key].get("name")

    return data

async def get_character_id(name = None, lang = "en"):
    
    avatar_data = await get_character(lang)
    if avatar_data.get("response") != 200:
        print("An error occurred while receiving data")
        return 
    data = {}
    for key in avatar_data.get("data", {}).get("items", {}):
        if not name is None:
            if name in avatar_data["data"]["items"][key].get("name"):
                return {avatar_data["data"]["items"][key].get("name"): key}
        data[avatar_data["data"]["items"][key].get("name")] = key

    return data



async def image_to_base64(image, format = "png"):
    buffered = BytesIO()
    image.save(buffered, format= format)
    img_str = base64.b64encode(buffered.getvalue())
    
    return img_str

async def get_link_image(img, api_key = None):
    """_summary_

    Args:
        img (base64,str): Image
        api_key (str, optional): The API key was obtained here: https://api.imgbb.com/. Defaults to None.

    Raises:
        TypeError: If api_key = None

    Returns:
        ApiImageLink: A class object containing information about the image uploaded to the server
    """
    if api_key is None:
        raise TypeError(800,'Get the API key on the page: https://api.imgbb.com/ (Click on "Get Api Key")')
    
    async with aiohttp.ClientSession() as session:
        url = 'https://api.imgbb.com/1/upload'
        headers = {
            'Accept': 'application/json'
        }

        par = {
            'key': api_key,
            'image': await image_to_base64(img) if not isinstance(img, str) else img
        }
        async with session.post(url, data=par, headers=headers) as req:
            data = await req.json()
            return utils_model.ApiImageLink(**data)   




def get_pixv_headers():
        return {"referer": "https://www.pixiv.net/"}


async def download_image(session, url, headers=None, allow_redirects=True, use_range=None, offset=0, size=None, **kwargs):
    if headers is None:
        headers = {}

    params = {
        'headers': headers,
        'allow_redirects': allow_redirects,
        **kwargs,
    }

    if use_range is None:
        async with session.head(url, **params) as response:
            if response.headers.get('accept-ranges') == 'bytes':
                use_range = True
            else:
                use_range = False

    if use_range:
        if size is None:
            if offset:
                headers['range'] = f"bytes={offset}-"
        else:
            headers['range'] = f"bytes={offset}-{offset + size - 1}"

    async with session.get(url, headers=headers, allow_redirects=allow_redirects, **kwargs) as response:
        if response.status != 416:
            response.raise_for_status()

            buffer = BytesIO()
            async for data in response.content.iter_any():
                length = len(data)

                if use_range:
                    if size is not None and offset + length > offset + size:
                        buffer.write(data[:offset + size - offset])
                        break
                    else:
                        buffer.write(data)
                else:
                    buffer.write(data)

            return buffer.getvalue()

async def get_mimetype(session, url, size=2048, allow_redirects=True, **kwargs):
    async with session:
        data = await download_image(session, url, size=size, allow_redirects=allow_redirects, **kwargs)
        if import_magic:
            mime_type = imghdr.what(None, h=data)
            if mime_type:
                return mime_type
            else:
                return "application/octet-stream"
        else:
            return magic.Magic(mime=True).from_buffer(data)

async def is_valid(session, url, allow_redirects=True, **kwargs):
    async with session:
        try:
            async with session.head(url, allow_redirects=allow_redirects, **kwargs) as response:
                return response.status == 200
        except aiohttp.ClientError:
            return False
    
async def is_valid_image(url,session=None,allow_redirects=True,strict=False,**kwargs):
    """Check the image from the link or not

    Args:
        url (str): link
        session (session, optional): aiohttp or other session. Defaults to None.
        allow_redirects (bool, optional): Allow redirection. Defaults to True.
        strict (bool, optional): .... . Defaults to False.

    Returns:
        bool: True - if the link leads to an image | False - if the link does not lead to an image
    """
    async with AsyncExitStack() as stack:
        if url is None:
            session, url = url,session
        
        if session is None:
            session = await stack.enter_async_context(aiohttp.ClientSession())
            
        async with session:
            try:
                async with session.head(url, allow_redirects=allow_redirects, **kwargs) as response:
                    if response.status != 200 or not response.headers.get('content-length'):
                        return False

                    content_type = response.headers.get('content-type')

                    if content_type == 'application/octet-stream' or strict:
                        use_range = response.headers.get('accept-ranges') == 'bytes'
                        content_type = await get_mimetype(session, url, use_range=use_range, allow_redirects=allow_redirects, **kwargs)

                    return content_type in IMAGE_TYPES
            except aiohttp.ClientError:
                return False