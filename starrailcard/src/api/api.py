import aiohttp
from typing import Optional

from ..tools import http, translator, ukrainization, options
from ..model import api_mihomo
from .error import StarRailCardError

_API_MIHOMO: str = "https://api.mihomo.me/sr_info_parsed/{uid}"
_API_MIHOMO_NAKED: str = "https://api.mihomo.me/sr_info/{uid}"



class ApiMiHoMo:
    """Class for interacting with the MiHoMo API."""

    def __init__(self, uid: str, lang: str = "en", v: int = 2, force_update: bool = False, user_agent: str = None, proxy = None) -> None:
        """Initialize the ApiMiHoMo object."""
        self.force_update: bool = force_update
        self.uid: str = uid
        self.lang: str = translator.SUPPORTED_LANGUAGES.get(lang, "en")
        self.ua_lang: str = lang == "en"
        self.user_agent: str = options.get_user_agent(user_agent)
        self.proxy: str = proxy
        api_mihomo.UA_LANG = False
        if lang == "ua":
            self.ua_lang = True
            api_mihomo.UA_LANG = True
            
        self.v = v
    
    async def get(self, parse: bool = True) -> Optional[api_mihomo.MiHoMoApi]:
        """Get data from the MiHoMo API."""
        try:
            params = {
                'lang': self.lang,
                'is_force_update': str(self.force_update),
                'version': f"v{self.v}"
            }
            
            headers = {
                "User-Agent": self.user_agent
            }
            data = await http.AioSession.get(_API_MIHOMO.format(uid=self.uid), headers = headers, params=params, proxy= self.proxy)
            
            if data is None:
                raise StarRailCardError(4, "Failed to get data from API, please try again")
            
            if 'detail' in data:
                detail = data['detail']
                if detail == 'User not found':
                    raise StarRailCardError(3, "User not found")
                elif detail == 'Invalid parameters':
                    raise StarRailCardError(2, "Invalid parameters")
                elif detail == 'Invalid uid':
                    raise StarRailCardError(1, "Invalid uid")
                else:
                    raise StarRailCardError(0, detail)
                
        except aiohttp.ClientConnectionError:
            raise StarRailCardError(1, "Server is not responding")
        except aiohttp.ClientResponseError as e:
            raise StarRailCardError(e.status, f"Server returned status code {e.status}")
        
        if data["player"]["space_info"].get("book_count") is None:
            self.dop_info = await http.AioSession.get(_API_MIHOMO_NAKED.format(uid=self.uid), headers = headers, params=params, proxy= self.proxy)
            data = await self.add_info(data)
        
        if self.ua_lang:
            await ukrainization.TranslateDataManager().load_translate_data()
        
        if parse:
            return api_mihomo.MiHoMoApi(player=data["player"], characters=data["characters"], dont_update_link= False)
        else:
            return data
    
    async def add_info(self, data):
        info = self.dop_info["detailInfo"]["recordInfo"]
        
        data["player"]["space_info"]["relicCount"] = info.get("relicCount", 0)
        data["player"]["space_info"]["musicCount"] = info.get("musicCount", 0)
        data["player"]["space_info"]["bookCount"] = info.get("bookCount", 0)
        
        memory_data = info.get("challengeInfo", {})
        data["player"]["space_info"]["memory_data"]["abyssStarCount"] = memory_data.get("abyssStarCount")
        data["player"]["space_info"]["memory_data"]["abyssLevel"] = memory_data.get("abyssLevel")
        
        return data