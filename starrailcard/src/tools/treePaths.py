# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import aiohttp

url = "https://raw.githubusercontent.com/FortOfFans/HSRMaps/master/maps/en/avatartree.json"

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json(content_type='text/plain')
            return data

map = {
    "Rogue":{
        "Point05": ["01"],
        "Point06":["02","03","04"],
        "Point07": ["05","06","07"],
        "Point08":["08","09","10"]
    },

    "Knight": {
        "Point05": ["01"],
        "Point06":["02","03","04"],
        "Point07": ["05","06","07"],
        "Point08":["08","09","10"]
    },

    "Warrior": {
        "Point05": ["01"],
        "Point06":["02","03","04"],
        "Point07": ["05","06","07"],
        "Point08":["08","09","10"]
    },

    "Priest": {
        "Point05": ["01","10"],
        "Point06":["02","03","04"],
        "Point07": ["05","06","07"],
        "Point08":["08","09"]
    },

    "Warlock": {
        "Point05": ["01","10"],
        "Point06":["02","03","04"],
        "Point07": ["05","06","07"],
        "Point08":["08","09"]
    },

    "Mage": {
        "Point05": ["01","10"],
        "Point06":["02","03","04"],
        "Point07": ["05","06","07"],
        "Point08":["08","09"]
    },

    "Shaman":{
        "Point05": ["01","04","07"],
        "Point06":["02","03"],
        "Point07": ["05","06"],
        "Point08":["08","09","10"]
    }
}

data = None


async def get_tree(path,skill_id):
    global data
    if data is None:
        data = await fetch_data()
    
    Point = data.get(str(skill_id))
    maps = map.get(path)

    if Point["pos"] in maps:
        return [f"{str(skill_id)[:4]}2{v}" for v in maps[Point["pos"]]] 
    else:
        return None
