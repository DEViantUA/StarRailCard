# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import anyio

import io
from PIL import ImageDraw,Image,ImageChops, ImageSequence, ImageFilter
import functools

from ..tools import git, options, treePaths
from ..tools.calculator import stats
from ..model.style import Card

from ..tools import pill

_of = git.ImageCache()
_of.set_mapping(4)


_DEFAULT_SCORE = {'count': 0, 
                  'rolls': {}, 
                  'rank': {'name': 'N/A', 
                           'color': (255, 255, 255, 255)
                    }
}

class Create:
    def __init__(self, data, lang, art, hide_uid, uid, seeleland,remove_logo, color) -> None:
        self.remove_logo = remove_logo
        self.data = data
        self.lang = lang
        self.art = art 
        self.hide_uid = hide_uid
        self.uid = uid
        
        self.gif = False
        self.GIFT_BG = []
        
        self.seeleland = seeleland
        self.total_eff = 0
        if not color is None:
            self.element_color = color
        else:
            self.element_color = self.data.element.color.rgba
    
    
    
    async def create_background(self):
        self.background = Image.new(Card.RGBA, Card.background_size, self.element_color)
        image_background =   Image.new(Card.RGBA, Card.background_size, (0,0,0,0))
        background = Image.new(Card.RGBA, Card.background_size, (0,0,0,0))
        
        logo = await _of.LOGO_GIT_INV
        shadow = await _of.background_shadow
        background_overlay = await _of.background_overlay
        
        if self.art:
            user_image = await pill.get_center_size(Card.art_size, self.art)
            position_art = Card.position_art
            mask = await _of.background_maska_art
        else:
            user_image = await pill.get_center_scale(Card.splash_size, await pill.get_download_img(self.data.portrait))
            position_art = Card.position_splash_art
            mask = await _of.background_maska_art #await _of.background_maska

        ll = await pill.light_level(self.element_color)

        if ll > 0.59 or self.element_color == (0, 255, 156, 255):
            background_dark = Image.new(Card.RGBA, Card.background_size, (0,0,0,70))  
            self.background.alpha_composite(background_dark)
            
        image_background.alpha_composite(user_image, position_art)
        self.background = ImageChops.soft_light(self.background, background_overlay.convert(Card.RGBA))

        self.background.alpha_composite(shadow,Card.position_shadow)
        background.paste(image_background.convert(Card.RGBA),(0,0), mask.convert("L"))
        self.background.alpha_composite(background)

        if not self.remove_logo:
            self.background.alpha_composite(logo,(1004,0))
        
        '''if not self.hide_uid:
            d = ImageDraw.Draw(self.background)
            font_10 = await pill.get_font(Card.font_uid)
            d.text(Card.position_uid, f"UID: {self.uid}", font=font_10, fill=(255, 255, 255, 255))
            d.text((Card.position_uid[0]-1, Card.position_uid[1]), f"UID: {self.uid}", font=font_10, fill=(0, 0, 0, 0))
        '''

    async def create_light_cone(self):
        if self.data.light_cone is None:
            self.light_cone_background = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            return 
        
        mask = await _of.maska_light_cones
        frame_light_cones = await _of.frame_light_cones
        blic_light_cones = await _of.blic_light_cones
        
        light_cone_holst = Image.new(Card.RGBA, Card.lc_background_size, (0, 0, 0, 0))
        light_cone_holst_image = Image.new(Card.RGBA, Card.lc_background_size, (0, 0, 0, 0))

        image = await pill.get_download_img(self.data.light_cone.portrait, size=Card.lc_image_size)
        light_cone_holst_image.alpha_composite(image, Card.lc_image_position)

        light_cone_holst.paste(light_cone_holst_image, (0, 0), mask.convert("L"))

        light_cone_holst_image = Image.new(Card.RGBA, Card.lc_background_size, (0, 0, 0, 0))
        
        shadow, frame, self.color = await pill.get_resource_light_cones(self.data.light_cone.rarity)
        
        light_cone_holst_image.alpha_composite(shadow)
        light_cone_holst_image.alpha_composite(frame, Card.lc_frame_position)
        light_cone_holst_image.alpha_composite(light_cone_holst)
        light_cone_holst_image.alpha_composite(frame_light_cones)
        light_cone_holst_image.alpha_composite(blic_light_cones)
        light_cone_holst_image.alpha_composite(frame)

        
        background_stat = await _of.stats_light_cones
        background_stat = background_stat.copy()
        font_size = 29
        font_color = (193, 162, 103, 255)

        font = await pill.get_font(font_size)

        d = ImageDraw.Draw(background_stat)
        rank = options.ups(self.data.light_cone.rank)
        x = int(font.getlength(rank) / 2)
        d.text((17 - x, 2), rank, font=font, fill=font_color)

        font = await pill.get_font(19)

        max_level = options.max_lvl(self.data.light_cone.promotion)

        d.text((40,9), f"{self.lang.lvl}: {self.data.light_cone.level}/{max_level}", font=font, fill=(255, 255, 255, 255))
        
        d.text((49, 53), self.data.light_cone.attributes[0].display, font=font, fill=(255, 255, 255, 255)) #HP
        d.text((152, 53), self.data.light_cone.attributes[1].display, font=font, fill=(255, 255, 255, 255)) #ATK
        d.text((49, 100), self.data.light_cone.attributes[2].display, font=font, fill=(255, 255, 255, 255)) #DEF
        
        stars = await options.get_stars(self.data.light_cone.rarity,type=3)
        
        name_light_cone = await pill.create_image_with_text(self.data.light_cone.name, 24, max_width=230, color=(255, 255, 255, 255))
        line = Image.new("RGBA", (1, name_light_cone.size[1] + 2), self.color)

        self.light_cone_background = Image.new("RGBA", (447, 255), (0, 0, 0, 0))
        self.light_cone_background.alpha_composite(light_cone_holst_image.resize((183, 244)))
        self.light_cone_background.alpha_composite(stars,(0,6))
        self.light_cone_background.alpha_composite(line, (191, 19))
        self.light_cone_background.alpha_composite(name_light_cone, (200, 23))
        
        y = int(22 + line.size[1])

        self.light_cone_background.alpha_composite(background_stat, (188, y))
    
    async def create_stats(self):
        self.background_stats = Image.new(Card.RGBA, (502, 657), (0, 0, 0, 0))

        combined_attributes = {}
        dop = {}
        
        for attribute in self.data.attributes + self.data.additions:
            field = attribute.field
            if field in combined_attributes:
                combined_attributes[field].value += attribute.value
                dop[field]["dop"] = f"+{attribute.display}"
            else:
                dop[field] = {"main": attribute.display, "dop": 0}
                combined_attributes[field] = attribute

        dop = {key: value for key, value in dop.items() if value['dop'] != 0}
        
        result = []
        
        self.element_color = await pill.get_light_pixel_color(self.element_color[:3], up= True)
        
        async for i, background in pill.create_stats(combined_attributes, dop, 
                      Card.stat_font_dop,Card.stat_font,
                      Card.stat_line_size, Card.stat_name_size, Card.stat_max_width, Card.stat_icon_size,
                      Card.stat_icon_position, Card.stat_name_position, Card.stat_x_position,
                      self.element_color,Card.stat_value_font
                      ,Card.stat_y_no_dop,Card.stat_y_yes_dop,Card.stat_y_dop,Card.stat_line_add):
            result.append(background)
                
        if len(result) <= 1:
            x = 0 
        
        x = int(657 / (len(result)))
        position_line = 0
        for key in result:
            self.background_stats.alpha_composite(key, (0, position_line))
            position_line += x
    
    async def get_score(self):
        self.score_info = await stats.Calculator(self.data).start(self.hoyo)
        
    async def create_relict(self,relict):
        background_main = Image.new(Card.RGBA,Card.relict_size, (0,0,0,0))
        background = Image.new(Card.RGBA,Card.relict_size, (0,0,0,0))
        background_image = Image.new("RGBA",Card.relict_size, (0,0,0,0))
        relict_frame = await _of.relict_frame
        relict_mask = await _of.relict_maska
        relict_score_frame = await _of.relict_score_frame
        relict_line = await _of.relict_line
        background_main.alpha_composite(relict_frame)
        
        image = await pill.get_download_img(relict.icon, size= Card.relict_icon_size)
        background_image.alpha_composite(image,Card.relict_icon_position)
        background.paste(background_image,(0,0),relict_mask.convert("L"))
        background_main.alpha_composite(relict_score_frame,(8,0))
        background_main.alpha_composite(background)
        background_main.alpha_composite(relict_line)
        score = self.score_info["score"].get(str(relict.id),_DEFAULT_SCORE)
        main_stat_icon = await pill.get_download_img(relict.main_affix.icon, size= Card.relict_main_stat_icon_size)
        color = options.color_element.get(relict.main_affix.type, None)
        if not color is None:
            main_stat_icon = await pill.recolor_image(main_stat_icon, color[:3])
        stars = await options.get_stars(relict.rarity, type = 1)
        background_main.alpha_composite(stars,Card.relict_position_star)
        background_main.alpha_composite(main_stat_icon,Card.relict_main_stat_icon_position)
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
            icon = await pill.get_download_img(k.icon, size=Card.relict_sub_icon_size)
            background_main.alpha_composite(icon,(142,y_icon))
            scoreR = score["rolls"].get(k.type,0)
            if k.type in self.score_info["bad"]:
                d.text((173, y_text), str(k.display), font=font_18, fill= (255,255,255,255))
            else:
                eff += 1
                d.text((173, y_text), str(k.display), font=font_18, fill= options.color_scoreR.get(scoreR,(255,255,255,255)))
            d.text((232, y_roll), f"+{scoreR}", font=font_18, fill= options.color_scoreR.get(scoreR,(255,255,255,255)))
            y_icon += 27
            y_text += 28
            y_roll += 27
            
        d.text((22, 4), "Score:", font=font_14, fill = (255,255,255,255))
        d.text((70, 4), str(score["count"]), font=font_14, fill = score["rank"]["color"])
        
        d.text((105, 4), "Rank:", font=font_14, fill = (255,255,255,255))
        d.text((149, 4), str(score["rank"]["name"]), font=font_14, fill = score["rank"]["color"])
        
        d.text((187, 4), "Eff Stat:", font=font_14, fill = (255,255,255,255))
        d.text((247, 4), str(eff), font=font_14, fill = options.color_scoreR.get(eff,(255,255,255,255)))
        
        self.total_eff += eff
        
        line_f = await _of.relict_frame_line
        line_f = line_f.copy()
        line_f = await pill.recolor_image(line_f, self.element_color[:3])
        background_main.alpha_composite(line_f,(0,21))
        
        return {"position": str(relict.id)[-1:] , "img": background_main}
    
    async def create_score_total(self):
        self.background_score = Image.new("RGBA",(536,43), (0,0,0,0))
        
        sclor_bg = await _of.relict_backgroundl_score_line
        sclor_bg = sclor_bg.copy().resize((536,16))
        sclor_bg_color = await _of.relict_full_score_line
        sclor_bg_color = sclor_bg_color.copy().resize((536,16))
        sclor_bg_color = await pill.recolor_image(sclor_bg_color, self.element_color[:3])
        
        result_percentage = (self.score_info["total_score"]['count'] / 260.53) * 100
        pixels_to_fill = int((result_percentage / 100)*536)
        if pixels_to_fill <= 0:
            pixels_to_fill = 1
        sclor_bg.alpha_composite(sclor_bg_color.resize((pixels_to_fill,16)))
        
        font_18 = await pill.get_font(14)
        
        d = ImageDraw.Draw(sclor_bg)
        x = 257 - int(font_18.getlength(f"{round(result_percentage,1)}%")/2)
        frame = await pill.get_colors(await pill.crop_image(sclor_bg), 15, common=True, radius=5, quality=800) 
        ll = await pill.light_level(frame)
        if ll > 0.6 or frame == (51, 51, 51):
            d.text((x, 0), f"{round(result_percentage,1)}%", font=font_18, fill = (0,0,0,166))
        else:
            d.text((x, 0), f"{round(result_percentage,1)}%", font=font_18, fill = (255,255,255,255))
        
        self.background_score.alpha_composite(sclor_bg,(0,27))
        
        font_21 = await pill.get_font(15)
        d = ImageDraw.Draw(self.background_score)
        
        d.text((249, -2), "Score:", font=font_21, fill = (255,255,255,255))
        d.text((300, -2), str(self.score_info["total_score"]['count']), font=font_21, fill = self.score_info["total_score"]["rank"]["color"])
        
        d.text((17, -2), "Summary Rank:", font=font_21, fill = (255,255,255,255))
        d.text((140, -2), str(self.score_info["total_score"]["rank"]["name"]), font=font_21, fill = self.score_info["total_score"]["rank"]["color"])
        
        d.text((393, -2), "Eff Stat:", font=font_21, fill = (255,255,255,255))
        d.text((457, -2), str(self.total_eff), font=font_21, fill = options.color_scoreR.get(self.total_eff,(255,255,255,255)))
    
    
    async def create_relict_sets(self):
        rel_set = options.calculator_relict_sets(self.data.relic_sets)

        self.background_sets = Image.new(Card.RGBA, Card.sets_background, (0,0,0,0))
        
        font = await pill.get_font(Card.sets_font)
        
        line_items = []
        i = 0
        for key in rel_set:
            sets = rel_set[key]
            holst_line = Image.new(Card.RGBA, Card.sets_line_size, (0,0,0,0))
            background_count = await _of.relict_count_sets
            background_count = background_count.copy()
            d = ImageDraw.Draw(background_count)
            d.text(Card.sets_count_position, str(sets["num"]), font=font, fill= Card.sets_name_color)
            d = ImageDraw.Draw(holst_line)
            sets_name_font,size = await pill.get_text_size_frame(sets["name"],15,492)
            if key[:1] == "1":
                holst_line.alpha_composite(background_count)
                d.text((39, 4), sets["name"], font=sets_name_font, fill=Card.sets_name_color)
                line_items.append({"setap": i, "line": holst_line})
                i += 1
            else:
                holst_line.alpha_composite(background_count,(503 ,0))
                d.text((int(490-size), 4), sets["name"], font=sets_name_font, fill=Card.sets_name_color)
                line_items.append({"setap": 1, "line": holst_line})
                
        for key in line_items:
            if key["setap"] == 1:
                self.background_sets.alpha_composite(key["line"],(0,29))
            elif key["setap"] == 2:
                self.background_sets.alpha_composite(key["line"],(0,29))
            else:
                self.background_sets.alpha_composite(key["line"],(0,0))
    
    async def build_relict(self):
        self.background_relict = Image.new(Card.RGBA, (536,577), (0,0,0,0))
        none_relict = await _of.none_relict
        position = {
            "1": (0,55),
            "2": (274,55),
            "3": (0,205),
            "4": (274,205),
            "5": (0,347),
            "6": (274,347),
        }
        
        map = {"1": None, "2": None, "3": None, "4": None, "5": None, "6": None}
        
        for key in self.relict:
            self.background_relict.alpha_composite(key["img"].resize((262,128)), position.get(key["position"]))
            map[key["position"]] = 0
        
        for key in map:
            if map[key] is None:
                self.background_relict.alpha_composite(none_relict, position.get(key))

        self.background_relict.alpha_composite(self.background_score,(0,0))
        self.background_relict.alpha_composite(self.background_sets,(2,486))
    
    async def build(self):
        self.background.alpha_composite(self.light_cone_background.resize(Card.build_lc_size),Card.build_lc_position)
        self.background.alpha_composite(self.background_stats, Card.build_stats_position)
        self.background.alpha_composite(self.background_relict, Card.build_relict_position)
        self.background.alpha_composite(self.stats, Card.build_skill_position)
        self.background.alpha_composite(self.background_skills,Card.build_constant_position)
        self.background.alpha_composite(self.background_name, (23,4))
    
    async def create_skill(self):
        holst_main = Image.new("RGBA", (69, 296), (0, 0, 0, 0))
        holst_dop = Image.new("RGBA", (265, 293), (0, 0, 0, 0))
        line = Image.new("RGBA", (15, 2), (255, 255, 255, 255))
        holst_point_add = Image.new("RGBA", (145, 68), (0, 0, 0, 0))
        point_add_position = 0
        position_dop = treePaths.tree.get(self.data.path.id)
        position_main_y = 0

        for key in self.data.skill_trees:
            if key.max_level != 1:
                font = await pill.get_font(24)
                color = (227, 215, 194, 255)
                icon_skill = Image.new("RGBA", (69, 68), (0, 0, 0, 0))
                background = await _of.talants_background
                background = background.copy()
                icon = await pill.get_download_img(key.icon, size=(55, 55))
                
                frame = await _of.talants_adaptationt_frame
                if key.max_level > 10:
                    color = options.color_element_talant.get(self.data.element.id.lower(), (255,255,255,255))
                if key.anchor in ["Point19", "Point20"]:
                    icon = await pill.recolor_image(icon, (215, 194, 227))
                    frame = await pill.recolor_image(frame.copy(),  (215, 194, 227))
                else:
                    icon = await pill.recolor_image(icon, (227, 215, 194))
                    frame = await pill.recolor_image(frame.copy(), (color[0], color[1], color[2]))
                
                background.alpha_composite(icon, (4, 4))
                count_background = await _of.talants_count
                count_background = count_background.copy()
                d = ImageDraw.Draw(count_background)
                x = int(font.getlength(str(key.level)) / 2)
                d.text((15 - x, 4), str(key.level), font=font, fill=color)
                background.alpha_composite(frame)
                icon_skill.alpha_composite(background, (5, 0))
                icon_skill.alpha_composite(count_background, (0, 37))
                if key.anchor in ["Point19", "Point20"]:
                    holst_point_add.alpha_composite(icon_skill, (point_add_position, 0))
                    point_add_position += 78

                else:
                    holst_main.alpha_composite(icon_skill, (0, position_main_y))
                    position_main_y += 76
            else:
                if key.anchor in ["Point05", "Point06", "Point07", "Point08"]:
                    icon_background = await _of.talants_main_stats
                    icon_background = icon_background.copy()
                    icon = await pill.get_download_img(key.icon, size=(40, 40))
                    icon = await pill.recolor_image(icon, (0, 0, 0))
                    icon_background.alpha_composite(icon, (13, 14))
                    if key.level == 0:
                        icon_background = await pill.apply_opacity(icon_background, opacity=0.5)
                    holst_dop.alpha_composite(icon_background, treePaths.position_point[key.anchor])
                else:
                    icon_background = await _of.talants_mini_stats
                    icon_background = icon_background.copy()
                    icon = await pill.get_download_img(key.icon, size=(40, 40))
                    icon = await pill.recolor_image(icon, (0, 0, 0))
                    icon_background.alpha_composite(icon, (0, 0))
                    if key.level == 0:
                        icon_background = await pill.apply_opacity(icon_background, opacity=0.5)
                    holst_dop.alpha_composite(icon_background, (222 - position_dop[str(key.id)[-2:]][0],position_dop[str(key.id)[-2:]][1]))
                    
                    holst_dop.alpha_composite(line, (266 - position_dop[str(key.id)[-2:]][0], position_dop[str(key.id)[-2:]][1] + 21))
        
        
        self.stats = Image.new("RGBA", (345, 367), (0, 0, 0, 0))        
        self.stats.alpha_composite(holst_point_add, (120, 4))
        self.stats.alpha_composite(holst_main, (275, 72))
        self.stats.alpha_composite(holst_dop, (0, 72))
        
    
    
    async def create_constant(self):
        self.background_skills = Image.new(Card.RGBA, Card.constant_size_background, (0, 0, 0, 0))
        y = 0
        rank = self.data.rank
        for key in self.data.rank_icons[:rank]:
            icon = await pill.get_download_img(key, size=Card.constant_size_icon)
            self.background_skills.alpha_composite(icon,(0,y))
            y += 46

        for key in self.data.rank_icons[rank:]:
            icon = await pill.get_download_img(key, size= Card.constant_size_icon)
            icon = await pill.apply_opacity(icon, opacity=Card.constant_size_icon_opacity)
            self.background_skills.alpha_composite(icon,(0,y))
            y += 46
        
    async def create_name(self):
        self.background_name = Image.new(Card.RGBA, Card.name_size, (0, 0, 0, 0))
        d = ImageDraw.Draw(self.background_name)
        names = await pill.create_image_with_text(self.data.name, Card.font_name_size , max_width=Card.name_with, color= Card.name_color)
        names_dark = await pill.recolor_image(names,(0,0,0))
        
        if names.size[1] <= Card.name_h_max:
            self.background_name.alpha_composite(names_dark,(Card.name_position-1,int(Card.name_h_max-names.size[1]/2)+1))
            self.background_name.alpha_composite(names,(Card.name_position,int(Card.name_h_max-names.size[1]/2)))
        else:
            self.background_name.alpha_composite(names_dark,(Card.name_position-1,int(Card.name_h_min-names.size[1]/2)+1))
            self.background_name.alpha_composite(names,(Card.name_position,int(Card.name_h_max-names.size[1]/2)))
        
        font_17 = await pill.get_font(Card.font_name_level)
        max_level = options.max_lvl(self.data.promotion)
        level = f"{self.lang.lvl}: {self.data.level}/{max_level}"
        d.text((Card.position_name_level[0]-1,Card.position_name_level[1]+1,), level, font=font_17, fill= (0,0,0,255))
        d.text(Card.position_name_level, level, font=font_17, fill= Card.color_name_level)
        starts = await options.get_stars(self.data.rarity)
        self.background_name.alpha_composite(starts, Card.position_name_star)

    async def start(self, build = None, hoyo = False ):
        _of.set_mapping(4)
        self.hoyo = hoyo
        
        if self.art:
            if "gif" in self.art:
                self.gif = True
            self.art = await pill.get_user_image(self.art)
            if self.gif:    
                n = 2           
                frame_count = 0
                with io.BytesIO(self.art) as f:
                    self.art = Image.open(f)
                    for frame in ImageSequence.Iterator(self.art):
                        self.element_color = await pill.get_colors(frame.convert("RGBA"), 15, common=True, radius=5, quality=800)
                        if frame_count >= 50:
                            break
                        if frame_count % n != 0:
                            self.art = frame.convert("RGBA")
                            await self.create_background()
                            self.GIFT_BG.append(self.background.copy())
                        frame_count += 1
            else:
                self.element_color = await pill.get_colors(self.art, 15, common=True, radius=5, quality=800)
                await self.create_background()
        else:
            await self.create_background()
        
        async with anyio.create_task_group() as tasks:
            tasks.start_soon(self.create_light_cone) #
            tasks.start_soon(self.create_stats) #
            tasks.start_soon(self.create_name) #
            tasks.start_soon(self.create_constant) #
            tasks.start_soon(self.create_relict_sets) #
            tasks.start_soon(self.get_score) #
            tasks.start_soon(self.create_skill)
            
        async def wait_all(*funcs):
            results = [None] * len(funcs)
            
            async with anyio.create_task_group() as tasks:
                async def process(func, i):
                    results[i] = await func()
                
                for i, func in enumerate(funcs):
                    tasks.start_soon(process, func, i)
            
            return results
        
        self.relict = await wait_all(*[
            functools.partial(self.create_relict, key)
            for key in self.data.relics
        ])
        
        await self.create_score_total()
        
        await self.build_relict()
        
        await self.build()
        
        
        data = {
                "id": self.data.id,
                "name": self.data.name,
                "animation": self.gif,
                "rarity": self.data.rarity,
                "card": self.background,
                "size": Card.background_size,
                "color": self.element_color,
                "build": build
            }
            
        return data