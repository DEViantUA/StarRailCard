import aiohttp
from typing import Optional, Union
import os

    
from ..tools import http, translator, ukrainization
from .enka_parsed import *
from .error import StarRailCardError
from ..tools.json_data import JsonManager
from ..tools.enums import PathData
from ..tools.translator import SUPPORTED_LANGUAGES
from .enka_parsed import AssetEnkaParsed
from ..model import api_mihomo

_API_ENKA = "https://enka.network/api/hsr/uid/{uid}"
_API_ENKA_HASH = "https://enka.network/api/profile/{name}/hoyos/"
_API_ENKA_BUILD = "https://enka.network/api/profile/{name}/hoyos/{hash}/builds/"


_INDEX_MIHOMO = "https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/index_new/{lang}/{index}.json"

_INDEX_NAME = [
    "avatars",
    "character_promotions",
    "character_ranks",
    "character_skill_trees",
    "character_skills",
    "characters",
    "elements",
    "light_cone_promotions",
    "light_cone_ranks",
    "light_cones",
    "paths",
    "properties",
    "relic_main_affixes",
    "relic_sets",
    "relic_sub_affixes",
    "relics"    
]



class ApiEnkaNetwork:
    def __init__(self, uid: Union[int, str] = 0, lang: str = "en", parsed: bool = True) -> None:
        self.uid: str = uid
        self.parsed: bool = parsed
        self.lang: str = translator.SUPPORTED_LANGUAGES.get(lang, "en")
        self.ua_lang: str = lang == "en"
        api_mihomo.UA_LANG = False
        if lang == "ua":
            self.ua_lang = True
            api_mihomo.UA_LANG = True
    
    async def get_build(self, name: str, hash: str, uid: Union[int, str]  = 0):
        
        if uid == 0:
            uid = self.uid
         
        if uid == 0:
            raise StarRailCardError(5, "Specify UID")
            
        try:
            data_build = await http.AioSession.get(_API_ENKA_BUILD.format(name=name, hash = hash))
            data = await self.get(uid, parsed = False)
            data["detailInfo"]["avatarDetailList"] = [data_build]
            if self.parsed:
                data = await AssetEnkaParsed(data).collect(True)
            else:
                return data
        except aiohttp.ClientConnectionError:
            raise StarRailCardError(1, "Server is not responding")
        except aiohttp.ClientResponseError as e:
            raise StarRailCardError(e.status, f"Server returned status code {e.status}")
        
        if self.ua_lang:
            await ukrainization.TranslateDataManager().load_translate_data()

                
        return api_mihomo.MiHoMoApi(player=data["player"], characters=data["characters"], dont_update_link = False)
    
    
    async def get_hash(self, name: str, hash: bool = True):
        """Return user's HASH
        Args:
            name (str): Profile nickname on the EnkaNetwork website
            hash (bool, optional): Return only the user's hash
        Raises:
            StarRailCardError: Server is not responding
        Returns:
            list: List of included dictionaries with hash and profile information
        """
        try:
            data = await http.AioSession.get(_API_ENKA_HASH.format(name=name))
        except aiohttp.ClientConnectionError:
            raise StarRailCardError(1, "Server is not responding")
        except aiohttp.ClientResponseError as e:
            raise StarRailCardError(e.status, f"Server returned status code {e.status}")
        
        if hash:
            return [
                    {
                        "enka": name,
                        "hash": key,
                        "region": data[key]["region"],
                        "uid": data[key]["uid"],
                        "icon": data[key]["player_info"]["headIcon"],
                        "name": data[key]["player_info"]["nickname"],
                        "level": data[key]["player_info"]["level"]
                    } for key in data if data[key]["hoyo_type"] == 1
                ]
        
        return data
            
    async def get(self, uid: Union[str,int] = 0, parsed: bool = True):
        """Get data from the EnkaNetwork API."""
        
        if uid == 0:
            uid = self.uid
            
            if uid == 0:
                raise StarRailCardError(5, "Specify UID")
        
        try:
            data = await http.AioSession.get(_API_ENKA.format(uid=uid))

            if self.parsed and parsed:
                data = await AssetEnkaParsed(data).collect()
            else:
                return data
        except aiohttp.ClientConnectionError:
            raise StarRailCardError(1, "Server is not responding")
        except aiohttp.ClientResponseError as e:
            raise StarRailCardError(e.status, f"Server returned status code {e.status}")
        
        if self.ua_lang:
            await ukrainization.TranslateDataManager().load_translate_data()

        return api_mihomo.MiHoMoApi(player=data["player"], characters=data["characters"], dont_update_link = False)
        
    async def update_assets(self, lang = None):
        print("===START UPDATE ASSET===")
        for name in _INDEX_NAME:
            for langs in SUPPORTED_LANGUAGES:
                if langs == "ua":
                    continue
                if not lang is None:
                    if langs != lang:
                        continue
                data = await http.AioSession.get(_INDEX_MIHOMO.format(lang = langs, index=name))
                if not os.path.exists(PathData.ENKA_INDEX.value / langs):
                    os.makedirs(PathData.ENKA_INDEX.value / langs)
                await JsonManager(PathData.ENKA_INDEX.value / langs /f"{name}.json").write(data)
                
            print(f"- Updated file: {name}")
        print("===END UPDATE ASSET===")        
        