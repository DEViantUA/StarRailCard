# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import anyio
from typing import Union
#import asyncio

from .src.tools import cache, http, ukrainization, options, translator, git
from .src.generator import style_relict_score, style_ticket, style_profile_phone, style_card
from .src.api import api, enka
from .src.model import StarRailCard,api_mihomo
from .src.tools.pill import image_control



class Card:
    def __init__(self, lang: str = "en", character_art = None, character_id = None, seeleland: bool = False,
                 user_font = None, save: bool = False, asset_save: bool = False, boost_speed: bool = False, remove_logo: bool = False,
                 cache = {"maxsize": 150, "ttl": 300}, enka: bool = False, api_data: api_mihomo.MiHoMoApi = None, proxy: str =  None, 
                 user_agent: str = None):
        """Main class for generating cards

        Args:
            lang (str, optional): Language in which generation will take place, supported languages: cht, cn, de, en, es, fr, id, jp, kr, pt, ru, th, vi, ua . Defaults to "en".
            character_art (dict, optional): A dictionary that contains a key - character id and link value (If you want to pass several images for 1 character, you can use list in the values). Defaults to None.
            character_id (str, optional): List character ids separated by commas. Defaults to None.
            seeleland (bool, optional): Enable Seeleland statistics. Defaults to False.
            user_font (srt, optional): Font path or font name. Defaults to None.
            save (bool, optional): Whether to save images or not (Does not work for animated cards). Defaults to False.
            asset_save (bool, optional): Save assets to the device so that in subsequent calls you do not have to download them, but open them from the device. Defaults to False.
            boost_speed (bool, optional): Allows you to download generation resources to your device for further use without downloading. !!!Fills up the device memory!!!.
            remove_logo (bool, optional): Remove GItHub logo. Defaults to False.
            cashe (dict, optional): Set your cache settings. Defaults to {"maxsize": 150, "ttl": 300}.
            api_data (MiHoMoApi, optional): Pass your data received via: api.ApiMiHoMo(uid,"en").get()
            proxy (str, optional): Proxy as a string: http://111.111.111.111:8888
            user_agent (str, optional): Custom User-Agent.
        """
        self.lang = lang
        self.character_art  = character_art
        self.character_id  = character_id
        self.seeleland = seeleland
        self.user_font = user_font
        self.save = save
        self.asset_save = asset_save
        self.remove_logo = remove_logo
        self.cache = cache
        self.enka = enka
        self.boost_speed = boost_speed
        self.api_data = api_data
        self.proxy = proxy
        self.user_agent = options.get_user_agent(user_agent)

        
    async def __aenter__(self):
        cache.Cache.get_cache(maxsize = self.cache.get("maxsize", 150), ttl = self.cache.get("ttl", 300))
        await http.AioSession.enter(self.proxy)
        
        await git.ImageCache.set_assets_download(self.asset_save)
        
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
        
        image_control._boost_speed = self.boost_speed

        
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
        await http.AioSession.exit(exc_type, exc, tb)
        
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
                
    async def set_user_font(self, user_font: str):
        """Will install a custom font

        Args:
            user_font (srt): Font path or font name.
        """
        await git.change_font(font_path = user_font)

    async def create_profile(self, uid: Union[int,str], style: bool = 1, hide_uid: bool = False, background = None, force_update: bool = False):
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
        if self.api_data is None:
            if self.enka:
                try:
                    data = await enka.ApiEnkaNetwork(uid, lang= self.lang).get()
                except Exception as e:
                    print("To use the EnkaNetwork API you need to download/update the asset\nExample: await enka.ApiEnkaNetwork().update_assets()")
                    data = await api.ApiMiHoMo(uid, lang= self.lang, force_update = force_update, user_agent= self.user_agent).get()
            else:
                data = await api.ApiMiHoMo(uid, lang= self.lang, force_update = force_update, user_agent= self.user_agent).get()
        else:
            data = self.api_data
            
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
        
        if not str(style) in ["1"]:
            style = 1
            
        if style == 1:
            response["card"] = await style_profile_phone.Create(data,self.translateLang,self.character_art,hide_uid,uid,background, self.remove_logo).start()

        for key in data.characters:
            response["character_id"].append(key.id)
            response["character_name"].append(key.name)
        
        if self.save:
            await options.save_card(uid,response["card"],"profile")
        
        return StarRailCard.StarRail(**response)
        
    async def create(self, uid: Union[int,str], style: bool = 1, hide_uid: bool = False, force_update: bool = False, style_settings = None, log: bool = False):
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
        
        if self.api_data is None:
            if self.enka:
                try:
                    data = await enka.ApiEnkaNetwork(uid, lang= self.lang).get()
                except Exception as e:
                    print("To use the EnkaNetwork API you need to download/update the asset")
                    data = await api.ApiMiHoMo(uid, lang= self.lang, force_update = force_update, user_agent= self.user_agent).get()
            else:
                data = await api.ApiMiHoMo(uid, lang= self.lang, force_update = force_update, user_agent= self.user_agent).get()
        else:
            data = self.api_data

        result = []
        
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
        
        async with anyio.create_task_group() as tasks:
            
            for key in data.characters:
                async def get_result(key):    
                    try:               
                        response["character_id"].append(key.id)
                        response["character_name"].append(key.name)
                        
                        if self.character_id:
                            if not str(key.id) in self.character_id:
                                return  
                        
                        art = None
                        if self.character_art:
                            if str(key.id) in self.character_art:
                                art = self.character_art[str(key.id)]
                        if style == 1:
                            result.append(await style_relict_score.Create(key,self.translateLang,art,hide_uid,uid, self.seeleland,self.remove_logo).start())
                        elif style == 2:
                            result.append(await style_ticket.Create(key,self.translateLang,art,hide_uid,uid, self.seeleland,self.remove_logo).start())
                        elif style == 3:
                            result.append(await style_card.Create(key,self.translateLang,art,hide_uid,uid, self.seeleland,self.remove_logo).start())
                    except Exception as e:
                        print(f"Error in get_result for character {key.id}: {e}")
                        
                tasks.start_soon(get_result, key)
                    
        response["card"] = result
        
        if self.lang == "ua":
            StarRailCard.UA_LANG = True
        else:
            StarRailCard.UA_LANG = False
        
        if self.save:
            async with anyio.create_task_group() as tasks:
                for key in response["card"]:
                    if key["animation"]:
                        continue
                    tasks.start_soon(options.save_card,uid,key["card"],key["id"])        
                                
        return StarRailCard.StarRail(**response)