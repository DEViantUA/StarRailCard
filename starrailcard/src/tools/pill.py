# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
from PIL import ImageFont,Image,ImageDraw,ImageChops
from io import BytesIO
from . import openFile
import aiohttp,re


async def get_font(size):
    return ImageFont.truetype(openFile.font, size)

async def get_dowload_img(link,size = None, thumbnail_size = None):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                image = await response.read()
    except:
        raise
    
    image = Image.open(BytesIO(image)).convert("RGBA")
    if size:
        return image.resize(size)
    elif thumbnail_size:
        image.thumbnail(thumbnail_size)
        return image
    else:
        return image
    
async def get_user_image(img):
    if type(img) != str:
        img = img
    elif type(img) == str:
        linkImg = re.search("(?P<url>https?://[^\s]+)", img)
        if linkImg:
            try:
                img = await get_dowload_img(linkImg.group())
            except:
                return None
        else:
            img = Image.open(img)
    else:
        return None
    return img.convert("RGBA")

async def get_resize_image(userImages,baseheight,basewidth):
    x,y = userImages.size
    if max(x, y) / min(x, y) < 1.1:
        hpercent = (baseheight / float (y)) 
        wsize = int ((float (x) * float (hpercent)))
        userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
        return {"img": userImages, "type": 0}
    elif x > y:
        hpercent = (baseheight / float (y)) 
        wsize = int ((float (x) * float (hpercent)))
        userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
        return {"img": userImages, "type": 1}
    else:
        wpercent = (basewidth / float(userImages.size[0]))
        hsize = int((float(userImages.size[1]) * float(wpercent)))
        userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)
        if hsize < baseheight:
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return {"img": userImages, "type": 2}
        return {"img": userImages, "type": 2}


async def get_text_size_frame(text,font_size,frame_width):
    font = await get_font(font_size)

    while font.getlength(text) > frame_width:
        font_size -= 1
        font = await get_font(font_size)

    return font,font.getlength(text)


async def create_image_text(text, font_size, max_width=336, max_height=None, color=(255, 255, 255, 255)):
    original_font = await get_font(font_size)
    font = original_font
    lines = []
    line = []
    for word in text.split():
        if line:
            temp_line = line + [word]
            temp_text = ' '.join(temp_line)
            temp_width = font.getmask(temp_text).getbbox()[2]
            if temp_width <= max_width:
                line = temp_line
            else:
                lines.append(line)
                line = [word]
        else:
            line = [word]
    if line:
        lines.append(line)

    width = 0
    height = 0
    for line in lines:
        line_width = font.getmask(' '.join(line)).getbbox()[2]
        width = max(width, line_width)
        height += font.getmask(' '.join(line)).getbbox()[3]

    if max_height is not None and height > max_height:
        reduction_ratio = max_height / height
        new_font_size = int(font_size * reduction_ratio)
        font = await get_font(new_font_size)

    img = Image.new('RGBA', (min(width, max_width), height + (font_size - 4)), color=(255, 255, 255, 0))

    draw = ImageDraw.Draw(img)
    y_text = 0
    for line in lines:
        text_width, text_height = font.getmask(' '.join(line)).getbbox()[2:]
        draw.text((0, y_text), ' '.join(line), font=font, fill=color)
        y_text += text_height + 5

    return img

async def create_image_with_text(text, font_size, max_width=336, color=(255, 255, 255, 255), alg="Left"):
    font = await get_font(font_size)

    lines = []
    line = []
    for word in text.split():
        if line:
            temp_line = line + [word]
            temp_text = ' '.join(temp_line)
            temp_width = font.getmask(temp_text).getbbox()[2]
            if temp_width <= max_width:
                line = temp_line
            else:
                lines.append(line)
                line = [word]
        else:
            line = [word]
    if line:
        lines.append(line)

    width = 0
    height = 0
    for line in lines:
        line_width = font.getmask(' '.join(line)).getbbox()[2]
        width = max(width, line_width)
        height += font.getmask(' '.join(line)).getbbox()[3]

    img = Image.new('RGBA', (min(width, max_width), height + (font_size)), color=(255, 255, 255, 0))

    draw = ImageDraw.Draw(img)
    
    y_text = 0
    for line_num, line in enumerate(lines):
        text_width, text_height = font.getmask(' '.join(line)).getbbox()[2:]
        if alg == "center" and line_num > 0:
            x_text = (max_width - text_width) // 2
        else:
            x_text = 0
        draw.text((x_text, y_text), ' '.join(line), font=font, fill=color)
        y_text += text_height + 5

    return img

async def resize_image(image, scale):
    width, height = image.size
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = image.resize((new_width, new_height))
    return resized_image

async def get_centr_honkai(size, file_name):
    # Открываем фоновое изображение и изображение для наложения
    background_image = Image.new('RGBA', size, color=(0, 0, 0, 0))
    foreground_image = file_name.convert("RGBA")

    # Уменьшаем исходное изображение на 10%
    scale = 0.65
    foreground_image = await resize_image(foreground_image, scale)

    background_size = background_image.size
    foreground_size = foreground_image.size

    # Определяем позицию для наложения изображения
    x = background_size[0] // 2 - foreground_size[0] // 2
    y = background_size[1] // 2 - foreground_size[1] // 2

    # Налагаем изображение на фон
    background_image.alpha_composite(foreground_image, (x, y))

    return background_image

async def creat_bg_teample_two(image,bg,maska = None, teample = 2):
    if teample == 3:
        bg_element = bg.convert("RGBA")
        splash = await get_dowload_img(link=image)
        frme_splash = await get_centr_honkai((582,802),splash)
        frme_splash.alpha_composite(openFile.ImageCache().shadow_art,(0,0))
        bg_element.alpha_composite(frme_splash,(1342,0))
    else:
        splash = await get_dowload_img(link=image)
        frme_splash = await get_centr_honkai((719,719),splash)
        bg_frame = Image.new('RGBA', (1916,719), color= (255,255,255,0))
        bg_frame.alpha_composite(frme_splash,(0,0))
        bg_element = bg.copy()
        maska_bg =  bg.copy()
        bg_element.alpha_composite(bg_frame,(0,0))
        bg_element.paste(maska_bg,(0,0),maska)
        bg_element.alpha_composite(openFile.ImageCache().shadow,(2,0))

    return bg_element



async def recolor_image(image, target_color):
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    pixels = image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            if a != 0:  # Проверяем, является ли текущий пиксель непрозрачным
                pixels[i, j] = target_color + (a,)  # Заменяем цвет, включая прозрачность
    return image

class GradientGenerator:
    def __init__(self, source_img_path):
        self.source_img = source_img_path
        self.frame = ()
        self.source_width, self.source_height = self.source_img.size

    async def generate(self, width, height, left = False):
        gradient_img = Image.new("RGB", (width, height))

        # Вычисляем ширину и высоту каждой полосы градиента
        top_height = height // 3
        bottom_height = height // 3
        center_height = height - top_height - bottom_height
        # Определяем координаты точек, с которых будем брать цвета
        if left:
            left = 3
            right = 4
        else:
            left = self.source_width - 3
            right = self.source_width - 2
        top_1 = 1
        bottom_1 = top_height - 1
        top_2 = top_height + 1
        bottom_2 = top_height + center_height - 1
        top_3 = top_height + center_height + 1
        bottom_3 = height - 2

        # Получаем цвета для каждой полосы
        top_color = await self._get_pixel_color(left, top_1, right, bottom_1)
        center_color = await self._get_pixel_color(left, top_2, right, bottom_2)
        bottom_color = await self._get_pixel_color(left, top_3, right, bottom_3)

        # Заполняем каждую полосу соответствующим цветом
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

        gradient_img
        return gradient_img

    async def _get_pixel_color(self, left, top, right, bottom):
        cropped_img = self.source_img.crop((left, top, right, bottom))
        resized_img = cropped_img.convert("RGB").resize((1, 1))
        return resized_img.getpixel((0, 0))

    def _get_interpolated_color(self, start_color, end_color, ratio):
        return tuple(int(start_color[i] + (end_color[i] - start_color[i]) * ratio) for i in range(3))


class ImageCreat():
    def __init__(self, size, source_img):
        self.source_img = source_img
        self.frame = Image.new("RGBA", size, (0, 0, 0, 0))
        self.resized_img = None

    async def get_centry_image(self, baseheight=0, basewidth=0, baseheight_wide=None, centry=776):
        if self.resized_img is None:
            self.resized_img = self.resize_image(baseheight, basewidth, baseheight_wide)

        x, y = self.resized_img.size
        position = (0, 0)

        if centry != 0:
            position = (int(centry - x / 2), 0)

        self.frame.alpha_composite(self.resized_img, position)

        return self.frame

    def resize_image(self, baseheight=0, basewidth=0, baseheight_wide=None):
        x, y = self.source_img.size

        if baseheight_wide is None:
            baseheight_wide = baseheight

        if max(x, y) / min(x, y) < 1.1:
            # Квадрат
            hpercent = baseheight / float(y)
            wsize = int(float(x) * float(hpercent))
            resized_img = self.source_img.resize((wsize, baseheight), Image.ANTIALIAS)
        elif x > y:
            # Широкоформат
            hpercent = baseheight_wide / float(y)
            wsize = int(float(x) * float(hpercent))
            resized_img = self.source_img.resize((wsize, baseheight_wide), Image.BICUBIC)
        else:
            # Вертикаль
            wpercent = basewidth / float(x)
            hsize = int(float(y) * float(wpercent))
            resized_img = self.source_img.resize((basewidth, hsize), Image.ANTIALIAS)

            if hsize < baseheight:
                hpercent = baseheight / float(y)
                wsize = int(float(x) * float(hpercent))
                resized_img = self.source_img.resize((wsize, baseheight), Image.BICUBIC)

        return resized_img




async def creat_user_image(img, teampl = "1", shadow = None, bg = None):
    position = {
        "1":
        {
            "frame": (769,719), #Область изображения
            "size_teample": (1916,719), #Размер всего изображения
            "baseheight": 770, #Квадрат
            "basewidth": 769, #Вертикально
            "baseheight_wide": None, #Широкий
            "centry": 385,
            "start_x": 0,
            "start_y": 0,
            "mask": openFile.ImageCache().MASKA_ART_CUSTUM.convert("L"), 
            "effect": openFile.ImageCache().effect_stars.convert("RGBA") 
        },
    }.get(teampl)
    frame = Image.new("RGBA", position["size_teample"], (0,0,0,0))
    userImagess = await ImageCreat(position["frame"],img).get_centry_image(baseheight = position["baseheight"], basewidth = position["basewidth"], baseheight_wide = position["baseheight_wide"], centry = position["centry"])
    grandient = await GradientGenerator(userImagess).generate(1,position["size_teample"][1])
    grandient = grandient.resize(position["size_teample"])
    grandient = ImageChops.soft_light(grandient.convert("RGBA"), position["effect"])

    frame.alpha_composite(userImagess,(position["start_x"],position["start_y"]))


    bg.paste(frame,(0,0), openFile.ImageCache().MASKA_ARTS.convert("L"))

    bg.paste(grandient,(0,0),position["mask"])

    bg.alpha_composite(shadow,(0,0))
    
    return bg

async def creat_user_image_tree(img):
    bg = Image.new("RGBA", (1924,802), (36,36,36,255))
    userImagess = await ImageCreat((582,802),img).get_centry_image(baseheight = 802, basewidth = 582, baseheight_wide = None, centry = 291)
    grandient = await GradientGenerator(userImagess).generate(1,802, left= True)
    grandient = grandient.resize((1350,802))
    bg.alpha_composite(grandient.convert("RGBA"),(0,0))
    grandient = ImageChops.soft_light(bg, openFile.ImageCache().overlay.convert("RGBA"))
    grandient.alpha_composite(openFile.ImageCache().art_frame,(0,0))
    userImagess.alpha_composite(openFile.ImageCache().shadow_art,(0,0))
    grandient.alpha_composite(userImagess,(1342,0))

    return grandient

