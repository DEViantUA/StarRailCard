# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import random
import aiofiles
import io
from PIL import Image
import os
import sys
import datetime

from .git import ImageCache
from .http import AioSession
from ... import __version__

_git = ImageCache()

def get_user_agent(user_agent):
    python_version = sys.version_info
    
    if not user_agent is None:
        if user_agent == "StarRailCard/{version} (Python {major}.{minor}.{micro})".format(version=__version__,major=python_version.major,minor=python_version.minor,micro=python_version.micro):
            return user_agent
        
        return f"StarRailCad/{__version__}: {user_agent}"
    
    return "StarRailCard/{version} (Python {major}.{minor}.{micro})".format(
        version=__version__,
        major=python_version.major,
        minor=python_version.minor,
        micro=python_version.micro
    )

_DEFAULT_SCORE = {'count': 0, 
                  'rolls': {}, 
                  'rank': {'name': 'N/A', 
                           'color': (255, 255, 255, 255)
                    }
}

color_score  = {
    4: (255, 250, 141, 255),
    3: (252, 209, 124, 255),
    2: (184, 157, 103, 255),
    1: (170, 145, 98, 255),
    0: (255, 255, 255, 255)
}

color_scoreR = {
    4: (255, 250, 141, 255),
    3: (252, 209, 124, 255),
    2: (234, 207, 153, 255),  # Было (184, 157, 103, 255)
    1: (220, 195, 148, 255),  # Было (170, 145, 98, 255)
    0: (255, 255, 255, 255)   # Было (255, 255, 255, 255)
}

color_element_stat = {
    'physical_dmg': (255, 255, 255, 255),
    'fire_dmg': (248, 79, 54, 255),
    'ice_dmg': (71, 199, 253, 255),
    'lightning_dmg': (136, 114, 241, 255),
    'wind_dmg': (0, 255, 156, 255),
    'quantum_dmg': (28, 41, 186, 255),
    'imaginary_dmg': (244, 210, 88, 255),
}

color_element_talant = {
    'physical': (255, 255, 255, 255),
    'fire': (248, 79, 54, 255),
    'ice': (71, 199, 253, 255),
    'lightning': (136, 114, 241, 255),
    'thunder': (136, 114, 241, 255),
    'wind': (0, 255, 156, 255),
    'quantum': (28, 41, 186, 255),
    'imaginary': (244, 210, 88, 255),
}

color_element = {
    'PhysicalAddedRatio': (255, 255, 255, 255),
    'PhysicalResistance': (255, 255, 255, 255),
    'FireAddedRatio': (248, 79, 54, 255),
    'FireResistance': (248, 79, 54, 255),
    'IceAddedRatio': (71, 199, 253, 255),
    'IceResistance': (71, 199, 253, 255),
    'ThunderAddedRatio': (136, 114, 241, 255),
    'ThunderResistance': (136, 114, 241, 255),
    'WindAddedRatio': (0, 255, 156, 255),
    'WindResistance': (0, 255, 156, 255),
    'QuantumAddedRatio': (28, 41, 186, 255),
    'QuantumResistance': (28, 41, 186, 255),
    'ImaginaryAddedRatio': (244, 210, 88, 255),
    'ImaginaryResistance': (244, 210, 88, 255)
}


color_lc_line = {
    "3": (150, 202, 255, 255),
    "4": (217, 150, 255, 255),
    "5": (255, 217, 144, 255),
}


async def get_charter_id(data):
    data = [value.strip() for value in data.split(',') if value.strip()]

    data = [value for value in data if value.isdigit()]
    
    if data == []:
        return None
    return data

async def style_setting(style, settings):
    if str(style) in ["1","2","3"]:
        return style, settings
    
    return 1, {}


def ups(x):
    if x == 5:
        return "V"
    elif x == 4:
        return "IV"
    elif x == 3:
        return "III"
    elif x == 2:
        return "II"
    elif x == 1:
        return "I"
    else:
        return "O"


def max_lvl(x):
    if x == 0:
        max = 20
    elif x == 1:
        max = 30
    elif x == 2:
        max = 40 
    elif x == 3:
        max = 50
    elif x == 4:
        max = 60
    elif x == 5:
        max = 70
    else:
        max = 80
    
    return max

async def get_color_user(color):
    processed_dict = {}
    for key, value in color.items():
        if isinstance(value, tuple):
            if len(value) >= 3 and len(value) <= 4:
                if all(0 <= x <= 255 for x in value):
                    processed_dict[key] = value
    if processed_dict != {}:
        return processed_dict
    return None

async def get_character_art(character_art, style=None):
    processed_dict = {}
    for key, value in character_art.items():
        if isinstance(value, list):
            if isinstance(value[0], dict):
                if style is not None:
                    matching_art = [v['art'] for v in value if v['style'] == style]
                    if matching_art:
                        processed_dict[key] = random.choice(matching_art)
                else:
                    processed_dict[key] = random.choice([v['art'] for v in value])
            else:
                processed_dict[key] = random.choice(value)
        elif isinstance(value, dict):
            if 'style' in value and value['style'] == style:
                processed_dict[key] = value['art']
        else:
            processed_dict[key] = value

    
    return processed_dict

async def get_stars(x, type = 1):
    if type == 1:
        if x == 5:
            return await _git.g_five
        elif x == 4:
            return await _git.g_four
        elif x == 3:
            return await _git.g_three
        elif x == 2:
            return await _git.g_two
        else:
            return await _git.g_one
    elif type == 2:
        if x == 1:
            return await _git.strs_1
        elif x == 2:
            return await _git.strs_2
        elif x == 3:
            return await _git.strs_3
        elif x == 4:
            return await _git.strs_4
        else:
            return await _git.strs_5
    elif type == 3:
        if x == 1:
            return await _git.stars_v_1
        elif x == 2:
            return await _git.stars_v_2
        elif x == 3:
            return await _git.stars_v_3
        elif x == 4:
            return await _git.stars_v_4
        else:
            return await _git.stars_v_5
        
def calculator_relict_sets(data):
    rel_set = {}
    for key in data:
        if key.id not in rel_set:
            if key.properties == []:
                rel_set[key.id] = {"num": int(key.num), "name": key.name, "icon": key.icon, "properties": None}
            else:
                rel_set[key.id] = {"num": int(key.num), "name": key.name, "icon": key.icon, "properties": {"icon": key.properties[0].icon, "display": key.properties[0].display}}
        else:
            rel_set[key.id]["num"] = int(key.num)
    
    return rel_set

async def get_background_path(path):
    if path == "Rogue":
        icon =  await _git.Rogue
    elif path == "Knight":
        icon =  await _git.Knight
    elif path == "Mage":
        icon =  await _git.Mage
    elif path == "Priest":
        icon =  await _git.Priest
    elif path == "Shaman":
        icon =  await _git.Shaman
    elif path == "Warlock":
        icon =  await _git.Warlock
    elif path == "Memory":
        icon =  await _git.Memory
    else:
        icon = await _git.Warrior
    
    return icon.copy()


async def get_seeleland(uid, charter_id):
    url = f"https://seeleland.azurewebsites.net/api/get_player_data?uid={uid}"
    data = await AioSession.get(url, response_format= "json")
    if data is None:
        return None
    for key in data:
        if key["k"] == str(charter_id):
            data = key.get("lb")

    if data == {} or data is None:
        return None
    if type(data) == list:
        for key in data:
            if "lb" in key:
                return key["lb"]["tutorial"] if "tutorial" in key["lb"] else None
    else:
        for key in data:
            return data[key]


async def save_card(uid, image_data, name):
    data = datetime.datetime.now().strftime("%d_%m_%Y %H_%M")
    path = os.getcwd()
    
    try:
        os.makedirs(f'{path}/RailCardImg/{uid}', exist_ok=True)
    except FileExistsError:
        pass
    
    file_name = f"{path}/RailCardImg/{uid}/{name}_{data}.png"
    
    async with aiofiles.open(file_name, 'wb') as file:
        if isinstance(image_data, Image.Image):
            img_bytes = io.BytesIO()
            image_data.save(img_bytes, format='PNG')
            await file.write(img_bytes.getvalue())
