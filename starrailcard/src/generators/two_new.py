# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import asyncio
from PIL import ImageDraw,Image,ImageFilter,ImageChops
from ..tools import calculators, pill, openFile, treePaths
from ..tools.calculator import stats
_of = openFile.ImageCache()


_DEFAULT_SCORE = {'count': 0, 
                  'rolls': {}, 
                  'rank': {'name': 'N/A', 
                           'color': (255, 255, 255, 255)
                    }
}

color_scoreR = {
    4: (255, 200, 91, 255),
    3: (202, 159, 74, 255),
    2: (134, 107, 53, 255),
    1: (120, 95, 48, 255),
    0: (255, 255, 255, 255)
}

color_element = {
    'PhysicalAddedRatio': (255, 255, 255, 255),
    'PhysicalResistance': (255, 255, 255, 255),
    'FireAddedRatio': (248, 79, 54, 255),
    'FireResistance': (248, 79, 54, 255),
    'IceAddedRatio': (71, 199, 253, 255),
    'IceResistance': (71, 199, 253, 255),
    'ThunderAddedRatio': (136, 114, 241, 255),
    'ThunderResistance': (136, 114, 241, 255),
    'WindAddedRatio': (0, 255, 156, 255),
    'WindResistance': (0, 255, 156, 255),
    'QuantumAddedRatio': (28, 41, 186, 255),
    'QuantumResistance': (28, 41, 186, 255),
    'ImaginaryAddedRatio': (244, 210, 88, 255),
    'ImaginaryResistance': (244, 210, 88, 255)
}

async def get_background_path(path):
    if path == "Rogue":
        return _of.Rogue.copy()
    elif path == "Knight":
        return _of.Knight.copy()
    elif path == "Mage":
        return _of.Mage.copy()
    elif path == "Priest":
        return _of.Priest.copy()
    elif path == "Shaman":
        return _of.Shaman.copy()
    elif path == "Warlock":
        return _of.Warlock.copy()
    else:
        return _of.Warrior.copy()

async def get_cone_frame(x):
    if x == 5:
        return _of.light_cone_frame_five
    elif x == 4:
        return _of.light_cone_frame_four
    else:
        return _of.light_cone_frame_three
    
color_lc_line = {
    "3": (150, 202, 255, 255),
    "4": (217, 150, 255, 255),
    "5": (255, 217, 144, 255),
}

async def max_lvl(x):
    if x == 0:
        max = 20
    elif x == 1:
        max = 30
    elif x == 2:
        max = 40 
    elif x == 3:
        max = 50
    elif x == 4:
        max = 60
    elif x == 5:
        max = 70
    else:
        max = 80
    
    return max

async def ups(x):
    if x == 5:
        return "V"
    elif x == 4:
        return "IV"
    elif x == 3:
        return "III"
    elif x == 2:
        return "II"
    elif x == 1:
        return "I"
    else:
        return "O"

async def get_stars(x):
    if x == 5:
        return _of.g_five
    elif x == 4:
        return _of.g_four
    elif x == 3:
        return _of.g_three
    elif x == 2:
        return _of.g_two
    else:
        return _of.g_one

class Creat:
    def __init__(self,characters, lang,img,hide,uid,seeleland) -> None:
        self.character = characters
        self.lang = lang
        self.img = img
        self.hide = hide
        self.uid = uid
        self.totall_eff = 0
        self.seeleland = seeleland
        self.element_color = self.character.element.color.rgba
        
    async def creat_bacground(self):
        self.background = Image.new("RGBA",(1920,782), (0,0,0,0))
        background_dark = Image.new("RGBA",(1920,782), (0,0,0,100))
        background_art = Image.new("RGBA",(1920,782), (0,0,0,0))
        background_blur = Image.new("RGBA",(1920,782), (0,0,0,0))
        
        if self.img:
            user_image = await pill.get_centr_honkai_art((782,782),self.img)
            bg = await pill.GradientGenerator(user_image).generate(1,782)
            bg = bg.resize((1920,782))
            user_image_op = await pill.apply_opacity(user_image, opacity=0.2)
            background_blur.alpha_composite(bg.convert("RGBA"))
            background_blur.alpha_composite(user_image_op)
            background_blur = background_blur.filter(ImageFilter.GaussianBlur(30))
            line,self.element_color = await pill.recolor_image(_of.background_line, self.element_color[:3], light = True)
        else:
            bg = _of.background_default.copy() 
            user_image = await pill.get_centr_honkai((850,782),await pill.get_dowload_img(self.character.portrait))
            user_image_op = await pill.apply_opacity(user_image, opacity=0.7)
            background_blur.alpha_composite(bg.convert("RGBA"))
            background_blur.alpha_composite(user_image_op)
            background_blur = background_blur.filter(ImageFilter.GaussianBlur(25))
            line = await pill.recolor_image(_of.background_line, self.element_color[:3])
            
        background_blur.alpha_composite(background_dark)
        self.background.paste(background_blur,(0,0),_of.background_maska_blur.convert("L"))
        if self.img:
            self.background = ImageChops.soft_light(self.background,_of.background_overlay.convert("RGBA"))
        
        background_art.alpha_composite(bg.convert("RGBA"))
        background_art.alpha_composite(user_image)
        self.background.paste(background_art,(0,0),_of.background_maska_art.convert("L"))
        self.background.alpha_composite(_of.background_shadow)
        self.background.alpha_composite(line,(693,-7))
        self.background.alpha_composite(_of.LOGO_GIT)
        
        if not self.hide:
            uid = Image.new("RGBA",(1920,782), (0,0,0,0))
            d = ImageDraw.Draw(uid)
            
            font_10 = await pill.get_font(10)
            d.text((0,0), f"UID: {self.uid}", font=font_10, fill=(255, 255, 255, 75))
            self.background.alpha_composite(uid,(7,768))
            
    async def creat_light_cone(self):
        self.background_light_cones = Image.new("RGBA", (330, 190), (0, 0, 0, 0))
        if self.character.light_cone is None:
            return
        
        background = Image.new("RGBA", (139, 190), (0, 0, 0, 0))
        image = await pill.get_dowload_img(self.character.light_cone.portrait, size=(118, 169))
        background.alpha_composite(image,(9,9))
        light_cone_frame_stars = await get_cone_frame(self.character.light_cone.rarity)
        background.alpha_composite(light_cone_frame_stars)
        background.alpha_composite(_of.light_cone_frame)
        
        self.background_light_cones.alpha_composite(background)
        
        background = _of.light_cone_stats.copy()
        
        d = ImageDraw.Draw(background)
        
        font_18 = await pill.get_font(18)
        d.text((28, 4), self.character.light_cone.attributes[0].display, font=font_18, fill=(255, 255, 255, 255))
        d.text((28, 30), self.character.light_cone.attributes[1].display, font=font_18, fill=(255, 255, 255, 255))
        d.text((28, 56), self.character.light_cone.attributes[2].display, font=font_18, fill=(255, 255, 255, 255))
        
        self.background_light_cones.alpha_composite(background,(140,100))
        
        background = _of.light_cone_ups.copy()
        d = ImageDraw.Draw(background)
        font_12 = await pill.get_font(12)
        up = await ups(self.character.light_cone.rank)
        x = int(font_12.getlength(str(up))/2)
        d.text((10-x, 4), up, font= font_12, fill=(255, 217, 144, 255))
        
        self.background_light_cones.alpha_composite(background,(140,68))
        d = ImageDraw.Draw(self.background_light_cones)
        max_level = await max_lvl(self.character.light_cone.promotion)
        d.text((165, 69), f"{self.lang.lvl}: {self.character.light_cone.level}/{max_level}", font=font_18, fill=(255, 255, 255, 255))
        
        names = await pill.create_image_with_text(self.character.light_cone.name, 18, max_width=180, color=(255, 255, 255, 255))
        line = Image.new("RGBA", (1,48), color_lc_line.get(str(self.character.light_cone.rarity), (150, 202, 255, 255)))
        
        
        self.background_light_cones.alpha_composite(line,(140,9))
        self.background_light_cones.alpha_composite(names,(146,int(34-names.size[1]/2)))
        
    async def creat_name(self):
        self.background_name = Image.new("RGBA", (288, 103), (0, 0, 0, 0))
        d = ImageDraw.Draw(self.background_name)
        names = await pill.create_image_with_text(self.character.name, 25, max_width=262, color=(255, 255, 255, 255))
        if names.size[1] <= 53:
            self.background_name.alpha_composite(names,(4,int(53-names.size[1]/2)))
        else:
            self.background_name.alpha_composite(names,(4,int(35-names.size[1]/2)))
        
        font_17 = await pill.get_font(17)
        max_level = await max_lvl(self.character.promotion)
        level = f"{self.lang.lvl}: {self.character.level}/{max_level}"
        d.text((4, 60), level, font=font_17, fill=(255, 255, 255, 255))
        starts = await get_stars(self.character.rarity)
        self.background_name.alpha_composite(starts,(2,85))
        
    async def creat_stats(self):
        self.background_stats = Image.new("RGBA", (563, 290), (0, 0, 0, 0))

        combined_attributes = {}
        dop = {}

        for attribute in self.character.attributes + self.character.additions:
            field = attribute.field
            if field in combined_attributes:
                combined_attributes[field].value += attribute.value
                dop[field]["dop"] = f"+{attribute.display}"
            else:
                dop[field] = {"main": attribute.display, "dop": 0}
                combined_attributes[field] = attribute

        dop = {key: value for key, value in dop.items() if value['dop'] != 0}
        
        xp,y = 0,0
        font = await pill.get_font(20)
        font_dop = await pill.get_font(12)
        
        for i, attribute in enumerate(combined_attributes):
            stat = combined_attributes[attribute]
            icon = await pill.get_dowload_img(stat.icon, size=(45,45))
            background = Image.new("RGBA", (273, 58), (0, 0, 0, 0))
            d = ImageDraw.Draw(background)
            value = "{:.1f}%".format(stat.value * 100) if stat.percent else round(stat.value)
            name_text = await pill.create_image_text(stat.name, 15, max_width=140, max_height=45, color=(255, 255, 255, 255))
            background.alpha_composite(name_text, (46,(int(29-name_text.size[1]/2))))
            background.alpha_composite(icon,(0,6))
            
            if attribute in dop: 
                x = 271 - int(font.getlength(str(value)))
                d.text((x, 6), str(value), font=font, fill=(255, 255, 255, 255))
    
                x = 271 - int(font_dop.getlength(dop[attribute]["dop"]))
                d.text((x, 25), dop[attribute]["dop"], font=font_dop, fill= self.element_color)

                x = x - int(font_dop.getlength(dop[attribute]["main"])) - 5
                d.text((x, 25), dop[attribute]["main"], font=font_dop, fill=(255, 255, 255, 255))
            else:
                x = 271 - int(font.getlength(str(value)))
                d.text((x, 13), str(value), font=font, fill=(255, 255, 255, 255))
        
            self.background_stats.alpha_composite(background,(xp,y))
            y += 45
            if i == 5:
                xp = 290
                y = 0
             
    async def creat_relict(self,relict):
        background_main = Image.new("RGBA",(273,134), (0,0,0,0))
        background = Image.new("RGBA",(273,134), (0,0,0,0))
        background_image = Image.new("RGBA",(273,134), (0,0,0,0))
        
        background_main.alpha_composite(_of.relict_frame)
        
        image = await pill.get_dowload_img(relict.icon, size=(113, 113))
        background_image.alpha_composite(image,(-6,21))
        background.paste(background_image,(0,0),_of.relict_maska.convert("L"))
        
        background_main.alpha_composite(_of.relict_score_frame,(8,0))
        background_main.alpha_composite(background)
        background_main.alpha_composite(_of.relict_line)
        score = self.score_info["score"].get(str(relict.id),_DEFAULT_SCORE)
        
        main_stat_icon = await pill.get_dowload_img(relict.main_affix.icon, size=(48, 48))
        color = color_element.get(relict.main_affix.type, None)
        if not color is None:
            main_stat_icon = await pill.recolor_image(main_stat_icon, color[:3])
        stars = await get_stars(relict.rarity)
        
        background_main.alpha_composite(stars,(51,27))
        background_main.alpha_composite(main_stat_icon,(90,41))
        
        font_22 = await pill.get_font(22)
        font_14 = await pill.get_font(14)
        font_18 = await pill.get_font(18)
        
        d = ImageDraw.Draw(background_main)
        x = 135 - int(font_22.getlength(relict.main_affix.display))
        d.text((x, 86), relict.main_affix.display, font= font_22, fill= (255,255,255,255))
        
        x = 121 - int(font_22.getlength(f"+{relict.level}")/2)
        d.text((x, 110), f"+{relict.level}", font= font_14, fill= self.element_color)
        
        y_icon = 21
        y_roll = 30
        y_text = 27
                
        eff = 0
        
        for k in relict.sub_affix:
            icon = await pill.get_dowload_img(k.icon, size=(29, 29))
            background_main.alpha_composite(icon,(142,y_icon))
            scoreR = score["rolls"].get(k.type,0)
            if k.type in self.score_info["bad"]:
                d.text((173, y_text), str(k.display), font=font_18, fill= (255,255,255,255))
            else:
                eff += 1
                d.text((173, y_text), str(k.display), font=font_18, fill= color_scoreR.get(scoreR,(255,255,255,255)))
            d.text((232, y_roll), f"+{scoreR}", font=font_18, fill= color_scoreR.get(scoreR,(255,255,255,255)))
            y_icon += 27
            y_text += 28
            y_roll += 27
            
        d.text((22, 4), "Score:", font=font_14, fill = (255,255,255,255))
        d.text((70, 4), str(score["count"]), font=font_14, fill = score["rank"]["color"])
        
        d.text((105, 4), "Rank:", font=font_14, fill = (255,255,255,255))
        d.text((149, 4), str(score["rank"]["name"]), font=font_14, fill = score["rank"]["color"])
        
        d.text((187, 4), "Eff Stat:", font=font_14, fill = (255,255,255,255))
        d.text((247, 4), str(eff), font=font_14, fill = color_scoreR.get(eff,(255,255,255,255)))
        
        self.totall_eff += eff
        
        line_f = _of.relict_frame_line.copy()
        line_f = await pill.recolor_image(line_f, self.element_color[:3])
        background_main.alpha_composite(line_f,(0,21))
        
        return {"position": str(relict.id)[-1:] , "img": background_main}

    async def creat_score_total(self):
        self.background_score = Image.new("RGBA",(559,43), (0,0,0,0))
        
        sclor_bg = _of.relict_backgroundl_score_line.copy()
        sclor_bg_color = _of.relict_full_score_line.copy()
        
        sclor_bg_color = await pill.recolor_image(sclor_bg_color, self.element_color[:3])
        
        result_percentage = (self.score_info["total_score"]['count'] / 260.53) * 100
        pixels_to_fill = int((result_percentage / 100)*599)
        if pixels_to_fill <= 0:
            pixels_to_fill = 1
        sclor_bg.alpha_composite(sclor_bg_color.resize((pixels_to_fill,16)))
        
        font_18 = await pill.get_font(18)
        
        d = ImageDraw.Draw(sclor_bg)
        x = 280 - int(font_18.getlength(f"{round(result_percentage,1)}%")/2)
        if self.element_color[:3] == (255,255,255):
            d.text((x, -1), f"{round(result_percentage,1)}%", font=font_18, fill = (0,0,0,255))
        else:
            d.text((x, -1), f"{round(result_percentage,1)}%", font=font_18, fill = (255,255,255,255))
        
        self.background_score.alpha_composite(sclor_bg,(0,27))
        
        font_21 = await pill.get_font(21)
        d = ImageDraw.Draw(self.background_score)
        
        d.text((249, -2), "Score:", font=font_21, fill = (255,255,255,255))
        d.text((320, -2), str(self.score_info["total_score"]['count']), font=font_21, fill = self.score_info["total_score"]["rank"]["color"])
        
        d.text((17, -2), "Summary Rank:", font=font_21, fill = (255,255,255,255))
        d.text((189, -2), str(self.score_info["total_score"]["rank"]["name"]), font=font_21, fill = self.score_info["total_score"]["rank"]["color"])
        
        d.text((393, -2), "Eff Stat:", font=font_21, fill = (255,255,255,255))
        d.text((497, -2), str(self.totall_eff), font=font_21, fill = color_scoreR.get(self.totall_eff,(255,255,255,255)))        
    
    async def creat_relict_sets(self):
        rel_set = {}
        for key in self.character.relic_sets:
            if key.id not in rel_set:
                if key.properties == []:
                    rel_set[key.id] = {"num": int(key.num), "name": key.name, "icon": key.icon, "properties": None}
                else:
                    rel_set[key.id] = {"num": int(key.num), "name": key.name, "icon": key.icon, "properties": {"icon": key.properties[0].icon, "display": key.properties[0].display}}
            else:
                rel_set[key.id]["num"] = int(key.num)

        self.background_sets = Image.new("RGBA", (559,56), (0,0,0,0))
        
        font = await pill.get_font(18)
        
        line_items = []
        i = 0
        for key in rel_set:
            sets = rel_set[key]
            holst_line = Image.new("RGBA", (559,28), (0,0,0,0))
            background_count = _of.relict_count_sets.copy()
            d = ImageDraw.Draw(background_count)
            d.text((8, 4), str(sets["num"]), font=font, fill=(255, 200, 91, 255))
            d = ImageDraw.Draw(holst_line)
            sets_name_font,size = await pill.get_text_size_frame(sets["name"],15,492)
            if key[:1] == "1":
                holst_line.alpha_composite(background_count)
                d.text((36, 4), sets["name"], font=sets_name_font, fill=(255, 200, 91, 255))
                line_items.append({"setap": i, "line": holst_line})
                i += 1
            else:
                holst_line.alpha_composite(background_count,(532,0))
                d.text((int(521-size), 4), sets["name"], font=sets_name_font, fill=(255, 200, 91, 255))
                line_items.append({"setap": 1, "line": holst_line})
                
        for key in line_items:
            if key["setap"] == 1:
                self.background_sets.alpha_composite(key["line"],(0,29))
            elif key["setap"] == 2:
                self.background_sets.alpha_composite(key["line"],(0,29))
            else:
                self.background_sets.alpha_composite(key["line"],(0,0))
    
    async def build_relict(self):
        self.background_relict = Image.new("RGBA",(1131,297), (0,0,0,0))
        
        position = {
            "1": (0,163),
            "2": (286,163),
            "3": (572,163),
            "4": (858,163),
            "5": (572,0),
            "6": (858,0),
        }
        
        map = {"1": None, "2": None, "3": None, "4": None, "5": None, "6": None}
        
        for key in self.relict:
            self.background_relict.alpha_composite(key["img"], position.get(key["position"]))
            map[key["position"]] = 0
        
        for key in map:
            if map[key] is None:
                self.background_relict.alpha_composite(_of.none_relict, position.get(key))

        self.background_relict.alpha_composite(self.background_score,(0,112))
        self.background_relict.alpha_composite(self.background_sets,(0,45))
    
    async def creat_path(self):
        self.background_path = await get_background_path(self.character.path.id)
        path = treePaths.map_new.get(self.character.path.id)
        font_15 = await pill.get_font(15) 
        for key in self.character.skill_trees:
            if key.anchor in ['Point01','Point02','Point03','Point04','Point05']:
                icon = await pill.get_dowload_img(key.icon, size=(47,47))
                icon = await pill.recolor_image(icon, (255,212,173))
                count = _of.path_count.copy()
                d = ImageDraw.Draw(count)
                if key.anchor == 'Point01':
                    if key.max_level > 6:
                        key.level += 1
                else:
                    if key.max_level > 10:
                        key.level += 2
                    
                x = 29 - int(font_15.getlength(f"{key.level}/{key.max_level}")/2)
                d.text((x, 1), f"{key.level}/{key.max_level}", font=font_15, fill = (255,255,255,255))
                self.background_path.alpha_composite(icon, path[key.anchor]["icon"])
                self.background_path.alpha_composite(count, path[key.anchor]["count"])
            elif key.anchor in ['Point06','Point07','Point08']:
                icon = await pill.get_dowload_img(key.icon, size=(47,47))
                icon = await pill.recolor_image(icon, (0,0,0))
                if key.level == key.max_level:
                    self.background_path.alpha_composite(icon, path[key.anchor]["icon"])
                else:
                    icon = await pill.apply_opacity(icon, opacity=0.5)
                    closed = _of.path_closed_main
                    self.background_path.alpha_composite(icon, path[key.anchor]["icon"])
                    self.background_path.alpha_composite(closed, path[key.anchor]["closed"])
            else:
                icon = await pill.get_dowload_img(key.icon, size=(35,35))
                icon = await pill.recolor_image(icon, (0,0,0))
                if key.level == key.max_level:
                    self.background_path.alpha_composite(icon, path[key.anchor]["icon"])
                else:
                    icon = await pill.apply_opacity(icon, opacity=0.5)
                    closed = _of.path_closed_dop
                    self.background_path.alpha_composite(icon, path[key.anchor]["icon"])
                    self.background_path.alpha_composite(closed, path[key.anchor]["icon"])
                
    async def creat_constant(self):
        self.background_skills = Image.new("RGBA", (403, 63), (0, 0, 0, 0))
        x = 0
        rank = self.character.rank
        for key in self.character.rank_icons[:rank]:
            bg = Image.new("RGBA", (163, 164), (0, 0, 0, 0))
            icon = await pill.get_dowload_img(key, size=(53,53))
            icon_blur = icon.filter(ImageFilter.GaussianBlur(3))
            icon_blur = await pill.recolor_image(icon_blur, self.element_color[:3])
            bg.alpha_composite(icon_blur,(5,5))
            bg.alpha_composite(icon,(5,5))
            self.background_skills.alpha_composite(bg,(x,0))
            x += 68

        for key in self.character.rank_icons[rank:]:
            bg = Image.new("RGBA", (163, 164), (0, 0, 0, 0))
            icon = await pill.get_dowload_img(key, size=(53,53))
            icon = await pill.apply_opacity(icon, opacity=0.2)
            bg.alpha_composite(icon,(5,5))
            self.background_skills.alpha_composite(bg,(x,0))
            x += 68

    async def build(self):
        self.background.alpha_composite(self.background_light_cones,(782,16))
        self.background.alpha_composite(self.background_name,(6,654))
        self.background.alpha_composite(self.background_stats,(781,220))
        self.background.alpha_composite(self.background_relict,(781,473))
        self.background.alpha_composite(self.background_skills.resize((320,47)),(1033,134))
        self.background.alpha_composite(self.background_path.resize((488,428)),(1409,16))
        self.background.alpha_composite(self.seelelen, (1120,35))
        
    async def get_score(self):
        self.score_info = await stats.Calculator(self.character).start()
    
    async def creat_seeleland(self):
        self.seelelen = Image.new("RGBA",(1,1), (0,0,0,0))
        
        if self.seeleland:
            self.seelelen = _of.seeleland_v2.copy()
            font = await pill.get_font(15)
            data = await calculators.get_seeleland(self.uid, self.character.id)
            if data is None:
                self.seelelen = Image.new("RGBA",(1,1), (0,0,0,0))
                return None
            if not "rank" in data:
                self.seelelen = Image.new("RGBA",(1,1), (0,0,0,0))
                return None
            draw = ImageDraw.Draw(self.seelelen)
            draw.text((143, 7), str(data["sc"]), font=font, fill=(255, 255, 255, 255))
            draw.text((136, 24), str(data["rank"]), font=font, fill=(255, 255, 255, 255))
            draw.text((127, 42), data["rank"].replace("top ", ""), font=font, fill=(255, 255, 255, 255))
            
    async def start(self):
        if self.img:
            self.element_color = await  pill.get_background_colors(self.img, 15, common=True, radius=5, quality=800)
            
        await asyncio.gather(self.creat_bacground(),
                             self.creat_light_cone(),
                             self.creat_name(),
                             self.creat_stats(),
                             self.creat_relict_sets(),
                             self.creat_constant(),
                             self.creat_path(),
                             self.get_score(),
                             self.creat_seeleland()
        )
        
        self.score_info = await stats.Calculator(self.character).start()
        
        relic_tasks = [self.creat_relict(key) for key in self.character.relics]
        self.relict = await asyncio.gather(*relic_tasks)
        
        await self.creat_score_total()
        await self.build_relict()
        await self.build()
        
        data = {
            "id": self.character.id,
            "name": self.character.name,
            "rarity": self.character.rarity,
            "card": self.background,
            "size": self.background.size
        }
        
        return data
        
        