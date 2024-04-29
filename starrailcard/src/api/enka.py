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
_ASSETS_ENKA = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/hsr/{asset}.json"
_INDEX_MIHOMO = "https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/index_new/{lang}/{index}.json"

_ASSET_NAME = [
    "avatars",
    "characters",
    "meta",
    "ranks",
    "relics",
    "skills",
    "skilltree",
    "weps",
    "hsr"
]

_INDEX_NAME = [
    "paths",
    "elements",
    "character_skills",
    "character_skill_trees",
    "properties",
    "light_cone_ranks",
    "relics",
    "relic_main_affixes",
    "relic_sub_affixes",
    "relic_sets",
    "character_ranks"
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
    
    async def get(self):
        """Get data from the MiHoMo API."""
        try:
            data = await http.AioSession.get(_API_ENKA.format(uid=self.uid))

            if self.parsed:
                data = await AssetEnkaParsed(data).collect()
                  
        except aiohttp.ClientConnectionError:
            raise StarRailCardError(1, "Server is not responding")
        except aiohttp.ClientResponseError as e:
            raise StarRailCardError(e.status, f"Server returned status code {e.status}")
        
        if self.ua_lang:
            await ukrainization.TranslateDataManager().load_translate_data()

        return api_mihomo.MiHoMoApi(player=data["player"], characters=data["characters"], dont_update_link=True)
        
    async def update_assets(self):
        print("===START UPDATE INDEX===")
        for name in _INDEX_NAME:
            for lang in SUPPORTED_LANGUAGES:
                if lang == "ua":
                    continue
                data = await http.AioSession.get(_INDEX_MIHOMO.format(lang = lang, index=name))
                if not os.path.exists(PathData.ENKA_INDEX.value / lang):
                    os.makedirs(PathData.ENKA_INDEX.value / lang)
                await JsonManager(PathData.ENKA_INDEX.value / lang /f"{name}.json").write(data)
                
            print(f"- Updated file: {name}")
        print("===END UPDATE INDEX===")
        print()
        print("===START UPDATE ASSETS===")
        for name in _ASSET_NAME:
            if name == "hsr":
                data = await http.AioSession.get(_ASSETS_ENKA.format(asset=name))
            else:
                data = await http.AioSession.get(_ASSETS_ENKA.format(asset=f"honker_{name}"))
            await JsonManager(PathData.ENKA.value / f"{name}.json").write(data)
            print(f"- Updated file: {name}")
            
        print("===END UPDATE ASSETS===")
        
        