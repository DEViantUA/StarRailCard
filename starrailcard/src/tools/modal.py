# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from pydantic import BaseModel
from typing import List ,Optional,Union

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
    card: Optional[Union[List[Card], Image.Image]] 
    cards: Optional[Image.Image]
    name: Optional[str]
    id: Optional[str]
    class Config:
        arbitrary_types_allowed = True



class MainAffix(BaseModel):
    type: Optional[str]
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: Optional[float]
    display: Optional[str]
    percent: Optional[bool]

class SubAffix(BaseModel):
    type: Optional[str]
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: Optional[float]
    display: Optional[Union[str, int]]
    percent: Optional[bool]

class Relict(BaseModel):
    id: Optional[str]
    name: Optional[str]
    set_id: Optional[str]
    set_name: Optional[str]
    rarity: Optional[int]
    level: Optional[int]
    icon: Optional[str]
    main_affix: Optional[MainAffix]
    sub_affix: Optional[List[SubAffix]]

class Score(BaseModel):
    score: Optional[float]
    rank: Optional[str]
    eff: Optional[int]
    cv: Optional[float]

class RelictData(BaseModel):
    card: Image.Image
    score: Optional[Score]
    relict: Optional[Relict]
    position: Optional[int]
    class Config:
        arbitrary_types_allowed = True


class StarRailRelict(BaseModel):
    uid: Optional[int]
    card: Image.Image 
    charter_id: Optional[int]
    relict: Optional[List[RelictData]]

    class Config:
        arbitrary_types_allowed = True
