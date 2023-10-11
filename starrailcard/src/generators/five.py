# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import asyncio
from PIL import ImageDraw,Image, ImageFilter
from ..tools import pill, openFile, calculator

_of = openFile.ImageCache()


async def get_bg(bg,cards):
    
    bg_size = [
        605,
        1056,
        1500,
        1989
    ]
    
    if bg:
        bg = _of.total_cards_bg.copy().convert("RGBA")
        bg = bg.crop((0, 0, bg_size[len(cards)-1], 887))
    else:
        bg = Image.new("RGBA", (bg_size[len(cards)-1],887), (0,0,0,0))
    
    p = [
        101,
        555,
        1009,
        1463
    ]
    for i,key in enumerate(cards):
        bg.alpha_composite(key["card"],(p[i],44))
    
    return bg


async def get_open_background(name):
    if name == "Wind":
        return _of.wind_five.copy()
    if name == "Fire":
        return _of.fire_five.copy()
    if name == "Ice":
        return _of.ice_five.copy()
    if name == "Thunder":
        return _of.electro_five.copy()
    if name == "Quantum":
        return _of.quantom_five.copy()
    if name == "Imaginary":
        return _of.imaginary_five.copy()
    else:
        return _of.psyhical_five.copy()
    

async def get_stars_icon(x, v = 1):
    if v == 0:
        if x == 1:
            return _of.strs_1
        elif x == 2:
            return _of.strs_2
        elif x == 3:
            return _of.strs_3
        elif x == 4:
            return _of.strs_4
        elif x == 5:
            return _of.strs_5
    else:
        if x == 5:
            return _of.strs_5_shadow
        elif x == 4:
            return _of.strs_4_shadow
        else:
            return _of.strs_3_shadow

async def frame_bg(x):
    if x == 5:
        return _of.stars_5_frame_up, _of.stars_5_frame
    else:
        return _of.stars_4_frame_up, _of.stars_4_frame
    
async def get_lc_res(x):
    if x == 5:
        return _of.shadow_5_lc, _of.star_5_frame, _of.star_5_frame_lc, (255,199,150,255)
    elif x == 4:
        return  _of.shadow_4_lc, _of.star_4_frame, _of.star_4_frame_lc, (217,150,255,255)
    else:
        return  _of.shadow_3_lc, _of.star_3_frame, _of.star_3_frame_lc, (150,202,255,255)

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
        return " I"
    else:
        return "O"

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

async def get_frame_relict(x):
    if x == 5:
        return _of.stars_5_frame_relict.copy()
    elif x == 4:
        return _of.stars_4_frame_relict.copy()
    elif x == 3:
        return _of.stars_3_frame_relict.copy()
    elif x == 2:
        return _of.stars_2_frame_relict.copy()
    else:
        return _of.stars_1_frame_relict.copy()

class Creat:

    def __init__(self,characters, lang,img) -> None:
        self.character = characters
        self.lang = lang
        self.img = img
        
    async def creat_charters(self):
        if self.img:
            bg = await pill.creat_user_image_five(self.img)
        else:
            bg = await get_open_background(self.character.element.id)
            bg = await pill.creat_bg_teample_two(self.character.portrait, bg, maska = _of.mask_bg_five.convert("L"), teample = 5)
        
        return bg
    
    async def creat_relics(self,relics):
        bg = await get_frame_relict(relics.rarity)

        icon_rel = await pill.get_dowload_img(relics.icon, size=(51, 51))
        bg.alpha_composite(icon_rel,(0,0))
        bg.alpha_composite(_of.shadow_frame_relict,(0,0))
        icon = await pill.get_dowload_img(relics.main_affix.icon, size=(18,18))
        bg.alpha_composite(icon,(30,3))
        
        display = relics.main_affix.display
        level = f"+{relics.level}"
        font_main = await pill.get_font(11)
        font = await pill.get_font(10)

        d = ImageDraw.Draw(bg)
        x = int(font_main.getlength(display))
        d.text((47- x, 17), display, font=font_main, fill=(0,0,0,255))
        d.text((48- x, 17), display, font=font_main, fill=(255,255,255,255))
        
        x = int(font.getlength(level)/2)
        d.text((36 - x, 33), str(level), font=font, fill=(0,0,0, 255))
        d.text((37 - x, 33), str(level), font=font, fill=(219,202,156, 255))
        
        #score, rank, eff = await calculator.get_rating(relics,self.character.id,)  

        return {"img": bg, "position": relics.id[-1:]}
    
    async def creat_lk(self):
        
        if self.character.light_cone is None:
            return Image.new("RGBA", (0, 0), (0, 0, 0, 0))
        
        lc = Image.new("RGBA", (337, 448), (0, 0, 0, 0))
        lc_img = Image.new("RGBA", (337, 448), (0, 0, 0, 0))
        image = await pill.get_dowload_img(self.character.light_cone.portrait, size=(298, 410))
        lc_img.alpha_composite(image,(19,23))
        
        lc.paste(lc_img,(0,0),_of.maska_lc.convert("L"))
        
        lc_img = Image.new("RGBA", (337, 448), (0, 0, 0, 0))
        shadow,total_frame,frame, color  = await get_lc_res(self.character.light_cone.rarity)
        lc_img.alpha_composite(shadow,(0,0))
        lc_img.alpha_composite(frame,(32,29))
        lc_img.alpha_composite(lc,(0,0))
        lc_img.alpha_composite(_of.frame_lc,(0,0))
        lc_img.alpha_composite(_of.blic_lc,(0,0))
        lc_img.alpha_composite(frame,(0,0))
        
        total_lc = Image.new("RGBA", (360, 114), (0, 0, 0, 0))
        if self.img:
            total_img = Image.new("RGBA", (360, 114), (0, 0, 0, 0))
            img = self.img.filter(ImageFilter.GaussianBlur(radius=10))
            total_img.alpha_composite(img,(0,0))
            total_lc.paste(total_img.convert("RGBA"),(0,0),_of.mask_lc_all.convert("L"))
            total_lc.alpha_composite(_of.dark,(0,0))
            total_lc.alpha_composite(_of.stars_lc,(0,0))
        else:
            total_lc.alpha_composite(_of.def_bg,(0,0))
        
        total_lc.alpha_composite(total_frame,(0,0))
        total_lc.alpha_composite(lc_img.resize((82,111)),(0,0)) 
        
        font_16 = await pill.get_font(16)
        
        names = await pill.create_image_with_text(self.character.light_cone.name, 13, max_width=219, color=(255, 255, 255, 255)) 
        line = Image.new("RGBA", (1, names.size[1]), color) 
        total_lc.alpha_composite(line,(96,15))
        total_lc.alpha_composite(names, (105, 15))
        
        rankes = _of.ranket.copy()
        d = ImageDraw.Draw(rankes)
        d.text((3,-3), await ups(self.character.light_cone.rank), font=font_16, fill=(193, 162, 103, 255))
        total_lc.alpha_composite(rankes,(96,15+line.size[1]+3))
        total_lc.alpha_composite(_of.stats_lc,(0,0))
        
        font_14 = await pill.get_font(14)
        font_12 = await pill.get_font(12)
        
        max_level = await max_lvl(self.character.light_cone.promotion)
        d = ImageDraw.Draw(total_lc)
        d.text((121,15+line.size[1]+1), f"{self.lang.lvl}: {self.character.light_cone.level}/{max_level}", font=font_14, fill=(255, 255, 255, 255))
        
        d.text((134, 79), self.character.light_cone.attributes[0].display, font=font_12, fill=(255, 255, 255, 255)) #HP
        d.text((270, 79), self.character.light_cone.attributes[1].display, font=font_12, fill=(255, 255, 255, 255)) #ATK
        d.text((202, 79), self.character.light_cone.attributes[2].display, font=font_12, fill=(255, 255, 255, 255)) #DEF
        
        return total_lc
        
        
        
    async def creat_constant(self):
        background_skills = Image.new("RGBA", (43, 288), (0, 0, 0, 0))
        y = 0
        rank = self.character.rank

        closed = _of.CLOSED_const.copy().resize((49,49))
        open_bg = _of.const_five

        for key in self.character.rank_icons[:rank]:
            bg = open_bg.copy()
            icon = await pill.get_dowload_img(key, size=(35,35))
            bg.alpha_composite(icon,(4,4))
            background_skills.alpha_composite(bg,(0,y))
            y += 49

        for key in self.character.rank_icons[rank:]:
            bg = open_bg.copy()
            icon = await pill.get_dowload_img(key, size=(35,35))
            bg.alpha_composite(icon,(4,4))
            bg.alpha_composite(closed,(-3,-3))
            background_skills.alpha_composite(bg,(0,y))
            y += 49
        return background_skills
    
    
    async def creat_stats(self):
        bg_new = Image.new("RGBA", (345, 73), (0, 0, 0, 0))

        combined_attributes = {}

        for attribute in self.character.attributes + self.character.additions:
            field = attribute.field
            if field in combined_attributes:
                combined_attributes[field].value += attribute.value
            else:
                combined_attributes[field] = attribute

        x_icon, y_icon, x_text, y_text = 0, 0, 30, 0
        d = ImageDraw.Draw(bg_new)
        font = await pill.get_font(16)

        for i, attribute in enumerate(combined_attributes.values()):
            icon = await pill.get_dowload_img(attribute.icon, size=(24, 24))
            icon_d = await pill.recolor_image(icon, (0,0,0))
            #bg_new.alpha_composite(icon, (x_icon-1, y_icon+1))
            bg_new.alpha_composite(icon_d, (x_icon-1, y_icon-1))
            bg_new.alpha_composite(icon, (x_icon, y_icon))

            value = "{:.1f}%".format(attribute.value * 100) if attribute.percent else round(attribute.value)
            #x = x_text - int(font.getlength(str(value)))
            d.text((x_text-1, y_text+1), str(value), font=font, fill=(0, 0, 0, 255))
            d.text((x_text, y_text), str(value), font=font, fill=(255, 255, 255, 255))

            y_icon += 25
            y_text += 25

            if (i + 1) % 3 == 0:
                y_icon = 0
                y_text = 0
                x_icon += 85
                x_text += 85
        
        return bg_new
    
    async def main_skills(self):

        font = await pill.get_font(11)
        font_15 = await pill.get_font(15)

        main_bg =  Image.new("RGBA", (51,257), (0, 0, 0, 0))
        position_main = 0

        dop_bg = Image.new("RGBA", (229,44), (0, 0, 0, 0))

        position_dop = 0
        
        data = {}
        closed_icon = _of.bg_dop_closed.copy()
        i = 0
        bg_dop = _of.bg_dop_skills
        for key in self.character.skill_trees:
            if key.max_level != 1:
                icon = await pill.get_dowload_img(key.icon, size=(41, 41))
                bg = _of.talants_bg.copy().resize((51,54))
                count = _of.talants_count.copy().resize((41,14))
                bg.alpha_composite(icon,(5,7))
                draw = ImageDraw.Draw(count)
                x = int(font.getlength( f"{key.level}/{key.max_level}")/2)
                draw.text((21-x,-3), f"{key.level}/{key.max_level}", font=font, fill=(255, 255, 255, 255))
                bg.alpha_composite(count,(5,41))
                main_bg.alpha_composite(bg,(0,position_main))
                position_main += 68
            else:
                if key.anchor in ["Point05","Point06","Point07","Point08"]:
                    icon = await pill.get_dowload_img(key.icon, size=(37, 37))
                    icon = await pill.recolor_image(icon, (0,0,0))
                    bg = bg_dop.copy()
                    bg.alpha_composite(icon,(4,3))
                    if key.level == 0:
                        bg.alpha_composite(closed_icon,(0,0))
                        
                    dop_bg.alpha_composite(bg,(position_dop,0))
                    position_dop += 58
                else:
                    if key.level != 0:
                        if not key.icon in data:
                            data[key.icon] = {"icon": key.icon, "count": 1}
                        else:
                            data[key.icon]["count"] += 1
                            
        bg_dop =  Image.new("RGBA", (79,41), (0, 0, 0, 0))
        position_x = [
            (0,0),
            (46,0),
            (0,24),
            (46,24),
            (92,0)
        ]
        for i, key in enumerate(data):
            bg = _of.dop_stats.copy().resize((33,17))
            icon = await pill.get_dowload_img(data[key]["icon"], size=(17,17))
            bg.alpha_composite(icon, (0,0))
            draw = ImageDraw.Draw(bg)
            draw.text((20,-4), str(data[key]["count"]), font=font_15, fill=(255, 251, 155, 255))
            bg_dop.alpha_composite(bg,position_x[i])
    
        return main_bg, dop_bg, bg_dop
    
    
    async def creat_name_banner(self):
        background_name = Image.new("RGBA", (372,128), (0,0,0,0))
        font = await pill.get_font(17)
        icon_element = await pill.get_dowload_img(self.character.element.icon, thumbnail_size=(22,22))
        icon_path = await pill.get_dowload_img(self.character.path.icon, size=(22,22))
        stars = await get_stars_icon(self.character.rarity)
        max_level = await max_lvl(self.character.promotion)
        level = f"{self.lang.lvl}: {self.character.level}/{max_level}"
        name = self.character.name

        icon_element_d = await pill.recolor_image(icon_element, (0,0,0))
        icon_path_d = await pill.recolor_image(icon_path, (0,0,0))
        
        background_name.alpha_composite(icon_element_d,(91,1))
        background_name.alpha_composite(icon_path_d,(118,2))
        
        background_name.alpha_composite(icon_element,(93,1))
        background_name.alpha_composite(icon_path,(119,2))
        
        background_name.alpha_composite(stars.resize((91,28)),(1,0))

        draw = ImageDraw.Draw(background_name)

        draw.text((0,25), name, font=font, fill=(0, 0, 0, 255))
        draw.text((1,25), name, font=font, fill=(255, 255, 255, 255))

        draw.text((0,45), level, font=font, fill=(0, 0, 0, 255))
        draw.text((1,45), level, font=font, fill=(255, 255, 255, 255))

        return background_name
    
    
    async def start(self):
        total_bg = Image.new("RGBA", (425,797), (0,0,0,0))
        frams_up, frams = await frame_bg(self.character.rarity)
        blink = _of.blink_bg_five.convert("RGBA")
        shadow = _of.shadow_bg_five.convert("RGBA")
        
        bg_task = self.creat_charters()
        lc_task = self.creat_lk()
        const_task = self.creat_constant()
        stats_task = self.creat_stats()
        ms, ds, minst = await self.main_skills()
        name_task = self.creat_name_banner()

        relic_tasks = [self.creat_relics(key) for key in self.character.relics]

        bg, lc, const, stats, name, *relics = await asyncio.gather(
            bg_task, lc_task, const_task, stats_task, name_task, *relic_tasks
        )

        

        total_bg.alpha_composite(frams,(0,6))
        total_bg.alpha_composite(bg,(29,124))
        total_bg.alpha_composite(shadow,(29,124))
        total_bg.alpha_composite(blink,(0,0))
        total_bg.alpha_composite(frams_up,(0,0))
        
        total_bg.alpha_composite(lc,(36,0))
        total_bg.alpha_composite(const,(0,146))
        total_bg.alpha_composite(stats,(41,694))
        
        total_bg.alpha_composite(ms,(374,411))
        total_bg.alpha_composite(ds,(45,640))
        total_bg.alpha_composite(minst,(286,642))
        total_bg.alpha_composite(name,(45,564))
        
        position = {
            "1": (370,152),
            "2": (370,216),
            "3": (370,280),
            "4": (370,344),
            "5": (3,447),
            "6": (3,508)
            
        }
        
        for key in relics:
            total_bg.alpha_composite(key["img"], position[key["position"]])
        
        data = {
            "id": self.character.id,
            "name": self.character.name,
            "rarity": self.character.rarity,
            "card": total_bg,
            "size": total_bg.size
        }
        
        return data