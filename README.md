<p align="center">
 <img src="https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/documentation/StarRailCardM.png" alt="Баннер"/>
</p>

____

## StarRailCard
Module for generating Honkai Star Rail character cards

* Ability to generate with or without background.<br>
* Ability to set a custom image.<br>
* Flexible map settings.

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

<details>
<summary>Add image author</summary>

``` python
from starrailcard import honkaicard 
import asyncio

async def mains():
    async with honkaicard.MiHoMoCard(template=1) as hmhm:
        r = await hmhm.creat(700649319)
        for key in r.card:
            cards = await hmhm.add_author(link= "https://www.deviantart.com/dezzso", card= key.card)
            #cards.save(f"{key.id}.png") #A function to save an image with the author's stamp added.
        print(r)

asyncio.run(mains())
```
</details>


<details>
<summary>Create a profile card.</summary>

``` python
from starrailcard import honkaicard 
import asyncio

async def mains():
    async with honkaicard.MiHoMoCard(template=1) as hmhm:
        r = await hmhm.get_profile(700649319,  card = True)
        print(r)

asyncio.run(mains())
```
</details>


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
 
[3]: https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/documentation/a-18.png
  
</details>


<details>
<summary>Sample 2 template</summary>
 
[![Adaptation][4]][4]
 
[4]: https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/documentation/a-19.png
 
</details>


<details>
<summary>Sample 3 template</summary>
 
[![Adaptation][2]][2]
 
[2]: https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/documentation/a-21.png
 
</details>


<details>
<summary>Sample profile template</summary>
 
[![Adaptation][1]][1]
 
[1]: https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/documentation/a-22.png
 
</details>
