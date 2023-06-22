# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import asyncio
from PIL import ImageDraw,Image
from ..tools import pill, openFile, treePaths

_of = openFile.ImageCache()


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

class Creat:

    def __init__(self,characters, lang,img,hide,uid,name,background) -> None:
        self.character = characters
        self.lang = lang
        self.img = img
        self.hide = hide
        self.uid = uid
        self.name = name
        self.background = background
    
    async def creat_constant(self):
        background_skills = Image.new("RGBA", (74, 363), (0, 0, 0, 0))
        y = 11
        rank = self.character.rank

        tasks = []
        for key in self.character.rank_icons[:rank]:
            tasks.append(self.create_open_icon(key, background_skills, y))
            y += 58

        for key in self.character.rank_icons[rank:]:
            tasks.append(self.create_closed_icon(key, background_skills, y))
            y += 58

        await asyncio.gather(*tasks)

        return background_skills

    async def create_open_icon(self, icon_key, background, position):
        icon = await pill.get_dowload_img(icon_key, size=(123, 124))
        bg = _of.open.copy()
        bg.alpha_composite(icon, (20, 19))
        background.alpha_composite(bg.resize((52, 52)), (9, position))

    async def create_closed_icon(self, icon_key, background, position):
        bg = _of.Closed.copy()
        icon = await pill.get_dowload_img(icon_key, size=(123, 124))
        loock = _of.Lock
        bg.alpha_composite(icon, (20, 19))
        bg.alpha_composite(loock, (0, 0))
        background.alpha_composite(bg.resize((52, 52)), (9, position))

    async def creat_charters(self):
        if self.img:
            bg_new = _of.bg_charters.copy()
            bg = bg_new.copy()
            user_image = await pill.get_resize_image(self.img, 478, 342)
            if user_image["type"] == 2:
                bg_new.alpha_composite(user_image["img"], (0, 0))
            else:
                bg_new.alpha_composite(user_image["img"], (int(174 - user_image["img"].size[0] / 2), 0))
            
            bg.paste(bg_new, (0, 0), _of.maska_charters.convert("L"))
        else:
            bg_new = _of.bg_charters.copy()
            image = await pill.get_dowload_img(self.character.preview)
            bg_new.alpha_composite(image, (-17, 9))
            bg = _of.bg_charters.copy()
            bg.paste(bg_new, (0, 0), _of.maska_charters.convert("L"))

        frame = _of.frame_charters.copy()

        tasks = []
        tasks.append(self.create_charters_image(frame, bg))

        await asyncio.gather(*tasks)

        return frame

    async def create_charters_image(self, frame, bg):
        path = await pill.get_dowload_img(self.character.path.icon, size=(40, 36))
        element = await pill.get_dowload_img(self.character.element.icon, thumbnail_size=(46, 46))
        stars = await get_stars_icon(self.character.rarity)

        frame.alpha_composite(path, (93, 493))
        frame.alpha_composite(element, (145, 488))
        frame.alpha_composite(stars.resize((69, 18)), (258, 519))
        max_level = await max_lvl(self.character.promotion)
        level = f"{self.lang.lvl}: {self.character.level}/{max_level}"
        prom = f"A{self.character.promotion}"

        d = ImageDraw.Draw(frame)
        font, size = await pill.get_text_size_frame(level, 22, 176)
        d.text((int(290 - size / 2), 483), level, font=font, fill=(255, 255, 255, 255))

        font, size = await pill.get_text_size_frame(self.character.name, 24, 304)
        d.text((int(229 - size / 2), -5), self.character.name, font=font, fill=(255, 255, 255, 255))

        font = await pill.get_font(24)
        x = int(font.getlength(prom) / 2)
        d.text((36 - x, 39), prom, font=font, fill=(255, 207, 131, 255))

        background_skills = await self.creat_constant()
        frame.alpha_composite(background_skills, (0, 77))
        frame.alpha_composite(bg, (45, 21))

        return frame

    async def creat_light_cone(self):
        bg_new = _of.bg_lc.copy()
        if self.character.light_cone is None:
            return Image.new("RGBA", (0,0), (0,0,0,0))
        image = await pill.get_dowload_img(self.character.light_cone.portrait, size=(203,276))
        bg_new.alpha_composite(image,(8,5))
        bg = _of.bg_lc.copy()
        bg.paste(bg_new,(0,0),_of.maska_lc.convert("L"))

        frame = _of.bg_lc_total.copy()

        tasks = []
        tasks.append(self.create_light_cone_image(frame, bg))

        await asyncio.gather(*tasks)

        return frame

    async def create_light_cone_image(self, frame, bg):
        path = await pill.get_dowload_img(self.character.light_cone.path.icon, size= (38,39))
        stars = await get_stars_icon(self.character.light_cone.rarity)
        rank = f"S{self.character.light_cone.rank}"
        max_level = await max_lvl(self.character.light_cone.promotion)
        level = f"{self.lang.lvl}: {self.character.light_cone.level}/{max_level}"

        frame.alpha_composite(path, (321,179))
        frame.alpha_composite(stars.resize((84,23)),(323,227))

        d = ImageDraw.Draw(frame)
        font,size = await pill.get_text_size_frame(level, 14, 84)
        d.text((int(366-size/2),146), level, font= font, fill=(255,255,255,255))

        font = await pill.get_font(24)
        x = int(font.getlength(rank)/2)
        d.text((384-x,184), rank, font= font, fill=(255,207,131,255))

        HP = self.character.light_cone.attributes[0].display
        ATK = self.character.light_cone.attributes[1].display
        DF = self.character.light_cone.attributes[2].display

        font = await pill.get_font(24)
        x = int(font.getlength(HP))
        d.text((302-x,145), HP, font= font, fill=(255,255,255,255))
        x = int(font.getlength(ATK))
        d.text((302-x,177), ATK, font= font, fill=(255,255,255,255))
        x = int(font.getlength(DF))
        d.text((302-x,208), DF, font= font, fill=(255,255,255,255))

        names = await pill.create_image_with_text(self.character.light_cone.name, 16, max_width=211, color=(255, 255, 255, 255))
        x_names = 310 - names.size[0] // 2
        frame.alpha_composite(names, (x_names, 105-names.size[1]))

        frame.alpha_composite(bg,(0,0))

    async def creat_stats(self):
        bg_new = _of.STATS.copy()

        combined_attributes = {}

        for attribute in self.character.attributes + self.character.additions:
            field = attribute.field
            if field in combined_attributes:
                combined_attributes[field].value += attribute.value
            else:
                combined_attributes[field] = attribute

        x_icon, y_icon, x_text, y_text = 20, 10, 130, 10
        d = ImageDraw.Draw(bg_new)
        font = await pill.get_font(24)

        for i, attribute in enumerate(combined_attributes.values()):
            icon = await pill.get_dowload_img(attribute.icon, size=(32, 34))
            bg_new.alpha_composite(icon, (x_icon, y_icon))

            value = "{:.1f}%".format(attribute.value * 100) if attribute.percent else round(attribute.value)
            x = x_text - int(font.getlength(str(value)))
            d.text((x, y_text), str(value), font=font, fill=(255, 255, 255, 255))

            y_icon += 43
            y_text += 43

            if (i + 1) % 4 == 0:
                y_icon = 10
                y_text = 10
                x_icon += 133
                x_text += 140

        return bg_new
                
    async def creat_info_user(self):
        bg = _of.uid.copy()
        font, font_uid = await asyncio.gather(
            pill.get_font(30),
            pill.get_font(18)
        )

        d = ImageDraw.Draw(bg)

        x = 124 - int(font.getlength(self.name) / 2)
        d.text((x, -5), self.name, font=font, fill=(255, 255, 255, 255))

        uid_text = f"UID: HIDDEN" if self.hide else f"UID: {self.uid}"
        d.text((22, 44), uid_text, font=font_uid, fill=(255, 255, 255, 255))

        return bg

    async def main_skills(self):
        bg = _of.bg_main.copy()
        positions = [
            (24, 13), (111, 13),
            (24, 85), (111, 85),
        ]

        tasks = []
        for i, key in enumerate(self.character.skills[:4]):
            tasks.append(self.create_skill_icon(bg, key, positions[i]))

        await asyncio.gather(*tasks)
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

    async def create_sets(self):
        font = await pill.get_font(20)
        fontC = await pill.get_font(14)

        rel_set = {}
        for key in self.character.relic_sets:
            if key.id not in rel_set:
                if key.properties == []:
                    rel_set[key.id] = {"num": int(key.num), "icon": key.icon, "properties": None}
                else:
                    rel_set[key.id] = {"num": int(key.num), "icon": key.icon, "properties": {"icon": key.properties[0].icon, "display": key.properties[0].display}}
            else:
                rel_set[key.id]["num"] = int(key.num)

        if len(rel_set) == 0:
            return Image.new("RGBA", (266, 98), (0, 0, 0, 0))

        tasks = []
        pos = [
            (0, 0),
            (86, 0),
            (172, 0),
        ]
        for key in rel_set:
            tasks.append(self.create_set_image(rel_set[key], pos.pop(0), font, fontC))

        images = await asyncio.gather(*tasks)
        combined = Image.new("RGBA", (266, 98), (0, 0, 0, 0))
        for image in images:
            combined.alpha_composite(image)

        return combined

    async def create_set_image(self, set_data, position, font, fontC):
        frame = _of.sets_bg.copy()
        count = _of.sets_count.copy()

        d = ImageDraw.Draw(count)
        d.text((15, 2), str(set_data["num"]), font=font, fill=(144, 238, 144, 255))

        d = ImageDraw.Draw(frame)
        icon = await pill.get_dowload_img(set_data["icon"], size=(56, 56))
        if set_data["properties"] is not None:
            icon_stats = await pill.get_dowload_img(set_data["properties"]["icon"], size=(23, 24))
            frame.alpha_composite(icon_stats, (10, 62))
            d.text((31, 63), str(set_data["properties"]["display"]), font=fontC, fill=(255, 255, 255, 255))

        frame.alpha_composite(icon, (17, 8))
        frame.alpha_composite(count, (52, 0))

        image = Image.new("RGBA", (266, 98), (0, 0, 0, 0))
        image.alpha_composite(frame, position)
        return image

    async def creat_relics(self, relics):
        bg = _of.ARTIFACT.copy()

        icon_rel = await pill.get_dowload_img(relics.icon, size=(59, 53))
        icon = await pill.get_dowload_img(relics.main_affix.icon, size=(25, 26))
        display = relics.main_affix.display
        level = f"+{relics.level}"
        stars = await get_stars_icon(relics.rarity)

        bg.alpha_composite(icon_rel, (15, 21))
        bg.alpha_composite(icon, (10, 72))
        bg.alpha_composite(stars.resize((54, 15)), (19, 0))

        d = ImageDraw.Draw(bg)

        font = await pill.get_font(16)
        x = int(font.getlength(display))
        d.text((80 - x, 73), str(display), font=font, fill=(255, 255, 255, 255))

        font = await pill.get_font(15)
        x = int(font.getlength(level) / 2)
        d.text((61 - x, 91), level, font=font, fill=(255, 207, 132, 255))

        position = 18
        tasks = []
        for k in relics.sub_affix:
            tasks.append(self.create_sub_affix_image(k, bg, position))
            position += 24

        await asyncio.gather(*tasks)

        return bg

    async def create_sub_affix_image(self, sub_affix, bg, position):
        icon = await pill.get_dowload_img(sub_affix.icon, size=(25, 26))
        value = sub_affix.display

        d = ImageDraw.Draw(bg)
        font = await pill.get_font(16)
        x = int(font.getlength(value))
        d.text((157 - x, position), str(value), font=font, fill=(255, 255, 255, 255))
        bg.alpha_composite(icon, (85, position))

    async def start(self):
        if self.background:
            bg = _of.total_bg.copy().convert("RGBA")
        else:
            bg = Image.new("RGBA", (1015,696), (0,0,0,0))

        tasks = [
            self.creat_charters(),
            self.creat_light_cone(),
            self.creat_stats(),
            self.creat_info_user(),
            self.main_skills(),
            self.create_sets(),
            self.dop_stats()
        ]

        backg, lc, stats, user, main_skills, sets, stats_dop = await asyncio.gather(*tasks)

        operations = [
            (backg, (190, 5)),
            (lc, (588, 77)),
            (stats, (585, 365)),
            (user, (4, 5)),
            (main_skills, (-2, 74)),
            (stats_dop, (-2, 229)),
            (sets, (0, 451)),
            (_of.logo, (679, 11))
        ]

        for image, position in operations:
            bg.alpha_composite(image, position)

        relic_tasks = [self.creat_relics(key) for key in self.character.relics]
        relics = await asyncio.gather(*relic_tasks)

        if relics == []:
            bg = bg.crop((0, 0, 1015, 556))

        position = 6

        for i, key in enumerate(relics):
            bg.alpha_composite(key, (position, 556))

            if (i + 1) % 4 == 0:
                position += 185
            else:
                position += 163

        data = {
            "id": self.character.id,
            "name": self.character.name,
            "rarity": self.character.rarity,
            "card": bg,
            "size": bg.size
        }

        return data

        