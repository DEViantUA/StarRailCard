# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from PIL import Image,ImageDraw
from .. import git, options, treePaths
from .text_control import get_font, create_image_with_text
from .image_control import get_download_img
from .color_control import  recolor_image, apply_opacity



async def create_stats(combined_attributes, dop, 
                      font_dop,font,
                      line_size, name_size, max_width, icon_size,
                      icon_position, name_position, x_position,
                      color_font, stat_value_font,
                      stat_y_no_dop = 13, stat_y_yes_dop = 6, stat_y_dop = 25, line = False):
    
    font = await get_font(font)
    font_dop = await get_font(font_dop)
    stat_value_font = await get_font(stat_value_font)
    
    for i, attribute in enumerate(combined_attributes):
        stat = combined_attributes[attribute]
        icon = await get_download_img(stat.icon, size= icon_size)
        if attribute in ["physical_dmg","fire_dmg","ice_dmg","lightning_dmg","wind_dmg","quantum_dmg", "imaginary_dmg"]:
            icon = await recolor_image(icon.copy(), options.color_element_stat.get(attribute, (255,255,255,255))[:3])
        background = Image.new("RGBA", line_size, (0, 0, 0, 0))
        d = ImageDraw.Draw(background)
        value = "{:.1f}%".format(stat.value * 100) if stat.percent else round(stat.value)
        name_text = await create_image_with_text(stat.name, name_size, max_width=max_width, color=(255, 255, 255, 255)) #max_height=45,
        background.alpha_composite(name_text, (name_position[0],(int(name_position[1]-name_text.size[1]/2))))
        background.alpha_composite(icon,icon_position)        
        if attribute in dop: 
            x = x_position - int(stat_value_font.getlength(str(value)))
            d.text((x, stat_y_yes_dop), str(value), font=stat_value_font, fill=(255, 255, 255, 255))

            x = x_position - int(font_dop.getlength(dop[attribute]["dop"]))
            d.text((x, stat_y_dop), dop[attribute]["dop"], font=font_dop, fill= color_font)

            x = x - int(font_dop.getlength(dop[attribute]["main"])) - 5
            d.text((x, stat_y_dop), dop[attribute]["main"], font=font_dop, fill=(255, 255, 255, 255))
        else:
            x = x_position - int(stat_value_font.getlength(str(value)))
            d.text((x, stat_y_no_dop), str(value), font=stat_value_font, fill=(255, 255, 255, 255))

        if line:
            x = line_size[0] - (int(stat_value_font.getlength(str(value))) + name_position[0] + name_text.size[0] + 10 * 3)   
            line_stat = Image.new("RGBA", (x,2), (255,255,255,50))
            background.alpha_composite(line_stat,(name_text.size[0]+icon_size[0] + 15, int(line_size[1]/2)))
            
            
        yield i, background
        

async def create_path(character):
    background_path = await options.get_background_path(character.path.id)
    path = treePaths.map_new.get(character.path.id)
    font_15 = await get_font(15) 
    if character.path.id == "Memory":
        closed = await git.ImageCache().path_closed_mage
    else:
        closed = await git.ImageCache().path_closed_main

    for key in character.skill_trees:
        if key.anchor in ['Point01','Point02','Point03','Point04','Point05','Point19','Point20']:
            icon = await get_download_img(key.icon, size=(47,47))
            icon = await recolor_image(icon, (255,212,173))
            count = await git.ImageCache().path_count
            count = count.copy()
            d = ImageDraw.Draw(count)
            if key.anchor == 'Point01':
                if key.max_level > 6:
                    key.level += 1
            else:
                if key.max_level > 10:
                    key.level += 2
                
            x = 29 - int(font_15.getlength(f"{key.level}/{key.max_level}")/2)
            d.text((x, 1), f"{key.level}/{key.max_level}", font=font_15, fill = (255,255,255,255))
            background_path.alpha_composite(icon, path[key.anchor]["icon"])
            background_path.alpha_composite(count, path[key.anchor]["count"])
        elif key.anchor in ['Point06','Point07','Point08']:
            icon = await get_download_img(key.icon, size=(47,47))
            icon = await recolor_image(icon, (0,0,0))
            if key.level == key.max_level:
                background_path.alpha_composite(icon, path[key.anchor]["icon"])
            else:
                icon = await apply_opacity(icon, opacity=0.5)
                
                background_path.alpha_composite(icon, path[key.anchor]["icon"])
                background_path.alpha_composite(closed, path[key.anchor]["closed"])
        else:
            icon = await get_download_img(key.icon, size=(35,35))
            icon = await recolor_image(icon, (0,0,0))
            if key.level == key.max_level:
                background_path.alpha_composite(icon, path[key.anchor]["icon"])
            else:
                icon = await apply_opacity(icon, opacity=0.5)
                closed = await git.ImageCache().path_closed_dop
                background_path.alpha_composite(icon, path[key.anchor]["icon"])
                background_path.alpha_composite(closed, path[key.anchor]["icon"])
                
    return background_path


_of = git.ImageCache()
_of.set_mapping(2)

async def get_resource_light_cones(x):
    if x == 3:
        return await _of.shadow_3_light_cone, await _of.star_3_frame_light_cone, (150, 202, 255, 255)
    elif x == 4:
        return await _of.shadow_4_light_cone, await _of.star_4_frame_light_cone, (217, 150, 255, 255)
    else:
        return await _of.shadow_5_light_cone, await _of.star_5_frame_light_cone, (255, 199, 150, 255)
    
    
