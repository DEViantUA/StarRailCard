# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import asyncio, time
from PIL import ImageDraw,Image
from ..tools import pill, openFile, calculator

_of = openFile.ImageCache()




async def open_frame_lc(x):
    if x == 5:
        return _of.lc_5_stars
    elif x == 4:
        return _of.lc_4_stars
    else:
        return _of.lc_3_stars

async def get_open_frame_art(x):
    if x == 5:
        return _of.frame_art_5.copy()
    elif x == 4:
        return _of.frame_art_4.copy()
    elif x == 3:
        return _of.frame_art_3.copy()
    elif x == 2:
        return _of.frame_art_2.copy()
    else:
        return _of.frame_art_1.copy()


async def get_stars_icon(x, v = 1):
    if v == 1:
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
        if x == 4:
            return _of.stars_four
        else:
            return _of.stars_five


async def ups(x):
    if x == 5:
        return "V"
    elif x == 5:
        return "IV"
    elif x == 5:
        return "III"
    elif x == 5:
        return "II"
    elif x == 5:
        return "I"
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

class Creat:

    def __init__(self,characters, lang,img,hide,uid,seeleland) -> None:
        self.seeleland = seeleland
        self.character = characters
        self.lang = lang
        self.img = img
        self.hide = hide
        self.uid = uid

    async def creat_lk(self):
        bg_new = Image.new("RGBA", (401, 238), (0, 0, 0, 0))
        lc = Image.new("RGBA", (175, 239), (0, 0, 0, 0))
        if self.character.light_cone is None:
            return Image.new("RGBA", (0, 0), (0, 0, 0, 0))
        image = await pill.get_dowload_img(self.character.light_cone.portrait, size=(151, 213))
        frame = await open_frame_lc(self.character.light_cone.rarity)
        stars = await get_stars_icon(self.character.light_cone.rarity)
        
        lc.alpha_composite(frame,(10,12))
        lc.alpha_composite(image,(12,14))
        lc.alpha_composite(_of.blink,(7,7))
        lc.alpha_composite(frame,(0,0))
        lc.alpha_composite(stars,(21,186))

        stat_icon = _of.lc_info.copy()
        stats = Image.new("RGBA", (167, 90), (0, 0, 0, 0))
        stats.alpha_composite(stat_icon,(0,0))
        d = ImageDraw.Draw(stats)
        max_level = await max_lvl(self.character.light_cone.promotion)


        font_20 = await pill.get_font(20)
        font_17 = await pill.get_font(17)

        d.text((31, -2), f"{self.lang.lvl}: {self.character.light_cone.level}/{max_level}", font=font_17, fill=(255, 255, 255, 255))
        d.text((5, -1), await ups(self.character.light_cone.rank), font=font_17, fill=(247, 212, 168, 255))
        d.text((28, 29), self.character.light_cone.attributes[0].display, font=font_20, fill=(255, 255, 255, 255))
        d.text((110, 29), self.character.light_cone.attributes[1].display, font=font_20, fill=(255, 255, 255, 255))
        d.text((28, 63), self.character.light_cone.attributes[2].display, font=font_20, fill=(255, 255, 255, 255))
        names = await pill.create_image_with_text(self.character.light_cone.name, 20, max_width=214, color=(255, 255, 255, 255))
        bg_new.alpha_composite(names, (184, 69 - names.size[1]))

        bg_new.alpha_composite(lc, (0,0))
        bg_new.alpha_composite(stats, (185,91))

        return bg_new
    
    async def creat_charters(self):
        bg = _of.splash_art.copy()
        if self.img:
            bg = await pill.creat_user_image_tree(self.img)
        else:
            bg = await pill.creat_bg_teample_two(self.character.portrait, bg, teample = 3)
        
        return bg


    async def main_skills(self):

        font = await pill.get_font(11)

        main_bg =  Image.new("RGBA", (291,58), (0, 0, 0, 0))
        position_main = 0

        dop_bg = Image.new("RGBA", (359,125), (0, 0, 0, 0))

        position_dop = (
            (0,0),
            (192,0),
            (0,71),
            (192,71),
            (63,14),
            (100,14),
            (137,14),
            (255,14),
            (292,14),
            (329,14),
            (63,84),
            (100,84),
            (137,84),
            (255,84),
            (292,84),
            (329,84),
        )
        
        i = 0
        for key in self.character.skill_trees:
            if key.max_level == 1:
                if key.anchor in ["Point05","Point06","Point07","Point08"]:
                    icon = await pill.get_dowload_img(key.icon, size=(38,38))
                else:
                    icon = await pill.get_dowload_img(key.icon, size=(30,30))
                    
                if key.level == 0:
                    if key.anchor in ["Point05","Point06","Point07","Point08"]:
                        bg = _of.dop.copy()
                        bg.alpha_composite(icon,(7,10))
                        bg.alpha_composite(_of.closed_main,(0,0))
                    else:
                        bg = _of.closed_trees.copy()
                        icon = await pill.recolor_image(icon,(247, 212, 168))
                        bg.alpha_composite(icon, (0,0))
                        bg.alpha_composite(icon, (0,0))
                else:
                    if key.anchor in ["Point05","Point06","Point07","Point08"]:
                        bg = _of.dop.copy()
                        bg.alpha_composite(icon,(7,10))
                    else:
                        bg = _of.open_trees.copy()
                        icon = await pill.recolor_image(icon, (0, 0, 0))
                        bg.alpha_composite(icon, (0,0))
                dop_bg.alpha_composite(bg, position_dop[i])
                i += 1
            else:
                icon = await pill.get_dowload_img(key.icon, size=(43, 43))
                icon = await pill.recolor_image(icon,(247, 212, 168))
                bg = _of.main_skills.copy()
                count = _of.count_tree.copy()
                bg.alpha_composite(icon,(4,4))
                draw = ImageDraw.Draw(count)

                x = int(font.getlength( f"{key.level}/{key.max_level}")/2)
                draw.text((22-x,-2), f"{key.level}/{key.max_level}", font=font, fill=(255, 255, 255, 255))
                bg.alpha_composite(count,(3,42))
                main_bg.alpha_composite(bg,(position_main,0))
                position_main += 80

        return {"main":main_bg, "dop": dop_bg}



    async def creat_stats(self):
        bg_new = Image.new("RGBA", (420,746), (0,0,0,0))
        main_bg = Image.new("RGBA", (420,746), (0,0,0,0))
        dop_bg = Image.new("RGBA", (420,746), (0,0,0,0))

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

        d = ImageDraw.Draw(main_bg)
        dd = ImageDraw.Draw(dop_bg)
        font = await pill.get_font(30)
        font_dop = await pill.get_font(18)

        position_icon_main = 0
        position_text_main = 6
        position_text_dop= 36
        position_text_stats = 45


        position_icon_dop = 0
        position_text_dop_stats = 10
        position_text_stats_dop = 45

        for attribute in combined_attributes:
            stat = combined_attributes[attribute]
            icon = await pill.get_dowload_img(stat.icon, size=(58, 58))

            value = "{:.1f}%".format(stat.value * 100) if stat.percent else round(stat.value)
            if attribute in dop:

                main_bg.alpha_composite(icon,(0,position_icon_main))


                name_text = await pill.create_image_text(stat.name, 30, max_width=249, max_height=34, color=(255, 255, 255, 255))
                main_bg.alpha_composite(name_text, (55,position_text_stats - 40))

                x = 418 - int(font.getlength(str(value)))
                d.text((x, position_text_main), str(value), font=font, fill=(255, 255, 255, 255))
    
                x = 418 - int(font_dop.getlength(dop[attribute]["dop"]))
                d.text((x, position_text_dop+2), dop[attribute]["dop"], font=font_dop, fill=(249, 195, 110, 255))

                x = x - int(font_dop.getlength(dop[attribute]["main"])) - 5
                d.text((x, position_text_dop+2), dop[attribute]["main"], font=font_dop, fill=(255, 255, 255, 255))

                position_icon_main += 68
                position_text_main += 68
                position_text_dop += 68
                position_text_stats += 68
            else:
                dop_bg.alpha_composite(icon,(0,position_icon_dop))
                name_text = await pill.create_image_text(stat.name, 30, max_width=249, max_height=34, color=(255, 255, 255, 255))
                dop_bg.alpha_composite(name_text, (55,position_text_stats_dop - 40))

                x = 418 - int(font.getlength(str(value)))
                dd.text((x, position_text_dop_stats), str(value), font=font, fill=(255, 255, 255, 255))

                position_icon_dop += 68
                position_text_dop_stats += 68
                position_text_stats_dop += 68
        bg_new.alpha_composite(main_bg,(0,0))
        bg_new.alpha_composite(dop_bg,(0,position_icon_main))

        return bg_new


    async def create_sub_affix_image(self, sub_affix, bg, position):
        icon = await pill.get_dowload_img(sub_affix.icon, size=(26, 26))
        value = sub_affix.display

        d = ImageDraw.Draw(bg)
        font = await pill.get_font(21)
        x = int(font.getlength(value))
        d.text((236 - x, position), str(value), font=font, fill=(255, 255, 255, 255))
        bg.alpha_composite(icon, (138, position))

    async def creat_relics(self, relics):
        
        bg = _of.artifact_tree.copy()
        icon_rel = await pill.get_dowload_img(relics.icon, size=(104, 108))
        icon = await pill.get_dowload_img(relics.main_affix.icon, size=(36, 36))
        stars = await get_stars_icon(relics.rarity)

        bg.alpha_composite(icon_rel,(6,8))
        bg.alpha_composite(icon,(133,9))
        bg.alpha_composite(stars.resize((72,20)),(21,88))

        d = ImageDraw.Draw(bg)
        
        display = relics.main_affix.display
        level = f"+{relics.level}"
        font = await pill.get_font(20)

        x = int(font.getlength(display)/2)
        d.text((154 - x, 43), str(display), font=font, fill=(255,255,255, 255))

        x = int(font.getlength(level)/2)
        d.text((154 - x, 66), level, font=font, fill=(153,195,238, 255))

        position = (
            (193,20),
            (299,20),
            (193,62),
            (299,62)
        )

        for i, k in enumerate(relics.sub_affix):
            icon = await pill.get_dowload_img(k.icon, size=(36, 36))
            bg.alpha_composite(icon,position[i])
            d.text((position[i][0]+40, position[i][1]), str(k.display), font=font, fill=(255,255,255, 255))
        
        creat_full_bg_art = Image.new("RGBA", (406, 111), (0, 0, 0, 0))
        open_frame_art = await get_open_frame_art(relics.rarity)
        creat_full_bg_art.alpha_composite(bg,(4,0))
        creat_full_bg_art.alpha_composite(open_frame_art,(0,0))

        return creat_full_bg_art

    async def creat_constant(self):
        background_skills = Image.new("RGBA", (403, 63), (0, 0, 0, 0))
        x = 0
        rank = self.character.rank

        for key in self.character.rank_icons[:rank]:
            bg = _of.ON_const.copy()
            icon = await pill.get_dowload_img(key, size=(53,53))
            bg.alpha_composite(icon,(5,5))
            background_skills.alpha_composite(bg,(x,0))
            x += 68

        for key in self.character.rank_icons[rank:]:
            bg = _of.OFF_const.copy()
            icon = await pill.get_dowload_img(key, size=(53,53))
            bg.alpha_composite(icon,(5,5))
            bg.alpha_composite(_of.CLOSED_const,(0,0))
            background_skills.alpha_composite(bg,(x,0))
            x += 68

        return background_skills
    
    async def create_sets(self):
        total_bg =  Image.new("RGBA", (400, 156), (0, 0, 0, 0))
        font = await pill.get_font(16)

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
        elif len(rel_set) == 1:
            position = [(0,54)]
        elif len(rel_set) == 2:
            position = [(0,27),(0,81)]
        else:
            position = [(0,0),(0,54),(0,108)]
            
        for i, key in enumerate(rel_set):
            bg = _of.sets_tree.copy()
            sets = rel_set[key]
            icon = await pill.get_dowload_img(sets["icon"], size=(42,42))
            bg.alpha_composite(icon,(3,3))
            d = ImageDraw.Draw(bg)

            d.text((383, 10), str(sets["num"]), font=font, fill=(247, 212, 168, 255))
            sets_name_font,size = await pill.get_text_size_frame(sets["name"],16,312)
            d.text((int(199-size/2), 11), sets["name"], font=sets_name_font, fill=(247, 212, 168, 255))
            total_bg.alpha_composite(bg,position[i])
                
        return total_bg

    async def creat_info(self):
        background_name = _of.name_banners.copy()
                
        icon_element = await pill.get_dowload_img(self.character.element.icon, thumbnail_size=(40,39))
        path = await pill.get_dowload_img(self.character.path.icon, thumbnail_size=(41,41))
        stars = await get_stars_icon(self.character.rarity, v = 2)
        max_level = await max_lvl(self.character.promotion)
        level = f"{self.lang.lvl}: {self.character.level}/{max_level}"
        name = self.character.name
        path_name = self.character.path.name

        background_name.alpha_composite(icon_element,(41,86))
        background_name.alpha_composite(path,(91,86))
        background_name.alpha_composite(stars,(0,2))

        draw = ImageDraw.Draw(background_name)

        sets_name_font,size = await pill.get_text_size_frame(name,28,315)
        draw.text((int(199-size/2), -4), name, font=sets_name_font, fill=(255, 255, 255, 255))

        sets_name_font,size = await pill.get_text_size_frame(level,28,218)
        draw.text((int(152-size/2), 38), level, font=sets_name_font, fill=(255, 255, 255, 255))

        sets_name_font,size = await pill.get_text_size_frame(path_name,22,120)
        draw.text((int(193-size/2), 89), path_name, font=sets_name_font, fill=(255, 255, 255, 255))

        return background_name

    async def creat_seeleland(self):
        bg = _of.seeleland.copy()
        font = await pill.get_font(13)
        data = await calculator.get_seeleland(self.uid, self.character.id)
        if data is None:
            return None
        draw = ImageDraw.Draw(bg)
        draw.text((143, 3), str(data["sc"]), font=font, fill=(255, 255, 255, 255))
        draw.text((136, 20), data["rank"], font=font, fill=(255, 255, 255, 255))
        draw.text((127, 38), data["percrank"].replace("top ", ""), font=font, fill=(255, 255, 255, 255))

        return bg

    async def start(self):
        bg, lc, skills, stats, const, sets, info = await asyncio.gather(
            self.creat_charters(),
            self.creat_lk(),
            self.main_skills(),
            self.creat_stats(),
            self.creat_constant(),
            self.create_sets(),
            self.creat_info()
        )

        relic_tasks = [self.creat_relics(key) for key in self.character.relics]
        relics = await asyncio.gather(*relic_tasks)

        bg.alpha_composite(lc, (32, 40))
        bg.alpha_composite(info, (1356, 649))
        bg.alpha_composite(stats, (885, 28))
        bg.alpha_composite(const, (449, 297))
        bg.alpha_composite(sets, (449, 363))
        bg.alpha_composite(skills["main"], (507, 59))
        bg.alpha_composite(skills["dop"], (469, 139))

        if self.seeleland:
            seeleland = await self.creat_seeleland()
            if not seeleland is None:
                bg.alpha_composite(seeleland,(1645,692))


        position = (
            (32, 297),
            (32, 411),
            (32, 525),
            (32, 639),
            (449, 525),
            (449, 639),
        )
        for i, key in enumerate(relics):
            bg.alpha_composite(key, position[i])

        font = await pill.get_font(20)
        uid_text = f"UID: HIDDEN" if self.hide else f"UID: {self.uid}"
        d = ImageDraw.Draw(bg)
        d.text((40, 756), uid_text, font=font, fill=(255, 255, 255, 255))

        data = {
            "id": self.character.id,
            "name": self.character.name,
            "rarity": self.character.rarity,
            "card": bg,
            "size": bg.size
        }
        
        return data