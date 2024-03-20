# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import asyncio

from .src.tools import http, ukrainization, options, translator, cashe, git
from .src.generator import style_relict_score, style_ticket, style_profile_phone
from .src.api import api
from .src.model import StarRailCard


class Card:
    def __init__(self, lang = "en", character_art = None, character_id = None, seeleland = False,
                 user_font = None, save = False, asset_save = False, remove_logo = False,
                 cashe = {"maxsize": 150, "ttl": 300}):
        """Main class for generating cards

        Args:
            lang (str, optional): Language in which generation will take place, supported languages: cht, cn, de, en, es, fr, id, jp, kr, pt, ru, th, vi, ua . Defaults to "en".
            character_art (dict, optional): A dictionary that contains a key - character id and link value (If you want to pass several images for 1 character, you can use list in the values). Defaults to None.
            character_id (str, optional): List character ids separated by commas. Defaults to None.
            seeleland (bool, optional): Enable Seeleland statistics. Defaults to False.
            user_font (srt, optional): Font path or font name. Defaults to None.
            save (bool, optional): Whether to save images or not (Does not work for animated cards). Defaults to False.
            asset_save (bool, optional): Save assets to the device so that in subsequent calls you do not have to download them, but open them from the device. Defaults to False.
            remove_logo (bool, optional): Remove GItHub logo. Defaults to False.
            cashe (dict, optional): Set your cache settings. Defaults to {"maxsize": 150, "ttl": 300}.
        """
        self.session = None
        self.lang = lang
        self.character_art  = character_art
        self.character_id  = character_id
        self.seeleland = seeleland
        self.user_font = user_font
        self.save = save
        self.asset_save = asset_save
        self.remove_logo = remove_logo
        self.cashe = cashe
        
    async def __aenter__(self):
        cashe.Cache.get_cache(maxsize = self.cashe.get("maxsize", 150), ttl = self.cashe.get("ttl", 300))
        self.session = await http.AioSession.creat_session()
        
        await git.ImageCache.set_assets_dowload(self.asset_save)
        
        if self.character_id:
            self.character_id = await options.get_charter_id(self.character_id)
        
        if self.character_art:
            if not isinstance(self.character_art, dict):
                raise TypeError(4,"The character_art parameter must be a dictionary, where the key is the name of the character, and the parameter is an image.\nExample: character_art = {'1235': 'img.png', '1235': ['img.png','http.../img2.png']} or {'123596': 'img.png', '123854': 'http.../img2.png', ...}")
            else:
                self.character_art = await options.get_character_art(self.character_art)
        
        if not self.lang in translator.SUPPORTED_LANGUAGES:
            self.lang = "en"
        
        if self.lang == "ua":
            await ukrainization.TranslateDataManager().check_update()
        
        self.translateLang = translator.Translator(self.lang)

            
        if self.user_font:
            await git.change_font(font_path = self.user_font)
        
        if self.remove_logo:
            print("""
                Thank you for using our StarRailCard!
                By removing the GitHub logo from the generated results, you acknowledge supporting the author through one of the following links:
                - Patreon: https://www.patreon.com/deviantapi/membership
                - Ko-fi: https://ko-fi.com/dezzso

                Failure to contribute to the project may lead to the author discontinuing updates in the future.
                """)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
    
    async def set_lang(self, lang):
        """Sets the language

        Args:
            lang (str): lang (str): Language in which generation will take place, supported languages: cht, cn, de, en, es, fr, id, jp, kr, pt, ru, th, vi, ua . Defaults to "en".
        """
        if not lang in translator.SUPPORTED_LANGUAGES:
            lang = "en"
            self.lang = "en"
        else:
            self.lang = lang
        
        if lang == "ua":
            await ukrainization.TranslateDataManager().check_update()
        
        self.translateLang = translator.Translator(lang)
                
    async def set_user_font(self, user_font):
        """Will install a custom font

        Args:
            user_font (srt): Font path or font name.
        """
        await git.change_font(font_path = user_font)
    
    async def creat_profile(self, uid, style = 1, hide_uid = False, background = None, force_update = False):
        """Function for generating a user profile card

        Args:
            uid (int): UID of the user in the game.
            style (int, optional): Card style. Defaults to 1.
            hide_uid (bool, optional): Hide UID. Defaults to False.
            background (str, optional): Link to custom card background. Defaults to None.
            force_update (bool, optional): Forced update of user data. Defaults to False.

        Returns:
            StarRail: A class object containing profile information and a profile card
        """
        data = await api.ApiMiHoMo(uid, lang= self.lang, force_update = force_update).get()
        
        response = {
            "settings": {
                "uid": int(uid),
                "lang": self.lang,
                "hide_uid": hide_uid,
                "save": self.save,
                "force_update": force_update,
                "style": int(style)
            },
            "player": data.player,
            "card": None,
            "character_name": [],
            "character_id": [],
        }
        
        if not str(style) in ["1"]:
            style = 1
            
        if style == 1:
            response["card"] = await style_profile_phone.Creat(data,self.translateLang,self.character_art,hide_uid,uid,background, self.remove_logo).start()

        for key in data.characters:
            response["character_id"].append(key.id)
            response["character_name"].append(key.name)
        
        await options.save_card(uid,response["card"],"profile")
        
        return StarRailCard.StarRail(**response)
        
    async def creat(self, uid, style = 1, hide_uid = False, force_update = False, style_settings = None):
        """Function for generating character cards

        Args:
            uid (int): UID of the user in the game
            style (int, optional): Card style. Defaults to 1.
            hide_uid (bool, optional): Hide UID. Defaults to False.
            force_update (bool, optional): forced update of user data. Defaults to False.
            style_settings (dict, optional): not implemented yet. Defaults to None.

        Returns:
            StarRail: A class object containing profile information and a character cards
        """
        
        data = await api.ApiMiHoMo(uid, lang= self.lang, force_update = force_update).get()
        task = []
                
        style, style_settings = await options.style_setting(style, style_settings)
        
        try:
            player = data.player.model_dump()
        except:
            player = data.player
        
        response = {
            "settings": {
                "uid": int(uid),
                "lang": self.lang,
                "hide_uid": hide_uid,
                "save": self.save,
                "force_update": force_update,
                "style": int(style)
            },
            "player": player,
            "card": None,
            "character_name": [],
            "character_id": [],
        }
        
        for key in data.characters:
            response["character_id"].append(key.id)
            response["character_name"].append(key.name)
            
            if self.character_id:
                if not str(key.id) in self.character_id:
                    continue  
            
            art = None
            if self.character_art:
                if str(key.id) in self.character_art:
                    art = self.character_art[str(key.id)]
                    
            if style == 1:
                task.append(style_relict_score.Creat(key,self.translateLang,art,hide_uid,uid, self.seeleland,self.remove_logo).start())
            elif style == 2:
                task.append(style_ticket.Creat(key,self.translateLang,art,hide_uid,uid, self.seeleland,self.remove_logo).start())
        
        response["card"] = await asyncio.gather(*task)
        
        if self.lang == "ua":
            StarRailCard.UA_LANG = True
        else:
            StarRailCard.UA_LANG = False
        task_save = []
        if self.save:
            for key in response["card"]:
                if key["animation"]:
                    continue
                task_save.append(options.save_card(uid,key["card"],key["id"]))
        
            await asyncio.gather(*task_save)
        
        return StarRailCard.StarRail(**response)
