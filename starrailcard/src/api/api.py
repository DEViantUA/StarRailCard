# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from ..tools import http, translator, ukrainization
from ..model import api_mihomo
from typing import Final

_API_MIHOMO: Final[str] = "https://api.mihomo.me/sr_info_parsed/{uid}?version=v2&lang={lang}&is_force_update={force_update}"


class ApiMiHoMo:
    def __init__(self,uid, lang = "en", force_update = False) -> None:
        self.force_update = force_update
        self.uid = uid
        api_mihomo.UA_LANG = False
        if lang == "ua":
            api_mihomo.UA_LANG = True
        self.lang = translator.SUPPORTED_LANGUAGES.get(lang, "en")
    
    async def get(self):
        data = await http.AioSession.get(_API_MIHOMO.format(uid = self.uid, lang = self.lang, force_update = self.force_update))
        if api_mihomo.UA_LANG:
            await ukrainization.TranslateDataManager().load_translate_data()
            
        return api_mihomo.MiHoMoApi(**data)