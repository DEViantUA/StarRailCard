
from enum import StrEnum, IntEnum

LangMap = {
    "zh-CN": "zh-cn",
    "zh-TW": "zh-tw",
    "de": "de-de",
    "en": "en-us",
    "es": "es-es",
    "fr": "fr-fr",
    "id": "id-id",
    "it": "it-it",
    "ja": "ja-jp",
    "ko": "ko-kr",
    "pt": "pt-pt",
    "ru": "ru-ru",
    "th": "th-th",
    "vi": "vi-vn",
    "tr": "tr",
}

class MiHoMoLink(StrEnum):
    PARSED = "https://api.mihomo.me/sr_info_parsed/{uid}"
    NAKED = "https://api.mihomo.me/sr_info/{uid}"
    
class EnkaLink(StrEnum):
    ENKA = "https://enka.network/api/hsr/uid/{uid}"
    HASH = "https://enka.network/api/profile/{name}/hoyos/"
    BUILD = "https://enka.network/api/profile/{name}/hoyos/{hash}/builds/"

class ApiType(IntEnum):
    MiHoMo = 1
    Enka = 2
    HoYoLab = 3

class LangMiHoMo(StrEnum):
    EN = "en"
    EN = "en"
    CHT = "cht"
    CN = "cn"
    DE = "de"
    ES = "es"
    FR = "fr"
    ID = "id"
    JP = "jp"
    KR = "kr"
    PT = "pt"
    RU = "ru"
    TH = "th"
    VI = "vi"
    UA = "ua"