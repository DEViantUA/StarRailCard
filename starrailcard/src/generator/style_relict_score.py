# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import anyio
import functools
import io
from PIL import ImageDraw,Image,ImageFilter,ImageChops, ImageSequence

from ..tools import git, options
from ..tools.calculator import stats
from ..model.style import RelictScore

from ..tools import pill

_of = git.ImageCache()

_DEFAULT_SCORE = {'count': 0, 
                  'rolls': {}, 
                  'rank': {'name': 'N/A', 
                           'color': (255, 255, 255, 255)
                    }
}

async def get_cone_frame(x):
    if x == 5:
        return await _of.light_cone_frame_five
    elif x == 4:
        return await _of.light_cone_frame_four
    else:
        return await _of.light_cone_frame_three

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
    
    async def create_bacground(self):
        self.background = Image.new(RelictScore.RGBA, RelictScore.background_size, (0,0,0,0))
        background_dark = Image.new(RelictScore.RGBA, RelictScore.background_size, (0,0,0,100))
        background_art = Image.new(RelictScore.RGBA, RelictScore.background_size, (0,0,0,0))
        background_blur = Image.new(RelictScore.RGBA, RelictScore.background_size, (0,0,0,0))
        lines = await _of.background_line
        logo = await _of.LOGO_GIT
        shadow = await _of.background_shadow
        maska_art = await _of.background_maska_art
        background_overlay = await _of.background_overlay
        background_maska_blur = await _of.background_maska_blur
        background_default = await _of.background_default
                
        if self.art:
            user_image = await pill.get_center_size(RelictScore.art_size, self.art)
            bg = await pill.GradientGenerator(user_image).generate(1,RelictScore.background_size[1])       
            bg = bg.resize(RelictScore.background_size)
            user_image_op = await pill.apply_opacity(user_image, opacity = RelictScore.opacity_art)

            background_blur.alpha_composite(bg.convert("RGBA"))
            background_blur.alpha_composite(user_image_op)
            
            background_blur = background_blur.filter(ImageFilter.GaussianBlur(RelictScore.blur_art))
            line,self.element_color = await pill.recolor_image(lines, self.element_color[:3], light = True)            
        else:
            bg = background_default.copy() 
            user_image = await pill.get_center_scale(RelictScore.splash_size, await pill.get_download_img(self.data.portrait))
            user_image_op = await pill.apply_opacity(user_image, opacity = RelictScore.opacity_splash)
            background_blur.alpha_composite(bg.convert("RGBA"))
            background_blur.alpha_composite(user_image_op)
            background_blur = background_blur.filter(ImageFilter.GaussianBlur(RelictScore.blur_splashart))
            line = await pill.recolor_image(lines, self.element_color[:3])
            
        background_blur.alpha_composite(background_dark)
        self.background.paste(background_blur,(0,0), background_maska_blur.convert("L"))
        if self.art:
            self.background = ImageChops.soft_light(self.background, background_overlay)
                
        background_art.alpha_composite(bg.convert("RGBA"))
        background_art.alpha_composite(user_image)
        self.background.paste(background_art,(0,0),maska_art.convert("L"))
        self.background.alpha_composite(shadow)
        self.background.alpha_composite(line, (RelictScore.position_line))
        if not self.remove_logo:
            self.background.alpha_composite(logo)
        
        if not self.hide_uid:
            uid = Image.new(RelictScore.RGBA, RelictScore.background_size, (0,0,0,0))
            d = ImageDraw.Draw(uid)
            
            font_10 = await pill.get_font(RelictScore.font_uid)
            d.text((0,0), f"UID: {self.uid}", font=font_10, fill=(255, 255, 255, 75))
            self.background.alpha_composite(uid,RelictScore.position_uid)
    
    async def create_light_cone(self):
        self.background_light_cones = Image.new(RelictScore.RGBA, (330, 190), (0, 0, 0, 0))
        if self.data.light_cone is None:
            return
        
        background = Image.new(RelictScore.RGBA, (139, 190), (0, 0, 0, 0))
        image = await pill.get_download_img(self.data.light_cone.portrait, size=(118, 169))
        background.alpha_composite(image,(9,9))
        light_cone_frame_stars = await get_cone_frame(self.data.light_cone.rarity)
        background.alpha_composite(light_cone_frame_stars)
        light_cone_frame = await _of.light_cone_frame
        background.alpha_composite(light_cone_frame)
        
        self.background_light_cones.alpha_composite(background)
        
        background = await _of.light_cone_stats
        background = background.copy()
        
        d = ImageDraw.Draw(background)
        
        font_18 = await pill.get_font(18)
        d.text((28, 4), self.data.light_cone.attributes[0].display, font=font_18, fill=(255, 255, 255, 255))
        d.text((28, 30), self.data.light_cone.attributes[1].display, font=font_18, fill=(255, 255, 255, 255))
        d.text((28, 56), self.data.light_cone.attributes[2].display, font=font_18, fill=(255, 255, 255, 255))
        
        self.background_light_cones.alpha_composite(background,(140,100))
        
        background = await _of.light_cone_ups
        background = background.copy()
        
        d = ImageDraw.Draw(background)
        font_12 = await pill.get_font(12)
        up = options.ups(self.data.light_cone.rank)
        x = int(font_12.getlength(str(up))/2)
        d.text((10-x, 4), up, font= font_12, fill=(255, 217, 144, 255))
        
        self.background_light_cones.alpha_composite(background,(140,68))
        d = ImageDraw.Draw(self.background_light_cones)
        d.text((165, 69), f"{self.lang.lvl}: {self.data.light_cone.level}/{options.max_lvl(self.data.light_cone.promotion)}", font=font_18, fill=(255, 255, 255, 255))
        
        names = await pill.create_image_with_text(self.data.light_cone.name, 18, max_width=180, color=(255, 255, 255, 255))
        line = Image.new("RGBA", (1,48), options.color_lc_line.get(str(self.data.light_cone.rarity), (150, 202, 255, 255)))
        
        
        self.background_light_cones.alpha_composite(line,(140,9))
        self.background_light_cones.alpha_composite(names,(146,int(34-names.size[1]/2)))   
    
    async def create_stats(self):
        self.background_stats = Image.new(RelictScore.RGBA, (563, 290), (0, 0, 0, 0))

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
        
        xp,y = 0,0

        async for i, background in pill.create_stats(combined_attributes, dop, 
                      RelictScore.stat_font_dop,RelictScore.stat_font,
                      RelictScore.stat_line_size, RelictScore.stat_name_size, RelictScore.stat_max_width, RelictScore.stat_icon_size,
                      RelictScore.stat_icon_position, RelictScore.stat_name_position, RelictScore.stat_x_position,
                      self.element_color, RelictScore.stat_value_font):
            self.background_stats.alpha_composite(background,(xp,y))
            y += 45
            if i == 5:
                xp = 290
                y = 0
 
    async def create_name(self):
        self.background_name = Image.new(RelictScore.RGBA, RelictScore.name_size, (0, 0, 0, 0))
        d = ImageDraw.Draw(self.background_name)
        names = await pill.create_image_with_text(self.data.name, RelictScore.font_name_size , max_width=RelictScore.name_with, color= RelictScore.name_color)
        if names.size[1] <= RelictScore.name_h_max:
            self.background_name.alpha_composite(names,(RelictScore.name_position,int(RelictScore.name_h_max-names.size[1]/2)))
        else:
            self.background_name.alpha_composite(names,(RelictScore.name_position,int(RelictScore.name_h_min-names.size[1]/2)))
        
        font_17 = await pill.get_font(RelictScore.font_name_level)
        max_level = options.max_lvl(self.data.promotion)
        level = f"{self.lang.lvl}: {self.data.level}/{max_level}"
        d.text(RelictScore.position_name_level, level, font=font_17, fill= RelictScore.color_name_level)
        starts = await options.get_stars(self.data.rarity)
        self.background_name.alpha_composite(starts,RelictScore.position_name_star)
       
    async def create_constant(self):
        self.background_skills = Image.new(RelictScore.RGBA, RelictScore.constant_size_background, (0, 0, 0, 0))
        x = 0
        rank = self.data.rank
        for key in self.data.rank_icons[:rank]:
            bg = Image.new(RelictScore.RGBA, RelictScore.constant_size, (0, 0, 0, 0))
            icon = await pill.get_download_img(key, size=RelictScore.constant_size_icon)
            icon_blur = icon.filter(ImageFilter.GaussianBlur(RelictScore.constant_blur))
            icon_blur = await pill.recolor_image(icon_blur, self.element_color[:3])
            bg.alpha_composite(icon_blur,RelictScore.constant_icon_position)
            bg.alpha_composite(icon,RelictScore.constant_icon_position)
            self.background_skills.alpha_composite(bg,(x,0))
            x += 68

        for key in self.data.rank_icons[rank:]:
            bg = Image.new(RelictScore.RGBA, RelictScore.constant_size, (0, 0, 0, 0))
            icon = await pill.get_download_img(key, size= RelictScore.constant_size_icon)
            icon = await pill.apply_opacity(icon, opacity=RelictScore.constant_size_icon_opacity)
            bg.alpha_composite(icon,RelictScore.constant_icon_position)
            self.background_skills.alpha_composite(bg,(x,0))
            x += 68
     
    async def create_relict_sets(self):
        rel_set = options.calculator_relict_sets(self.data.relic_sets)

        self.background_sets = Image.new(RelictScore.RGBA, RelictScore.sets_background, (0,0,0,0))
        
        font = await pill.get_font(RelictScore.sets_font)
        
        line_items = []
        i = 0
        for key in rel_set:
            sets = rel_set[key]
            holst_line = Image.new(RelictScore.RGBA, RelictScore.sets_line_size, (0,0,0,0))
            background_count = await _of.relict_count_sets
            background_count = background_count.copy()
            d = ImageDraw.Draw(background_count)
            d.text(RelictScore.sets_count_position, str(sets["num"]), font=font, fill= RelictScore.sets_name_color)
            d = ImageDraw.Draw(holst_line)
            sets_name_font,size = await pill.get_text_size_frame(sets["name"],15,492)
            if key[:1] == "1":
                holst_line.alpha_composite(background_count)
                d.text((36, 4), sets["name"], font=sets_name_font, fill=RelictScore.sets_name_color)
                line_items.append({"setap": i, "line": holst_line})
                i += 1
            else:
                holst_line.alpha_composite(background_count,(530 - background_count.size[0],0))
                d.text((int(521 - background_count.size[0] -size), 4), sets["name"], font=sets_name_font, fill=RelictScore.sets_name_color)
                line_items.append({"setap": 1, "line": holst_line})
                
        for key in line_items:
            if key["setap"] == 1:
                self.background_sets.alpha_composite(key["line"],(0,29))
            elif key["setap"] == 2:
                self.background_sets.alpha_composite(key["line"],(0,29))
            else:
                self.background_sets.alpha_composite(key["line"],(0,0))
    
    async def create_relict(self,relict):
        background_main = Image.new(RelictScore.RGBA,RelictScore.relict_size, (0,0,0,0))
        background = Image.new(RelictScore.RGBA,RelictScore.relict_size, (0,0,0,0))
        background_image = Image.new("RGBA",RelictScore.relict_size, (0,0,0,0))
        relict_frame = await _of.relict_frame
        relict_maska = await _of.relict_maska
        relict_score_frame = await _of.relict_score_frame
        relict_line = await _of.relict_line
        
        background_main.alpha_composite(relict_frame)
        image = await pill.get_download_img(relict.icon, size= RelictScore.relict_icon_size)
        background_image.alpha_composite(image,RelictScore.relict_icon_position)
        background.paste(background_image,(0,0),relict_maska.convert("L"))
        
        background_main.alpha_composite(relict_score_frame,(8,0))
        background_main.alpha_composite(background)
        background_main.alpha_composite(relict_line)
        score = self.score_info["score"].get(str(relict.id),_DEFAULT_SCORE)
        
        main_stat_icon = await pill.get_download_img(relict.main_affix.icon, size= RelictScore.relict_main_stat_icon_size)
        color = options.color_element.get(relict.main_affix.type, None)
        if not color is None:
            main_stat_icon = await pill.recolor_image(main_stat_icon, color[:3])
        stars = await options.get_stars(relict.rarity, type = 1)
        
        background_main.alpha_composite(stars,RelictScore.relict_position_star)
        background_main.alpha_composite(main_stat_icon,RelictScore.relict_main_stat_icon_position)
        
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
            icon = await pill.get_download_img(k.icon, size=RelictScore.relict_sub_icon_size)
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
    
    async def get_path(self):
        self.background_path = await pill.create_path(self.data)
    
    async def get_score(self):
        self.score_info = await stats.Calculator(self.data).start(self.hoyo)
        
    async def build_relict(self):
        self.background_relict = Image.new(RelictScore.RGBA, (1131,297), (0,0,0,0))
        none_relict = await _of.none_relict
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
                self.background_relict.alpha_composite(none_relict, position.get(key))

        self.background_relict.alpha_composite(self.background_score,(0,112))
        self.background_relict.alpha_composite(self.background_sets,(0,45))
    
    async def create_seeleland(self):
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
    
    async def create_score_total(self):
        self.background_score = Image.new("RGBA",(559,43), (0,0,0,0))
        
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
        if ll > 0.6 or frame == (51, 51, 51):
            d.text((x, -1), f"{round(result_percentage,1)}%", font=font_18, fill = (0,0,0,166))
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
        d.text((497, -2), str(self.total_eff), font=font_21, fill = options.color_scoreR.get(self.total_eff,(255,255,255,255)))   
    
    async def build(self):
        bg = Image.new(RelictScore.RGBA, RelictScore.background_size, (0,0,0,0))
        bg.alpha_composite(self.background_light_cones,RelictScore.build_lc_position)
        bg.alpha_composite(self.background_stats,RelictScore.build_stats_position)
        bg.alpha_composite(self.background_name,RelictScore.build_name_position)
        bg.alpha_composite(self.background_skills.resize(RelictScore.build_constant_size),RelictScore.build_constant_position)
        bg.alpha_composite(self.background_path.resize(RelictScore.build_skill_size),RelictScore.build_skill_position)
        bg.alpha_composite(self.background_relict,RelictScore.build_relict_position)
        bg.alpha_composite(self.seelelen,RelictScore.build_seelelen_position)
        
        if self.gif:
            self.background = []
            for key in self.GIFT_BG:
                key.alpha_composite(bg)
                self.background.append(key.convert("RGB"))
        else:
            self.background.alpha_composite(bg)
                    
    async def start(self, build = None, hoyo = False):
        _of.set_mapping(1)
        self.hoyo = hoyo
        if self.art:
            if "gif" in self.art:
                self.gif = True
            self.art = await pill.get_user_image(self.art)
            
        if self.gif:    
            n = 2           
            frame_count = 0
            color = True
            with io.BytesIO(self.art) as f:
                self.art = Image.open(f)
                for frame in ImageSequence.Iterator(self.art):
                    if color:
                        self.element_color = await pill.get_colors(frame.convert("RGBA"), 15, common=True, radius=5, quality=800)
                        color = False
                    if frame_count >= 50:
                        break
                    if frame_count % n != 0:
                        self.art = frame.convert("RGBA")
                        await self.create_bacground()
                        self.GIFT_BG.append(self.background.copy())
                    frame_count += 1            
        else:
            if self.art:
                self.element_color = await pill.get_colors(self.art, 15, common=True, radius=5, quality=800)
            
            await self.create_bacground()
        
             
        async with anyio.create_task_group() as tasks:
            tasks.start_soon(self.create_light_cone)
            tasks.start_soon(self.create_stats)
            tasks.start_soon(self.create_name)
            tasks.start_soon(self.create_constant)
            tasks.start_soon(self.create_relict_sets)
            tasks.start_soon(self.get_score)
            tasks.start_soon(self.get_path)
            tasks.start_soon(self.create_seeleland)
        
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
            "animation":  self.gif,
            "name": self.data.name,
            "rarity": self.data.rarity,
            "card": self.background,
            "size": RelictScore.background_size,
            "color": self.element_color,
            "build": build
        }
        
        return data