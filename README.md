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
    async with honkaicard.MiHoMoCard(template=1) as hmhm:
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



<details>
<summary>Sample 1 template</summary>
 
[![Adaptation][3]][3]
 
[3]: https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/a-18.png
  
</details>


<details>
<summary>Sample 2 template</summary>
 
[![Adaptation][4]][4]
 
[4]: https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/a-19.png
 
</details>
