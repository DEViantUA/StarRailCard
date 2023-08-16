# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
from PIL import Image
import threading
from weakref import WeakValueDictionary
from pathlib import Path

assets = Path(__file__).parent.parent / 'assets'
font = str(assets / 'font' / 'NotoSansKR-Bold.otf')

async def change_font(x):
    global font
    if x == "cn":
        font = str(assets / 'font' / 'NotoSansCJKsc-Bold.otf')
    else:
        font = str(assets / 'font' / 'NotoSansKR-Bold.otf')


mapping = {
    'total_bg': assets/'bg'/'bg.png',
    'bg_charters': assets/'bg'/'bg_charters.png',
    'frame_charters': assets/'bg'/'frame_charters.png',
    'maska_charters': assets/'bg'/'maska.png',

    'strs_1': assets/'stars'/'strs_1.png',
    'strs_2': assets/'stars'/'strs_2.png',
    'strs_3': assets/'stars'/'strs_3.png',
    'strs_4': assets/'stars'/'strs_4.png',
    'strs_5': assets/'stars'/'strs_5.png',

    'Closed': assets/'const'/'Closed.png',
    'Lock': assets/'const'/'Lock.png',
    'open': assets/'const'/'open.png',

    'bg_lc_total': assets/'lc'/'bg.png',
    'bg_lc': assets/'lc'/'bg_lc.png',
    'maska_lc': assets/'lc'/'maska.png',

    'logo': assets/'LOGO.png',
    'uid': assets/'UID.png',
    'STATS': assets/'STATS.png',

    'ARTIFACT': assets/'ARTIFACT.png',

    'bg_main': assets/'Tallants'/'bg_main.png',
    'bg_dop': assets/'Tallants'/'bg_dop.png',
    'bg_talants': assets/'Tallants'/'bg.png',
    'count_talants': assets/'Tallants'/'count.png',
    'dop_0': assets/'Tallants'/'dop_0.png',
    'dop_1': assets/'Tallants'/'dop_1.png',
    'dop_2': assets/'Tallants'/'dop_2.png',
    'dop_3': assets/'Tallants'/'dop_3.png', 

    'sets_bg': assets/'Sets'/'bg.png',
    'sets_count': assets/'Sets'/'count.png',

    #TEAMPLE TWO

    "bg_wind": assets/'teample_two'/'bg'/'ANEMO.png',
    "bg_electro": assets/'teample_two'/'bg'/'ELECTRO.png',
    "bg_fire": assets/'teample_two'/'bg'/'FIRE.png',
    "bg_ice": assets/'teample_two'/'bg'/'ICE.png',
    "bg_imaginary": assets/'teample_two'/'bg'/'IMAGINARY.png',
    "bg_quantom": assets/'teample_two'/'bg'/'QUANTOM.png',
    "bg_psyhical": assets/'teample_two'/'bg'/'PSYHICAL.png',
    "MASKA_ART": assets/'teample_two'/'bg'/'MASKA_ART.png',
    "MASKA_ART_CUSTUM": assets/'teample_two'/'bg'/'MASKA_ART_CUSTUM.png',
    "MASKA_ARTS": assets/'teample_two'/'bg'/'MASKA_ARTS.png',
    "shadow": assets/'teample_two'/'bg'/'SHADOW.png',
    "effect_stars": assets/'teample_two'/'bg'/'stars.png',

    "Maska_LC": assets/'teample_two'/'LC'/'Maska.png',
    "shadow_LC": assets/'teample_two'/'LC'/'shadow.png',
    "icons_LC": assets/'teample_two'/'LC'/'icons.png',

    "bg_relic_ANEMO": assets/'teample_two'/'artifact'/'ANEMO.png',
    "bg_relic_ELECTRO": assets/'teample_two'/'artifact'/'ELECTRO.png',
    "bg_relic_FIRE": assets/'teample_two'/'artifact'/'FIRE.png',
    "bg_relic_ICE": assets/'teample_two'/'artifact'/'ICE.png',
    "bg_relic_IMAGINARY": assets/'teample_two'/'artifact'/'IMAGINARY.png',
    "bg_relic_PSYHICAL": assets/'teample_two'/'artifact'/'PSYHICAL.png',
    "bg_relic_QUANTOM": assets/'teample_two'/'artifact'/'QUANTOM.png',
    "relic_mask": assets/'teample_two'/'artifact'/'maska.png',
    "relic_frame": assets/'teample_two'/'artifact'/'frame.png',
    "rank": assets/'teample_two'/'artifact'/'rank.png',
    "sets_relic": assets/'teample_two'/'artifact'/'sets.png',

    "stats_frame": assets/'teample_two'/'stats'/'bg.png',
    "total_stats_frame": assets/'teample_two'/'artifact'/'rank_total.png',


    "Knight": assets/'teample_two'/'path'/'Knight.png',
    "Mage": assets/'teample_two'/'path'/'Mage.png',
    "Priest": assets/'teample_two'/'path'/'Priest.png',
    "Rogue": assets/'teample_two'/'path'/'Rogue.png',
    "Shaman": assets/'teample_two'/'path'/'Shaman.png',
    "Warlock": assets/'teample_two'/'path'/'Warlock.png',
    "Warrior": assets/'teample_two'/'path'/'Warrior.png',

    "path_closed": assets/'teample_two'/'path'/'closed.png',
    "path_closed_dop": assets/'teample_two'/'path'/'closed_dop.png',
    "path_count": assets/'teample_two'/'path'/'count.png',



    "shadow_bg": assets/'teample_tree'/'bg'/'shadow_bg.png',
    "splash_art": assets/'teample_tree'/'bg'/'splash_art.png',
    "shadow_art": assets/'teample_tree'/'bg'/'shadow_art.png',
    "art_frame": assets/'teample_tree'/'bg'/'art_frame.png',
    "overlay": assets/'teample_tree'/'bg'/'overlay.png',

    "lc_3_stars": assets/'teample_tree'/'lc'/'3_stars.png',
    "lc_4_stars": assets/'teample_tree'/'lc'/'4_stars.png',
    "lc_5_stars": assets/'teample_tree'/'lc'/'5_stars.png',
    "blink": assets/'teample_tree'/'lc'/'blink.png',
    "lc_info": assets/'teample_tree'/'lc'/'info.png',

    "closed_main": assets/'teample_tree'/'skills'/'closed_main.png',
    "main_skills": assets/'teample_tree'/'skills'/'main.png',
    "closed_trees": assets/'teample_tree'/'skills'/'closed_trees.png',
    "count_tree": assets/'teample_tree'/'skills'/'count_tree.png',
    "dop": assets/'teample_tree'/'skills'/'dop.png',
    "open_trees": assets/'teample_tree'/'skills'/'open_trees.png',

    "ON_const": assets/'teample_tree'/'const'/'ON.png',
    "OFF_const": assets/'teample_tree'/'const'/'OFF.png',
    "CLOSED_const": assets/'teample_tree'/'const'/'CLOSED.png',

    "artifact_tree": assets/'teample_tree'/'artifact'/'artifact.png',
    "sets_tree": assets/'teample_tree'/'artifact'/'sets.png',


    "frame_art_1": assets/'teample_tree'/'artifact'/'frame_art_1.png',
    "frame_art_2": assets/'teample_tree'/'artifact'/'frame_art_2.png',
    "frame_art_3": assets/'teample_tree'/'artifact'/'frame_art_3.png',
    "frame_art_4": assets/'teample_tree'/'artifact'/'frame_art_4.png',
    "frame_art_5": assets/'teample_tree'/'artifact'/'frame_art_5.png',

    "name_banners": assets/'teample_tree'/'name_banners.png',
    "stars_five": assets/'teample_tree'/'stars_five.png',
    "stars_four": assets/'teample_tree'/'stars_four.png',

    "icon": assets/"icon.png",
    "icon_maska": assets/"icon_maska.png",


    "seeleland": assets/"seeleland.png"

    




}


class ImageCache:
    def __init__(self):
        self.mapping = mapping
        self.cache = WeakValueDictionary()
        self.lock = threading.Lock()
        self.assets = assets

    def __dir__(self):
        return sorted(set([*globals(), *self.mapping]))

    def __getattr__(self, name):
        path = self.mapping.get(name)
        if not path:
            raise AttributeError(name)
    
        with self.lock:
            try:
                image = self.cache[name]
            except KeyError:
                self.cache[name] = image = Image.open(self.assets / path)
        
            return image