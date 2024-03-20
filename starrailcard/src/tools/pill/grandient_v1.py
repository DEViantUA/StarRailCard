# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image

from .color_controle import light_level, _get_light_pixel_color, _get_dark_pixel_color

class GradientGenerator:
    def __init__(self, source_img_path):
        self.source_img = source_img_path
        self.frame = ()
        self.source_width, self.source_height = self.source_img.size

    async def generate(self, width, height, left = False):
        gradient_img = Image.new("RGB", (width, height))
        top_height = height // 3
        bottom_height = height // 3
        center_height = height - top_height - bottom_height
        if left:
            left = 3
            right = 4
        else:
            left = self.source_width - 142
            right = self.source_width - 141
        top_1 = 1
        bottom_1 = top_height - 1
        top_2 = top_height + 1
        bottom_2 = top_height + center_height - 1
        top_3 = top_height + center_height + 1
        bottom_3 = height - 2

        top_color = await self._get_pixel_color(left, top_1, right, bottom_1)
        ll = await light_level(top_color)
        if ll < 45:
            top_color = await _get_light_pixel_color(top_color)
        elif ll > 200:
            top_color = await _get_dark_pixel_color(top_color)

        center_color = await self._get_pixel_color(left, top_2, right, bottom_2)
        
        ll = await light_level(center_color)
        if ll < 45:
            center_color = await _get_light_pixel_color(center_color)
        elif ll > 200:
            center_color = await _get_dark_pixel_color(center_color)

        bottom_color = await self._get_pixel_color(left, top_3, right, bottom_3)
        ll = await light_level(bottom_color)
        if ll < 45:
            bottom_color = await _get_light_pixel_color(bottom_color)
        elif ll > 200:
            bottom_color = await _get_dark_pixel_color(bottom_color)

        for y in range(top_height):
            for x in range(width):
                ratio = y / (top_height - 1)
                gradient_color = self._get_interpolated_color(top_color, center_color, ratio)
                gradient_img.putpixel((x, y), gradient_color)

        for y in range(center_height):
            for x in range(width):
                ratio = y / (center_height - 1)
                gradient_color = self._get_interpolated_color(center_color, bottom_color, ratio)
                gradient_img.putpixel((x, y + top_height), gradient_color)

        for y in range(bottom_height):
            for x in range(width):
                gradient_color = bottom_color
                gradient_img.putpixel((x, y + top_height + center_height), gradient_color)

        return gradient_img.convert("RGBA")

    async def _get_pixel_color(self, left, top, right, bottom):
        cropped_img = self.source_img.crop((left, top, right, bottom))
        resized_img = cropped_img.convert("RGB").resize((1, 1))
        pixel_color = resized_img.getpixel((0, 0))
        
        return pixel_color
    
    def _get_interpolated_color(self, start_color, end_color, ratio):
        return tuple(int(start_color[i] + (end_color[i] - start_color[i]) * ratio) for i in range(3))