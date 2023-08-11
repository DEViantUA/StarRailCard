from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from PIL import Image,ImageDraw
import aiohttp
from ..tools import pill, openFile



async def get_site_info(url):
    parsed_url = urlparse(url)
    site_name = parsed_url.hostname.split('.')[-2]
    profile_name = url.split("/")[-1]
    
    return site_name, profile_name



async def get_site_icon(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')
            icon_link = soup.find("link", rel="icon")      
            if icon_link:
                icon = urljoin(url, icon_link.get("href"))
                icon = await pill.get_dowload_img(icon, size= (30,30))
            else:
                icon = openFile.ImageCache().icon

            return icon



async def start(text,icon,types = 0):
    img = Image.new('RGBA', (242,30), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font_autrhor = await pill.get_font(20)
    if types == 0:
        icon_bg = Image.new('RGBA', (30,30), color=(255, 255, 255, 0))
        icon_bg.paste(icon,(0,0), openFile.ImageCache().icon_maska.convert("L"))
    else:
        icon_bg = icon

    img.alpha_composite(icon_bg,(0,0))
    draw.text((37,-1), text, font=font_autrhor, fill=(0, 0, 0, 255))
    draw.text((38,-1), text, font=font_autrhor, fill=(255, 255, 255, 255))

    return img

        