# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.


def get_relic_score_color(score):
    if score < 11:
        return (172, 126, 255, 255)
    elif 11 <= score < 17:
        return (172, 126, 255, 255)
    elif 17 <= score < 21:
        return (126, 175, 255, 255)
    elif 21 <= score < 29:
        return (126, 255, 190, 255)
    elif 29 <= score < 35:
        return (187, 255, 126, 255)
    elif 35 <= score < 41:
        return (255, 168, 126, 255)
    elif 41 <= score < 47:
        return (255, 126, 126, 255)
    elif 47 <= score:
        return (255, 126, 126, 255)
    

def get_total_score_color(score):
    if score < 11:
        return (172, 126, 255, 255)
    elif 11 <= score < 17:
        return (172, 126, 255, 255)
    elif 17 <= score < 21:
        return (126, 175, 255, 255)
    elif 21 <= score < 29:
        return (126, 255, 190, 255)
    elif 29 <= score < 35:
        return (187, 255, 126, 255)
    elif 35 <= score < 41:
        return (255, 168, 126, 255)
    elif 41 <= score < 47:
        return (255, 126, 126, 255)
    elif 47 <= score:
        return (255, 126, 126, 255)
    
def get_relic_score_text(score):
    if score < 11:
        return "D"
    elif 11 <= score < 17:
        return "C"
    elif 17 <= score < 21:
        return "B"
    elif 21 <= score < 29:
        return "A"
    elif 29 <= score < 35:
        return "S"
    elif 35 <= score < 41:
        return "SS"
    elif 41 <= score < 47:
        return "SSS"
    elif 47 <= score:
        return "SSS"

def get_relic_full_score_text(score):
    if score < 60:
        return "D"
    elif 60 <= score < 100:
        return "C"
    elif 100 <= score < 140:
        return "B"
    elif 140 <= score < 180:
        return "A"
    elif 180 <= score < 210:
        return "S"
    elif 210 <= score < 250:
        return "SS"
    elif 280 <= score:
        return "SSS"
