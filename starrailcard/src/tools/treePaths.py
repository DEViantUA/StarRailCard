# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import aiohttp

url = "https://raw.githubusercontent.com/FortOfFans/HSRMaps/master/maps/en/avatartree.json"

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json(content_type='text/plain')
            return data



point_map = {
   "Warlock":{
      "Point01":{
         "icon":(157,186),
         "count":(160,236)
      },
      "Point02":{
         "icon":(367,186),
         "count":(370,236)
      },
      "Point03":{
         "icon":(262,174),
         "count":(265,228)
      },
      "Point04":{
         "icon":(262,91),
         "count":(265,142)
      },
      "Point05":{
         "icon":(262,278)
      },
      "Point09":{
         "icon":(270,357)
      },
      "Point18":{
         "icon":(270,435)
      },
      "Point06":{
         "icon":(75,152)
      },
      "Point10":{
         "icon":(5,244)
      },
      "Point11":{
         "icon":(70,327)
      },
      "Point12":{
         "icon":(137,
         406)
      },
      "Point07":{
         "icon":(453,
         152)
      },
      "Point13":{
         "icon":(527,
         244)
      },
      "Point14":{
         "icon":(467,
         327)
      },
      "Point15":{
         "icon":(401,
         406)
      },
      "Point08":{
         "icon":(262,
         8)
      },
      "Point16":{
         "icon":(153,
         32)
      },
      "Point17":{
         "icon":(385,
         32)
      }
   },
   "Warrior":{
      "Point01":{
         "icon":(147,
         214),
         "count":(150,
         265)
      },
      "Point02":{
         "icon":(373,
         214),
         "count":(375,
         265)
      },
      "Point03":{
         "icon":(259,
         229),
         "count":(262,
         282)
      },
      "Point04":{
         "icon":(259,
         137),
         "count":(262,
         189)
      },
      "Point05":{
         "icon":(259,
         334)
      },
      "Point09":{
         "icon":(266,
         431)
      },
      "Point06":{
         "icon":(141,
         347)
      },
      "Point10":{
         "icon":(69,
         301)
      },
      "Point11":{
         "icon":(0,
         235)
      },
      "Point12":{
         "icon":(62,
         142)
      },
      "Point07":{
         "icon":(381,
         347)
      },
      "Point13":{
         "icon":(463,
         301)
      },
      "Point14":{
         "icon":(531,
         235)
      },
      "Point15":{
         "icon":(467,
         142)
      },
      "Point08":{
         "icon":(260,
         63)
      },
      "Point16":{
         "icon":(266,
         1)
      },
      "Point17":{
         "icon":(148,
         20)
      },
      "Point18":{
         "icon":(383,
         20)
      }
   },
   "Rogue":{
      "Point01":{
         "icon":(158,
         187),
         "count":(160,
         239)
      },
      "Point02":{
         "icon":(360,
         187),
         "count":(361,
         239)
      },
      "Point03":{
         "icon":(259,
         236),
         "count":(261,
         288)
      },
      "Point04":{
         "icon":(259,
         135),
         "count":(261,
         186)
      },
      "Point05":{
         "icon":(259,
         325)
      },
      "Point09":{
         "icon":(266,
         434)
      },
      "Point06":{
         "icon":(155,
         333)
      },
      "Point10":{
         "icon":(88,
         270)
      },
      "Point11":{
         "icon":(16,
         201)
      },
      "Point12":{
         "icon":(90,
         111)
      },
      "Point07":{
         "icon":(366,
         333)
      },
      "Point13":{
         "icon":(443,
         270)
      },
      "Point14":{
         "icon":(515,
         201)
      },
      "Point15":{
         "icon":(442,
         111)
      },
      "Point08":{
         "icon":(259,
         64)
      },
      "Point16":{
         "icon":(266,
         0)
      },
      "Point17":{
         "icon":(150,
         18)
      },
      "Point18":{
         "icon":(382,
         18)
      }
   },
   "Priest":{
      "Point01":{
         "icon":(165,
         226),
         "count":(170,
         280)
      },
      "Point02":{
         "icon":(351,
         226),
         "count":(354,
         280)
      },
      "Point03":{
         "icon":(256,
         244),
         "count":(261,
         297)
      },
      "Point04":{
         "icon":(256,
         149),
         "count":(261,
         206)
      },
      "Point05":{
         "icon":(256,
         337)
      },
      "Point09":{
         "icon":(212,
         434)
      },
      "Point18":{
         "icon":(316,
         434)
      },
      "Point06":{
         "icon":(119,
         368)
      },
      "Point10":{
         "icon":(62,
         297)
      },
      "Point11":{
         "icon":(22,
         233)
      },
      "Point12":{
         "icon":(97,
         165)
      },
      "Point07":{
         "icon":(401,
         368)
      },
      "Point13":{
         "icon":(466,
         298)
      },
      "Point14":{
         "icon":(509,
         233)
      },
      "Point15":{
         "icon":(432,
         165)
      },
      "Point08":{
         "icon":(257,
         8)
      },
      "Point16":{
         "icon":(152,
         36)
      },
      "Point17":{
         "icon":(380,
         36)
      }
   },
   "Mage":{
      "Point01":{
         "icon":(167,
         251),
         "count":(170,
         309)
      },
      "Point02":{
         "icon":(352,
         251),
         "count":(354,
         309)
      },
      "Point03":{
         "icon":(259,
         251),
         "count":(261,
         309)
      },
      "Point04":{
         "icon":(259,
         143),
         "count":(261,
         197)
      },
      "Point05":{
         "icon":(259,
         407)
      },
      "Point09":{
         "icon":(175,
         405)
      },
      "Point18":{
         "icon":(358,
         405)
      },
      "Point06":{
         "icon":(91,
         251)
      },
      "Point10":{
         "icon":(26,
         258)
      },
      "Point11":{
         "icon":(44,
         339)
      },
      "Point12":{
         "icon":(44,
         177)
      },
      "Point07":{
         "icon":(431,
         251)
      },
      "Point13":{
         "icon":(506,
         258)
      },
      "Point14":{
         "icon":(487,
         339)
      },
      "Point15":{
         "icon":(487,
         177)
      },
      "Point08":{
         "icon":(260,
         18)
      },
      "Point16":{
         "icon":(151,
         44)
      },
      "Point17":{
         "icon":(382,
         44)
      }
   },
   "Knight":{
      "Point01":{
         "icon":(162,
         236),
         "count":(165,
         292)
      },
      "Point02":{
         "icon":(357,
         238),
         "count":(359,
         292)
      },
      "Point03":{
         "icon":(259,
         223),
         "count":(262,
         278)
      },
      "Point04":{
         "icon":(259,
         132),
         "count":(262,
         186)
      },
      "Point05":{
         "icon":(259,
         332)
      },
      "Point09":{
         "icon":(267,
         415)
      },
      "Point06":{
         "icon":(152,
         412)
      },
      "Point10":{
         "icon":(67,
         314)
      },
      "Point11":{
         "icon":(0,
         232)
      },
      "Point12":{
         "icon":(85,
         155)
      },
      "Point07":{
         "icon":(370,
         412)
      },
      "Point13":{
         "icon":(464,
         314)
      },
      "Point14":{
         "icon":(531,
         232)
      },
      "Point15":{
         "icon":(445,
         157)
      },
      "Point08":{
         "icon":(259,
         61)
      },
      "Point16":{
         "icon":(266,
         0)
      },
      "Point17":{
         "icon":(148,
         18)
      },
      "Point18":{
         "icon":(383,
         17)
      }
   },
   "Shaman":{
      "Point01":{
         "icon":(179,
         196),
         "count":(183,
         249)
      },
      "Point02":{
         "icon":(369,
         196),
         "count":(373,
         249)
      },
      "Point03":{
         "icon":(275,
         179),
         "count":(279,
         232)
      },
      "Point04":{
         "icon":(275,
         268),
         "count":(279,
         321)
      },
      "Point05":{
         "icon":(275,
         357)
      },
      "Point09":{
         "icon":(282,
         434)
      },
      "Point12":{
         "icon":(177,
         415)
      },
      "Point15":{
         "icon":(386,
         415)
      },
      "Point06":{
         "icon":(56,
         242)
      },
      "Point10":{
         "icon":(13,
         182)
      },
      "Point11":{
         "icon":(94,
         135)
      },
      "Point07":{
         "icon":(496,
         242)
      },
      "Point13":{
         "icon":(460,
         330)
      },
      "Point14":{
         "icon":(381,
         302)
      },
      "Point08":{
         "icon":(275,
         76)
      },
      "Point16":{
         "icon":(282,
         0)
      },
      "Point17":{
         "icon":(170,
         20)
      },
      "Point18":{
         "icon":(393,
         20)
      }
   }
}



map_icon = {
    "Warlock": {
        "Point01": {"icon": (157,186), "count": (160,236)},
        "Point02": {"icon": (367,186), "count": (370,236)},
        "Point03": {"icon": (262,174), "count": (265,228)},
        "Point04": {"icon": (262,91), "count": (265,142)},
        "Point05": {"icon": (262,278), "dop_point": {"01": (270,357),"10": (270,435)}},
        "Point06": {"icon": (75,152), "dop_point": {"02": (5,244),"03": (70,327),"04": (137,406)}},
        "Point07": {"icon": (453,152), "dop_point": {"05": (527,244),"06": (467,327),"07": (401,406)}},
        "Point08": {"icon": (262,8), "dop_point": {"08": (153,32),"09": (385,32)}},
    },
    "Warrior": {
        "Point01": {"icon": (147,214), "count": (150,265)},
        "Point02": {"icon": (373,214), "count": (375,265)},
        "Point03": {"icon": (259,229), "count": (262,282)},
        "Point04": {"icon": (259,137), "count": (262,189)},
        "Point05": {"icon": (259,334), "dop_point": {"01": (266,431)}},
        
        "Point06":{"icon": (141,347), "dop_point": {"02": (69,301), "03": (0,235), "04": (62,142)}, "closed": (145,325)}, 
        "Point07": {"icon": (381,347), "dop_point": {"05": (463,301), "06": (531,235), "07": (467,142)}, "closed": (357,325)},
        "Point08":{"icon": (260,63), "dop_point": {"08": (266,1), "09": (148,20), "10": (383,20)}, "closed": (251,53)}
    },

    "Rogue": {
        "Point01": {"icon": (158,187), "count": (160,239)},
        "Point02": {"icon": (360,187), "count": (361,239)},
        "Point03": {"icon": (259,236), "count": (261,288)},
        "Point04": {"icon": (259,135), "count": (261,186)},
        "Point05": {"icon": (259,325), "dop_point": {"01": (266,434)}},
        
        "Point06":{"icon": (155,333), "dop_point": {"02": (88,270), "03": (16,201), "04": (90,111)}}, 
        "Point07": {"icon": (366,333), "dop_point": {"05": (443,270), "06": (515,201), "07": (442,111)}},
        "Point08":{"icon": (259,64), "dop_point": {"08": (266,0), "09": (150,18), "10": (382,18)}}
    },
    "Priest": {
        "Point01": {"icon": (165,226), "count": (170,280)},
        "Point02": {"icon": (351,226), "count": (354,280)},
        "Point03": {"icon": (256,244), "count": (261,297)},
        "Point04": {"icon": (256,149), "count": (261,206)},

        "Point05": {"icon": (256,337), "dop_point": {"01": (212,434),"10": (316,434 )}},
        "Point06": {"icon": (119,368), "dop_point": {"02": (62,297),"03": (22,233),"04": (97,165)}},
        "Point07": {"icon": (401,368), "dop_point": {"05": (466,298),"06": (509,233),"07": (432,165)}},
        "Point08": {"icon": (257,8), "dop_point": {"08": (152,36),"09": (380,36)}},
    },
    "Mage": {
        "Point01": {"icon": (167,251), "count": (170,309)},
        "Point02": {"icon": (352,251), "count": (354,309)},
        "Point03": {"icon": (259,251), "count": (261,309)},
        "Point04": {"icon": (259,143), "count": (261,197)},
        "Point05": {"icon": (259,407), "dop_point": {"01": (175,405),"10": (358,405 )}},

        "Point06": {"icon": (91,251), "dop_point": {"02": (26,258),"03": (44,339),"04": (44,177)}},
        "Point07": {"icon": (431,251), "dop_point": {"05": (506,258),"06": (487,339),"07": (487,177)}},
        "Point08": {"icon": (260,18), "dop_point": {"08": (151,44),"09": (382,44)}},
    },
    "Knight": {
        "Point01": {"icon": (162,236), "count": (165,292)},
        "Point02": {"icon": (357,238), "count": (359,292)},
        "Point03": {"icon": (259,223), "count": (262,278)},
        "Point04": {"icon": (259,132), "count": (262,186)},
        "Point05": {"icon": (259,332), "dop_point": {"01": (267,415)}},        
        "Point06":{"icon": (152,412), "dop_point": {"02": (67,314), "03": (0,232), "04": (85,155)}}, 
        "Point07": {"icon": (370,412), "dop_point": {"05": (464,314), "06": (531,232), "07": (445,157)}},
        "Point08":{"icon": (259,61), "dop_point": {"08": (266,0), "09": (148,18), "10": (383,17)}}
    },
    "Shaman": {
        "Point01": {"icon": (179,196), "count": (183,249)},
        "Point02": {"icon": (369,196), "count": (373,249)},
        "Point03": {"icon": (275,179), "count": (279,232)},
        "Point04": {"icon": (275,268), "count": (279,321)},
        "Point05": {"icon": (275,357), "dop_point": {"01": (282,434),"04": (177,415),"07": (386,415)}},

        "Point06": {"icon": (56,242), "dop_point": {"02": (13,182),"03": (94,135)}},
        "Point07": {"icon": (496,242), "dop_point": {"05": (460,330),"06": (381,302)}},
        "Point08": {"icon": (275,76), "dop_point": {"08": (282,0),"09": (170,20),"10": (393,20)}},
    },
}


map = {
    "Rogue":{
        "Point05": ["01"],
        "Point06":["02","03","04"],
        "Point07": ["05","06","07"],
        "Point08":["08","09","10"]
    },

    "Knight": {
        "Point05": ["01"],
        "Point06":["02","03","04"],
        "Point07": ["05","06","07"],
        "Point08":["08","09","10"]
    },

    "Warrior": {
        "Point05": ["01"],
        "Point06":["02","03","04"],
        "Point07": ["05","06","07"],
        "Point08":["08","09","10"]
    },

    "Priest": {
        "Point05": ["01","10"],
        "Point06":["02","03","04"],
        "Point07": ["05","06","07"],
        "Point08":["08","09"]
    },

    "Warlock": {
        "Point05": ["01","10"],
        "Point06":["02","03","04"],
        "Point07": ["05","06","07"],
        "Point08":["08","09"]
    },

    "Mage": {
        "Point05": ["01","10"],
        "Point06":["02","03","04"],
        "Point07": ["05","06","07"],
        "Point08":["08","09"]
    },

    "Shaman":{
        "Point05": ["01","04","07"],
        "Point06":["02","03"],
        "Point07": ["05","06"],
        "Point08":["08","09","10"]
    }
}

data = None


async def get_data(skill_id):
    global data
    if data is None:
        data = await fetch_data()
    
    return data.get(str(skill_id))

async def get_tree(path,skill_id):
    global data
    if data is None:
        data = await fetch_data()
    
    Point = data.get(str(skill_id))
    maps = map.get(path)
    if Point is None:
        return None
    else:
        if Point["pos"] in maps:
            return [f"{str(skill_id)[:4]}2{v}" for v in maps[Point["pos"]]] 
        else:
            return None
async def get_tree_icon(path,skill_id):
    global data
    if data is None:
        data = await fetch_data()
    
    Point = data.get(str(skill_id))
    maps = map.get(path)

    if Point["pos"] in maps:
        return [f"{str(skill_id)[:4]}2{v}" for v in maps[Point["pos"]]], map_icon.get(path)
    else:
        return None
