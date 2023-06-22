<p align="center">
 <img src="https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/StarRailCardM.png" alt="Баннер"/>
</p>

____

## StarRailCard
Module for generating Honkai Star Rail character cards
:white_medium_square: Ability to generate with or without background.<br>
:white_medium_square: Ability to set a custom image.<br>
:white_medium_square: Flexible map settings.

## Installation:
```
pip install starrailcard
```

## Launch:
``` python
from starrailcard import honkaicard 
import asyncio

async def mains():
    while True:
        async with honkaicard.MiHoMoCard() as hmhm:
            r = await hmhm.creat(700649319)
            print(r)

asyncio.run(mains())
```

## Languages Supported
| Languege    |  Code   | Languege    |  Code   | Languege    |  Code   |
|-------------|---------|-------------|---------|-------------|---------|
|  English    |     en  |  русский    |     ru  |  Chinese    |    chs  |
|  Tiếng Việt |     vi  |  ไทย        |     th  | Taiwan     |    cht  |
|  português  |     pt  | 한국어      |     kr  | deutsch    |     de  |
|  日本語      |     jp  | 中文        |     zh  | español    |     es  |
|  中文        |     zh  | Indonesian |     id  | français   |     fr  |
|  Khaenri'ah  |     kh  | Khaenri'ah |