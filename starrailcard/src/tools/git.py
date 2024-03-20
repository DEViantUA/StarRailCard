# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image
import os
import threading
from pathlib import Path
from io import BytesIO

from .http import AioSession
from .cashe import Cache

lock = threading.Lock()

_caches = Cache.get_cache()

assets = Path(__file__).parent.parent / 'assets'

_BASE_URL = 'https://raw.githubusercontent.com/DEViantUA/StarRailCardData/main/asset/'

font = str(assets / 'font' / 'font_hsr.ttf')


def determine_font_path_automatically(font_file = 'Times New Roman.ttf'):
    font_dirs = [
        '/usr/share/fonts',          
        '/usr/local/share/fonts',    
        '/Library/Fonts',           
    ]
        
    for font_dir in font_dirs:
        font_path = os.path.join(font_dir, font_file)
        if os.path.isfile(font_path):
            return font_path

    return None

async def change_font(font_path = None):
    global font
    if font_path is None:
        font = str(assets / 'font' / 'font_hsr.ttf')
    else:
        font_path = os.path.abspath(font_path)
        if os.path.isfile(font_path):
            font = font_path 
        else:
            font_path = determine_font_path_automatically(font_path)
            if font_path is None:
                font = str(assets / 'font' / 'font_hsr.ttf')


total_style = {
    'g_five': 'teample_two_new/stars/g_five.png',
    'g_four': 'teample_two_new/stars/g_four.png',
    'g_three': 'teample_two_new/stars/g_three.png',
    'g_two': 'teample_two_new/stars/g_two.png',
    'g_one': 'teample_two_new/stars/g_one.png',
    
    'strs_1': 'stars/strs_1.png',
    'strs_2': 'stars/strs_2.png',
    'strs_3': 'stars/strs_3.png',
    'strs_4': 'stars/strs_4.png',
    'strs_5': 'stars/strs_5.png',
    
    'stars_v_5': 'three/stars/stars_5.png',
    'stars_v_4': 'three/stars/stars_4.png',
    'stars_v_3': 'three/stars/stars_3.png',
    'stars_v_2': 'three/stars/stars_2.png',
    'stars_v_1': 'three/stars/stars_1.png',
    
    "Knight": 'teample_two_new/path/Knight.png',
    "Mage": 'teample_two_new/path/Mage.png',
    "Priest": 'teample_two_new/path/Priest.png',
    "Rogue": 'teample_two_new/path/Rogue.png',
    "Shaman": 'teample_two_new/path/Shaman.png',
    "Warlock": 'teample_two_new/path/Warlock.png',
    "Warrior": 'teample_two_new/path/Warrior.png',
    
    'relict_backgroundl_score_line': 'teample_two_new/relict/backgroundl_score_line.png',
    'relict_full_score_line': 'teample_two_new/relict/full_score_line.png',
    
    'light_cone_ups': 'teample_two_new/light_cone/ups.png',
    
    'LOGO_GIT': 'teample_two_new/LOGO.png',
    'LOGO_GIT_INV': 'three/LOGO.png',
    'seeleland_v2': "seeleland_v2.png"
}

relict_score = {
    'background_default': 'teample_two_new/background/background_default.png',
    'background_line': 'teample_two_new/background/line.png',
    'background_maska_art': 'teample_two_new/background/maska_art.png',
    'background_maska_blur': 'teample_two_new/background/maska_blur.png',
    'background_overlay': 'teample_two_new/background/overlay.png',
    'background_shadow': 'teample_two_new/background/shadow.png',
    
    
    'light_cone_frame': 'teample_two_new/light_cone/frame.png',
    'light_cone_frame_five': 'teample_two_new/light_cone/frame_five.png',
    'light_cone_frame_four': 'teample_two_new/light_cone/frame_four.png',
    'light_cone_frame_three': 'teample_two_new/light_cone/frame_three.png',
    'light_cone_stats': 'teample_two_new/light_cone/stats.png',
        
    'relict_backgroundl_score_line': 'teample_two_new/relict/backgroundl_score_line.png',
    'relict_full_score_line': 'teample_two_new/relict/full_score_line.png',
    'relict_count_sets': 'teample_two_new/relict/count_sets.png',
    'relict_frame_line': 'teample_two_new/relict/frame_line.png',    
    'relict_line': 'teample_two_new/relict/line.png',
    'relict_frame': 'teample_two_new/relict/relict_frame.png',
    'relict_maska': 'teample_two_new/relict/relict_maska.png',
    'relict_score_frame': 'teample_two_new/relict/score_frame.png',
    'none_relict': 'teample_two_new/relict/none_relict.png',

    'path_count': 'teample_two_new/path/count.png',
    'path_closed_main': 'teample_two_new/path/closed_main.png',
    'path_closed_dop': 'teample_two_new/path/closed_dop.png',
}

ticket = {
    "background_line": 'three/bg/art_frame.png',
    "background_shadow": 'three/bg/shadow_art.png',
    "background_overlay": 'three/bg/overlay.png',
    
    'shadow_3_light_cone': 'three/light_cones/3_shadow_lc.png',
    'star_3_frame_light_cone': 'three/light_cones/3_star_frame_lc.png',
    'shadow_4_light_cone': 'three/light_cones/4_shadow_lc.png',
    'star_4_frame_light_cone': 'three/light_cones/4_star_frame_lc.png',
    'shadow_5_light_cone': 'three/light_cones/5_shadow_lc.png',
    'star_5_frame_light_cone': 'three/light_cones/5_star_frame_lc.png',
    'blic_light_cones': 'three/light_cones/blic.png',
    'frame_light_cones': 'three/light_cones/frame_lc.png',
    'maska_light_cones': 'three/light_cones/maska_lc.png',
    'stats_light_cones': 'three/light_cones/stats.png',
    
    
    'relict_count': 'three/relict/count.png',
    'relict_count_lvl': 'three/relict/count_lvl.png',
    'relict_background': 'three/relict/relict_background.png',
    'relict_maska': 'three/relict/relict_maska.png',
    'relict_score_frame': 'three/relict/score_frame.png',
    'none_relict': 'three/relict/none.png',
    'relict_icon_sets': 'three/relict/icon_sets.png',
    'relict_count_sets': 'three/relict/count_sets.png',
    
    "closed_main": 'three/skills/closed_main.png',
    "main_skills": 'three/skills/main.png',
    
    "frame_main": 'three/skills/frame_main.png',
    "bg_main": 'three/skills/main.png',
    
    "closed_trees": 'three/skills/closed_trees.png',
    "count_tree": 'three/skills/count_tree.png',
    "dop": 'three/skills/dop.png',
    "open_trees": 'three/skills/open_trees.png',

    "ON_const": 'three/const/ON.png',
    "OFF_const": 'three/const/OFF.png',
    "CLOSED_const": 'three/const/CLOSED.png',
}

profile_phone = {
    "bg_1": 'profile_phone/bg_1.png',
    "bg_2": 'profile_phone/bg_2.png',
    "bg_3": 'profile_phone/bg_3.png',
    "bg_5": 'profile_phone/bg_5.png',
    "desc_frame": 'profile_phone/desc_frame.png',
    "maska_prof_bg": 'profile_phone/maska_prof_bg.png',
    "menu": 'profile_phone/menu.png',
    "avatar_four": 'profile_phone/avatar_four.png',
    "avatar_five": 'profile_phone/avatar_five.png',
    'maska_character': 'profile_phone/maska_charter.png'
}

class ImageCache:
    
    _assets_dowload = False
    _mapping = {}
            
    @classmethod
    async def set_assets_dowload(cls, dowload = False):
        cls._assets_dowload = dowload
    
    @classmethod
    def set_mapping(cls,style):
        if style == 1:
            cls._mapping = relict_score
        elif style == 2:
            cls._mapping = ticket
        elif style == 3:
            cls._mapping = profile_phone
        
    @classmethod
    async def _load_image(cls, name):
        
        try:
            image = _caches[name]
        except KeyError:
            try:
                _caches[name] = image = Image.open(assets / name)
                return _caches[name]
            except Exception as e:
                pass
        
        try:
            _caches[name] = image = Image.open(assets / name)
            return _caches[name]
        except Exception as e:
            pass
        
        url = _BASE_URL + name
        if url in _caches:
            return _caches[name]
        else:
            image_data = await AioSession.get(url, response_format= "bytes")
            image = Image.open(BytesIO(image_data))
            _caches[name] = image
        
        if cls._assets_dowload:
            file_path = assets / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(str(assets / name))
        
        return image

    async def __getattr__(cls, name):
        if name in cls._mapping:
            return await cls._load_image(cls._mapping[name])
        else:
            if name in total_style:
                return await cls._load_image(total_style[name]) 
            else:
                raise AttributeError(f"'{cls.__class__.__name__}' object has no attribute '{name}'")
        
    async def download_icon_stats(self, prop_id):
        if 'icon_stats' in self.mapping:
            url = self.mapping['icon_stats'].format(prop_id=prop_id)
            full_url = _BASE_URL + url
            if full_url in _caches:
                return _caches[full_url].copy()
            else:
                image_data = await self.download_image(full_url)
                image = Image.open(image_data)
                _caches[full_url] = image
                return image.copy()
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute 'icon_stats'")

    async def download_icon_constant(self, element, unlock, resizes = None):
        if 'icon_const_unlock' in self.mapping and "icon_const_lock" in self.mapping:
            if unlock:
                url = self.mapping['icon_const_unlock'].format(element=element.upper())
            else:
                url = self.mapping['icon_const_lock'].format(element=element.upper())
            full_url = _BASE_URL + url
            key = (full_url, resizes, unlock)
            if key in _caches:
                return _caches[key].copy()
            else:
                image_data = await self.download_image(full_url)
                image = Image.open(image_data)
                if not resizes is None:
                    image = image.resize(resizes)
                    
                _caches[full_url] = image
                return image.copy()
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute 'icon_stats'")