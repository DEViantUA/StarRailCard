from ..tools.json_data import JsonManager
from ..tools.enums import PathData
import json

_DEFFAULT_ASSETS_LINK = "https://enka.network/ui/hsr/"

_DEFFAULT_ASSETS_HSR_LINK = "https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/{catalog}/{key}.png"
_DEFFAULT_ASSETS_HSR_LINK_SKILL = "https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/"


fiel = {
    "BaseHP": "hp",
    "BaseAttack": "atk",
    "BaseDefence": "def",
}

proc = {
    "false": False,
    'true': True
}

class AssetEnkaParsed:
    def __init__(self, data: dict, lang: str = "en") -> None:
        self.data = data["detailInfo"]
        self.lang = lang
       
    async def creat_player(self):
        avatar_link = await AssetEnkaParsed.get_icon_avatar(self.data["headIcon"])
        self.player = {
            "uid": 0,#self.data["uid"],
            "nickname": self.data["nickname"],
            "level": self.data["level"],
            "is_display": self.data["isDisplayAvatar"],
            "avatar": {"id": str(self.data["headIcon"]), "name": avatar_link.split("/")[-1:][0], "icon": _DEFFAULT_ASSETS_LINK + avatar_link},
            "signature": self.data["signature"],
            "friend_count": self.data["friendCount"],
            "world_level": self.data["worldLevel"],
            "space_info": {
                "pass_area_progress": self.data["recordInfo"]["challengeInfo"]["scheduleMaxLevel"],
                "light_cone_count": self.data["recordInfo"]["equipmentCount"],
                "avatar_count": self.data["recordInfo"]["avatarCount"],
                "achievement_count": self.data["recordInfo"]["achievementCount"],
            }
        }
        
    
    async def creat_avatar(self):
        self.charter = []
        for key in self.data["avatarDetailList"]:      
            charter_info = await AssetEnkaParsed.get_info_character(key["avatarId"],self.lang)
            path_info = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "paths.json").read()
            element_info = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "elements.json").read()
            skills_info = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "character_skills.json").read()
            skill_trees_info = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "character_skill_trees.json").read()
            character_ranks = await JsonManager(PathData.ENKA_INDEX.value / self.lang / "character_ranks.json").read()
            light_cone = await AssetEnkaParsed.add_light_cone(key,self.lang,path_info)
            relics = [await AssetEnkaParsed.add_relics(keys, self.lang) for keys in key["relicList"]]
            skill_trees = await AssetEnkaParsed.add_skill_trees(skill_trees_info,charter_info,skills_info,key)

            data = {
                "id": key["avatarId"],
                "name": charter_info["AvatarName"]["name"],
                "rarity": charter_info["Rarity"],
                "rank": key.get("rank",0),
                "level": key["level"],
                "promotion": key["promotion"],
                "icon": _DEFFAULT_ASSETS_HSR_LINK.format(catalog = "icon/avatar", key = key["avatarId"]),
                "preview": _DEFFAULT_ASSETS_HSR_LINK.format(catalog = "image/character_preview", key = key["avatarId"]),
                "portrait": _DEFFAULT_ASSETS_HSR_LINK.format(catalog = "image/character_portrait", key = key["avatarId"]),
                "path": await AssetEnkaParsed.get_path(path_info,charter_info),
                "rank_icons": [_DEFFAULT_ASSETS_HSR_LINK_SKILL + character_ranks.get(str(key))["icon"] for key in charter_info["RankIDList"]],
                "element":  await AssetEnkaParsed.get_element(element_info,charter_info["Element"]),
                "skills": await AssetEnkaParsed.add_skills(element_info,charter_info,key, self.lang),
                "skill_trees": skill_trees,
                "light_cone": light_cone if light_cone != {} else None,
                "relics": relics,
                "relic_sets": await AssetEnkaParsed.add_relict_sets(key["relicList"], self.lang),
                "additions": await AssetEnkaParsed.add_additions(key, self.lang, light_cone.get("attributes",[])),
                "attributes": await AssetEnkaParsed.add_attributes(relics, skill_trees, self.lang),
                "properties": None, #await AssetEnkaParsed.add_properties(key["skillTreeList"], self.lang),
                "pos": [key.get("pos", 0)]
            }
            
            self.charter.append(data)
        
        
    
    async def collect(self):
        await self.creat_player()
        await self.creat_avatar()

        await JsonManager(PathData.ENKA.value / "TEST_API.json").write(self.charter)
        
        return {"player": self.player, "characters":self.charter}
    '''
    @classmethod
    async def add_properties(cls, skillTreeList, lang):
        property = await JsonManager(PathData.ENKA_INDEX.value / lang / "properties.json").read()
        skill_trees_info = await JsonManager(PathData.ENKA_INDEX.value / lang / "character_skill_trees.json").read()
    '''
    
    @classmethod
    async def add_attributes(cls, relict, skill, lang):
        skill_trees_info = await JsonManager(PathData.ENKA_INDEX.value / lang / "character_skill_trees.json").read()
        property = await JsonManager(PathData.ENKA_INDEX.value / lang / "properties.json").read()
        
        data = {}          
        
        for key in relict:
            if not key["main_affix"]["field"] in data:
                data[key["main_affix"]["field"]] = {
                    "field": key["main_affix"]["field"],
                    "name": key["main_affix"]["name"],
                    "icon": key["main_affix"]["icon"],
                    "value": key["main_affix"]["value"],
                    "display": AssetEnkaParsed.get_display(key["main_affix"]["value"], key["main_affix"]["percent"]),
                    "percent": key["main_affix"]["percent"]
                    }
            else:
                data[key["main_affix"]["field"]]["value"] += key["main_affix"]["value"]
                data[key["main_affix"]["field"]]["display"] = AssetEnkaParsed.get_display(data[key["main_affix"]["field"]]["value"], key["main_affix"]["percent"])
            
            for keys in key["sub_affix"]:
                if not keys["field"] in data:
                    data[keys["field"]] = {
                        "field": keys["field"],
                        "name": keys["name"],
                        "icon": keys["icon"],
                        "value": keys["value"],
                        "display": AssetEnkaParsed.get_display(keys["value"], keys["percent"]),
                        "percent": keys["percent"]
                        }
                else:
                    
                    data[keys["field"]]["value"] += keys["value"]
                    data[keys["field"]]["display"] = AssetEnkaParsed.get_display(data[keys["field"]]["value"], keys["percent"])
            
        for key in skill:
            info = skill_trees_info.get(str(key["id"]))["levels"]
            if info == []:
                continue
            info = info[0]["properties"]
            if info == []:
                continue
            info = info[0]
            
            property_info = property.get(info["type"])
            
            if not property_info["field"] in data:
                data[property_info["field"]] = {
                    "field": property_info["field"],
                    "name": property_info["name"],
                    "icon": property_info["icon"],
                    "value": info["value"],
                    "display": AssetEnkaParsed.get_display(info["value"], property_info["percent"]),
                    "percent": property_info["percent"]
                    }
            else:
                
                data[property_info["field"]]["value"] += info["value"]
                data[property_info["field"]]["display"] = AssetEnkaParsed.get_display(data[property_info["field"]]["value"], property_info["percent"])
            
                
            
        return [data[key] for key in data]
    
    @classmethod
    async def add_additions(cls, data,lang, light_cone):
        promotion_id = data["promotion"]
        avatarId = data["avatarId"]
        level = data["level"] 
        
        if level > 1:
            level = data["level"]-1
        
        property = await JsonManager(PathData.ENKA_INDEX.value / lang / "properties.json").read()
        meta = await JsonManager(PathData.ENKA.value / "meta.json").read()
        meta = meta["avatar"].get(str(avatarId)).get(str(promotion_id))
        

        name = {
            "hp": "HPBase",
            "atk": "AttackBase",
            "def": "DefenceBase",
            "spd": "SpeedBase",
            "crit_rate": "CriticalChance",
            "crit_dmg": "CriticalDamage",
        }
        
        base = [
            {
               "field":"hp",
               "name":"BaseHP",
               "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL + "icon/property/IconMaxHP.png",
               "value": 0,
               "display": None,
               "percent": False
            },
            {
               "field":"atk",
               "name": "BaseAttack",
               "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL + "icon/property/IconAttack.png",
               "value": 0,
               "display": None,
               "percent": False
            },
            {
               "field":"def",
               "name": "BaseDefence",
               "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL + "icon/property/IconDefence.png",
               "value": 0,
               "display": None,
               "percent": False
            },
            {
               "field":"spd",
               "name": "SpeedDelta",
               "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL + "icon/property/IconSpeed.png",
               "value": 0,
               "display": None,
               "percent": False
            },
            {
               "field":"crit_rate",
               "name": "CriticalChanceBase",
               "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL + "icon/property/IconCriticalChance.png",
               "value":0.,
               "display": None,
               "percent": True
            },
            {
               "field":"crit_dmg",
               "name": "CriticalDamageBase",
               "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL + "icon/property/IconCriticalDamage.png",
               "value":0,
               "display": None,
               "percent": True
            }
         ]
        
        for key in base:
            name_meta = name.get(key["field"])
            key["name"] = property.get(key["name"])["name"]
            if not key["percent"]:
                if light_cone != []:
                    for keys in light_cone:
                        if key["field"] == keys["field"]:
                            key["value"] = meta[name_meta] + (meta.get(name_meta.replace("Base", "Add"), 0) * level) + keys["value"]
                else:
                    key["value"] = meta[name_meta] + (meta.get(name_meta.replace("Base", "Add"), 0) * level)
            else:
                key["value"] = meta[name_meta]
            key["display"] = AssetEnkaParsed.get_display(key["value"], key["percent"])
        
        return base
    
    @classmethod
    async def add_relict_sets(cls, data, lang):
        
        new_data = []
        sets_num = {}
        done = []
        data_relics = await JsonManager(PathData.ENKA.value / "relics.json").read()
        data_relics_sets = await JsonManager(PathData.ENKA_INDEX.value / lang / "relic_sets.json").read()
        
        for key in data:
            relics = data_relics.get(str(key["tid"]))
            if not relics["SetID"] in sets_num:
                sets_num[relics["SetID"]] = 1
            else:
                sets_num[relics["SetID"]] += 1
        
        property = await JsonManager(PathData.ENKA_INDEX.value / lang / "properties.json").read()
        
        for key in data:
            relics = data_relics.get(str(key["tid"]))
            if sets_num[relics["SetID"]] < 2 or relics["SetID"] in done:
                continue
            
            relics_sets = data_relics_sets.get(str(relics["SetID"]))

            index_desc = 0
            if sets_num[relics["SetID"]] >= 4:
                index_desc = 1
            
            properties = relics_sets["properties"][index_desc]
            if properties == []:
                properties = relics_sets["properties"][0]
            new_data.append({"id": str(relics["SetID"]),
                "name": relics_sets["name"],
                "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL +  relics_sets["icon"],
                "num": sets_num[relics["SetID"]],
                "desc": relics_sets["desc"][index_desc],
                "properties":[
                    {
                        "type": properties[0]["type"],
                        "field": property.get(properties[0]["type"])["field"],
                        "name": property.get(properties[0]["type"])["name"],
                        "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL +  property.get(properties[0]["type"])["icon"],
                        "value": properties[0]["value"],
                        "display": AssetEnkaParsed.get_display(properties[0]["value"], property.get(properties[0]["type"])["percent"]),
                        "percent": property.get(properties[0]["type"])["percent"]
                    } if properties != [] else []
                ]
                }
            )
            done.append(relics["SetID"])
        
        return new_data
        

    @classmethod
    async def add_relics(cls, data,lang):

        relics = await JsonManager(PathData.ENKA.value / "relics.json").read()
        relics = relics.get(str(data["tid"]))
        
        relicsMiHoMo = await JsonManager(PathData.ENKA_INDEX.value / lang /"relics.json").read()
        relicsMiHoMo = relicsMiHoMo.get(str(data["tid"]))
        
        hash = await JsonManager(PathData.ENKA.value / "hsr.json").read()
        hash = hash.get(lang)
        
        main_affix = await JsonManager(PathData.ENKA_INDEX.value / lang / "relic_main_affixes.json").read()
        main_affix = main_affix.get(relicsMiHoMo["main_affix_id"])
        main_affix = main_affix["affixes"].get(str(data["mainAffixId"]))
        
        
            
        property = await JsonManager(PathData.ENKA_INDEX.value / lang / "properties.json").read()

        data = {
                "id": data["tid"],
                "name": relicsMiHoMo["name"],
                "set_id": data["_flat"]["setID"],
                "set_name": hash.get(str(data["_flat"]["setName"])),
                "rarity": relics["Rarity"],
                "level": data["level"],
                "icon": f"https://enka.network/ui/hsr/{relics['Icon']}",
                "main_affix":{
                    "type": main_affix["property"],
                    "field": property.get(main_affix["property"])["field"],
                    "name": property.get(main_affix["property"])["name"],
                    "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL +  property.get(main_affix["property"])["icon"],
                    "value": data["_flat"]["props"][0]["value"],
                    "display": AssetEnkaParsed.get_display(data["_flat"]["props"][0]["value"], property.get(main_affix["property"])["percent"]),
                    "percent": property.get(main_affix["property"])["percent"]
                },
                "sub_affix": [ await AssetEnkaParsed.add_sub_affix(key, index, property, lang, data["_flat"]["props"]) for index, key in enumerate(data["subAffixList"], start = 2)]
                }
        
        return data
        
    @classmethod
    async def add_sub_affix(cls, affix, index, property, lang, flat):
        affixId = str(affix["affixId"])
        sub_affix = await JsonManager(PathData.ENKA_INDEX.value / lang / "relic_sub_affixes.json").read()
        sub_affix = sub_affix.get(str(index))

        return {
            "type": sub_affix["affixes"][affixId]["property"],
            "field":property.get(sub_affix["affixes"][affixId]["property"])["field"],
            "name": property.get(sub_affix["affixes"][affixId]["property"])["name"],
            "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL +  property.get(sub_affix["affixes"][affixId]["property"])["icon"],
            "value": flat[index-1]["value"],
            "display": AssetEnkaParsed.get_display(flat[index-1]["value"], property.get(sub_affix["affixes"][affixId]["property"])["percent"]),
            "percent":property.get(sub_affix["affixes"][affixId]["property"])["percent"],
            "count": affix.get("cnt", 0),
            "step": affix.get("step", 0)
        }

    
    @classmethod
    async def add_light_cone(cls, key,lang,path_info):        
        if key.get("equipment", {}) != {}:
            data = await AssetEnkaParsed.get_info_light_cone(key["equipment"]["tid"],lang)
            property = await JsonManager(PathData.ENKA_INDEX.value / lang / "properties.json").read()
            light_cone_ranks = await JsonManager(PathData.ENKA_INDEX.value / lang / "light_cone_ranks.json").read()
            
            return {
                "id": key["equipment"]["tid"],
                "name": data["EquipmentName"]["name"],
                "rarity": data["Rarity"],
                "rank": key["equipment"]["rank"],
                "level": key["equipment"]["level"],
                "promotion": key["equipment"]["promotion"],
                "icon": _DEFFAULT_ASSETS_HSR_LINK.format(catalog = "icon/light_cone", key = key["equipment"]["tid"]),
                "preview": _DEFFAULT_ASSETS_HSR_LINK.format(catalog = "image/light_cone_preview", key = key["equipment"]["tid"]),
                "portrait": _DEFFAULT_ASSETS_HSR_LINK.format(catalog = "image/light_cone_portrait", key = key["equipment"]["tid"]),
                "path": await AssetEnkaParsed.get_path(path_info,data),
                "attributes": [
                    {
                        "field": fiel.get(keys["type"]),
                        "name": property.get(keys["type"])["name"],
                        "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL +  property.get(keys["type"])["icon"],
                        "value": keys["value"],
                        "display": AssetEnkaParsed.get_display(keys["value"],property.get(keys["type"])["percent"]),
                        "percent":property.get(keys["type"])["percent"]
                    }
                for keys in key["equipment"]["_flat"]["props"]],

                "properties": [{
                    "type": keys["type"],
                    "field": property.get(keys["type"])["field"],
                    "name": property.get(keys["type"])["name"],
                    "icon": property.get(keys["type"])["icon"],
                    "value": keys["value"],
                    "display": AssetEnkaParsed.get_display(keys["value"],property.get(keys["type"])["percent"]),
                    "percent": property.get(keys["type"])["percent"]
                    } for keys in light_cone_ranks.get(str(key["equipment"]["tid"]))["properties"][key["equipment"]["rank"]-1] ]
            }
            
        return {}
    
    @classmethod
    async def get_info_light_cone(cls, ids,lang):
        data = await JsonManager(PathData.ENKA.value / "weps.json").read()

        charter = data.get(str(ids))
        
        hash = await JsonManager(PathData.ENKA.value / "hsr.json").read()
        
        charter["EquipmentName"]["name"] = hash.get(lang).get(str(charter["EquipmentName"]["Hash"]))

        return charter
    
    @classmethod
    async def add_skill_trees(cls, skill_trees_info,charter_info,skills_info,key):
            
        return [{
            "id": keys["pointId"],
            "level": keys["level"],
            "anchor": skill_trees_info[str(keys["pointId"])]["anchor"],
            "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL + skill_trees_info[str(keys["pointId"])]["icon"],
            "max_level": AssetEnkaParsed.get_max_level(skill_trees_info[str(keys["pointId"])],charter_info,skills_info,key.get("rank",0)),
            "parent": AssetEnkaParsed.get_parent(skill_trees_info[str(keys["pointId"])]),
            } for keys in key["skillTreeList"]]
    
    @classmethod
    async def add_skills(cls, element_info,charter_info,key,lang):
        skill_trees_info = await JsonManager(PathData.ENKA_INDEX.value / lang / "character_skill_trees.json").read()
        skills_info = await JsonManager(PathData.ENKA_INDEX.value / lang / "character_skills.json").read()
        
        data = []
        
        for keys in key["skillTreeList"]:
            pointId = str(keys["pointId"])
            if skill_trees_info.get(pointId)["level_up_skills"] == []:
                continue
            
            skills_info_id = str(skill_trees_info.get(pointId)["level_up_skills"][0]["id"])
            
            if not int(skills_info_id) in charter_info["SkillList"]:
                continue
            
            info = skills_info.get(skills_info_id)
            
            max_level = skill_trees_info.get(pointId)["max_level"]
            if keys["level"] > max_level:
                max_level = info["max_level"]

            data.append(
                {
                    "id": skills_info_id,
                    "name": info["name"],
                    "level": keys["level"],
                    "max_level": max_level,
                    "element": await AssetEnkaParsed.get_element(element_info, info["element"]),
                    "type": info["type"],
                    "type_text": info["type_text"],
                    "effect": info["effect"],
                    "effect_text": info["effect_text"],
                    "simple_desc": info["simple_desc"],
                    "desc": info["desc"],
                    "icon": _DEFFAULT_ASSETS_HSR_LINK_SKILL +  info["icon"],
                }
            )
            
        return data

    @classmethod
    async def get_icon_avatar(cls, ids):
        data = await JsonManager(PathData.ENKA.value / "avatars.json").read()
        
        return data.get(str(ids))["Icon"]
    
    @classmethod
    async def get_info_character(cls, ids,lang):
        data = await JsonManager(PathData.ENKA.value / "characters.json").read()

        charter = data.get(str(ids))
        
        hash = await JsonManager(PathData.ENKA.value / "hsr.json").read()
        
        charter["AvatarFullName"]["name"] = hash.get(lang).get(str(charter["AvatarFullName"]["Hash"]))
        charter["AvatarName"]["name"] = hash.get(lang).get(str(charter["AvatarName"]["Hash"]))

        return charter
    
    @classmethod
    async def get_element(cls, element_info,element):
        if element != "":
            return {"id": element_info[element]["id"],
                    "name": element_info[element]["name"],
                    "color": element_info[element]["color"],
                    "icon": _DEFFAULT_ASSETS_HSR_LINK.format(catalog = "icon/element", key = element_info[element]["id"].replace("Thunder", "Lightning"))
                }
        else:
            return None

    @classmethod
    async def get_path(cls, path_info,charter_info):
        return {
            "id": path_info[charter_info["AvatarBaseType"]]["id"],
            "name": path_info[charter_info["AvatarBaseType"]]["name"],
            "icon": _DEFFAULT_ASSETS_HSR_LINK.format(catalog = "icon/path", key = path_info[charter_info["AvatarBaseType"]]["text"]),
        }

    @classmethod
    def get_max_level(cls, skill_trees_info,charter_info,skills_info,rank):
        max_level = skill_trees_info["max_level"]
        if skill_trees_info.get("level_up_skills", []) != []:
            if int(skill_trees_info.get("level_up_skills")[0]["id"]) in charter_info["RankIDList"][:rank]:
                max_level = skills_info[skill_trees_info.get("level_up_skills")[0]["id"]]["max_level"]

        return max_level
    
    @classmethod
    def get_parent(cls, parent):
        if parent["pre_points"] != []:
            return parent["pre_points"][0]
        return None
    
    @classmethod
    def get_display(cls, value,percent):
        if percent:
            percentage_value = value * 100
            return f"{percentage_value:.1f}%"
        else:
            if value < 1:
                value = value * 100
                
            return str(round(value))