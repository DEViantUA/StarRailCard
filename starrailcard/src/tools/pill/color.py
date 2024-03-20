# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image,ImageFilter
from more_itertools import chunked

import numpy as np

from .color_controle import light_level, _get_light_pixel_color, _get_dark_pixel_color

async def get_average_color(image):
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    channels = image.split()
    
    return (
        round(np.average(channels[0], weights=channels[-1])),
        round(np.average(channels[1], weights=channels[-1])),
        round(np.average(channels[2], weights=channels[-1])),
    )


async def get_dominant_colors(
    image,
    number,
    *,
    dither=Image.Quantize.FASTOCTREE,
    common=True,
):
    if image.mode != 'RGB':
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        if not common:
            width = image.width
            height = image.height
            
            image = Image.fromarray(np.array([np.repeat(
                np.reshape(image.convert('RGB'), (width * height, 3)),
                np.reshape(image.split()[-1], width * height),
                0,
            )]), 'RGB')
    
    if image.mode == 'RGBA':
        if dither == Image.Quantize.FASTOCTREE:
            simple_image = image.copy()
            simple_image.putalpha(255)
        else:
            simple_image = image.convert('RGB')
    else:
        simple_image = image
    
    reduced = simple_image.quantize(dither=dither, colors=number)
    
    palette = [*chunked(reduced.getpalette(), 3)]
    
    if common and image.mode == 'RGBA':
        alpha = np.array(image.split()[-1])
        
        colors = sorted((
            (
                np.sum(alpha * reduced.point([0] * i + [1] + [0] * (255 - i))),
                tuple(palette[i]),
            )
            for _, i in reduced.getcolors()
        ), reverse=True)
    else:
        colors = [
            (n, tuple(palette[i]))
            for n, i in sorted(reduced.getcolors(), reverse=True)
        ]
    
    return tuple(colors)


async def get_distance_alpha(image, converter=(lambda x: x)):
    width = image.width
    height = image.height
    
    radius = np.hypot(1, 1)
    
    return Image.fromarray(np.fromfunction(
        lambda y, x: np.uint8(255 * converter(np.hypot(
            2 * x / (width - 1) - 1,
            2 * y / (height - 1) - 1,
        ) / radius)),
        (height, width),
    ), 'L')


async def get_background_alpha(image):
    return await get_distance_alpha(
        image,
        lambda x: x * np.sin(x * np.pi / 2),
    )


async def get_foreground_alpha(image):
    return await get_distance_alpha(
        image,
        lambda x: 1 - x * np.sin(x * np.pi / 2),
    )

async def get_colors(image,number,*,common=False,radius=1,quality=None):
    if quality is not None:
        image = image.copy()
        image.thumbnail((quality, quality), 0)
    
    if radius > 1:
        image = image.filter(ImageFilter.BoxBlur(radius))
    
    filtered_image = image.convert('RGB')
    
    if image.mode != 'RGBA':
        filtered_image.putalpha(await get_background_alpha(image))
    else:
        filtered_image.putalpha(Image.fromarray(np.uint8(
            np.uint16(await get_background_alpha(image))
            * image.split()[-1]
            / 255
        ), 'L'))
    
    color_palette = await get_dominant_colors(filtered_image, number, common=common)
    color_palette = color_palette[0][1]
    ll = await light_level(color_palette)
    if ll < 0.15:
        color_palette = await _get_light_pixel_color(color_palette)
    elif ll > 0.80:
        color_palette = await _get_dark_pixel_color(color_palette)
        
        
    return color_palette