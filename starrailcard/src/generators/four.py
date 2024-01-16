# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import asyncio
from PIL import ImageDraw,Image
from ..tools import calculators, pill, openFile

_of = openFile.ImageCache()


async def open_frame_lc(x):
    if x == 5:
        return _of.lc_5_stars
    elif x == 4:
        return _of.lc_4_stars
    else:
        return _of.lc_3_stars


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

async def open_background(name):
    if name == "Wind":
        return _of.ANEMO.copy()
    if name == "Fire":
        return _of.PYRO.copy()
    if name == "Ice":
        return _of.CRYO.copy()
    if name == "Thunder":
        return _of.Electro.copy()
    if name == "Quantum":
        return _of.quantom.copy()
    if name == "Imaginary":
        return _of.imaginary.copy()
    else:
        return _of.psyhical.copy()
    

async def open_background_const(name):
    if name == "Wind":
        return _of.CONST_ANEMO
    if name == "Fire":
        return _of.CONST_PYRO
    if name == "Ice":
        return _of.CONST_CRYO
    if name == "Thunder":
        return _of.CONST_Electro
    if name == "Quantum":
        return _of.CONST_quantom
    if name == "Imaginary":
        return _of.CONST_imaginary
    else:
        return _of.CONST_psyhical
    

async def open_background_talants(name):
    if name == "Wind":
        return _of.wind_stats
    if name == "Fire":
        return _of.pyro_stats
    if name == "Ice":
        return _of.cryo_stats
    if name == "Thunder":
        return _of.electro_stats
    if name == "Quantum":
        return _of.quantom_stats
    if name == "Imaginary":
        return _of.imaginari_stats
    else:
        return _of.psyhical_stats


class Creat:

    def __init__(self,characters, lang,img,hide,uid,seeleland) -> None:
        self.seeleland = seeleland
        self.character = characters
        self.lang = lang
        self.img = img
        self.hide = hide
        self.uid = uid
    

    async def creat_name_banner(self):
        background_name = Image.new("RGBA", (372,128), (0,0,0,0))
        font = await pill.get_font(28)
        icon_element = await pill.get_dowload_img(self.character.element.icon, thumbnail_size=(40,39))
        icon_path = await pill.get_dowload_img(self.character.path.icon, size=(41,41))
        stars = await get_stars_icon(self.character.rarity)
        max_level = await max_lvl(self.character.promotion)
        level = f"{self.lang.lvl}: {self.character.level}/{max_level}"
        name = self.character.name

        background_name.alpha_composite(icon_element,(2,0))
        background_name.alpha_composite(icon_path,(2,42))
        background_name.alpha_composite(stars,(2,83))

        draw = ImageDraw.Draw(background_name)

        draw.text((48,1), name, font=font, fill=(0, 0, 0, 255))
        draw.text((51,1), name, font=font, fill=(255, 255, 255, 255))

        draw.text((46,43), level, font=font, fill=(0, 0, 0, 255))
        draw.text((49,43), level, font=font, fill=(255, 255, 255, 255))

        return background_name


    async def creat_lk(self):
        bg_new = _of.lc_frame.copy()
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
        
        bg_new.alpha_composite(lc.resize((109,148)),(7,0))
        bg_new.alpha_composite(stars,(0,110))
        
        d = ImageDraw.Draw(bg_new)
        max_level = await max_lvl(self.character.light_cone.promotion)


        font_18 = await pill.get_font(18)
        font_26 = await pill.get_font(26)

        x = int(font_18.getlength(f"{self.lang.lvl}:{self.character.light_cone.level}/{max_level}")/2)
        d.text((229-x, 63), f"{self.lang.lvl}: {self.character.light_cone.level}/{max_level}", font=font_18, fill=(255, 255, 255, 255))


        d.text((122, 59), await ups(self.character.light_cone.rank), font=font_26, fill=(247, 212, 168, 255))

        d.text((156, 106), self.character.light_cone.attributes[0].display, font=font_18, fill=(255, 255, 255, 255)) #HP
        d.text((341, 106), self.character.light_cone.attributes[1].display, font=font_18, fill=(255, 255, 255, 255)) #ATK
        d.text((248, 106), self.character.light_cone.attributes[2].display, font=font_18, fill=(255, 255, 255, 255)) #DEF
        names = await pill.create_image_with_text(self.character.light_cone.name, 18, max_width=297, color=(255, 255, 255, 255))
        bg_new.alpha_composite(names, (119, 53 - names.size[1]))

        return bg_new

    async def creat_charters(self):
        if self.img:
            bg = await pill.creat_user_image_four(self.img)
        else:
            bg = await open_background(self.character.element.id)
            bg = await pill.creat_bg_teample_two(self.character.portrait, bg, maska = _of.maska_background.convert("L"), teample = 4)
        
        return bg


    async def creat_relics(self,relics):
        bg = _of.artifact_bg.copy()
        bg_icon_rel = Image.new("RGBA", (491, 114), (0, 0, 0, 0))
        bg_icon_rel_two = Image.new("RGBA", (491, 114), (0, 0, 0, 0))
        icon_rel = await pill.get_dowload_img(relics.icon, size=(153, 153))
        bg_icon_rel.alpha_composite(icon_rel,(-17,-14))
        icon = await pill.get_dowload_img(relics.main_affix.icon, size=(47,47))
        stars = await get_stars_icon(relics.rarity, v = 0)
        bg_icon_rel_two.paste(bg_icon_rel,(0,0), _of.artifact_mask.convert("L"))

        bg.alpha_composite(bg_icon_rel_two,(0,0))
        bg.alpha_composite(icon,(168,-4))
        bg.alpha_composite(stars,(0,78))
        
        display = relics.main_affix.display
        level = f"+{relics.level}"
        font_main = await pill.get_font(32)
        font = await pill.get_font(22)
        count_icon = _of.artifact_count.copy()

        d = ImageDraw.Draw(count_icon)
        x = int(font.getlength(level)/2)
        d.text((23 - x, -1), level, font=font, fill=(72,253,170,255))
        bg.alpha_composite(count_icon,(159,77))

        d = ImageDraw.Draw(bg)
        x = int(font_main.getlength(display))
        d.text((207 - x, 40), str(display), font=font_main, fill=(0,0,0, 255))
        d.text((209 - x, 40), str(display), font=font_main, fill=(255,255,255, 255))

        position = (
            (220,9),
            (220,58),
            (344,9),
            (344,58)
        )

        for i, k in enumerate(relics.sub_affix):
            icon = await pill.get_dowload_img(k.icon, size=(36, 36))
            bg.alpha_composite(icon,position[i])
            d.text((position[i][0]+51, position[i][1]+4), str(k.display), font=font, fill=(255,255,255, 255))
        
        score, rank, eff = await calculators.get_rating(relics,self.character.id,relics.id[-1:])
        

        return {"img": bg, "stats": {"eff": eff, "score": score}}


    async def creat_constant(self):
        background_skills = Image.new("RGBA", (72, 507), (0, 0, 0, 0))
        y = 0
        rank = self.character.rank

        open_bg = await open_background_const(self.character.element.id)

        for key in self.character.rank_icons[:rank]:
            bg = open_bg.copy()
            icon = await pill.get_dowload_img(key, size=(53,53))
            bg.alpha_composite(icon,(8,8))
            background_skills.alpha_composite(bg,(4,y))
            y += 88

        for key in self.character.rank_icons[rank:]:
            bg = _of.CONST_CLOSED.copy()
            icon = await pill.get_dowload_img(key, size=(53,53))
            bg.alpha_composite(icon,(5,5))
            bg.alpha_composite(_of.CONST_CLOSED_LOCK,(0,0))
            background_skills.alpha_composite(bg,(4,y))
            y += 88
        return background_skills

    async def main_skills(self):

        font = await pill.get_font(18)
        font_15 = await pill.get_font(15)

        main_bg =  Image.new("RGBA", (78,424), (0, 0, 0, 0))
        position_main = 0

        dop_bg = Image.new("RGBA", (124,124), (0, 0, 0, 0))

        position_dop = (
            (0,0),
            (66,0),
            (0,66),
            (66,66),
        )
        
        data = {}
        closed_icon = _of.CONST_CLOSED_LOCK.copy()
        i = 0
        bg_dop = await open_background_talants(self.character.element.id)
        for key in self.character.skill_trees:
            if key.max_level != 1:
                icon = await pill.get_dowload_img(key.icon, size=(57, 57))
                bg = _of.talants_bg.copy()
                count = _of.talants_count.copy()
                bg.alpha_composite(icon,(10,15))
                draw = ImageDraw.Draw(count)
                x = int(font.getlength( f"{key.level}/{key.max_level}")/2)
                draw.text((32-x,0), f"{key.level}/{key.max_level}", font=font, fill=(255, 255, 255, 255))
                bg.alpha_composite(count,(7,68))
                main_bg.alpha_composite(bg,(0,position_main))
                position_main += 111
            else:
                if key.anchor in ["Point05","Point06","Point07","Point08"]:
                    if key.level != 0:
                        bg = bg_dop.copy()
                        icon = await pill.get_dowload_img(key.icon, size=(49, 49))
                        bg.alpha_composite(icon,(4,4))
                        dop_bg.alpha_composite(bg,position_dop[i])
                    else:
                        bg = bg_dop.copy()
                        icon = await pill.get_dowload_img(key.icon, size=(49, 49))
                        bg.alpha_composite(icon,(4,4))
                        bg.alpha_composite(closed_icon.resize((56,56)),(1,1))
                        dop_bg.alpha_composite(bg,position_dop[i])
                    i += 1
                else:
                    if key.level != 0:
                        if not key.icon in data:
                            data[key.icon] = {"icon": key.icon, "count": 1}
                        else:
                            data[key.icon]["count"] += 1
        bg_dop =  Image.new("RGBA", (207,25), (0, 0, 0, 0))
        total_bg =  Image.new("RGBA", (207,458), (0, 0, 0, 0))
        x = 159
        for key in data:
            bg = _of.dop_stats.copy()
            icon = await pill.get_dowload_img(data[key]["icon"], size=(25,25))
            bg.alpha_composite(icon, (0,0))
            draw = ImageDraw.Draw(bg)
            draw.text((30,4), str(data[key]["count"]), font=font_15, fill=(255, 251, 155, 255))
            bg_dop.alpha_composite(bg,(x,0))
            x -= 53
        total_bg.alpha_composite(main_bg,(130,0))
        total_bg.alpha_composite(dop_bg,(0,288))
        total_bg.alpha_composite(bg_dop,(0,433))

        return total_bg

    async def create_sets(self):
        total_bg =  _of.artifact_sets.copy()
        font = await pill.get_font(20)

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
            return total_bg
        elif len(rel_set) == 1:
            position = [31]
            position_count = [29]
        elif len(rel_set) == 2:
            position = [15,47]
            position_count = [13,45]
        else:
            position = [2,31,60]
            position_count = [0,29,58]
            
        for i, key in enumerate(rel_set):
            sets = rel_set[key]
            
            bg_count = _of.artifact_sets_count.copy()
            d = ImageDraw.Draw(bg_count)
            d.text((23, 2), str(sets["num"]), font=font, fill=(109, 255, 143, 255))
            total_bg.alpha_composite(bg_count,(598,position_count[i]))

            d = ImageDraw.Draw(total_bg)
            sets_name_font,size = await pill.get_text_size_frame(sets["name"],20,418)
            d.text((int(315-size/2), position[i]), sets["name"], font=sets_name_font, fill=(109, 255, 143, 255))

        return total_bg
    
    async def creat_stats(self):
        bg_new = Image.new("RGBA", (745,492), (0,0,0,0))
        dop_bg = Image.new("RGBA", (745,300), (0,0,0,0))
        
        bg_main_frame = _of.stats_frame_enc.copy()

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

        d = ImageDraw.Draw(bg_main_frame)
        dd = ImageDraw.Draw(dop_bg)
        font = await pill.get_font(25)
        font_dop = await pill.get_font(18)

        position_icon_main = [
            (5,4),(383,4),
            (5,62),(383,62),
            (5,120),(383,120),

        ]
        position_text_main = [
            (366,11),(743,11),
            (366,69),(743,69),
            (366,127),(743,127),
        ]

        position_icon_dop = 0
        position_text_dop_stats = 6
        position_text_stats_dop = 6

        
        im = 0
        for attribute in combined_attributes:
            stat = combined_attributes[attribute]
            icon = await pill.get_dowload_img(stat.icon, size=(41,41))

            value = "{:.1f}%".format(stat.value * 100) if stat.percent else round(stat.value)
            if attribute in dop:

                bg_main_frame.alpha_composite(icon,position_icon_main[im])


                name_text = await pill.create_image_text(f"{stat.name}:", 25, max_width=199, max_height=34, color=(255, 255, 255, 255))
                bg_main_frame.alpha_composite(name_text, (position_icon_main[im][0]+40,position_text_main[im][1]))

                x = position_text_main[im][0] - int(font.getlength(str(value)))
                d.text((x, position_text_main[im][1]), str(value), font=font, fill=(255, 255, 255, 255))
    
                x = position_text_main[im][0] - int(font_dop.getlength(dop[attribute]["dop"]))
                d.text((x, position_text_main[im][1]+26), dop[attribute]["dop"], font=font_dop, fill=(229, 195, 144, 255))

                x = x - int(font_dop.getlength(dop[attribute]["main"])) - 5
                d.text((x, position_text_main[im][1]+26), dop[attribute]["main"], font=font_dop, fill=(255, 255, 255, 255))

                im += 1
            else:
                dop_bg.alpha_composite(icon,(0,position_icon_dop))
                name_text = await pill.create_image_text(f"{stat.name}:", 25, max_width=533, max_height=34, color=(255, 255, 255, 255))
                dop_bg.alpha_composite(name_text, (45,position_text_stats_dop))

                x = 743 - int(font.getlength(str(value)))
                dd.text((x, position_text_dop_stats), str(value), font=font, fill=(255, 255, 255, 255))

                position_icon_dop += 52
                position_text_dop_stats += 52
                position_text_stats_dop += 52


        bg_new.alpha_composite(bg_main_frame,(0,0))
        bg_new.alpha_composite(dop_bg,(0,182))
        
        return bg_new

    async def creat_seeleland(self):
        bg = _of.seeleland.copy()
        font = await pill.get_font(13)
        data = await calculators.get_seeleland(self.uid, self.character.id)
        if data is None:
            return None
        draw = ImageDraw.Draw(bg)
        draw.text((143, 3), str(data["sc"]), font=font, fill=(255, 255, 255, 255))
        draw.text((136, 20), data["rank"], font=font, fill=(255, 255, 255, 255))
        draw.text((127, 38), data["percrank"].replace("top ", ""), font=font, fill=(255, 255, 255, 255))

        return bg

    async def start(self):
        tasks = [
            self.creat_charters(),
            self.creat_lk(),
            self.creat_name_banner(),
            self.creat_constant(),
            self.main_skills(),
            self.create_sets(),
            self.creat_stats(),
            pill.get_font(18),
        ]

        relic_tasks = [self.creat_relics(key) for key in self.character.relics]

        results = await asyncio.gather(*tasks, *relic_tasks)

        bg, lc, name, const, talants, sets, stats, font, *relics = results

        if self.seeleland:
            seeleland = await self.creat_seeleland()
            if not seeleland is None:
                bg.alpha_composite(seeleland,(1180,89))
                
        uid_text = f"UID: HIDDEN" if self.hide else f"UID: {self.uid}"
        d = ImageDraw.Draw(bg)
        d.text((27, 765), uid_text, font=font, fill=(255, 255, 255, 255))

        bg.alpha_composite(lc, (661, 14))
        bg.alpha_composite(name, (4, 14))
        bg.alpha_composite(const, (4, 238))
        bg.alpha_composite(talants, (447, 287))
        bg.alpha_composite(sets, (710, 702))
        bg.alpha_composite(stats, (661, 188))

        y = 20
        total_eff = 0
        total_score = 0

        for key in relics:
            bg.alpha_composite(key["img"].resize((490, 113)), (1429, y))
            total_eff += key["stats"]["eff"]
            total_score += key["stats"]["score"]
            y += 127

        data = {
            "id": self.character.id,
            "name": self.character.name,
            "rarity": self.character.rarity,
            "card": bg,
            "size": bg.size
        }
                
        return data