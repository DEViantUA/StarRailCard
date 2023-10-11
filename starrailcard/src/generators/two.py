# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import asyncio
from PIL import ImageDraw,Image
from ..tools import pill, openFile, treePaths, calculator

_of = openFile.ImageCache()




async def bg_element(name):
    if name == "Wind":
        return _of.bg_wind.copy()
    if name == "Fire":
        return _of.bg_fire.copy()
    if name == "Ice":
        return _of.bg_ice.copy()
    if name == "Thunder":
        return _of.bg_electro.copy()
    if name == "Quantum":
        return _of.bg_quantom.copy()
    if name == "Imaginary":
        return _of.bg_imaginary.copy()
    else:
        return _of.bg_psyhical.copy()
    
async def bg_relic_element(name):
    if name == "Wind":
        return _of.bg_relic_ANEMO.copy()
    if name == "Fire":
        return _of.bg_relic_FIRE.copy()
    if name == "Ice":
        return _of.bg_relic_ICE.copy()
    if name == "Thunder":
        return _of.bg_relic_ELECTRO.copy()
    if name == "Quantum":
        return _of.bg_relic_QUANTOM.copy()
    if name == "Imaginary":
        return _of.bg_relic_IMAGINARY.copy()
    else:
        return _of.bg_relic_PSYHICAL.copy()

async def get_stars_icon(x):
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


async def get_quality_color(rank):
    if rank == "SSS":
        return (255, 0, 0, 255)  # Ярко-красный цвет (Bright Red)
    elif rank == "SS":
        return (255, 69, 0, 255)  # Ярко-оранжевый цвет (Bright Orange)
    elif rank == "S":
        return (255, 215, 0, 255)  # Ярко-желтый цвет (Bright Yellow)
    elif rank == "A":
        return (0, 255, 0, 255)  # Ярко-зеленый цвет (Bright Green)
    elif rank == "B":
        return (50, 205, 50, 255)  # Зеленый цвет (Green)
    elif rank == "C":
        return (0, 255, 255, 255)  # Ярко-голубой цвет (Bright Cyan)
    elif rank == "D":
        return (0, 0, 255, 255)  # Ярко-синий цвет (Bright Blue)
    else:
        return (128, 128, 128, 255)  # Серый цвет (Gray)
    

async def get_eff_color(rank):
    if rank == 4:
        return (168, 234, 8, 255)
    elif rank == 3:
        return (234, 179, 8, 255)
    elif rank == 2:
        return (248, 113, 113, 255)
    elif rank == 1:
        return (161, 98, 7, 255) 
    else:
        return (128, 128, 128, 255)


async def get_path_img(path):
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



async def icon_tree(type,icon):
    if type == 2:
        icon = await pill.get_dowload_img(f'https://raw.githubusercontent.com/FortOfFans/HSR/main/skillIcon/{icon}.png', size=(47, 47))
    elif type== 3:
        icon = await pill.get_dowload_img(f'https://raw.githubusercontent.com/FortOfFans/HSR/main/skillIconblack/{icon}.png', size=(47, 47))
    else:
        icon = await pill.get_dowload_img(f'https://raw.githubusercontent.com/FortOfFans/HSR/main/statsblack/{icon}.png', size=(36, 36))

    return icon

class Creat:

    def __init__(self,characters, lang,img,hide,uid) -> None:
        self.character = characters
        self.lang = lang
        self.img = img
        self.hide = hide
        self.uid = uid
    

    async def creat_name_banner(self):
        background_name = Image.new("RGBA", (335,113), (0,0,0,0))
        font = await pill.get_font(35)

        icon_element = await pill.get_dowload_img(self.character.element.icon, thumbnail_size=(56,56))
        stars = await get_stars_icon(self.character.rarity)
        level = f"{self.lang.lvl}: {self.character.level}/80"
        name = self.character.name

        background_name.alpha_composite(icon_element,(0,8))
        background_name.alpha_composite(stars,(0,72))

        draw = ImageDraw.Draw(background_name)

        draw.text((58,-2), name, font=font, fill=(0, 0, 0, 255))
        draw.text((60,-3), name, font=font, fill=(255, 255, 255, 255))

        draw.text((59,32), level, font=font, fill=(0, 0, 0, 255))
        draw.text((60,30), level, font=font, fill=(255, 255, 255, 255))
        return background_name


    async def creat_constant(self):
        background_skills = Image.new("RGBA", (68, 498), (0, 0, 0, 0))
        y = 0
        rank = self.character.rank

        tasks = []
        for key in self.character.rank_icons[:rank]:
            tasks.append(self.create_open_icon(key, background_skills, y))
            y += 86

        for key in self.character.rank_icons[rank:]:
            tasks.append(self.create_closed_icon(key, background_skills, y))
            y += 86

        await asyncio.gather(*tasks)
        return background_skills

    async def create_open_icon(self, icon_key, background, position):
        icon = await pill.get_dowload_img(icon_key, size=(129, 130))
        bg = _of.open.copy()
        bg.alpha_composite(icon, (17, 16))
        background.alpha_composite(bg.resize((68, 68)), (0, position))

    async def create_closed_icon(self, icon_key, background, position):
        bg = _of.Closed.copy()
        icon = await pill.get_dowload_img(icon_key, size=(129, 130))
        loock = _of.Lock
        bg.alpha_composite(icon, (17, 16))
        bg.alpha_composite(loock, (0, 0))
        background.alpha_composite(bg.resize((68, 68)), (0, position))


    async def creat_charters(self):
        bg = await bg_element(self.character.element.id)
        if self.img:
            bg = await pill.creat_user_image(self.img,teampl="1",shadow=_of.shadow, bg = bg)
        else:
            bg = await pill.creat_bg_teample_two(self.character.portrait,bg, _of.MASKA_ART.convert("L"))
        return bg
    
    async def creat_lc(self):
        bg_new = Image.new("RGBA", (192, 268), (0, 0, 0, 0))
        frame = Image.new("RGBA", (424, 268), (0, 0, 0, 0))

        if self.character.light_cone is None:
            return Image.new("RGBA", (0, 0), (0, 0, 0, 0))

        # Load images
        light_cone = self.character.light_cone
        lc_mask = _of.Maska_LC.convert("L")
        lc_shadow = _of.shadow_LC
        lc_icons = _of.icons_LC

        # Load fonts
        font_23 = await pill.get_font(23)
        font_24 = await pill.get_font(24)

        # Create images
        image = await pill.get_dowload_img(light_cone.portrait, size=(192, 268))
        icon = await pill.get_dowload_img(light_cone.icon, size=(106, 108))
        stars = await get_stars_icon(light_cone.rarity)
        max_level = await max_lvl(light_cone.promotion)
        path_icon = await pill.get_dowload_img(light_cone.path.icon, size=(39, 39))
        names = await pill.create_image_with_text(light_cone.name, 17, max_width=170, color=(255, 255, 255, 255))

        # Compose images
        bg_new.paste(image, (0, 0), lc_mask)
        bg_new.alpha_composite(lc_shadow, (0, 0))

        frame.alpha_composite(bg_new, (61, 0))
        frame.alpha_composite(icon, (8, 64))
        frame.alpha_composite(stars, (0, 171))
        frame.alpha_composite(path_icon, (18, 209))
        frame.alpha_composite(lc_icons, (256, 91))

        # Draw text
        d = ImageDraw.Draw(frame)
        d.text((65, 206), f"{self.lang.lvl}: {light_cone.level}/{max_level}", font=font_23, fill=(255, 255, 255, 255))
        d.text((65, 233), f"S{light_cone.rank}", font=font_23, fill=(255, 207, 131, 255))
        d.text((284, 82), light_cone.attributes[0].display, font=font_24, fill=(255, 255, 255, 255))
        d.text((284, 115), light_cone.attributes[1].display, font=font_24, fill=(255, 255, 255, 255))
        d.text((284, 144), light_cone.attributes[2].display, font=font_24, fill=(255, 255, 255, 255))
        frame.alpha_composite(names, (255, 59 - names.size[1]))

        return frame


    async def create_sub_affix_image(self, sub_affix, bg, position):
        icon = await pill.get_dowload_img(sub_affix.icon, size=(26, 26))
        value = sub_affix.display

        d = ImageDraw.Draw(bg)
        font = await pill.get_font(21)
        x = int(font.getlength(value))
        d.text((236 - x, position), str(value), font=font, fill=(255, 255, 255, 255))
        bg.alpha_composite(icon, (138, position))

    async def creat_relics(self, relics):
        bg = await bg_relic_element(self.character.element.id)
        bg_two = Image.new("RGBA", (261,198), (0,0,0,0))
        bg_r = Image.new("RGBA", (261,198), (0,0,0,0))
        icon_rel = await pill.get_dowload_img(relics.icon, size=(180, 179))
        bg_r.alpha_composite(icon_rel,(0,1))
        
        icon = await pill.get_dowload_img(relics.main_affix.icon, size=(36, 36))
        display = relics.main_affix.display
        level = f"+{relics.level}"
        stars = await get_stars_icon(relics.rarity)
        stars = stars.resize((89,25))
        
        bg_two.paste(bg_r, (0,0),_of.relic_mask.convert("L"))
        bg.alpha_composite(bg_two, (0,0))
        bg.alpha_composite(icon, (202, 7))
        bg.alpha_composite(stars, (51, 150))
        bg.alpha_composite(_of.relic_frame, (125, 43))

        d = ImageDraw.Draw(bg)

        font = await pill.get_font(31)
        x = int(font.getlength(display))
        d.text((196 - x, 3), str(display), font=font, fill=(0,0,0, 255))
        d.text((197 - x, 3), str(display), font=font, fill=(255, 255, 255, 255))

        font = await pill.get_font(23)
        x = int(font.getlength(level) / 2)
        d.text((209 - x, 35), level, font=font, fill=(249, 195, 110, 255))

        position = 71
        tasks = []
        for k in relics.sub_affix:
            tasks.append(self.create_sub_affix_image(k, bg, position))
            position += 25

        await asyncio.gather(*tasks)

        score, rank, eff = await calculator.get_rating(relics,self.character.id,str(relics.id[-1:]))
        
        rank_bg = _of.rank.copy()
        color = await get_quality_color(rank)
        color_eff = await get_eff_color(eff)

        d = ImageDraw.Draw(rank_bg)
        font = await pill.get_font(14)

        d.text((46, -4), rank, font=font, fill=color)
        d.text((139, -4), str(eff), font=font, fill=color_eff)
        d.text((213, -4), str(score), font=font, fill=color)

        bg.alpha_composite(rank_bg,(11,182))
        return {"img": bg, "stats": {"eff": eff, "score": score}}

    async def creat_stats(self):
        bg_new = Image.new("RGBA", (346,381), (0,0,0,0))

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
        position_icon = [
            (0,0), (200,0),
            (0,67), (200,67),
            (0,134), (200,134),
            (0,201), (200,201),
            (0,268), (200,268),
            (0,335), (200,335),
        ]

        position_text = 143
        position_text_dop_y = [33,33,100,100,167,167,234,234]

        d = ImageDraw.Draw(bg_new)
        font = await pill.get_font(25)
        font_dop = await pill.get_font(13)
        z = 0
        for i, attribute in enumerate(combined_attributes):
            stat = combined_attributes[attribute]
            bg = _of.stats_frame.copy()
            icon = await pill.get_dowload_img(stat.icon, size=(128, 128))
            bg.alpha_composite(icon,(0,0))
            bg = bg.resize((46,46))
            
            bg_new.alpha_composite(bg,position_icon[i])

            value = "{:.1f}%".format(stat.value * 100) if stat.percent else round(stat.value)
            if attribute in dop:
                x = position_text - int(font.getlength(str(value)))
                d.text((x, position_icon[i][1]-3), str(value), font=font, fill=(255, 255, 255, 255))

                x = position_text - int(font_dop.getlength(dop[attribute]["dop"]))
                d.text((x, position_text_dop_y[z]-5), dop[attribute]["dop"], font=font_dop, fill=(249, 195, 110, 255))

                x = x - int(font_dop.getlength(dop[attribute]["main"])) - 5
                d.text((x, position_text_dop_y[z]-5), dop[attribute]["main"], font=font_dop, fill=(255, 255, 255, 255))
                z += 1
            else:
                x = position_text - int(font.getlength(str(value)))
                d.text((x, position_icon[i][1]), str(value), font=font, fill=(255, 255, 255, 255))
            
            if position_text == 143:
                position_text = 342
            else:
                position_text = 143
        return bg_new

    async def create_sets(self):
        font = await pill.get_font(22)

        rel_set = {}
        for key in self.character.relic_sets:
            if key.id not in rel_set:
                if key.properties == []:
                    rel_set[key.id] = {"num": int(key.num), "name": key.name, "icon": key.icon, "properties": None}
                else:
                    rel_set[key.id] = {"num": int(key.num), "name": key.name, "icon": key.icon, "properties": {"icon": key.properties[0].icon, "display": key.properties[0].display}}
            else:
                rel_set[key.id]["num"] = int(key.num)

        if len(rel_set) == 0:
            return Image.new("RGBA", (266, 98), (0, 0, 0, 0))

        tasks = []
        pos = [
            (0, 0),
            (0, 83),
            (0, 164),
        ]
        for key in rel_set:
            tasks.append(self.create_set_image(rel_set[key], font))

        images = await asyncio.gather(*tasks)
        combined = Image.new("RGBA", (367, 233), (0, 0, 0, 0))
        for _, image in enumerate(images):
            combined.alpha_composite(image.resize((367,69)), pos[_])
        return combined
 
    async def create_set_image(self, set_data, font):
        frame = _of.sets_relic.copy()
        d = ImageDraw.Draw(frame)
        d.text((393, 21), str(set_data["num"]), font=font, fill=(110, 249, 123, 255)) 
        sets_name_font,size = await pill.get_text_size_frame(set_data["name"],15,272)
        
        d.text((int(215-size/2), 27), set_data["name"], font=sets_name_font, fill=(110, 249, 123, 255))  
        icon = await pill.get_dowload_img(set_data["icon"], size=(78, 78))
        frame.alpha_composite(icon, (0,0))
        return frame

    async def main_skills(self):
        PATH = self.character.path.id

        font = await pill.get_font(16)
        bg = await get_path_img(PATH)
        dop_path_closed = _of.path_closed

        position = treePaths.point_map.get(PATH)
        for key in self.character.skill_trees:
            if key.max_level == 1:
                if key.anchor in ["Point05","Point06","Point07","Point08"]:
                    icon = await pill.get_dowload_img(key.icon, size=(47,47))
                else:
                    icon = await pill.get_dowload_img(key.icon, size=(36,36))
                if key.anchor == "Point05":
                    icon = await pill.recolor_image(icon, (247, 212, 168))
                else:
                    icon = await pill.recolor_image(icon, (0, 0, 0))

                bg.alpha_composite(icon, position[key.anchor]["icon"])
                if key.level == 0:
                    if key.anchor in ["Point05","Point06","Point07","Point08"]:
                        bg.alpha_composite(dop_path_closed, position[key.anchor]["icon"])
                    else:
                        bg.alpha_composite(dop_path_closed.resize((36,35)), position[key.anchor]["icon"])
            else:
                icon = await pill.get_dowload_img(key.icon, size=(47, 47))
                icon = await pill.recolor_image(icon,(247, 212, 168))
                count = _of.path_count.copy()
                draw = ImageDraw.Draw(count)
                draw.text((6,-5), f"{key.level}/{key.max_level}", font=font, fill=(255, 255, 255, 255))
                bg.alpha_composite(icon, position[key.anchor]["icon"]) 
                if "count" in  position[key.anchor]:
                    bg.alpha_composite(count, position[key.anchor]["count"]) 

        return bg      

    async def create_skill_icon(self, bg, skill, position):
        count = _of.count_talants.copy()
        d = ImageDraw.Draw(count)
        bg_talants = _of.bg_talants.copy()
        icon, font = await asyncio.gather(
            pill.get_dowload_img(skill.icon, size=(35, 30)),
            pill.get_font(14)
        )

        if skill.level > 9:
            d.text((3, -2), str(skill.level), font=font, fill=(255, 255, 255, 255))
        else:
            d.text((7, -2), str(skill.level), font=font, fill=(255, 255, 255, 255))

        bg_talants.alpha_composite(icon, (11, 14))
        bg_talants.alpha_composite(count, (17, 46))
        bg.alpha_composite(bg_talants, position)

    async def create_dop_stats_icon(self, bg_full, key, res, position, y):
        data_dop = []
        
        for keys in self.character.skill_trees:
            if str(keys.id) in res:
                data_dop.append(keys.icon)

        bg = _of.dop_0.copy() if len(data_dop) == 0 else \
            _of.dop_1.copy() if len(data_dop) == 1 else \
            _of.dop_2.copy() if len(data_dop) == 2 else \
            _of.dop_3.copy()

        icon_stats = await pill.get_dowload_img(key.icon, size=(35, 35))
        bg.alpha_composite(icon_stats, (3, 5))

        for i, icon in enumerate(data_dop):
            icons = await pill.get_dowload_img(icon, size=(29, 29))
            bg.alpha_composite(icons, (position[i], 7))
        bg_full.alpha_composite(bg, (19, y))

    async def dop_stats(self):
        bg_full = _of.bg_dop.copy()
        path = self.character.path.id

        position = [48, 83, 118]
        y = 20

        tasks = []
        for key in self.character.skill_trees:
            res = await treePaths.get_tree(path, key.id)  # ["08", "09", "10"]
            if res is None:
                continue
            tasks.append(self.create_dop_stats_icon(bg_full, key, res, position.copy(), y))
            y += 49

        await asyncio.gather(*tasks)
        return bg_full


    async def start(self):
        bg_two = Image.new("RGBA", (1916, 812), (0, 0, 0, 0))

        sets, bg, const, name, lc, stats, mainSkill = await asyncio.gather(
            self.create_sets(),
            self.creat_charters(),
            self.creat_constant(),
            self.creat_name_banner(),
            self.creat_lc(),
            self.creat_stats(),
            self.main_skills()
        )

        '''
        sets =  await self.create_sets()
        bg =  await self.creat_charters() #-
        const =  await self.creat_constant()
        name = await self.creat_name_banner()
        lc = await self.creat_lc() #-
        stats = await self.creat_stats()
        mainSkill = await self.main_skills() #-
        '''
        relic_tasks = [self.creat_relics(key) for key in self.character.relics]
        relics = await asyncio.gather(*relic_tasks)
        bg_two.alpha_composite(bg, (0, 33))
        bg_two.alpha_composite(const, (25, 147))
        bg_two.alpha_composite(name, (541, 51))
        bg_two.alpha_composite(lc, (913, 55))
        bg_two.alpha_composite(stats, (541, 193))
        bg_two.alpha_composite(sets, (913, 341))
        bg_two.alpha_composite(mainSkill, (1343, 83))

        position = 243
        total_eff = 0
        total_score = 0
        for i, key in enumerate(relics):
            bg_two.alpha_composite(key["img"], (position, 606))
            total_eff += key["stats"]["eff"]
            total_score += key["stats"]["score"]
            if (i + 1) % 4 == 0:
                position += 315
            else:
                position += 270

        total_stats_frame = _of.total_stats_frame.copy()
        d = ImageDraw.Draw(total_stats_frame)
        font = await pill.get_font(23)
        rank = await calculator.get_total_rank(total_score)
        color = await  get_quality_color(rank)
        color_eff = await  get_eff_color(total_eff)

        d.text((250, -6), rank, font=font, fill=color)
        d.text((374, -6), str(total_eff), font=font, fill=color_eff)
        d.text((627, -6), str(round(total_score, 2)), font=font, fill=color)
        uid_text = f"UID: HIDDEN" if self.hide else f"UID: {self.uid}"
        d = ImageDraw.Draw(bg_two)
        d.text((25, 715), uid_text, font=font, fill=(255, 255, 255, 255))
        bg_two.alpha_composite(total_stats_frame, (59, 4))
        data = {
            "id": self.character.id,
            "name": self.character.name,
            "rarity": self.character.rarity,
            "card": bg_two,
            "size": bg_two.size
        }
        return data



