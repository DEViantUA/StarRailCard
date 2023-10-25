# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import aiohttp

url = "https://raw.githubusercontent.com/Mar-7th/StarRailScore/master/score.json"

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json(content_type='text/plain')
            return data
        

data = None

async def get_rank(value):
    if value >= 43.7:
        return "SSS"
    elif value >= 37.8 and value < 43.7:
        return "SS"
    elif value >= 33.5 and value  < 37.8:
        return "S"
    elif value >= 29.1 and value < 33.5:
        return "A"
    elif value >= 23.3 and value  < 29.1:
        return "B"
    elif value >= 17.5 and value  < 23.3:
        return "C"
    elif value >= 11.6 and value  < 17.5:
        return "D"
    else:
        return "N/A"

async def get_total_rank(value):
    value /= 6
    if value >= 43.7:
        return "SSS"
    elif value >= 37.8 and value < 43.7:
        return "SS"
    elif value >= 33.5 and value  < 37.8:
        return "S"
    elif value >= 29.1 and value < 33.5:
        return "A"
    elif value >= 23.3 and value  < 29.1:
        return "B"
    elif value >= 17.5 and value  < 23.3:
        return "C"
    elif value >= 11.6 and value  < 17.5:
        return "D"
    else:
        return "N/A"



async def get_rating(relict,chart_id, position):
    global data
    if data is None:
        data = await fetch_data()

    Eff_Stat = 0
    value_main = 0
    if str(chart_id):
        if str(chart_id) in data:
            if relict.main_affix.type in data[str(chart_id)]["main"][position]:
                value_main = data[str(chart_id)]["main"][position][relict.main_affix.type]
        
            i = 0
            score = 0
            for key in relict.sub_affix:
                value = 0
                if key.type in data[str(chart_id)]["weight"]:
                    if data[str(chart_id)]["weight"][key.type] > 0:
                        Eff_Stat += 1
                    value = data[str(chart_id)]["weight"][key.type]

                i += 1
                score += value

            score += Eff_Stat * value_main
            score = 55/10.0*score

            return score, await get_rank(score), Eff_Stat
    return 0, await get_rank(0), 0


from pydantic import BaseModel

class Affix(BaseModel):
    type: str
    field: str
    name: str
    icon: str
    value: float
    display: str
    percent: bool = False
    count: int = 0
    step: int = 0

class Relict(BaseModel):
    id: str
    name: str
    set_id: str
    set_name: str
    rarity: int
    level: int
    icon: str
    main_affix: Affix
    sub_affix: list[Affix]


async def fetch_data_seeleland(uid):
    url = f"https://seeleland.azurewebsites.net/api/get_player_data?uid={uid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data


async def get_seeleland(uid, charter_id):
    data = await fetch_data_seeleland(uid)
    if data is None:
        return None
    for key in data:
        if key["k"] == str(charter_id):
            data = key.get("lb")
    
    if data != {} and data is not None:
        for key in data:
            return data[key]
    else:
        return None

    
