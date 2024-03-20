# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from pydantic import BaseModel
from typing import List, Optional,Final

from ..tools.ukrainization import TranslateDataManager

UA_LANG = False
MAIN_LINK: Final[str] = "https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{icon}"


def hex_to_rgba(hex_code):
    hex_code = hex_code.strip('#')
    
    red = int(hex_code[0:2], 16)
    green = int(hex_code[2:4], 16)
    blue = int(hex_code[4:6], 16)
    
    alpha = 255 
    
    return red, green, blue, alpha

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
        self.icon = MAIN_LINK.format(icon = self.icon)
    
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

class RelicMainAffix(BaseModel):
    type: Optional[str]
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: float
    display: Optional[str]
    percent: bool
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = MAIN_LINK.format(icon = self.icon)
    
        if UA_LANG:
            self.name = TranslateDataManager._data.stats.get(self.type, self.name)

class RelicSubAffix(BaseModel):
    type: Optional[str]
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: float
    display: Optional[str]
    percent: bool
    count: int
    step: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = MAIN_LINK.format(icon = self.icon)
    
        if UA_LANG:
            self.name = TranslateDataManager._data.stats.get(self.type, self.name)
            
class Relic(BaseModel):
    id: Optional[str]
    name: Optional[str]
    set_id: Optional[str]
    set_name: Optional[str]
    rarity: int
    level: int
    icon: Optional[str]
    main_affix: RelicMainAffix
    sub_affix: List[RelicSubAffix]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = MAIN_LINK.format(icon = self.icon)
    
        if UA_LANG:
            self.set_name = TranslateDataManager._data.relict_sets.get(self.set_id, self.set_name)
            
class RelicSetProperties(BaseModel):
    type: Optional[str]
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: float
    display: Optional[str]
    percent: bool
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = MAIN_LINK.format(icon = self.icon)
    
        if UA_LANG:
            self.name = TranslateDataManager._data.stats.get(self.type, self.name)

class RelicSet(BaseModel):
    id: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    num: int
    desc: Optional[str]
    properties: List[RelicSetProperties]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = MAIN_LINK.format(icon = self.icon)
    
        if UA_LANG:
            self.name = TranslateDataManager._data.relict_sets.get(self.id, self.name)
            
class LightConeAttributes(BaseModel):
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: float
    display: Optional[str]
    percent: bool
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = MAIN_LINK.format(icon = self.icon)
    
        if UA_LANG:
            self.name = TranslateDataManager._data.stats.get(self.field, self.name)

class Path(BaseModel):
    id: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = MAIN_LINK.format(icon = self.icon)
    
        if UA_LANG:
            self.name = TranslateDataManager._data.paths.get(self.id, self.name)

class LightCone(BaseModel):
    id: Optional[str]
    name: Optional[str]
    rarity: int
    rank: int
    level: int
    promotion: int
    icon: Optional[str]
    preview: Optional[str]
    portrait: Optional[str]
    path: Path
    attributes: List[LightConeAttributes]
    properties: List[LightConeAttributes]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = MAIN_LINK.format(icon = self.icon)
        self.preview = MAIN_LINK.format(icon = self.preview)
        self.portrait = MAIN_LINK.format(icon = self.portrait)
    
        if UA_LANG:
            self.name = TranslateDataManager._data.weapons.get(self.id, self.name)
            
class ColorElement(BaseModel):
    hex: Optional[str]
    rgba: Optional[tuple]
     
class Element(BaseModel):
    id: Optional[str]
    name: Optional[str]
    color: Optional[str]
    icon: Optional[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = MAIN_LINK.format(icon = self.icon)
        self.color = ColorElement(hex = self.color, rgba = hex_to_rgba(self.color))
        
        if UA_LANG:
            self.name = TranslateDataManager._data.element.get(self.id, self.name)
               
class Skill(BaseModel):
    id: Optional[str]
    name: Optional[str]
    level: int
    max_level: int
    element: Optional[Element]
    type: Optional[str]
    type_text: Optional[str]
    effect: Optional[str]
    effect_text: Optional[str]
    simple_desc: Optional[str]
    desc: Optional[str]
    icon: Optional[str]
    
class SkillTree(BaseModel):
    id: Optional[str]
    level: int
    anchor: Optional[str]
    max_level: int
    icon: Optional[str]
    parent: Optional[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = MAIN_LINK.format(icon = self.icon)
        
class CharacterAttributes(BaseModel):
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: float
    display: Optional[str]
    percent: bool
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = MAIN_LINK.format(icon = self.icon)

        if UA_LANG:
            self.name = TranslateDataManager._data.stats.get(self.field, self.name)
            
class Character(BaseModel):
    id: Optional[str]
    name: Optional[str]
    rarity: int
    rank: int
    level: int
    promotion: int
    icon: Optional[str]
    preview: Optional[str]
    portrait: Optional[str]
    rank_icons: list
    path: Path
    element: Optional[Element]
    skills: List[Skill]
    skill_trees: List[SkillTree]
    light_cone: Optional[LightCone]
    relics: Optional[List[Relic]]
    relic_sets: Optional[List[RelicSet]]
    attributes: List[CharacterAttributes]
    additions: List[CharacterAttributes]
    properties: List[CharacterAttributes]
    pos: list
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = MAIN_LINK.format(icon = self.icon)
        self.preview = MAIN_LINK.format(icon = self.preview)
        self.portrait = MAIN_LINK.format(icon = self.portrait)
        self.pos = self.pos[0]
        new_rank_icons = []
        for key in self.rank_icons:
            new_rank_icons.append(MAIN_LINK.format(icon = key))
        self.rank_icons = new_rank_icons
        
        if UA_LANG:
            self.name = TranslateDataManager._data.avatar.get(self.id, self.name)
    
class MiHoMoApi(BaseModel):
    player: Player
    characters: List[Character]
