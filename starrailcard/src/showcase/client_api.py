import aiohttp
from typing import Union
from ..model import api_mihomo
from .error import StarRailCardError
from ..tools import http, translator, ukrainization, options
from .config import (ApiType,
                     LangMiHoMo,
                     EnkaLink,
                     MiHoMoLink,
                     LangMap
                     )

class ShowcaseApi:
    def __init__(self, lang: LangMiHoMo = LangMiHoMo.EN, user_agent: str = None,  proxy: Union[dict,str] = None, parsed_info: bool = True,
                 force_update: bool = True, v: int = 2) -> None:
        self.parsed_info = parsed_info
        self.lang = translator.SUPPORTED_LANGUAGES.get(lang, "en")
        self.force_update = force_update
        self.proxy = proxy
        self.headers = {
            "User-Agent": options.get_user_agent(user_agent)
        }
        api_mihomo.UA_LANG = False
        if lang == "ua":
            self.lang = "en"
            self.ua_lang = True
            api_mihomo.UA_LANG = True
        
        self.convert_lang = LangMap.get(self.lang)
        self.v = v
    
    async def get_params(self, api_id: int = 1):
        if api_id == 2:
            return {}
        return {
                'lang': self.lang,
                'is_force_update': str(self.force_update),
                'version': f"v{self.v}"
            }
    
    async def request_data(self, link, uid, params):
        try:
            data = await http.AioSession.get(link.format(uid=uid), headers = self.headers, params=params, proxy= self.proxy)
            if data is None:
                raise StarRailCardError(4, "Failed to get data from API, please try again")
        except aiohttp.ClientConnectionError:
            raise StarRailCardError(1, "Server is not responding")
        except aiohttp.ClientResponseError as e:
            raise StarRailCardError(e.status, f"Server returned status code {e.status}")

        return data
    
    async def get_link_api(self, api_id: ApiType = ApiType.MiHoMo):
        if api_id == 1:
            if self.parsed_info:
                self.parsed_info = False
                return MiHoMoLink.PARSED
            else:
                return MiHoMoLink.NAKED
        elif api_id == 2:     
            return EnkaLink.ENKA   
    
    async def get_parsed(self, data: dict):
        if self.ua_lang:
            await ukrainization.TranslateDataManager().load_translate_data()
        
        data = await AssetEnkaParsed(data).collect()
    
    
    async def get(self, uid: Union[int,str], cookie: dict, api: ApiType = ApiType.MiHoMo):
        if not api in [1,2,3]:
            raise Exception("Invalid api value passed.")
        
        params = await self.get_params(api_id = api)
        
        link = await self.get_link_api(api = api)
            
                 
        if api == 3:
            try:
                import genshin
            except ImportError:
                raise StarRailCardError(100, "Install the genshin.py module\n- pip install genshin")
                
            player = await self.request_data(MiHoMoLink.NAKED, uid, params)
            
            try:
                client = genshin.Client(cookie, game= genshin.Game.STARRAIL, lang= self.convert_lang)
                data = await client.get_starrail_characters(uid)
            except Exception as e:
                print(e)
                raise
            #data = await self.get_parsed()
            
            #data = await AssetHoYoLabParsed(data, data.property_info).collect()

            return 
        
        else:
            data = await self.request_data(link,uid,params)

            if self.parsed_info:
                data = await self.get_parsed(data)
            
        return api_mihomo.MiHoMoApi(player=player["player"], characters= data, dont_update_link = False)
        
            

import asyncio    

async def main():
    await ShowcaseApi().get(7544644, api = 1)

asyncio.run(main())