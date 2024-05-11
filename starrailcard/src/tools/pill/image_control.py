# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import os
import re
import json

from PIL import Image
from io import BytesIO
from ..git import assets
from .. import cache, http

_caches = cache.Cache.get_cache()
_boost_speed = False


async def resize_image(image, scale):
    width, height = image.size
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = image.resize((new_width, new_height))
    return resized_image


async def get_center_size(size, file_name): #get_centr_honkai_art
    background_image = Image.new('RGBA', size, color=(0, 0, 0, 0))
    foreground_image = file_name.convert("RGBA")

    scale = max(size[0] / foreground_image.size[0], size[1] / foreground_image.size[1])
    foreground_image = foreground_image.resize((int(foreground_image.size[0] * scale), int(foreground_image.size[1] * scale)))

    background_size = background_image.size
    foreground_size = foreground_image.size

    x = background_size[0] // 2 - foreground_size[0] // 2

    if foreground_size[1] > background_size[1]:
        y_offset = max(int(0.3 * (foreground_size[1] - background_size[1])), int(0.5 * (-foreground_size[1])))
        y = -y_offset
    else:
        y = background_size[1] // 2 - foreground_size[1] // 2

    background_image.alpha_composite(foreground_image, (x, y))

    return background_image


async def get_center_scale(size, file_name):
    
    background_image = Image.new('RGBA', size, color=(0, 0, 0, 0))
    foreground_image = file_name.convert("RGBA")
    
    scale = 0.65
    foreground_image = await resize_image(foreground_image, scale)

    background_size = background_image.size
    foreground_size = foreground_image.size

    x = background_size[0] // 2 - foreground_size[0] // 2
    y = background_size[1] // 2 - foreground_size[1] // 2

    background_image.alpha_composite(foreground_image, (x, y))

    return background_image


async def get_image_from_boost_speed(link):
    path = f"/boost_speed/{link.split('master')[1]}"
    full_path = os.path.join(assets, path.lstrip('/'))

    if os.path.exists(full_path):
        try:
            return Image.open(full_path).convert("RGBA")
        except Exception as e:
            raise IOError(f"Error reading image file: {e}")
    else:
        return None

async def download_image(link, headers=None):
    try:
        image = await http.AioSession.get(link, headers=headers, response_format="bytes")
        return image
    except:
        raise TypeError(f"Error Dowload image: {link}")

async def save_image(image, full_path):
    directory = os.path.dirname(full_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(full_path, 'wb') as f:
        f.write(image)

async def open_image(image_data):
    try:
        return Image.open(BytesIO(image_data)).convert("RGBA")
    except Exception as e:
        raise TypeError(f"Error Open image: {e}")

async def get_download_img(link, size=None, thumbnail_size=None, gif=False):
    cache_key = json.dumps((link, size, thumbnail_size), sort_keys=True)
    image_boost = None
    
    if _boost_speed:
        if "StarRailRes" in link:
            image_boost = await get_image_from_boost_speed(link)

    if not gif:
        if cache_key in _caches:
            return _caches[cache_key]
    
    
    
    if image_boost is None:
        headers_p = None
    
        if "pximg" in link:
            headers_p = {
                "referer": "https://www.pixiv.net/",
            }
        image = await download_image(link, headers_p)
        
        if _boost_speed:
            if "StarRailRes" in link:
                full_path = os.path.join(assets, f"/boost_speed/{link.split('master')[1]}".lstrip('/'))
                await save_image(image, full_path)
                
        image = await open_image(image)
    else:
        image = image_boost

    if gif:
        return image
    
    try:
        if size:
            image = image.resize(size)
            _caches[cache_key] = image
            return image
        elif thumbnail_size:
            image.thumbnail(thumbnail_size)
            _caches[cache_key] = image
            return image
        else:
            _caches[cache_key] = image
            return image
    except Exception as e:
        raise TypeError(f"Error setting image: {link}")
    
async def crop_image(img):
    width, height = img.size
    target_pixel_x = 275
    target_pixel_y = height // 2
    crop_size = 8
    left = max(0, target_pixel_x - crop_size // 2)
    right = min(width, target_pixel_x + crop_size // 2 + 1)
    cropped_img = img.crop((left, 0, right, height))
    
    return cropped_img

async def get_user_image(img):
    if type(img) != str:
        img = img
    elif type(img) == str:
        linkImg = re.search("(?P<url>https?://[^\s]+)", img)
        if linkImg:
            try:
                if "gif" in linkImg.group():
                    img = await get_download_img(linkImg.group(), gif = True)
                    return img
                else:
                    img = await get_download_img(linkImg.group())
            except:
                return None
        else:
            img = Image.open(img)
    else:
        return None
    return img.convert("RGBA")
