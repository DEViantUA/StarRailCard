# Copyright 2023 DEViantUa <t.me/deviant_ua>
# All rights reserved.

from .src.tools import translation, pill, modal, openFile
from .src.generators import one, two
from honkairail import starrailapi
import asyncio,re,os,datetime

def process_input(characterImgs, characterName):
    if characterImgs:
        if isinstance(characterImgs, dict):
            characterImgs = {key.lower(): value for key, value in characterImgs.items()}
        else:
            raise TypeError("The charterImg parameter must be a dictionary, where the key is the name of the character, and the parameter is an image.\nExample: charterImg = {'Himeko': 'img.png'} or {'Himeko': 'img.png', 'Seele': 'img2.jpg', ...}")

    if characterName:
        if isinstance(characterName, str):
            characterName = [name.strip().lower() for name in characterName.split(",")]
        else:
            raise TypeError("The name parameter must be a string, to pass multiple names, list them separated by commas.\nExample: name = 'Himeko' or name = 'Himeko, Seele',..")
    
    return characterImgs, characterName


def remove_html_tags(text):
    clean_text = re.sub('<.*?>', '', text)
    return clean_text


async def saveBanner(uid, res, name):
    data = datetime.datetime.now().strftime("%d_%m_%Y %H_%M")
    path = os.path.join(os.getcwd(), "RailCard", str(uid))
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, f"{name}_{data}.png")
    res.save(file_path)

class MiHoMoCard():
    def __init__(self,lang = "ru", characterImgs = None, characterName = None, hide = False, save = False, background = True, template = 1):

        """
        :param lang: str, What language to receive information supported:  en, ru, vi, th, pt, kr, jp, zh, id, fr, es, de, chs, cht.
        :param characterImgs: dict, Dictionary: {"Name_charter_1": "image link","Name_charter_2": "image link",...}.
        :param characterName: str, If we want to get certain characters: "Name_charter_1,Name_charter_1,Name_charter_1" Character names must be in the same language as in the lang parameter.
        :param hide: bool, Display UID.
        :param save: bool, Save images or not.
        :param background: bool, Generate image with or without background.

        """        
        
        self.template = template

        if not int(template) in [1,2]:
            self.template = 1

        if not lang in translation.supportLang:
            self.lang = "en"
        else:
            self.lang = lang
        
        self.translateLang = translation.Translator(lang)
        self.background = background
        
        try:
            self.characterImgs, self.characterName = process_input(characterImgs, characterName)
        except Exception as e:
            print(e.message)
            return

        self.API = starrailapi.StarRailApi(lang, v = 2)
        self.save = save
        self.hide = hide
        self.img = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
    
    async def characterImg(self,name,ids):
        if name in self.characterImgs:
            self.img = await pill.get_user_image(self.characterImgs[name])
        else:
            self.img = None
        
        if ids in self.characterImgs:
            self.img = await pill.get_user_image(self.characterImgs[ids])

    async def creat(self, uid):
        await openFile.change_font(self.lang)
        task = []
        data = await self.API.get_full_data(uid)
        user = {
            "settings": {
                "uid": int(uid),
                "lang": self.lang,
                "hide": self.hide,
                "save": self.save,
                "background": self.background
            },
            "player": data.player,
            "card": [],
            "name": "",
            "id": "",
        }

        
        for key in data.characters:
            
            user["name"] += f"{key.name}, "
            user["id"] += f"{key.id}, "
            
            if self.characterName:
                if not key.name.lower() in self.characterName and not str(key.id) in self.characterName:
                    continue       

            if self.characterImgs:
                await self.characterImg(key.name.lower(), str(key.id))
            if self.template == 1:
                task.append(one.Creat(key, self.translateLang,self.img,self.hide,int(uid),remove_html_tags(data.player.nickname),self.background).start())
            else:
                task.append(two.Creat(key, self.translateLang,self.img,self.hide,int(uid)).start())

        user["card"] = await asyncio.gather(*task)

        if self.save:
            for keys in user["card"]:
                await saveBanner(uid,keys["card"], keys["name"])

        return modal.HSRCard(**user)

        