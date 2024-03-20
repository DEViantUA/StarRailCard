# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import colorsys
from .. import cashe 

_caches = cashe.Cache.get_cache()

async def apply_opacity(image, opacity=0.2):
    result_image = image.copy()
    alpha = result_image.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    result_image.putalpha(alpha)

    return result_image

async def light_level(pixel_color):
    cache_key = pixel_color
    if cache_key in _caches:
        return _caches[cache_key]
    
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3])) 
    _caches[cache_key] = l
    return l

def color_distance(color1, color2):
    return sum((a - b) ** 2 for a, b in zip(color1, color2)) ** 0.5

async def replace_color(image, old_color, new_color, radius=100):
    image = image.convert("RGBA")
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            current_color = pixels[x, y][:3]
            if color_distance(current_color, old_color) <= radius:
                pixels[x, y] = (*new_color, pixels[x, y][3])
    
    return image


async def recolor_image(image, target_color, light = False):
    if light:
        ll = await light_level(target_color)
        if ll < 45:
            target_color = await _get_light_pixel_color(target_color,up = True)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    image = image.copy()

    pixels = image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            if a != 0:
                pixels[i, j] = target_color + (a,)
    if light:
        return image, target_color
    return image

async def _get_light_pixel_color(pixel_color, up = False):
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3]))
    if up:
        l = min(max(0.6, l), 0.9)
    else:
        l = min(max(0.3, l), 0.8)
    return tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))
  
async def _get_dark_pixel_color(pixel_color):
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3]))
    l = min(max(0.8, l), 0.2)
    a = tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))
    
    return  a




