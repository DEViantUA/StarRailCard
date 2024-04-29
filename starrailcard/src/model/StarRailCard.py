# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.


from pydantic import BaseModel
from PIL import Image
from typing import List ,Optional,Final, Union

try:
    from moviepy.editor import ImageSequenceClip
except:
    pass

import numpy as np

from ..tools.ukrainization import TranslateDataManager
from ..tools.http import AioSession

UA_LANG = False
MAIN_LINK: Final[str] = "https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{icon}"

class MemoryInfo(BaseModel):
    level: Optional[int]
    chaos_id: Optional[int]
    chaos_level: Optional[int]
    
class SpaceInfo(BaseModel):
    memory_data: Optional[MemoryInfo]
    universe_level: Optional[int]
    light_cone_count: Optional[int]
    avatar_count: Optional[int]
    achievement_count: Optional[int]

class Avatar(BaseModel):
    id: str
    name: str
    icon: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.icon = MAIN_LINK.format(icon = self.icon)
    
        if UA_LANG:
            self.name = TranslateDataManager._data.avatar.get(self.id, self.name)

class Player(BaseModel):
    uid: Optional[str]
    nickname: Optional[str]
    level: int
    world_level: int
    friend_count: int
    avatar: Avatar
    signature: Optional[str]
    is_display: bool
    space_info: Optional[SpaceInfo]

class Card(BaseModel):
    id: int
    name: Optional[str]
    rarity: int
    card: Union[Image.Image,list]
    animation: bool
    size: Optional[tuple]
    color: Optional[tuple]
    class Config:
        arbitrary_types_allowed = True
    
    async def get_info(self, lang = "en"):
        #await AioSession.get_session()
        url = f"https://api.yatta.top/hsr/v2/{lang}/avatar/{self.id}"
        data = await AioSession.get(url, response_format = "json")
        data["data"]["icon"] = {"icon": f'https://api.yatta.top/hsr/assets/UI/avatar/medium/{data["data"]["icon"]}.png', 
                                "splash": f'https://api.yatta.top/hsr/assets/UI/avatar/large/{data["data"]["icon"]}.png',
                                "avatar": f'https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/icon/avatar/{data["data"]["icon"]}.png'
        }        
        #await AioSession.close_session()
        
        return data["data"]
    
    def show(self):
        if self.animation:
            self.card[0].show()
        else:
            self.card.show()
    
    def save_gif(self, method = "pillow", name_file = None, format = "gif", resize = None):
        if name_file is None:
            name_file = f"{self.id}_{self.rarity}"
        if isinstance(self.card, list):
            if not format in ["gif", "webp"]:
                format = "gif"
            if format == "webp":
                method = "pillow"
            
            if method.lower() == "pillow":
                self.card[0].save(f"{name_file}.{format}", format = format.capitalize(), save_all=True, append_images=self.card[1:], optimize=True, quality=100, duration=100, loop=0)
            else:
                if resize is None:
                    self.card = [np.array(frame) for frame in self.card]
                else:
                    self.card = [np.array(frame.resize(resize)) for frame in self.card]
                clip = ImageSequenceClip(self.card, fps=10)
                clip.write_gif(f"{name_file}.{format}", fps=10, loop=True, program='ffmpeg', fuzz=0, opt='OptimizeTransparency', logger = None )
        else:
            self.card.save(f"{name_file}.png")
        
class Setting(BaseModel):
    uid: int
    lang: Optional[str]
    hide_uid: bool
    save: bool
    force_update: bool
    style: int
    
class StarRail(BaseModel):
    settings: Setting
    player: Player
    card: Union[List[Card], Image.Image]
    character_id: list
    character_name: list
    
    class Config:
        arbitrary_types_allowed = True
    
    def __str__(self):
        return f"card={self.card} character_name = {self.character_name} character_id={self.character_id}"
    
    def get_charter(self, setting = False, name = False):
        if setting:
            card_ids = [str(card.id) for card in self.card]

            if name:
                return {name: id for id, name in zip(self.character_id, self.character_name) if id in card_ids}
            return {id: name for id, name in zip(self.character_id, self.character_name) if id in card_ids}
        
        if name:
            return {name: id for id, name in zip(self.character_id, self.character_name)}
        
        return {id: name for id, name in zip(self.character_id, self.character_name)}