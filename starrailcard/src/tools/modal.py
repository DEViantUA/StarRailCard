# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from pydantic import BaseModel
from typing import List ,Optional
from PIL import Image

class Avatar(BaseModel):
    id: Optional[str]
    name: Optional[str]
    icon: Optional[str]

class SpaceInfo(BaseModel):
    pass_area_progress: Optional[int]
    light_cone_count: Optional[int]
    avatar_count: Optional[int]
    achievement_count: Optional[int]

class PlayerV2(BaseModel):
    uid: Optional[str]
    nickname: Optional[str]
    level: Optional[int]
    avatar: Avatar
    signature: Optional[str]
    friend_count: Optional[int]
    world_level: Optional[int]
    birthday: Optional[str]
    space_info: SpaceInfo



class Card(BaseModel):
    id: Optional[str]
    name: Optional[str]
    rarity: Optional[int]
    card: Image.Image
    class Config:
        arbitrary_types_allowed = True
    size: Optional[tuple]
class Settings(BaseModel):
    uid: Optional[int]
    lang: Optional[str]
    hide: Optional[bool]
    save: Optional[bool]
    background: Optional[bool]

class HSRCard(BaseModel):
    settings: Settings
    player: PlayerV2
    card: List[Card]
    name: Optional[str]
