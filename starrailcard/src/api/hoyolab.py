from typing import Optional, Union

import aiohttp

from ..model import api_mihomo
from ..tools import http, options, translator, ukrainization
from .api import ApiMiHoMo
from .error import StarRailCardError
from .hoyolab_parsed import AssetHoYoLabParsed

LANG_MAP = {
    "zh-CN": "zh-cn",
    "zh-TW": "zh-tw",
    "de": "de-de",
    "en": "en-us",
    "es": "es-es",
    "fr": "fr-fr",
    "id": "id-id",
    "it": "it-it",
    "ja": "ja-jp",
    "ko": "ko-kr",
    "pt": "pt-pt",
    "ru": "ru-ru",
    "th": "th-th",
    "vi": "vi-vn",
    "tr": "tr",
}

class HoYoLabApi:
    """Class for interacting with the MiHoMo API."""

    def __init__(self, uid: str = 0, lang: str = "en"):
        """Initialize the HoYoLabApi object."""
        self.uid: str = uid
        self.lang: str = translator.SUPPORTED_LANGUAGES.get(lang, "en")
        self.ua_lang: str = lang == "en"
        api_mihomo.UA_LANG = False
        if lang == "ua":
            self.ua_lang = True
            api_mihomo.UA_LANG = True
            self.lang = "en"
        
        self.convert_lang = LANG_MAP.get(self.lang)



    async def get(self,cookie: dict, uid: Union[str,int] = 0):
        try:
            import genshin
        except ImportError:
            raise StarRailCardError(100, "Install the genshin.py module\n- pip install genshin")
        
        if uid == 0:
            uid = self.uid
            if uid == 0:
                raise StarRailCardError(5, "Specify UID")
            
        player = await ApiMiHoMo(uid, self.lang).get(parse= False)
        
        try:
            client = genshin.Client(cookie, game= genshin.Game.STARRAIL, lang= self.convert_lang or "en-us")
            data = await client.get_starrail_characters(uid)
        except Exception as e:
            print(e)
            raise
        data = await AssetHoYoLabParsed(data, data.property_info).collect()
        
        
        if self.ua_lang:
            await ukrainization.TranslateDataManager().load_translate_data()

        return api_mihomo.MiHoMoApi(player=player["player"], characters= data, dont_update_link = False)
    

    
    
        