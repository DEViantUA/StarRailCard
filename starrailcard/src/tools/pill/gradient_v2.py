# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image, ImageDraw, ImageChops
import numpy as np
import colorsys

class GradientBackground:
    def __init__(self, image, size, overlay = None, size_art = None):
        self.image = image
        self.overlay = overlay
        self.size_art = size_art
        self.width = size[0]
        self.height = size[1]

    def get_centered_image(self, size):
        background_image = Image.new('RGBA', size, color=(0, 0, 0, 0))
        foreground_image = self.image

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

    def start(self, art_add = False, overlay_add = False, left = False):
        if self.size_art:
            image = self.get_centered_image(self.size_art)
        else:
            image = self.image
        gradient = Image.new('RGBA', (self.width, self.height))
        draw = ImageDraw.Draw(gradient)

        top_color, middle_color, bottom_color = self.get_image_colors(image, left = left)

        for y in range(self.height):
            t = y / (self.height - 1)
            gradient_color = self.interpolate_color(top_color, middle_color, bottom_color, t)
            draw.line([(0, y), (self.width, y)], fill=gradient_color)

        if overlay_add:
            gradient = ImageChops.screen(gradient, self.overlay)
        
        if art_add:
            mask = self.create_transition_mask(image.width, image.height)
            gradient = ImageChops.composite(image, gradient, mask)

        return gradient

    @staticmethod
    def light_level(pixel_color):
        h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3]))    
        return l
    
    @staticmethod
    def _get_light_pixel_color(pixel_color, up=False):
        h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3]))
        if up:
            l = min(max(l + 0.2, 0), 1)
        else:
            l = min(max(l - 0.2, 0), 1)
        return tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))
    
    @staticmethod
    def _get_dark_pixel_color(pixel_color):
        h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3]))
        l = min(max(0.8, l), 0.2)
        a = tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))
        
        return  a
    
    
    def get_image_colors(self, image, num_sections=3, left = False):
        width, height = image.size
        section_height = height // num_sections

        colors = []
        for i in range(num_sections):
            if left:
                left_coord = 0
                right_coord = int(width * 0.1)
            else:
                left_coord = int(width * 0.9)
                right_coord = width
            
            top = i * section_height
            bottom = (i + 1) * section_height
            section = image.crop((left_coord, top, right_coord, bottom))
            pixels = section.getdata()
            filtered_pixels = [pixel[:3] for pixel in pixels if pixel[3] > 10]
            if filtered_pixels:
                avg_color = tuple(np.mean(filtered_pixels, axis=0, dtype=int))
            else:
                avg_color = (0, 0, 0)

            ll = self.light_level(avg_color)
            if ll > 0.75:
                avg_color = self._get_light_pixel_color(avg_color)
                ll = self.light_level(avg_color)
            
            colors.append(avg_color)

        return colors

    @staticmethod
    def interpolate_color(start_color, middle_color, end_color, t):
        start_alpha = start_color[3] if len(start_color) > 3 else 255
        middle_alpha = middle_color[3] if len(middle_color) > 3 else 255
        end_alpha = end_color[3] if len(end_color) > 3 else 255

        if t < 0.5:
            t = t * 2
            r = int((1 - t) * start_color[0] + t * middle_color[0])
            g = int((1 - t) * start_color[1] + t * middle_color[1])
            b = int((1 - t) * start_color[2] + t * middle_color[2])
            a = int((1 - t) * start_alpha + t * middle_alpha)
        else:
            t = (t - 0.5) * 2
            r = int((1 - t) * middle_color[0] + t * end_color[0])
            g = int((1 - t) * middle_color[1] + t * end_color[1])
            b = int((1 - t) * middle_color[2] + t * end_color[2])
            a = int((1 - t) * middle_alpha + t * end_alpha)

        return (r, g, b, a)

    @staticmethod
    def create_transition_mask(width, height):
        mask = Image.new('L', (width, height), 255)
        draw = ImageDraw.Draw(mask)
        for x in range(width):
            alpha = int(255 * 2 * (1 - x / width))
            draw.line([(x, 0), (x, height)], fill=alpha)

        return mask