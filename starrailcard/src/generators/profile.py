# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import asyncio, time
from PIL import ImageDraw,Image
from ..tools import pill, openFile, calculator
from collections import defaultdict

_of = openFile.ImageCache()


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


async def open_frame_charter(x):
    if x == 5:
        return _of.frame_stars_charters_5
    else:
        return _of.frame_stars_charters_4

async def open_element_panel(name):
    if name == "Wind":
        return _of.element_wind.copy()
    if name == "Fire":
        return _of.element_fire.copy()
    if name == "Ice":
        return _of.element_ice.copy()
    if name == "Thunder":
        return _of.element_electro.copy()
    if name == "Quantum":
        return _of.element_quantom.copy()
    if name == "Imaginary":
        return _of.element_IMAGINARY.copy()
    else:
        return _of.element_psyhical.copy()

async def get_stars(x, v = False):
    if v:
        pass
    else:
        if x == 4:
            return _of.stars_four
        else:
            return _of.stars_five


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

class Creat:

    def __init__(self,data,lang,img,hide) -> None:
        self.user = data.player
        self.characters = data.characters
        self.lang = lang
        self.img = img
        self.hide = hide


    async def creat_banner(self):
        if self.img:
            bg = await pill.get_centr_honkai_art((694,314),self.img)
            bg.alpha_composite(_of.bg_shadow,(0,262))
            return bg 
        else:
            return _of.default_bg.copy()
        
    async def creat_name_banner(self):
        bg = _of.name_frame.copy()
        d = ImageDraw.Draw(bg)
        font = await pill.get_font(16)
        
        x = 74 - int(font.getlength(self.user.nickname)/2)
        d.text((x, -3), self.user.nickname, font=font, fill=(255, 255, 255, 255))

        if self.hide:
            d.text((19,21), "UID: HIDDEN", font=font, fill=(255, 255, 255, 255))
        else:
            d.text((19, 21), f"UID: {self.user.uid}", font=font, fill=(255, 255, 255, 255))

        x = 69 - int(font.getlength(f"{self.lang.lvl}: {self.user.level}")/2)
        d.text((x, 44), f"{self.lang.lvl}: {self.user.level}", font=font, fill=(255, 255, 255, 255)) #-4

        d.text((134, 44), f"{self.lang.WL}:{self.user.world_level}", font=font, fill=(219, 194, 145, 255))
        
        return bg

    async def creat_bg_banner(self):
        frame_bg = await pill.apply_blur_and_overlay(self.img, (681, 459))
        dark_shadow = Image.new("RGBA", (681, 459), (0, 0, 0, 190))
        frame_bg.alpha_composite(dark_shadow, (0,0))

        return frame_bg


    async def creat_lc(self,data):
        bg = Image.new("RGBA", (149, 60), (0, 0, 0, 0))
        if data is None:
            return bg
        icon = await pill.get_dowload_img(data.icon, size= (60,60))
        bg.alpha_composite(icon,(0,0))

        d = ImageDraw.Draw(bg)

        max_level = await max_lvl(data.promotion)
        level = f"{self.lang.lvl}: {data.level}/{max_level}"
        sets_name_font,size = await pill.get_text_size_frame(level,12,88)
        d.text((59, 10), level, font=sets_name_font, fill=(219, 194, 145, 255))
        ups_info = await ups(data.rank)
        font = await pill.get_font(17)
        up = _of.ups.copy()
        d = ImageDraw.Draw(up)
        d.text((4,-3), ups_info, font=font, fill=(219, 194, 145, 255))
        bg.alpha_composite(up.resize((17,17)),(60,30))

        stars = await get_stars_icon(data.rarity)
        bg.alpha_composite(stars.resize((65,18)),(80,29))


        return bg


    async def creat_charters(self, character):
        name = character.name
        element_panel_task = open_element_panel(character.element.id)
        path_task = pill.get_dowload_img(character.path.icon, size=(31, 30))
        icon_task = pill.get_dowload_img(character.preview, size=(149, 202))
        frame_task = open_frame_charter(character.rarity)
        stars_task = get_stars(character.rarity)
        ups_info_task = ups(character.rank)
        font_task = pill.get_font(17)
        sets_name_font_task = pill.get_text_size_frame(name, 18, 153)
        max_level_task = max_lvl(character.promotion)
        element_panel, path, icon, frame, stars, ups_info, font, sets_name_font, max_level = await asyncio.gather(
            element_panel_task, path_task, icon_task, frame_task, stars_task, ups_info_task, font_task, sets_name_font_task, max_level_task
        )

        bg = _of.charter_icon_bg.copy()
        bg.alpha_composite(icon, (4, -7))
        bg.alpha_composite(path, (8, 5))
        bg.alpha_composite(element_panel.resize((135, 30)), (11, 154))
        bg.alpha_composite(frame, (0, 0))
        bg.alpha_composite(stars, (136, 47))

        up = _of.ups.copy()
        d = ImageDraw.Draw(up)
        d.text((4, -3), ups_info, font=font, fill=(219, 194, 145, 255))
        bg.alpha_composite(up, (13, 47))

        draw = ImageDraw.Draw(bg)
        draw.text((161, 0), name, font=sets_name_font[0], fill=(255, 255, 255, 255))
        level = f"{self.lang.lvl}: {character.level}/{max_level}"
        draw.text((161, 31), level, font=font, fill=(255, 255, 255, 255))

        stats_bg = _of.stats_frame_icon.copy()
        draw = ImageDraw.Draw(stats_bg)
        position = [
            (102, -6),
            (25, -6),
            (25, 27),
            (102, 27),
        ]

        combined_attributes = defaultdict(float)

        for attribute in character.attributes[:4] + character.additions:
            if attribute.field in ["hp", "def", "atk", "spd"]:
                combined_attributes[attribute.field] += attribute.value

        for i, (key, value) in enumerate(combined_attributes.items()):
            draw.text(position[i], str(round(value)), font=font, fill=(255, 255, 255, 255))
        
        bg.alpha_composite(stats_bg, (175, 63))

        lc = await self.creat_lc(character.light_cone)

        bg.alpha_composite(lc, (167, 124))

        return bg



    async def create_empty_frame_bg(self):
        return Image.new("RGBA", (681, 459), (0, 0, 0, 0))

    async def start(self):
        bg_two = Image.new("RGBA", (694, 802), (36, 36, 36, 255))

        banner, banner_name, frame_bg = await asyncio.gather(
            self.creat_banner(),
            self.creat_name_banner(),
            self.creat_bg_banner() if self.img else self.create_empty_frame_bg()
        )

        banner.alpha_composite(banner_name, (-13, 220))
        bg_two.alpha_composite(banner, (0, 0))
        bg_two.alpha_composite(frame_bg, (6, 336))
        bg_two.alpha_composite(_of.total_bg_frame, (0, 0))

        character_tasks = [self.creat_charters(key) for key in self.characters]
        characters = await asyncio.gather(*character_tasks)

        position = [
            (15, 391),
            (350, 391),
            (15, 588),
            (350, 588)
        ]
        
        for key, pos in zip(characters, position):
            bg_two.alpha_composite(key, pos)

        return bg_two
