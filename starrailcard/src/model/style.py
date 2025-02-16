class Card:
    #TOTAL SETTING
    RGBA = "RGBA"
    font_size = None
    font_color = None
    
    #BACKGROUND SETTING
    font = 25
    background_size = (1083, 1280)
    art_size = (900, 900)
    splash_size = (997, 997)
    blur_art = None
    blur_splashart = None
    opacity_art = None
    opacity_splash = None
    position_line = None
    position_art = (92, -77)
    position_splash_art = (25, -120)
    position_shadow = (0, 0)
    
    #LIGHT_CONE SETTING
    lc_background_size = (337, 448)
    lc_image_size = (298, 410)
    lc_image_position = (19, 23)
    lc_frame_position = (32, 29)
    
    #UID SETTING
    font_uid = 15
    position_uid = (24, 110)
    
    #NAME SETTING
    font_name_size = 25
    name_with = 262
    name_color = (255, 255, 255, 255)
    name_h_max = 53
    name_h_min = 35
    name_position = 4
    name_size = (288, 103)
    font_name_level = 17
    color_name_level = (255, 255, 255, 255)
    position_name_level = (4, 60)
    position_name_star = (2, 85)
    
    #CONSTANT SETTING
    constant_size_background = (46, 276)
    constant_size = None
    constant_size_icon = (46, 46)
    constant_size_icon_opacity = 0.2
    constant_blur = None
    constant_icon_position = None
    
    #RELICT SETTING
    relict_size = (273, 134)
    relict_icon_size = (113, 113)
    relict_icon_position = (-6, 21)
    relict_main_stat_icon_size = (48, 48)
    relict_main_stat_icon_position = (90, 41)
    relict_position_star = (51, 27)
    relict_sub_icon_size = (29, 29)
    
    #RELICT_SETS SETTING
    sets_background = (559, 56)
    sets_line_size = (559, 28)
    sets_name_color = (255, 200, 91, 255)
    sets_count_position = (8, 4)
    sets_font = 18
    
    #STATS SETTING
    stat_font_dop = 18
    stat_font = 20
    stat_value_font = 30
    stat_line_size = (502, 52)
    stat_name_size = 20
    stat_max_width = 275
    
    stat_y_no_dop = 15
    stat_y_yes_dop = 3
    stat_y_dop = 32
    
    stat_icon_size = (52, 52)
    stat_icon_position = (0, 0)
    stat_name_position = (59, 35)
    stat_x_position = 500
    stat_line_add = True
    stat_additional_variable = None

    #BUILD
    build_lc_position = (12,366)
    build_lc_size = (383,219)
    
    build_stats_position = (12,604)
    build_stats_size = None
    
    build_relict_position = (542,685)
    build_relict_size = None
    
    build_skill_position = (733,309)
    build_skill_size = None
    
    build_constant_position = (1028,96)
    build_constant_size = None
    
    build_name_position = (24,4)
    build_name_size = None
    
    build_UID_position = None
    build_UID_size = None
    
    build_seelelen_position = (1120,35)
    build_seelelen_size = None
    
class RelictScore:
    #TOTAL SETTING
    RGBA = "RGBA"
    font_size = None
    font_color = None
    
    #BACKGROUND SETTING
    font = 25
    background_size = (1920, 782)
    art_size = (782, 782)
    splash_size = (850, 782)
    blur_art = 30
    blur_splashart = 25
    opacity_art = 0.5
    opacity_splash = 0.7
    position_line = (693, -7)
    
    #UID SETTING
    font_uid = 10
    position_uid = (7, 768)
    
    #NAME SETTING
    font_name_size = 25
    name_with = 262
    name_color = (255, 255, 255, 255)
    name_h_max = 53
    name_h_min = 35
    name_position = 4
    name_size = (288, 103)
    font_name_level = 17
    color_name_level = (255, 255, 255, 255)
    position_name_level = (4, 60)
    position_name_star = (2, 85)
    
    #CONSTANT SETTING
    constant_size_background = (403, 63)
    constant_size = (163, 164)
    constant_size_icon = (53, 53)
    constant_size_icon_opacity = 0.2
    constant_blur = 3
    constant_icon_position = (5, 5)
    constant_additional_variable = None
    
    #RELICT SETTING
    relict_size = (273, 134)
    relict_icon_size = (113, 113)
    relict_icon_position = (-6, 21)
    relict_main_stat_icon_size = (48, 48)
    relict_main_stat_icon_position = (90, 41)
    relict_position_star = (51, 27)
    relict_sub_icon_size = (29, 29)
    
    #RELICT_SETS SETTING
    sets_background = (530, 88)
    sets_line_size = (530, 28)
    sets_name_color = (255, 200, 91, 255)
    sets_count_position = (8, 4)
    sets_font = 18
    
    #STATS SETTING
    stat_font_dop = 12
    stat_font = 20
    stat_value_font = 20
    stat_line_size = (273, 58)
    stat_name_size = 15
    stat_max_width = 140
    stat_icon_size = (45, 45)
    stat_icon_position = (0, 6)
    stat_name_position = (46, 29)
    stat_x_position = 271
    stat_line_add = False
    stat_additional_variable = None

    #BUILD
    build_lc_position = (782,16)
    build_lc_size = None
    
    build_stats_position = (781,220)
    build_stats_size = None
    
    build_relict_position = (781,473)
    build_relict_size = None
    
    build_skill_position = (1409,16)
    build_skill_size = (488,428)
    
    build_constant_position = (1033,134)
    build_constant_size = (320,47)
    
    build_name_position = (6,654)
    build_name_size = None
    
    build_UID_position = None
    build_UID_size = None
    
    build_seelelen_position = (1120,35)
    build_seelelen_size = None

    build_score_position = None
    build_score_size = None
    
class Ticket:
    #TOTAL SETTING
    RGBA = "RGBA"
    font_size = None
    font_color = None
    
    #LIGHT_CONE SETTING
    lc_background_size = (337, 448)
    lc_image_size = (298, 410)
    lc_image_position = (19, 23)
    lc_frame_position = (32, 29)
    
    #BACKGROUND SETTING
    font = 25
    background_default_color = (30, 30, 30, 255)
    background_size = (1924, 802)
    background_splash_size = (1341, 802)
    art_size = (693, 802)
    splash_size = (582, 802)
    blur_art = None
    blur_splashart = None
    opacity_art = None
    opacity_splash = None
    position_shadow = (1341, 0)
    position_line = (0, 0)
    position_art = (1341, 0)
    position_splash_art = (1342, 0)
    
    #UID SETTING
    font_uid = 10
    position_uid = (1443, 779)
    
    #NAME SETTING
    font_name_size = 25
    name_with = 262
    name_color = (255, 255, 255, 255)
    name_h_max = 53
    name_h_min = 35
    name_position = 4
    name_size = (288, 103)
    font_name_level = 17
    color_name_level = (255, 255, 255, 255)
    position_name_level = (4, 60)
    position_name_star = (2, 85)
    
    #CONSTANT SETTING
    constant_size_background = (403, 63)
    constant_size = (163, 164)
    constant_size_icon = (53, 53)
    constant_size_icon_opacity = 0.2
    constant_blur = 3
    constant_icon_position = (5, 5)
    
    #RELICT SETTING
    relict_size = (273, 134)
    relict_icon_size = (113, 113)
    relict_icon_position = (-6, 21)
    relict_main_stat_icon_size = (38, 38)
    relict_main_stat_icon_position = (77, 0)
    relict_position_star = (0, 20)
    relict_sub_icon_size = (38, 38)
    relict_additional_variable = None
    
    #RELICT_SETS SETTING
    sets_background = (807, 545)
    sets_line_size = (394, 38)
    sets_name_color = (255, 185, 85, 255)
    sets_count_position = (7, 2)
    sets_font = 15
    
    #STATS SETTING
    stat_font_dop = 18
    stat_font = 20
    stat_value_font = 30
    stat_line_size = (434, 52)
    stat_name_size = 20
    stat_max_width = 275
    
    stat_y_no_dop = 15
    stat_y_yes_dop = 3
    stat_y_dop = 32
    
    stat_icon_size = (52, 52)
    stat_icon_position = (0, 0)
    stat_name_position = (59, 27)
    stat_x_position = 432
    stat_line_add = False
    stat_additional_variable = None

    #BUILD
    build_lc_position = (29,35)
    build_lc_size = (302,182)
    
    build_stats_position = (884,56)
    build_stats_size = None
    
    build_relict_position = (29,310)
    build_relict_size = None
    
    build_sets_position = (29,222)
    build_relict_size = None
    
    build_skill_position_total = None
    build_skill_position_main = (500,68)
    build_skill_position_main_add = (410,68)
    build_skill_position_dop = (446,165)
    build_skill_size = (488,428) #
    
    build_constant_position = (455,327)
    build_constant_size = None
    
    build_name_position = (1350,691)
    build_name_size = None
    
    build_UID_position = None
    build_UID_size = None
    
    build_seelelen_position = (1688,718)
    build_seelelen_size = None
    
    build_score_position = (442,436)
    build_score_size = None