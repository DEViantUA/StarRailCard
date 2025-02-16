import math
from pathlib import Path
from copy import deepcopy

from ..tools.json_data import JsonManager
from ..tools.enums import PathData

CHARACTERS_LINK_ICON = "icon/{catalog}/{character_id}.png"
CHARACTERS_LINK_IMAGE = "image/{catalog}/{character_id}.png"
ENKA_INDEX = Path(__file__).parent / "assets" / "enka_api" / "index"
ENKA = Path(__file__).parent.parent / "assets" / "enka_api"

field = {
    "BaseHP": "hp",
    "BaseAttack": "atk",
    "BaseDefence": "def",
}


class AssetEnkaParsed:
    def __init__(self, data) -> None:
        self.data = data
        self.lang = "en"
    
    async def load_assets(self):
        self.character = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "characters.json").read()
        self.element = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "elements.json").read()
        self.path =  await JsonManager(PathData.ENKA_INDEX.value / self.lang / "paths.json").read()
        self.character_rank = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "character_ranks.json").read()
        self.character_promotions = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "character_promotions.json").read()
        self.skill = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "character_skills.json").read()
        self.skill_trees_info = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "character_skill_trees.json").read()
        self.light_cone = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "light_cones.json").read()
        self.propertie = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "properties.json").read()
        self.light_cone_rank = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "light_cone_ranks.json").read()
        self.relics = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "relics.json").read()
        self.relics_set = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "relic_sets.json").read()
        self.relic_main_affixes = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "relic_main_affixes.json").read()
        self.relic_sub_affixes = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "relic_sub_affixes.json").read()
        self.relic_set = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "relic_sets.json").read()
        self.light_cone_promotion = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "light_cone_promotions.json").read()
        self.avatar = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "avatars.json").read()
    
    async def collect(self, build = False):
        await self.load_assets()
        if build:
            charters = []
            for key in self.data["detailInfo"]["avatarDetailList"]:
                for k in key:
                    if isinstance(key[k], list):
                        for data in key[k]:
                            buildInfo = {
                                "id": data.get("id", 0),
                                "name_build": data.get("name", ""),
                            }
                            charters.append(await self.get_character(data["avatar_data"], buildInfo))
                    else:
                        buildInfo = {
                                "id": key[k].get("id", 0),
                                "name_build": key[k].get("name", ""),
                            }
                        charters.append(await self.get_character(key[k], buildInfo))
        else:
            charters = [await self.get_character(key) for key in self.data["detailInfo"]["avatarDetailList"]]
            
        data = {
            "player": await self.get_player(),
            "characters": charters
        }
        
        return data
    
    async def get_memory_data(self):
        data = self.data["detailInfo"]["recordInfo"]["challengeInfo"]
        return {
            "chaos_id": data.get("scheduleGroupId", 0),
            "chaos_level": data.get("scheduleMaxLevel", 0),
            "abyss_level": data.get("abyssLevel", 0),
            "abyss_star_count": data.get("abyssStarCount", 0),
        }
        pass
    
    async def get_space_info(self):
        data = self.data["detailInfo"]["recordInfo"]
        return {
            "relic_count": data.get("relicCount", 0),
            "music_count": data.get("musicCount", 0),
            "book_count": data.get("bookCount", 0),
            "universe_level": data["maxRogueChallengeScore"],
            "light_cone_count": data["equipmentCount"],
            "avatar_count": data["avatarCount"],
            "achievement_count": data["achievementCount"],
            "memory_data": await self.get_memory_data()
        }
    async def get_avatar_info(self, avatar_id):
        if str(avatar_id) not in self.avatar:
            return None
        return {
            "id": avatar_id,
            "name": self.avatar[avatar_id]["name"],
            "icon": self.avatar[avatar_id]["icon"]
        }
    async def get_player(self):

        return {
            "uid": self.data["detailInfo"]["uid"],
            "nickname": self.data["detailInfo"]["nickname"],
            "level": self.data["detailInfo"]["level"],
            "world_level": self.data["detailInfo"]["worldLevel"],
            "friend_count": self.data["detailInfo"]["friendCount"],
            "avatar": await self.get_avatar_info(str(self.data["detailInfo"]["headIcon"])),
            "signature": self.data["detailInfo"].get("signature", ""),
            "is_display": self.data["detailInfo"]["isDisplayAvatar"],
            "space_info": await self.get_space_info()
            
            
        }
    
    async def get_light_cone(self, data):
        info = self.light_cone.get(str(data.get("tid")))
        
        id = str(data.get("tid"))
        name = info.get("name")
        rarity = info.get("rarity")
        rank = data.get("rank")
        level = data.get("level")
        promotion = data.get("promotion", 0)
        icon = info.get("icon")
        preview = info.get("preview")
        portrait = info.get("portrait")
        path = await self.get_path(info.get("path"))
        attributes = await self.get_light_cone_attribute_from_promotion(id, promotion, level)
        properties = await self.get_light_cone_property_from_rank(id, rank)
        
        return {
            "id": id,
            "name": name,
            "rarity": rarity,
            "rank": rank,
            "level": level,
            "promotion": promotion,
            "icon": icon,
            "preview": preview,
            "portrait": portrait,
            "path": path,
            "attributes": attributes,
            "properties": properties,
        }
    
    async def get_light_cone_property_from_rank(self, id: str, rank: int):
        if id not in self.light_cone_rank:
            return []
        if rank not in range(1, 5 + 1):
            return []
        properties = []
        
        for i in self.light_cone_rank[id]["properties"][rank - 1]:
            if i["type"] not in self.propertie:
                continue
            property = self.propertie[i["type"]]
            properties.append(
                {
                    "type": i["type"],
                    "field": property["field"],
                    "name": property["name"],
                    "icon": property["icon"],
                    "value": i["value"],
                    "display": await self.get_display(i["value"], property["percent"]),
                    "percent": property["percent"],
                }
            )
        return properties
    
    async def get_light_cone_attribute_from_promotion(self, id: str, promotion: int, level: int):
        if id not in self.light_cone_promotion:
            return []
        if promotion not in range(0, 6 + 1):  # 0-6
            return []
        if level not in range(1, 80 + 1):  # 1-80
            return []
        attributes = []
        for k, v in self.light_cone_promotion[id]["values"][promotion].items():
            property = None
            for i in self.propertie.values():
                if i["field"] == k:
                    property = i
                    break
            if property is None:
                continue
            attributes.append(
                {
                    "field": k,
                    "name": property["name"],
                    "icon": property["icon"],
                    "value": v["base"] + v["step"] * (level - 1),
                    "display": await self.get_display(v["base"] + v["step"] * (level - 1), property["percent"]),
                    "percent": property["percent"],
                }
            )
        return attributes
    
    async def get_character(self, data, build = {}):
        id = str(data.get("avatarId"))
        name = self.character.get(str(id)).get("name")
        if "{NICKNAME}" in name:
            name = "Trailblazer"
        rarity = self.character.get(str(id)).get("rarity")
        rank = data.get("rank", 0)
        level = data.get("level")
        promotion = data.get("promotion", 0)
        icon = self.character.get(str(id)).get("icon")
        preview = self.character.get(str(id)).get("preview")
        portrait = self.character.get(str(id)).get("portrait")
        rank_icons = [await self.get_rank_icons(key) for key in self.character.get(str(id)).get("ranks")]
        path = await self.get_path(self.character.get(str(id)).get("path"))
        element = await self.get_element(self.character.get(str(id)).get("element"))
        skills = await self.get_skill(data, str(id), self.character.get(str(id)).get("element"))
        skill_trees = await self.get_skill_trees(data, str(id), rank)
        light_cone = await self.get_light_cone(data.get("equipment")) if data.get("equipment") else None
        attributes = await self.get_attributes(str(id), promotion, level)
        properties = await self.get_properties(str(id), data["skillTreeList"])
                
        relic_infos = [await self.get_relic_info(relic) for relic in data.get("relicList", [])]
        relics = [
            relic_info for relic_info in relic_infos if relic_info is not None
        ]
        relic_sets = await self.get_relic_sets_info(relics) if relics else []
        
        attributes = await self.merge_attribute(
            [
                attributes,
                light_cone["attributes"] if light_cone else [],
            ]
        )

        
        relic_properties = []
        for relic in relics:
            if relic["main_affix"]:
                relic_properties.append(relic["main_affix"])
            relic_properties += [
                {
                    "type": affix["type"],
                    "field": affix["field"],
                    "name": affix["name"],
                    "icon": affix["icon"],
                    "value": affix["value"],
                    "display": affix["display"],
                    "percent": affix["percent"],
                } for affix in relic.get("sub_affix", [])
            ]

        for relic_set in relic_sets:
            relic_properties += relic_set["properties"]
                
        properties = await self.merge_property(
            [
                properties,
                light_cone["properties"] if light_cone else [],
                relic_properties,
            ]
        )
        
        additions = await self.get_additions(attributes, properties)        
      
        return {
            "id": id,
            "name": name,
            "rarity": rarity,
            "rank": rank,
            "level": level,
            "promotion": promotion,
            "icon": icon,
            "preview": preview,
            "portrait": portrait,
            "rank_icons": rank_icons,
            "path": path,
            "element": element,
            "skills": skills,
            "skill_trees": skill_trees,
            "light_cone": light_cone,
            
            "relics": relics,
            "relic_sets": relic_sets,
            "attributes": attributes,
            "additions": additions,
            "properties": properties,
            "build": build,
            "pos": [data.get("pos", 0)],
        }
        
    async def get_additions(self, attributes, properties):
        attribute_dict = {}
        addition_dict = {}
        for attribute in attributes:
            if not attribute["field"]  in addition_dict:
                attribute_dict[attribute["field"]] = attribute["value"]
        for property in properties:
            if (
                self.propertie[property["type"]]["ratio"]
                and property["field"] in attribute_dict
            ):
                value = property["value"] * attribute_dict[property["field"]]
            else:
                value = property["value"]
            if property["field"] not in addition_dict:
                addition_dict[property["field"]] = value
            else:
                addition_dict[property["field"]] += value
        additions = []
        for k, v in addition_dict.items():
            property = None
            for i in self.propertie.values():
                if i["field"] == k:
                    property = i
                    break
                
            if property is None:
                continue
            
            additions.append(
                {
                    "field": k,
                    "name": property["name"],
                    "icon": property["icon"],
                    "value": v,
                    "display": await self.get_display(v, property["percent"]),
                    "percent": property["percent"],
                }
            )
            
        return additions
    
    async def get_attributes(self, character_id, promotion, level):
        
        if character_id not in self.character_promotions:
            return []
        if promotion not in range(0, 6 + 1):  # 0-6
            return []
        if level not in range(1, 80 + 1):  # 1-80
            return []
        attributes = []
        for k, v in self.character_promotions[character_id]["values"][promotion].items():
            property = None
            for i in self.propertie.values():
                if i["field"] == k:
                    property = i
                    break
            if property is None:
                continue
            
            attributes.append(
                {
                    "field": k,
                    "name": property["name"],
                    "icon": property["icon"],
                    "value": v["base"] + v["step"] * (level - 1),
                    "display": await self.get_display(v["base"] + v["step"] * (level - 1), property["percent"]),
                    "percent": property["percent"]
                }
            )
        return attributes
    
    async def get_properties(self, characters_id, info):
        skill_trees = self.character[characters_id]["skill_trees"]
        properties = []
        
        for skill_tree in info:
            pointId = str(skill_tree["pointId"])
            if pointId in skill_trees and pointId in self.skill_trees_info:
                property_list = (self.skill_trees_info[pointId]["levels"][skill_tree["level"] - 1]["properties"])
                for i in property_list:
                    if self.propertie.get(i.get("type")) is None or i["value"] <= 0:
                        continue
                    property = self.propertie[i["type"]]             
                    properties.append(
                        {
                            "type": i["type"],
                            "field": property["field"],
                            "name": property["name"],
                            "icon": property["icon"],
                            "value": i["value"],
                            "display": await self.get_display( i["value"], property["percent"]),
                            "percent": property["percent"],
                            "type": i["type"],
                        }
                    )
        return properties
    
    async def get_skill_trees(self, data, character_id, rank):
        infos = []
        for key in self.character[character_id]["skill_trees"]:
            active = False
            for keys in data["skillTreeList"]:
                if str(keys["pointId"]) == key:
                    active = True
                    break
                
            infos.append(
                {
                    "id": str(key),
                    "level": 1 if active else 0,
                    "anchor": self.skill_trees_info.get(str(key))["anchor"],
                    "icon": self.skill_trees_info.get(str(key))["icon"],
                    "max_level": await self.get_max_level(self.character.get(character_id)["ranks"], str(key), rank),
                    "parent": await self.get_parent(int(key))
                }

            )
        
        return infos
    
    async def get_skill(self, data, character_data, element):

        character_data = self.character.get(character_data)
        
        response= []
        
        for keys in data["skillTreeList"]:
            pointId = str(keys["pointId"])
            if self.skill_trees_info.get(pointId)["level_up_skills"] == []:
                continue
            
            skills_info_id = str(self.skill_trees_info.get(pointId)["level_up_skills"][0]["id"])
            
            if not str(skills_info_id) in character_data["skills"]:
                continue
            
            info = self.skill.get(skills_info_id)
            
            max_level = self.skill_trees_info.get(pointId)["max_level"]
            if keys["level"] > max_level:
                max_level = info["max_level"]

            response.append(
                {
                    "id": skills_info_id,
                    "name": info["name"],
                    "level": keys["level"],
                    "max_level": max_level,
                    "element": await self.get_element(element),
                    "type": info["type"],
                    "type_text": info["type_text"],
                    "effect": info["effect"],
                    "effect_text": info["effect_text"],
                    "simple_desc": info["simple_desc"],
                    "desc": info["desc"],
                    "icon": info["icon"],
                }
            )
            
        return response
                
    async def get_relic_info(self, data):
        if str(data["tid"]) not in self.relics:
            return None
        
        relics_info = self.relics.get(str(data["tid"]))
        
        info = {
                "id": str(data["tid"]),
                "name": relics_info["name"],
                "set_id": str(data["_flat"]["setID"]),
                "set_name": self.relics_set[relics_info["set_id"]]["name"],
                "rarity": relics_info["rarity"],
                "level": data.get("level", 0),
                "icon": relics_info['icon'],
                "main_affix": await self.get_relic_main_affix(str(data["tid"]), data.get("level", 0), str(data["mainAffixId"])),
                "sub_affix": await self.get_relic_sub_affix(str(data["tid"]), data["subAffixList"])
                }

        return info
    
    async def get_relic_sub_affix(self, relict_id, sub_affix_info):
        if relict_id not in self.relics:
            return []
        
        sub_affix_group = self.relics[relict_id]["sub_affix_id"]
        if sub_affix_group not in self.relic_sub_affixes:
            return []
        
        properties = []
        for sub_affix in sub_affix_info:
            if str(sub_affix["affixId"]) not in self.relic_sub_affixes[sub_affix_group]["affixes"]:
                continue
            affix = self.relic_sub_affixes[sub_affix_group]["affixes"][str(sub_affix["affixId"]) ]

            property = self.propertie[affix["property"]]
            
            properties.append(
                {
                    "type": affix["property"],
                    "field": property["field"],
                    "name": property["name"],
                    "icon": property["icon"],
                    "value": affix["base"] * sub_affix["cnt"] + affix["step"] * sub_affix.get("step", 0),
                    "display":  await self.get_display(affix["base"] * sub_affix["cnt"] + affix["step"] * sub_affix.get("step", 0), property["percent"]),
                    "percent": property["percent"],
                    "count": sub_affix["cnt"],
                    "step": sub_affix.get("step", 0)
                }
            )
        return properties
    
    async def get_relic_main_affix(self, relict_id, level, main_affix_id):
        if str(relict_id) not in self.relics:
            return None
        if not main_affix_id:
            return None
        
        main_affix_group = self.relics[str(relict_id)]["main_affix_id"]            
            
        if main_affix_group not in self.relic_main_affixes or main_affix_id not in self.relic_main_affixes[main_affix_group]["affixes"]:
            return None
        
        affix = self.relic_main_affixes[main_affix_group]["affixes"][main_affix_id]
        
        property = self.propertie[affix["property"]]
          
        return {
                "type": affix["property"],
                "field": property["field"],
                "name": property["name"],
                "icon": property["icon"],
                "value":affix["base"] + + affix["step"] * level,
                "display": await self.get_display(affix["base"] + + affix["step"] * level, property["percent"]),
                "percent": property["percent"]
            }  
    
    async def get_relic_sets_info(self, data):
        set_num = {}
        for relic in data:
            if relic["set_id"] not in set_num:
                set_num[relic["set_id"]] = 1
            else:
                set_num[relic["set_id"]] += 1
                
        relic_sets = []
        for k, v in set_num.items():
            info = self.relic_set[str(k)]
            if v >= 2:
                prop = [{
                    "type": i["type"],
                    "field": self.propertie.get(i["type"])["field"],
                    "name": self.propertie.get(i["type"])["name"],
                    "icon": self.propertie.get(i["type"])["icon"],
                    "value": i["value"],
                    "display": await self.get_display(i["value"], self.propertie.get(i["type"])["percent"]),
                    "percent": self.propertie.get(i["type"])["percent"],
                } for i in info["properties"][0]]
                
                relic_sets.append(
                    {
                        "id": k,
                        "name": info["name"],
                        "icon": info["icon"],
                        "num": 2,
                        "desc": info["desc"][0],
                        "properties": prop,
                    }
                )
            if v >= 4:
                prop = [
                    {
                        "type": i["type"],
                        "field": self.propertie.get(i["type"])["field"],
                        "name": self.propertie.get(i["type"])["name"],
                        "icon": self.propertie.get(i["type"])["icon"],
                        "value": i["value"],
                        "display": await self.get_display(i["value"], self.propertie.get(i["type"])["percent"]),
                        "percent": self.propertie.get(i["type"])["percent"],
                    } for i in info["properties"][1] if len(info["properties"]) > 1
                ]

                relic_sets.append(
                    {
                        "id": k,
                        "name": info["name"],
                        "icon": info["icon"],
                        "num": 4,
                        "desc": info["desc"][1] if len(info["desc"]) > 1 else "",
                        "properties": prop,
                    }
                )
        return relic_sets
    
    async def merge_property(self, properties):
        property_dict = {}
        for property_list in properties:
            for property in property_list:
                if isinstance(property, list):
                    if len(property) == 0:
                        continue
                    property = property[0]

                if property["type"] not in property_dict:
                    property_dict[property["type"]] = {}
                    property_dict[property["type"]]["value"] = property["value"]
                    property_dict[property["type"]]["origin"] = deepcopy(property)
                else:
                    property_dict[property["type"]]["value"] += property["value"]
        property_res = []
        
        for v in property_dict.values():
            
            info = v["origin"]
            info["value"] = v["value"]
            info["display"] = await self.get_display(v["value"], info["percent"])

            property_res.append(info)
        return property_res
    
    async def merge_attribute(self, attributes):
        attribute_dict = {}
        for attribute_list in attributes:
            for attribute in attribute_list:
                if attribute["field"] not in attribute_dict:
                    attribute_dict[attribute["field"]] = {}
                    attribute_dict[attribute["field"]]["value"] = attribute["value"] 
                    attribute_dict[attribute["field"]]["origin"] = deepcopy(attribute)
                else:
                    attribute_dict[attribute["field"]]["value"] += attribute["value"] 
        attribute_res = []
        for v in attribute_dict.values():
            attribute_info = v["origin"]
            attribute_info["value"] = v["value"]
            attribute_info["display"] = await self.get_display(
                v["value"], attribute_info["percent"]
            )
            attribute_res.append(attribute_info)
            
        return attribute_res
    
    async def get_parent(self, skill_id):
        parent = self.skill_trees_info.get(str(skill_id)).get("pre_points")
        if parent == []:
            return None
        else:
            return parent[0]   
         
    async def get_rank_icons(self, rank_id):
        return self.character_rank.get(rank_id).get("icon")
    
    async def get_path(self, path):
        return {"id": self.path.get(path)["id"], "name": self.path.get(path)["name"], "icon": self.path.get(path)["icon"]}

    async def get_element(self, element):
        return {"id": self.element.get(element)["id"], "name": self.element.get(element)["name"], "color": self.element.get(element)["color"], "icon": self.element.get(element)["icon"]}
    
    async def get_max_level(self, ranks_list,skill_id,rank):
        
        skill_trees_info = self.skill_trees_info.get(skill_id)
        
        max_level = skill_trees_info["max_level"]
        if skill_trees_info.get("level_up_skills", []) != []:
            if int(skill_trees_info.get("level_up_skills")[0]["id"]) in ranks_list[:rank]:
                max_level = self.skill[skill_trees_info.get("level_up_skills")[0]["id"]]["max_level"]

        return max_level
    
    async def get_display(self, value, percent):
        if percent:
            return format(math.floor(value * 1000) / 10.0, ".1f") + "%"
        else:
            return f"{math.floor(value)}"