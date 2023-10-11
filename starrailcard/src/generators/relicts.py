# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.
import json
from PIL import ImageDraw,Image
from ..tools import pill, openFile, calculator, modal

_of = openFile.ImageCache()



async def get_rarity_sourse(x):
    if x == 1:
        return _of.strs_1, _of.relict_1_stars.copy()
    elif x == 2:
        return _of.strs_2, _of.relict_2_stars.copy()
    elif x == 3:
        return _of.strs_3, _of.relict_3_stars.copy()
    elif x == 4:
        return _of.strs_4, _of.relict_4_stars.copy()
    elif x == 5:
        return _of.strs_5, _of.relict_5_stars.copy()


async def get_quality_color(rank):
    if rank == "SSS":
        return (255, 0, 0, 255)  # Ярко-красный цвет (Bright Red)
    elif rank == "SS":
        return (255, 69, 0, 255)  # Ярко-оранжевый цвет (Bright Orange)
    elif rank == "S":
        return (255, 215, 0, 255)  # Ярко-желтый цвет (Bright Yellow)
    elif rank == "A":
        return (0, 255, 0, 255)  # Ярко-зеленый цвет (Bright Green)
    elif rank == "B":
        return (50, 205, 50, 255)  # Зеленый цвет (Green)
    elif rank == "C":
        return (0, 255, 255, 255)  # Ярко-голубой цвет (Bright Cyan)
    elif rank == "D":
        return (0, 0, 255, 255)  # Ярко-синий цвет (Bright Blue)
    else:
        return (128, 128, 128, 255)  # Серый цвет (Gray)

    

async def get_eff_color(rank):
    if rank == 4:
        return (168, 234, 8, 255)
    elif rank == 3:
        return (234, 179, 8, 255)
    elif rank == 2:
        return (248, 113, 113, 255)
    elif rank == 1:
        return (161, 98, 7, 255) 
    else:
        return (128, 128, 128, 255)

async def creat(relics,character_id, indx, name_charter = None):


    data = {
        "card": None,
        "score": {"score": 0, "rank": 0, "eff": 0, "cv": 0},
        "relict": {},
        "position": 0
    }

    CRIT_DMG = 0
    CRIT_RATE = 0

    name = relics.name
    set_name = relics.set_name

    level = f"+{relics.level}"

    icon = await pill.get_dowload_img(relics.icon, thumbnail_size=(169,169))
    stars, bg = await get_rarity_sourse(relics.rarity)

    main_icon = await pill.get_dowload_img(relics.main_affix.icon, thumbnail_size=(39,39))
    main_stats = relics.main_affix.display

    if  relics.main_affix.field == "crit_dmg":
        CRIT_DMG += relics.main_affix.value
    elif relics.main_affix.field  == "crit_rate":
        CRIT_RATE += relics.main_affix.value

    bg.alpha_composite(icon,(342,0))
    bg.alpha_composite(stars,(365,126))
    bg.alpha_composite(main_icon,(71,121))
    

    names = await pill.create_image_with_text(name, 18, max_width=321, color=(255, 255, 255, 255))
    bg.alpha_composite(names, (16, 7))

    set_names = await pill.create_image_with_text(set_name, 15, max_width=271, color=(69, 255, 231, 255))
    bg.alpha_composite(set_names, (16, names.size[1]+1))
    

    font = await pill.get_font(25)
    d = ImageDraw.Draw(bg)

    x = int(font.getlength(level)/2)
    d.text((38-x, 126), level, font=font, fill=(69, 255, 231, 255))
    d.text((109, 126), str(main_stats), font=font, fill=(255, 255, 255, 255))
    if name_charter is None:
        d.text((15, 295), "No Name", font=font, fill=(255, 255, 255, 255))
    else:
        d.text((15, 295), name_charter, font=font, fill=(255, 255, 255, 255))
    
    position = (
            (6,187),
            (150,187),
            (6,237),
            (150,237)
        )

    for i, k in enumerate(relics.sub_affix):
        icon = await pill.get_dowload_img(k.icon, size=(36, 36))
        bg.alpha_composite(icon,position[i])
        d.text((position[i][0]+40, position[i][1]+2), str(k.display), font=font, fill=(255,255,255, 255))
        if  k.field == "crit_dmg":
            CRIT_DMG += k.value
        elif k.field  == "crit_rate":
            CRIT_RATE += k.value
    

    tcvR = float('{:.2f}'.format(CRIT_DMG* 100 + (CRIT_RATE* 100 *2)))

    x = int(font.getlength(f"{tcvR} CV"))
    d.text((505-x, 297), f"{tcvR} CV", font=font, fill=(255, 255, 255, 255))

    bg_score = _of.relict_stats.copy()

    score, rank, eff = await calculator.get_rating(relics,character_id,str(indx))
    color = await get_quality_color(rank)
    color_eff = await get_eff_color(eff)

    d = ImageDraw.Draw(bg_score)
    font = await pill.get_font(20)
    x = int(font.getlength(rank))
    d.text((200-x, -2), rank, font=font, fill=color)
    x = int(font.getlength(str(eff)))
    d.text((200-x, 29), str(eff), font=font, fill=color_eff)
    x = int(font.getlength(str(float('{:.2f}'.format(score)))))
    d.text((200-x, 60), str(float('{:.2f}'.format(score))), font=font, fill=color)
    
    bg.alpha_composite(bg_score,(305,190))
    
    data["relict"] = json.loads(relics.json())
    data["score"] = {"score": float('{:.2f}'.format(score)), "rank": rank, "eff": eff, "cv": tcvR}
    data["card"] = bg
    data["position"] = int(indx)


    return modal.RelictData(**data)