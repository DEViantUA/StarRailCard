# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from typing import Dict, Any, Optional,Final
from .enums import PathData, Ukrainization
from .json_data import JsonManager
from .http import AioSession
from ..model import ukrainization_model 


MAIN_LINK: Final[str] = "https://raw.githubusercontent.com/DEViantUA/StarRailCardUA/main/{file}"


class TranslateDataManager:
    
    _data =  Dict[str, Optional[Dict[str, Any]]]
    
    def __init__(self):
        self.data = {
            "stats": None,
            "weapons": None,
            "avatar": None,
            "relict_sets": None,
            "paths": None,
            "element": None,
        }
    
    async def load_translate_data(self):
        for file in Ukrainization:
            self.data[file.value] = await JsonManager(str(PathData.UKRAINIZATION.value / f'{file.value}.json')).read()
        TranslateDataManager._data = ukrainization_model.UkrainizationModel(**self.data)
        
    async def update(self):
        for file in Ukrainization:
            data = await AioSession.get(MAIN_LINK.format(file = f"{file.value}.json"))
            await JsonManager(str(PathData.UKRAINIZATION.value / f'{file.value}.json')).write(data)
        
    async def check_update(self):
        keys = await JsonManager(str(PathData.UKRAINIZATION.value / "keys.json")).read()
        keys_data = await AioSession.get(MAIN_LINK.format(file = "keys.json"))
        
        if keys_data["key"] == keys["key"]:
            return True
        
        await self.update()
        await JsonManager(str(PathData.UKRAINIZATION.value / "keys.json")).write(keys_data)
        
        
        
            
        
    