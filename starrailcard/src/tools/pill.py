# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import ImageFont,Image,ImageDraw
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


async def create_image_with_text(text, font_size, max_width = 336, color = (255,255,255,255)):
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

    img = Image.new('RGBA', (min(width, max_width), height+(font_size-4)), color= (255,255,255,0))

    draw = ImageDraw.Draw(img)
    y_text = 0
    for line in lines:
        text_width, text_height = font.getmask(' '.join(line)).getbbox()[2:]
        draw.text((0, y_text), ' '.join(line), font=font, fill=color)
        y_text += text_height+5
    
    return img


async def get_text_size_frame(text,font_size,frame_width):
    font = await get_font(font_size)

    while font.getlength(text) > frame_width:
        font_size -= 1
        font = await get_font(font_size)

    return font,font.getlength(text)


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