# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import anyio

import io
from PIL import ImageDraw,Image,ImageChops, ImageSequence
import functools

from ..tools import git, options
from ..tools.calculator import stats
from ..model.style import Ticket

from ..tools import pill

_DEFAULT_SCORE = {'count': 0, 
                  'rolls': {}, 
                  'rank': {'name': 'N/A', 
                           'color': (255, 255, 255, 255)
                    }
}

_of = git.ImageCache()
_of.set_mapping(2)


class Creat:
    def __init__(self, data, lang, art, hide_uid, uid, seeleland, remove_logo) -> None:
        self.data = data
        self.remove_logo = remove_logo
        self.lang = lang
        self.art = art
        self.hide_uid = hide_uid
        self.uid = uid
        self.seeleland = seeleland
        self.totall_eff = 0
        self.seeleland = seeleland
        self.element_color = self.data.element.color.rgba
        self.gif = False
        self.GIFT_BG = []
        
    async def creat_bacground(self):
        self.background = Image.new(Ticket.RGBA, Ticket.bacground_size, (0,0,0,0))
        background_splash = Image.new(Ticket.RGBA, Ticket.background_splash_size, Ticket.bacground_default_color)
        background_dark = Image.new(Ticket.RGBA, Ticket.background_splash_size, (0,0,0,100))       
        
        line = await _of.background_line
        logo = await _of.LOGO_GIT_INV
        shadow = await _of.background_shadow
        splash = True
        background_overlay = await _of.background_overlay
        
        if self.art:
            user_image = await pill.get_centr_size(Ticket.art_size, self.art)
            self.background = pill.grandiend_v2.GrandientBackground(user_image,(1,Ticket.bacground_size[1])).start(left= True,overlay_add = False)
            line,self.element_color = await pill.recolor_image(line, self.element_color[:3], light = True)
            
                
            self.background = self.background.resize(Ticket.bacground_size)
            position_art = Ticket.position_art
            splash = False
            self.background = ImageChops.soft_light(self.background, background_overlay.convert(Ticket.RGBA))
            ll = await pill.light_level(self.element_color)
            if ll > 0.6:
                self.background.alpha_composite(background_dark)
        else:
            self.background = Image.new(Ticket.RGBA, Ticket.bacground_size, Ticket.bacground_default_color)
            user_image = await pill.get_centr_scale(Ticket.splash_size, await pill.get_dowload_img(self.data.portrait))
            position_art = Ticket.position_splash_art
            
        
        
        self.background.alpha_composite(user_image.convert(Ticket.RGBA),position_art)
        if splash:
            self.background.alpha_composite(background_splash)
        self.background.alpha_composite(line,Ticket.position_line)
        self.background.alpha_composite(shadow,Ticket.position_shadow)
        if not self.remove_logo:
            self.background.alpha_composite(logo,(1845,0))
        
        if not self.hide_uid:
            uid = Image.new(Ticket.RGBA, Ticket.bacground_size, (0,0,0,0))
            d = ImageDraw.Draw(uid)
            
            font_10 = await pill.get_font(Ticket.font_uid)
            d.text((0,0), f"UID: {self.uid}", font=font_10, fill=(255, 255, 255, 100))
            self.background.alpha_composite(uid,Ticket.position_uid)
    
    async def creat_light_cone(self):
        if self.data.light_cone is None:
            self.light_cone_background = Image.new("RGBA", (447, 255), (0, 0, 0, 0))
            return 
        
        maska = await _of.maska_light_cones
        frame_light_cones = await _of.frame_light_cones
        blic_light_cones = await _of.blic_light_cones
        
        light_cone_holst = Image.new(Ticket.RGBA, Ticket.lc_bacgrount_size, (0, 0, 0, 0))
        light_cone_holst_image = Image.new(Ticket.RGBA, Ticket.lc_bacgrount_size, (0, 0, 0, 0))

        image = await pill.get_dowload_img(self.data.light_cone.portrait, size=Ticket.lc_image_size)
        light_cone_holst_image.alpha_composite(image, Ticket.lc_image_position)

        light_cone_holst.paste(light_cone_holst_image, (0, 0), maska.convert("L"))

        light_cone_holst_image = Image.new(Ticket.RGBA, Ticket.lc_bacgrount_size, (0, 0, 0, 0))
        
        shadow, frame, self.color = await pill.get_resurs_light_cones(self.data.light_cone.rarity)
        
        light_cone_holst_image.alpha_composite(shadow)
        light_cone_holst_image.alpha_composite(frame, Ticket.lc_frame_position)
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
    
    async def creat_relict(self,relict):
        
        font_15 = await pill.get_font(15)
        font_26 = await pill.get_font(26)
        font_14 = await pill.get_font(14)
        font_17 = await pill.get_font(17)
        
        background = Image.new(Ticket.RGBA, (394,115), (0,0,0,0))
        
        relict_background = await _of.relict_background
        relict_background = relict_background.copy()
        
        count = await _of.relict_count_lvl
        relict_maska = await _of.relict_maska
        relict_score_frame = await _of.relict_score_frame
        
        relict_background_icon = Image.new(Ticket.RGBA, (387,88), (0,0,0,0))
        image = await pill.get_dowload_img(relict.icon, size= (108,108))
        relict_background_icon.alpha_composite(image,(-6,-10))
        
        line = Image.new(Ticket.RGBA, (1,81), (255,255,255,255))
        
        relict_background.paste(relict_background_icon,(0,0),relict_maska.convert("L"))
        relict_background.alpha_composite(line,(117,4))
        relict_background.alpha_composite(line,(251,4))
        
        score = self.score_info["score"].get(str(relict.id),_DEFAULT_SCORE)
        main_stat_icon = await pill.get_dowload_img(relict.main_affix.icon, size= Ticket.relict_main_stat_icon_size)
        color = options.color_element.get(relict.main_affix.type, None)
        if not color is None:
            main_stat_icon = await pill.recolor_image(main_stat_icon, color[:3])
        
        stars = await options.get_stars(relict.rarity, type = 3)
        stars = stars.resize((25,82))
        
        relict_background.alpha_composite(main_stat_icon,Ticket.relict_main_stat_icon_position)
        relict_background.alpha_composite(count,(71,65))
        d = ImageDraw.Draw(relict_background)
        
        x = int(font_26.getlength(relict.main_affix.display))
        d.text((112-x, 36), relict.main_affix.display, font= font_26, fill= (0,0,0,255))
        d.text((113-x, 36), relict.main_affix.display, font= font_26, fill= (255,255,255,255))
        
        x = 93 - int(font_15.getlength(f"+{relict.level}")/2)
        d.text((x, 65), f"+{relict.level}", font= font_15, fill= (234,187,111,255))

        count = await _of.relict_count
        y_icon = 4
        x_icon = 118
        
        y_text = 16
        x_text = 211      
        
        p_roll_x = 222
        p_roll_y = 15
        
        eff = 0
        
        for i, k in enumerate(relict.sub_affix):
            count_draw  = count.copy()
            icon = await pill.get_dowload_img(k.icon, size=Ticket.relict_sub_icon_size)
            relict_background.alpha_composite(icon,(x_icon,y_icon))
            scoreR = score["rolls"].get(k.type,0)
            x = x_text - int(font_17.getlength(str(k.display)))
            
            if k.type in self.score_info["bad"]:
                d.text((x, y_text), str(k.display), font=font_17, fill= (255,255,255,255))
            else:
                eff += 1
                d.text((x, y_text), str(k.display), font=font_17, fill= options.color_scoreR.get(scoreR,(255,255,255,255)))
            
            
            draws = ImageDraw.Draw(count_draw)
            x = 12 - int(font_15.getlength(f"+{scoreR}")/2)
            draws.text((x, 0), f"+{scoreR}", font=font_15, fill= options.color_scoreR.get(scoreR,(255,255,255,255)))
            relict_background.alpha_composite(count_draw,(p_roll_x,p_roll_y))
            
            y_icon += 41
            y_text += 41
            p_roll_y += 41
            
            if i == 1:
                y_icon = 4
                x_icon = 251
                
                y_text = 16
                x_text = 344      
                
                p_roll_x = 355
                p_roll_y = 15
        
        
        background.alpha_composite(relict_score_frame)
        background.alpha_composite(relict_background, (7,17))
        background.alpha_composite(stars,Ticket.relict_position_star)
        
        d = ImageDraw.Draw(background)
        d.text((19, 1), "Score:", font=font_14, fill = (255,255,255,255))
        d.text((67, 1), str(score["count"]), font=font_14, fill = score["rank"]["color"])
        
        d.text((136, 1), "Rank:", font=font_14, fill = (255,255,255,255))
        d.text((178, 1), str(score["rank"]["name"]), font=font_14, fill = score["rank"]["color"])
        
        d.text((239, 1), "Eff Stat:", font=font_14, fill = (255,255,255,255))
        d.text((301, 1), str(eff), font=font_14, fill = options.color_scoreR.get(eff,(255,255,255,255)))
        
        self.totall_eff += eff
                
        return {"position": str(relict.id)[-1:] , "img": background}        

    
    async def creat_relict_sets(self):
        rel_set = options.calculator_relict_sets(self.data.relic_sets)

        self.background_sets = Image.new(Ticket.RGBA, Ticket.sets_background, (0,0,0,0))
        icons_sets = await _of.relict_icon_sets
        background_counts = await _of.relict_count_sets
        font = await pill.get_font(Ticket.setst_font)
        
        line_items = []
        i = 0
        for key in rel_set:
            sets = rel_set[key]
            holst_line = Image.new(Ticket.RGBA, Ticket.setst_line_size, (0,0,0,0))
            icon = await pill.get_dowload_img(sets["icon"], size = (33,33))
            icons_sets.alpha_composite(icon, (3,3))
            
            background_count = background_counts.copy()
            d = ImageDraw.Draw(background_count)
            d.text(Ticket.setst_count_position, str(sets["num"]), font=font, fill= Ticket.setst_name_color)
            
            d = ImageDraw.Draw(holst_line)
            sets_name_font,size = await pill.get_text_size_frame(sets["name"],15,280)
            if key[:1] == "1":
                if i != 0:
                    holst_line.alpha_composite(icons_sets, (356,0))
                    holst_line.alpha_composite(background_count,(0,10))
                    d.text((int(185-size/2), 12), sets["name"], font=sets_name_font, fill=Ticket.setst_name_color)
                    line_items.append({"setap": i, "line": holst_line})
                else:
                    holst_line.alpha_composite(icons_sets, (0,0))
                    holst_line.alpha_composite(background_count,(370,10))
                    d.text((int(185-size/2), 12), sets["name"], font=sets_name_font, fill=Ticket.setst_name_color)
                    line_items.append({"setap": i, "line": holst_line})
                i += 1
            else:
                holst_line.alpha_composite(icons_sets, (0,0))
                holst_line.alpha_composite(background_count,(370,10))
                d.text((int(185-size/2), 12), sets["name"], font=sets_name_font, fill=Ticket.setst_name_color)
                line_items.append({"setap": 3, "line": holst_line})
        
        
        
        for key in line_items:
            if key["setap"] == 0:
                self.background_sets.alpha_composite(key["line"],(0,0))
            elif key["setap"] == 3:
                self.background_sets.alpha_composite(key["line"],(413,507))
            else:
                self.background_sets.alpha_composite(key["line"],(0,45))
                
    async def get_score(self):
        self.score_info = await stats.Calculator(self.data).start()
    
    async def creat_stats(self):
        self.background_stats = Image.new(Ticket.RGBA, (434, 692), (0, 0, 0, 0))

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
                
        async for i, background in pill.creat_stats(combined_attributes, dop, 
                      Ticket.stat_font_dop,Ticket.stat_font,
                      Ticket.stat_line_size, Ticket.stat_name_size, Ticket.stat_max_width, Ticket.stat_icon_size,
                      Ticket.stat_icon_position, Ticket.stat_name_position, Ticket.stat_x_position,
                      self.element_color,Ticket.stat_value_font
                      ,Ticket.stat_y_no_dop,Ticket.stat_y_yes_dop,Ticket.stat_y_dop):
            result.append(background)
                
        if len(result) <= 1:
            x = 0 
        
        x = int(692 / (len(result)))
        position_line = 0
        for key in result:
            self.background_stats.alpha_composite(key, (0, position_line))
            position_line += x
                   
    async def creat_path(self):
        font = await pill.get_font(11)
        font_13 = await pill.get_font(13)

        self.main_bg =  Image.new("RGBA", (282,58), (0, 0, 0, 0))
        position_main = 0

        self.dop_bg = Image.new("RGBA", (399,124), (0, 0, 0, 0))

        position_dop = (
            (0,0),
            (192,0),
            (0,70),
            (192,70),
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
        for key in self.data.skill_trees:
            if key.max_level == 1:

                if key.anchor in ["Point05","Point06","Point07","Point08"]:
                    icon = await pill.get_dowload_img(key.icon, size=(38,38))
                else:
                    icon = await pill.get_dowload_img(key.icon, size=(30,30))
                    
                if key.level == 0:
                    if key.anchor in ["Point05","Point06","Point07","Point08"]:
                        bg = await _of.dop
                        bg = bg.copy()
                        bg.alpha_composite(icon,(7,10))
                        closed_main = await _of.closed_main
                        bg.alpha_composite(closed_main,(0,0))
                    else:
                        bg = await _of.closed_trees
                        bg = await pill.recolor_image(bg.copy(), (0, 0, 0))
                        icon = await pill.recolor_image(icon,self.element_color[:3])
                        bg.alpha_composite(icon, (0,0))
                else:
                    if key.anchor in ["Point05","Point06","Point07","Point08"]:
                        bg = await _of.dop
                        bg = bg.copy()
                        bg.alpha_composite(icon,(7,10))
                    else:
                        bg = await _of.open_trees
                        bg = await pill.recolor_image(bg.copy(), self.element_color[:3])
                        icon = await pill.recolor_image(icon, (0, 0, 0))
                        bg.alpha_composite(icon, (0,0))
                self.dop_bg.alpha_composite(bg, position_dop[i])
                i += 1
            else:
                icon = await pill.get_dowload_img(key.icon, size=(43, 43))
                bg = await _of.bg_main
                frame_bg = await _of.frame_main
                bg = bg.copy()
                frame_bg = await pill.recolor_image(frame_bg.copy(),self.element_color[:3])
                bg.alpha_composite(frame_bg)
                
                count = await _of.count_tree
                count = await pill.recolor_image(count.copy(),self.element_color[:3])
                bg.alpha_composite(icon,(4,4))
                draw = ImageDraw.Draw(count)
                if key.anchor == 'Point01':
                    if key.max_level > 6:
                        key.level += 1
                else:
                    if key.max_level > 10:
                        key.level += 2
                x = int(font.getlength( f"{key.level}/{key.max_level}")/2)
                ll = await pill.light_level(self.element_color)
                if ll > 0.6:
                    draw.text((18-x,0), f"{key.level}/{key.max_level}", font=font_13, fill=(0, 0, 0, 255))
                else:
                    draw.text((18-x,0), f"{key.level}/{key.max_level}", font=font_13, fill=(255, 255, 255, 255))
                bg.alpha_composite(count,(4,44))
                self.main_bg.alpha_composite(bg,(position_main,0))
                position_main += 77


    async def creat_name(self):
        self.background_name = Image.new(Ticket.RGBA, Ticket.name_size, (0, 0, 0, 0))
        d = ImageDraw.Draw(self.background_name)
        names = await pill.create_image_with_text(self.data.name, Ticket.font_name_size , max_width=Ticket.name_with, color= Ticket.name_color)
        names_dark = await pill.recolor_image(names,(0,0,0))
        if names_dark.size[1] <= Ticket.name_h_max:
            self.background_name.alpha_composite(names_dark,(Ticket.name_position - 1,int(Ticket.name_h_max-names.size[1]/2)))
        else:
            self.background_name.alpha_composite(names_dark,(Ticket.name_position - 1,int(Ticket.name_h_min-names.size[1]/2)))
            
        if names.size[1] <= Ticket.name_h_max:
            self.background_name.alpha_composite(names,(Ticket.name_position,int(Ticket.name_h_max-names.size[1]/2)))
        else:
            self.background_name.alpha_composite(names,(Ticket.name_position,int(Ticket.name_h_min-names.size[1]/2)))
        
            
        font_17 = await pill.get_font(Ticket.font_name_level)
        max_level = options.max_lvl(self.data.promotion)
        level = f"{self.lang.lvl}: {self.data.level}/{max_level}"
        d.text((Ticket.position_name_level[0]-1, Ticket.position_name_level[1]), level, font=font_17, fill= (0,0,0,255))
        d.text(Ticket.position_name_level, level, font=font_17, fill= Ticket.color_name_level)
        starts = await options.get_stars(self.data.rarity)
        self.background_name.alpha_composite(starts,Ticket.position_name_star)   
    
    async def creat_constant(self):
        self.background_skills = Image.new(Ticket.RGBA, (381, 54), (0, 0, 0, 0))
        x = 0
        rank = self.data.rank
        closed = await _of.CLOSED_const
        closed = closed.resize((54,54))
        closed = await pill.recolor_image(closed.copy(), self.element_color[:3])
        for key in self.data.rank_icons[:rank]:
            bg = await _of.ON_const
            bg = await pill.recolor_image(bg.resize((54,54)).copy(),self.element_color[:3])
            icon = await pill.get_dowload_img(key, size=(43,43))
            icon = await pill.recolor_image(icon, self.element_color[:3])
            bg.alpha_composite(icon,(5,5))
            self.background_skills.alpha_composite(bg,(x,0))
            x += 65
        for key in self.data.rank_icons[rank:]:
            bg = await _of.OFF_const
            bg = bg.resize((54,54)).copy()
            icon = await pill.get_dowload_img(key, size=(43,43))
            icon = await pill.apply_opacity(icon, 0.3)
            bg.alpha_composite(icon,(5,5))
            bg.alpha_composite(closed,(0,0))
            self.background_skills.alpha_composite(bg,(x,0))
            x += 65
   
    
    async def creat_score_total(self):
        self.background_score = Image.new("RGBA",(442,37), (0,0,0,0))
        
        sclor_bg = await _of.relict_backgroundl_score_line
        sclor_bg = sclor_bg.copy()
        sclor_bg_color = await _of.relict_full_score_line
        sclor_bg_color = sclor_bg_color.copy()
        sclor_bg_color = await pill.recolor_image(sclor_bg_color, self.element_color[:3])
        
        result_percentage = (self.score_info["total_score"]['count'] / 260.53) * 100
        pixels_to_fill = int((result_percentage / 100)*599)
        if pixels_to_fill <= 0:
            pixels_to_fill = 1
        sclor_bg.alpha_composite(sclor_bg_color.resize((pixels_to_fill,16)))
        
        font_18 = await pill.get_font(18)
        
        d = ImageDraw.Draw(sclor_bg)
        x = 280 - int(font_18.getlength(f"{round(result_percentage,1)}%")/2)
        frame = await pill.get_colors(await pill.crop_image(sclor_bg), 15, common=True, radius=5, quality=800) 
        ll = await pill.light_level(frame)
        if ll > 0.6 or frame == (102, 53, 0):
            d.text((x, -1), f"{round(result_percentage,1)}%", font=font_18, fill = (0,0,0,0))
        else:
            d.text((x, -1), f"{round(result_percentage,1)}%", font=font_18, fill = (255,255,255,255))
        
        self.background_score.alpha_composite(sclor_bg.resize((394,13)),(0,24))
        
        font_16 = await pill.get_font(16)
        d = ImageDraw.Draw(self.background_score)
        
        d.text((178, -2), "Score:", font=font_16, fill = (255,255,255,255))
        d.text((233, -2), str(self.score_info["total_score"]['count']), font=font_16, fill = self.score_info["total_score"]["rank"]["color"])
        
        d.text((0, -2), "Summary Rank:", font=font_16, fill = (255,255,255,255))
        d.text((132, -2), str(self.score_info["total_score"]["rank"]["name"]), font=font_16, fill = self.score_info["total_score"]["rank"]["color"])
        
        d.text((287, -2), "Eff Stat:", font=font_16, fill = (255,255,255,255))
        d.text((366, -2), str(self.totall_eff), font=font_16, fill = options.color_scoreR.get(self.totall_eff,(255,255,255,255)))
    
    
    async def build_relict(self):
        self.background_relict = Image.new(Ticket.RGBA, (807,457), (0,0,0,0))
        none_relict = await _of.none_relict
        position = {
            "1": (0,0),
            "2": (0,115),
            "3": (0,237),
            "4": (0,352),
            "5": (413,185),
            "6": (413,300),
        }
        
        map = {"1": None, "2": None, "3": None, "4": None, "5": None, "6": None}
        
        for key in self.relict:
            self.background_relict.alpha_composite(key["img"], position.get(key["position"]))
            map[key["position"]] = 0
        
        for key in map:
            if map[key] is None:
                self.background_relict.alpha_composite(none_relict, position.get(key))
    
    
    async def creat_seeleland(self):
        self.seelelen = Image.new("RGBA",(1,1), (0,0,0,0))
        
        if self.seeleland:
            self.seelelen = await _of.seeleland_v2
            self.seelelen = self.seelelen.copy()
            font = await pill.get_font(15)
            data = await options.get_seeleland(self.uid, self.data.id)
            if data is None:
                self.seelelen = Image.new("RGBA",(1,1), (0,0,0,0))
                return None
            if not "rank" in data:
                self.seelelen = Image.new("RGBA",(1,1), (0,0,0,0))
                return None
            draw = ImageDraw.Draw(self.seelelen)
            draw.text((143, 7), str(data["sc"]), font=font, fill=(255, 255, 255, 255))
            draw.text((136, 24), f'{data["rank"][:-2]}..', font=font, fill=(255, 255, 255, 255))
            draw.text((127, 42), data["percrank"].replace("top ", ""), font=font, fill=(255, 255, 255, 255))
    
    async def build(self):
        bg = Image.new(Ticket.RGBA, Ticket.bacground_size, (0,0,0,0))
        
        bg.alpha_composite(self.light_cone_background.resize((302,182)),(29,35))
        bg.alpha_composite(self.background_relict,(29,310)) 
        bg.alpha_composite(self.background_sets,(29,222))
        bg.alpha_composite(self.background_stats,(884,56))
        bg.alpha_composite(self.main_bg,(500,68))
        bg.alpha_composite(self.dop_bg,(446,165))
        bg.alpha_composite(self.background_skills,(455,327))
        bg.alpha_composite(self.background_name,(1350,691))
        bg.alpha_composite(self.background_score,(442,436))
        bg.alpha_composite(self.seelelen,(1688,718)) 
        
        if self.gif:
            self.background = []
            for key in self.GIFT_BG:
                key.alpha_composite(bg)
                self.background.append(key.convert("RGB"))
        else:
            self.background.alpha_composite(bg)
        
    async def start(self):
        _of.set_mapping(2)
        
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
                            await self.creat_bacground()
                            self.GIFT_BG.append(self.background.copy())
                        frame_count += 1
            else:
                self.element_color = await pill.get_colors(self.art, 15, common=True, radius=5, quality=800)
                await self.creat_bacground()
        else:
            self.element_color = (255,213,167,255)
            await self.creat_bacground()
        
        async with anyio.create_task_group() as tasks:
            tasks.start_soon(self.creat_light_cone)
            tasks.start_soon(self.creat_stats)
            tasks.start_soon(self.creat_name)
            tasks.start_soon(self.creat_constant)
            tasks.start_soon(self.creat_relict_sets)
            tasks.start_soon(self.get_score)
            tasks.start_soon(self.creat_path)
            tasks.start_soon(self.creat_seeleland)
        
        async def wait_all(*funcs):
            results = [None] * len(funcs)
            
            async with anyio.create_task_group() as tasks:
                async def process(func, i):
                    results[i] = await func()
                
                for i, func in enumerate(funcs):
                    tasks.start_soon(process, func, i)
            
            return results
        
        self.relict = await wait_all(*[
            functools.partial(self.creat_relict, key)
            for key in self.data.relics
        ])


            #self.relict = await asyncio.gather(*relic_tasks)
        
        
        
        await self.creat_score_total()
        await self.build_relict()
        await self.build()
        
        data = {
                "id": self.data.id,
                "name": self.data.name,
                "animation": self.gif,
                "rarity": self.data.rarity,
                "card": self.background,
                "size": Ticket.bacground_size,
                "color": self.element_color,
            }
            
        return data