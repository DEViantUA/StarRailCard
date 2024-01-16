# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
from PIL import ImageFont,Image,ImageDraw,ImageChops,ImageFilter,ImageStat
from io import BytesIO
from . import openFile
import aiohttp,re, json
import colorsys
from cachetools import TTLCache
import numpy as np
import colorsys
from more_itertools import chunked

async def get_font(size):
    return ImageFont.truetype(openFile.font, size)


xId = "91470304"
ccokie = "first_visit_datetime_pc=2022-08-06+03:53:37; p_ab_id=1; p_ab_id_2=5; p_ab_d_id=1897822829; yuid_b=IFV4MVY; privacy_policy_agreement=5; c_type=23; privacy_policy_notification=0; a_type=0; b_type=1; __utmc=235335808; __utmz=235335808.1675712222.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gcl_au=1.1.1586580017.1675934633; _gid=GA1.2.67267752.1677021212; PHPSESSID=91470304_hbEoBFwL6Ss8hQHDiSkc26NAN2BgUaww; device_token=cbf72f380348bc4dcc9910df20a3b368; QSI_S_ZN_5hF4My7Ad6VNNAi=v:100:0; __utmv=235335808.|2=login ever=yes=1^3=plan=premium=1^5=gender=male=1^6=user_id=91470304=1^9=p_ab_id=1=1^10=p_ab_id_2=5=1^11=lang=en=1; _ga_MZ1NL4PHH0=GS1.1.1677021212.1.1.1677021635.0.0.0; __utma=235335808.1013236179.1675712222.1677021201.1677023923.4; login_ever=yes; __cf_bm=uIwLHChsA9lvfHUYdc_qU3KBp.pYrFxzrlv_4crFoE4-1677024971-0-AaFldWtGUM9OmDn1Kfcwc03QpGNuGGlE8Ev1PZtv6Q6PavyffvJ2dmVVIDVdeTM6cD8GNSLlL8ta93GxurhWiQqj+rxXEWgO3LDUqV0uXNORvDhI4+KP930Hf962s6ivFp1Zz6aG5fVGtpySkJBAEcVUAoxfpO6+KGijUP4sJAvftKvKK8NZaD6zcqDr47mOMJsHCvdck/DW4GqbSDeuIJo=; __utmt=1; tag_view_ranking=_EOd7bsGyl~ziiAzr_h04~azESOjmQSV~Ie2c51_4Sp~Lt-oEicbBr~WMwjH6DkQT~HY55MqmzzQ~yREQ8PVGHN~MnGbHeuS94~BSlt10mdnm~tgP8r-gOe_~fg8EOt4owo~b_rY80S-DW~1kqPgx5bT5~5oPIfUbtd6~KN7uxuR89w~QaiOjmwQnI~0Sds1vVNKR~pA1j4WTFmq~aPdvNeJ_XM~vzTU7cI86f~HHxwTpn5dx~pnCQRVigpy~eVxus64GZU~rOnsP2Q5UN~-98s6o2-Rp~EZQqoW9r8g~iAHff6Sx6z~jk9IzfjZ6n~PsltMJiybA~TqiZfKmSCg~IfWbVPYrW4~0TgyeJ7TQv~g2IyszmEaU~28gdfFXlY7~DCzSewSYcl~n15dndrA2h~CActc_bORM~U51WZv5L6G~-7RnTas_L3~zyKU3Q5L4C~QwUeUr8yRJ~j3leh4reoN~vgqit5QC27~t1Am7AQCDs~5cTBH7OrXg~-HnQonkV01~oCqKGRNl20~ba025Wj3s2~TAc-DD8LV2~p0NI-IYoo2~wqBB0CzEFh~U-RInt8VSZ~oiDfuNWtp4~fAWkkRackx~i54EuUSPdz~Js5EBY4gOW~ZQJ8wXoTHu~Cm1Eidma50~CMvJQbTsDH~ocDr8uHfOS~pzZvureUki~ZNRc-RnkNl~nWC-P2-9TI~q1r4Vd8vYK~hZzvvipTPD~DpYZ-BAzxm~096PrTDcN1~3WI2JuKHdp~faHcYIP1U0~1n-RsNEFpK~Bd2L9ZBE8q~txZ9z5ByU7~r01unnQL0a~EEUtbD_K_n~cb-9gnu4GK~npWJIbJroU~XbjPDXsKD-~lkoWqucyTw~P8OX_Lzc1b~RmnFFg7HS4~6rYZ-6JKHq~d80xTahBd1~OYl5wlor4w~2R7RYffVfj~1CWwi2xr7g~c7QmKEJ54V~rlExNugdTH~wO2lnVhO8m~vc2ipXnqbX~Is5E1jIZcw~c_aC4uL3np~vzxes78G4k; _ga=GA1.2.714813637.1675712223; _gat_UA-1830249-3=1; _ga_75BBYNYN9J=GS1.1.1677023923.4.1.1677025390.0.0.0; __utmb=235335808.52.9.1677024704913"

headers = {
    "accept-type": "application/json",
    "accept-encoding": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,af;q=0.6",
    "language": "gzip, deflate, br",
    "cookie": ccokie,
    "dnt": "1",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "x-user-id": xId,
    "referer": "https://www.pixiv.net/",
}

cache = TTLCache(maxsize=1000, ttl=300)  

async def get_dowload_img(link,size = None, thumbnail_size = None):
    cache_key = json.dumps((link, size, thumbnail_size), sort_keys=True)  # Преобразовываем в строку
        
    if cache_key in cache:
        return cache[cache_key]
    

    try:
        if "pximg" in link:
            async with aiohttp.ClientSession(headers=headers) as session, session.get(link) as r:
                try:
                    image = await r.read()
                finally:
                    await session.close()
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as response:
                    try:
                        image = await response.read()
                    finally:
                        await session.close()
    except:
        raise
    try:
        image = Image.open(BytesIO(image)).convert("RGBA")
    except:
        #print(link)
        image = Image.new("RGBA",(1,1),(0,0,0,0))
    if size:
        image = image.resize(size)
        cache[cache_key] = image
        return image
    elif thumbnail_size:
        image.thumbnail(thumbnail_size)
        cache[cache_key] = image
        return image
    else:
        cache[cache_key] = image
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
    elif teample == 4:
        splash = await get_dowload_img(link=image)
        frme_splash = await get_centr_honkai((685,802),splash)
        bg_frame = Image.new('RGBA', (685,802), color= (255,255,255,0))
        bg_frame.alpha_composite(frme_splash,(0,0))
        bg_element = bg.copy().convert("RGBA")
        maska_bg =  bg.copy()
        bg_element.alpha_composite(bg_frame,(0,0))
        bg_element.paste(maska_bg,(0,0),maska)
        bg_element.alpha_composite(openFile.ImageCache().shadow_enc,(0,0))
    elif teample == 5:
        splash = await get_dowload_img(link=image)
        frme_splash = await get_centr_honkai((370,663),splash)
        bg_element = Image.new('RGBA', (370,663), color= (255,255,255,0))
        bg_element.paste(frme_splash,(0,0),maska)
        bg.alpha_composite(bg_element,(0,0))        
        return bg
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

async def light_level(pixel_color):
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3]))    
    return l

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
            if a != 0:  # Проверяем, является ли текущий пиксель непрозрачным
                pixels[i, j] = target_color + (a,)  # Заменяем цвет, включая прозрачность
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

        return gradient_img

    async def _get_pixel_color(self, left, top, right, bottom):
        cropped_img = self.source_img.crop((left, top, right, bottom))
        resized_img = cropped_img.convert("RGB").resize((1, 1))
        pixel_color = resized_img.getpixel((0, 0))
        
        return pixel_color
    
    def _get_interpolated_color(self, start_color, end_color, ratio):
        return tuple(int(start_color[i] + (end_color[i] - start_color[i]) * ratio) for i in range(3))

async def apply_opacity(image, opacity=0.2):
    result_image = image.copy()
    alpha = result_image.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    result_image.putalpha(alpha)

    return result_image

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
            resized_img = self.source_img.resize((wsize, baseheight), Image.LANCZOS)
        elif x > y:
            # Широкоформат
            hpercent = baseheight_wide / float(y)
            wsize = int(float(x) * float(hpercent))
            resized_img = self.source_img.resize((wsize, baseheight_wide), Image.BICUBIC)
        else:
            # Вертикаль
            wpercent = basewidth / float(x)
            hsize = int(float(y) * float(wpercent))
            resized_img = self.source_img.resize((basewidth, hsize), Image.LANCZOS)

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

async def creat_user_image_tree(img,characterBackgroundimg,backgroundBlur):
    bg = Image.new("RGBA", (1924,802), (36,36,36,255))
    userImagess = await ImageCreat((582,802),img).get_centry_image(baseheight = 802, basewidth = 582, baseheight_wide = None, centry = 291)
    if characterBackgroundimg is None:
        grandient = await GradientGenerator(userImagess).generate(1,802, left= True)
        grandient = grandient.resize((1350,802))
        bg.alpha_composite(grandient.convert("RGBA"),(0,0))
        grandient = ImageChops.soft_light(bg, openFile.ImageCache().overlay.convert("RGBA"))
        grandient.alpha_composite(openFile.ImageCache().art_frame,(0,0))
        userImagess.alpha_composite(openFile.ImageCache().shadow_art,(0,0))
        grandient.alpha_composite(userImagess,(1342,0))
    else:
        #ТУТ ДОБАВЛЯЕМ ФОН ПОЛЬЗОВАТЕЛЯ
        if backgroundBlur:
            shadow = Image.new("RGBA", (1350,802), (0,0,0,20))
            bgmagess = await ImageCreat((1350,802),characterBackgroundimg).get_centry_image(baseheight = 802, basewidth = 1350, baseheight_wide = 900, centry = 675)
            grandient = bgmagess.filter(ImageFilter.GaussianBlur(5))
            grandient.alpha_composite(shadow,(0,0))
            bg.alpha_composite(grandient.convert("RGBA"),(0,0))
            grandient = ImageChops.soft_light(bg, openFile.ImageCache().overlay.convert("RGBA"))
            grandient.alpha_composite(openFile.ImageCache().art_frame,(0,0))
            userImagess.alpha_composite(openFile.ImageCache().shadow_art,(0,0))
            grandient.alpha_composite(userImagess,(1342,0))
            #ТУТ РАЗМЫВАЕМ и ДОБАВЛЕМ ТЕНЬ
        else:
            shadow = Image.new("RGBA", (1350,802), (0,0,0,20))
            grandient = await ImageCreat((1350,802),characterBackgroundimg).get_centry_image(baseheight = 802, basewidth = 1350, baseheight_wide = 900, centry = 675)
            grandient.alpha_composite(shadow,(0,0))
            bg.alpha_composite(grandient.convert("RGBA"),(0,0))
            grandient = ImageChops.soft_light(bg, openFile.ImageCache().overlay.convert("RGBA"))
            grandient.alpha_composite(openFile.ImageCache().art_frame,(0,0))
            userImagess.alpha_composite(openFile.ImageCache().shadow_art,(0,0))
            grandient.alpha_composite(userImagess,(1342,0))

    return grandient

async def creat_user_image_five(img):
    bg = Image.new("RGBA", (370,663), (0,0,0,0))
    userImagess = await ImageCreat((370,663),img).get_centry_image(baseheight = 663, basewidth = 370, baseheight_wide = None, centry = 185)
    bg.paste(userImagess,(0,0),openFile.ImageCache().mask_bg_five.convert("L"))
    bg.alpha_composite(openFile.ImageCache().shadow_bg_five,(0,0))
    
    return bg
    

async def creat_user_image_four(img):
    bg = Image.new("RGBA", (1924,802), (0,0,0,0))
    userImagess = await get_centr_honkai_art((685,802),img) #await ImageCreat((685,803),img).get_centry_image(baseheight = 1082, basewidth = 582, baseheight_wide = None, centry = 342)
    grandient = await GradientGenerator(userImagess).generate(1,802)
    grandient = grandient.resize((1924,802)).convert("RGBA")
    
    grandient = ImageChops.soft_light(grandient, openFile.ImageCache().effect_soft.convert("RGBA"))
    bg.alpha_composite(grandient,(0,0))
    bg.alpha_composite(userImagess,(0,0))
    bg.paste(grandient.resize((1924,802)),(0,0),openFile.ImageCache().maska_background.convert("L"))
    bg.alpha_composite(openFile.ImageCache().shadow_enc,(0,0))
    return bg

async def get_centr_honkai_art(size, file_name):
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



async def apply_blur_and_overlay(img):
    background = Image.new("RGBA", (681, 459), (0, 0, 0, 0))

    overlay = await get_centr_honkai_art((694, 802),img)

    overlay_blurred = overlay.filter(ImageFilter.GaussianBlur(radius=10))

    background.alpha_composite(overlay_blurred,(0,-343))

    return background



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

async def get_background_colors(image,number,*,common=False,radius=1,quality=None):
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
     


async def get_foreground_colors(image,number,*,common=False,radius=1,quality=None):
    if quality is not None:
        image = image.copy()
        image.thumbnail((quality, quality), 0)
    
    if radius > 1:
        image = image.filter(ImageFilter.BoxBlur(radius))
    
    filtered_image = image.convert('RGB')
    
    if image.mode != 'RGBA':
        filtered_image.putalpha(await get_foreground_alpha(image))
    else:
        filtered_image.putalpha(Image.fromarray(np.uint8(
            np.uint16(await  get_foreground_alpha(image))
            * image.split()[-1]
            / 255
        ), 'L'))
    
    return await  get_dominant_colors(filtered_image, number, common=common)