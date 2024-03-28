# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from enum import Enum
from pathlib import Path
    
class Ukrainization(Enum):
    STATS = "stats"
    WEAPON = "weapons"
    AVATAR = "avatar"
    RELICT_SETS = "relict_sets"
    PATH = "paths"
    ELEMENT = "element"
    
    @classmethod
    def __iter__(cls):
        return iter(file.value for file in cls)
    
class PathData(Enum):
    UKRAINIZATION = Path(__file__).parent.parent / "data"
    
class Style(Enum):
    RELICT_SCORE = 1
    TICKET = 2
    ENKA = 3
