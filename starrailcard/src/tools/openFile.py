# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
from PIL import Image
import threading
from weakref import WeakValueDictionary
from pathlib import Path

assets = Path(__file__).parent.parent / 'assets'
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