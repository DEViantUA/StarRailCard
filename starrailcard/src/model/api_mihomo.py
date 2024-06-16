# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from typing import Final, List, Optional, Union

from pydantic import BaseModel, Field

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
    chaos_id: Optional[int]
    chaos_level: Optional[int]
    abyss_level: Optional[int] =  Field(0, alias= "abyssLevel")
    abyss_star_count: Optional[int] =  Field(0, alias= "abyssStarCount")
    
    class Config:
        populate_by_name = True
    
class SpaceInfo(BaseModel):
    relic_count: Optional[int] =  Field(0, alias= "relicCount")
    music_count: Optional[int] =  Field(0, alias= "musicCount")
    book_count: Optional[int] =  Field(0, alias= "bookCount")
    memory_data: Optional[MemoryInfo]
    universe_level: Optional[int]
    light_cone_count: Optional[int]
    avatar_count: Optional[int]
    achievement_count: Optional[int]

    class Config:
        populate_by_name = True
        
class Avatar(BaseModel):
    id: str
    name: str
    icon: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if UA_LANG:
            self.name = TranslateDataManager._data.avatar.get(self.id, self.name)
        
class Player(BaseModel):
    uid: Optional[Union[str,int]]
    nickname: Optional[str]
    level: int
    world_level: int
    friend_count: int
    avatar: Avatar
    signature: Optional[str]
    is_display: Optional[bool]
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
    
        if UA_LANG:
            self.name = TranslateDataManager._data.stats.get(self.type, self.name)

class RelicSet(BaseModel):
    id: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    num: int
    desc: Optional[str]
    properties: List[RelicSetProperties] = Field([], alias="properties")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
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

        if UA_LANG:
            self.name = TranslateDataManager._data.stats.get(self.field, self.name)

class Path(BaseModel):
    id: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
        if UA_LANG:
            self.name = TranslateDataManager._data.paths.get(self.id, self.name)

class LightCone(BaseModel):
    id: Optional[str]
    name: Optional[str]
    rarity: int
    rank: int
    level: int
    promotion: int = 0
    icon: Optional[str]
    preview: Optional[str]
    portrait: Optional[str]
    path: Path
    attributes: List[LightConeAttributes]
    properties: Optional[List[LightConeAttributes]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        
class CharacterAttributes(BaseModel):
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: float
    display: Optional[str]
    percent: bool
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if UA_LANG:
            self.name = TranslateDataManager._data.stats.get(self.field, self.name)
            
class CharacterProperties(BaseModel):
    type: Optional[str]
    field: Optional[str]
    name: Optional[str]
    icon: Optional[str]
    value: float
    display: Optional[str]
    percent: bool
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
    relic_sets: Optional[List[RelicSet]] = Field([], alias="relic_sets")
    attributes: List[CharacterAttributes]
    additions: List[CharacterAttributes]
    properties: Optional[List[CharacterProperties]]
    build: Optional[dict] = Field(None)
    pos: list
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        if UA_LANG:
            self.name = TranslateDataManager._data.avatar.get(self.id, self.name)
    
class MiHoMoApi(BaseModel):
    player: Player
    characters: List[Character]
    dont_update_link: Optional[bool] = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.dont_update_link:
            self.player.avatar.icon = MAIN_LINK.format(icon = self.player.avatar.icon)
            for character in self.characters:
                character.icon = MAIN_LINK.format(icon=character.icon)
                character.preview = MAIN_LINK.format(icon=character.preview)
                character.portrait = MAIN_LINK.format(icon=character.portrait)
                character.rank_icons = [MAIN_LINK.format(icon=icon) for icon in character.rank_icons]

                if character.light_cone:
                    character.light_cone.icon = MAIN_LINK.format(icon=character.light_cone.icon)
                    character.light_cone.preview = MAIN_LINK.format(icon=character.light_cone.preview)
                    character.light_cone.portrait = MAIN_LINK.format(icon=character.light_cone.portrait)

                for relic in character.relics:
                    relic.icon = MAIN_LINK.format(icon=relic.icon)
                    for sub_affix in relic.sub_affix:
                        sub_affix.icon = MAIN_LINK.format(icon=sub_affix.icon)
                    relic.main_affix.icon = MAIN_LINK.format(icon=relic.main_affix.icon)

                for relic_set in character.relic_sets:
                    relic_set.icon = MAIN_LINK.format(icon=relic_set.icon)
                    for property in relic_set.properties:
                        property.icon = MAIN_LINK.format(icon=property.icon)

                for skill in character.skills:
                    if skill.icon:
                        skill.icon = MAIN_LINK.format(icon=skill.icon)

                for skill_tree in character.skill_trees:
                    if skill_tree.icon:
                        skill_tree.icon = MAIN_LINK.format(icon=skill_tree.icon)

                for attribute in character.attributes:
                    attribute.icon = MAIN_LINK.format(icon=attribute.icon)

                
                for addition in character.additions:
                    addition.icon = MAIN_LINK.format(icon=addition.icon)

                if character.properties:
                    for property in character.properties:
                        property.icon = MAIN_LINK.format(icon=property.icon)

                character.element.icon = MAIN_LINK.format(icon = character.element.icon)

                for skills in character.skills:
                    if "icon" in skills:
                        skills = MAIN_LINK.format(icon = skills)

                character.path.icon = MAIN_LINK.format(icon=character.path.icon)

                
                
                if not character.light_cone is None:
                    for light_cone_attr in character.light_cone.attributes:
                        light_cone_attr.icon = MAIN_LINK.format(icon=light_cone_attr.icon)
                        
                    if character.light_cone.properties:
                        for property in character.light_cone.properties:
                            property.icon = MAIN_LINK.format(icon=property.icon)

