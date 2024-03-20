# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.


import aiohttp
import json

from pathlib import Path
from .src import utils

def decrypt_url(encrypted_url, key):
    decrypted = ''.join(chr(ord(c) ^ key) for c in encrypted_url)
    return decrypted

n = "FODFCDE"
r = "kLMHBJpWBQqBJOgJP@LQGaLW"
k = "5ceb5d1b20945b82dd21c7`g2909g1e4711d802b"


_LINK_SCORE = "https://raw.githubusercontent.com/"+decrypt_url(n,42)+"/"+decrypt_url(r,35)+"/"+"main"+"/generate/weight.json"
_LINK_DATA = "https://raw.githubusercontent.com/"+decrypt_url(n,42)+"/"+decrypt_url(r,35)+"/"+"main"+"/generate/{name}.json"

_PATH = Path(__file__).parent /"src"/"assets"

_PATH_FILE_NAME = [
    "max",
    "relic_id",
    "rolls",
    "score"
]
async def get_score(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            data = await response.json(content_type='text/plain')
            return data



def open_score(name):
    with open(_PATH/f"{name}.json", 'r', encoding="utf-8") as file:
        data = json.load(file)

    return data

def save(name,data):
    with open(_PATH/f"{name}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

class Calculator:
    def __init__(self, data) -> None:
        self.data = data
        self.score = open_score("score")
        self.rolls = open_score("rolls")
        self.relict_id = open_score("relic_id")
        self.max = open_score("max")

        self.result = {
            "score": {},
            "total_score": {"count": 0, "rank": {"name": "N/A", "color": None}},
            "bad": []
        }
    
    def get_rolls(self,rarity, stats):
        low = self.rolls[stats.type][str(rarity)][0]
        mid = self.rolls[stats.type][str(rarity)][1]
        high = self.rolls[stats.type][str(rarity)][2]
        value = stats.value
        result = None
        max_margin = 100
        for i in range(rarity + 1):
            for j in range(rarity + 1):
                for k in range(rarity + 1):
                    if i + j + k > rarity + 1:
                        break
                    value_sum = i * low + j * mid + k * high
                    if abs(value_sum - value) < max_margin:
                        max_margin = abs(value_sum - value)
                        result = i+j+k 
        return result
    
    async def get_relic_score(self, chara_id, relic_json):
        result_json = {}
        
        main_weight = self.score[chara_id]["main"][self.relict_id.get(relic_json.id, relic_json.id)[-1]][relic_json.main_affix.type]
        main_affix_score = (relic_json.level + 1) / 16 * main_weight
        result_json["main_formula"] = f'{round((relic_json.level + 1) / 16 * 100, 1)}×{main_weight}={main_affix_score * 100}'
        
        sub_affix_formulas = []
        dont_sub = []
        for sub_affix_json in relic_json.sub_affix:
            if self.score[chara_id]["weight"][sub_affix_json.type] <= 0.3:
                dont_sub.append(sub_affix_json.type)
            sub_affix_formulas.append(f'{round(sub_affix_json.value / self.max[sub_affix_json.type] * 100, 1)}×{round(self.score[chara_id]["weight"][sub_affix_json.type], 1)}')
        sub_affix_score = sum((sub_affix_json.value / self.max[sub_affix_json.type]) * self.score[chara_id]["weight"][sub_affix_json.type] for sub_affix_json in relic_json.sub_affix)

        result_json["score"] = main_affix_score * 0.2 + sub_affix_score * 0.2
        result_json["sub_formulas"] = sub_affix_formulas

        return result_json,dont_sub

    async def start(self):
        
        if not self.data.id in self.score:
            await self.update_score()
            self.score = open_score("score")

        for key in self.data.relics:
            relic_score_json, bad = await self.get_relic_score(self.data.id,key)
            self.result["bad"] = list(set(self.result["bad"] + bad))
            relic_score = round(relic_score_json["score"] * 100, 1)
            self.result["total_score"]["count"] += relic_score
            self.result["score"][key.id] = {"count": relic_score, "rolls": {}, "rank": {"name": utils.get_relic_score_text(relic_score), "color": utils.get_relic_score_color(relic_score)}}
            for sub in key.sub_affix:
                rolls = self.get_rolls(key.rarity, sub)
                self.result["score"][key.id]["rolls"][sub.type] = rolls
        
        for key in self.result["score"]:
            self.result["total_score"]["count"] += self.result["score"][key]["count"]
        
        self.result["total_score"]["count"] = round(self.result["total_score"]["count"] /2, 1)
        self.result["total_score"]["rank"] = {"name": utils.get_relic_full_score_text(self.result["total_score"]["count"]), "color": utils.get_total_score_color(self.result["total_score"]["count"])}
         
        return self.result

        
    async def update_score(self):
        
        for key in _PATH_FILE_NAME:
            if key == "score":
                data = await get_score(_LINK_SCORE)
            else:
                data = await get_score(_LINK_DATA.format(name=key))
        
            save(key,data)