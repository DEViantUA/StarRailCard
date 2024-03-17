<p align="center">
 <img src="https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/Examples/image/starRailCardBanner.png" alt="Баннер"/>
</p>

____

## StarRailCard
Module for generating Honkai Star Rail character cards

* Ability to generate with or without background.<br>
* Ability to set a custom image.<br>
* Flexible map settings.

## Api:
> You can use the API to generate cards if you are using a different programming language.
[Documentation](https://github.com/DEViantUA/StarRailCard/wiki/StarRailCard-API)

## Installation:
```
pip install starrailcard
```

## Launch:
``` python
import asyncio
import starrailcard

async def main():
    async with starrailcard.Card() as card:
        data = await card.creat(700649319, style=2)
    print(data)

asyncio.run(main())
```

<details>
<summary>Create a profile card.</summary>

``` python
import asyncio
import starrailcard

async def main():
    async with starrailcard.Card() as card:
        data = await card.creat_profile(700649319)
    print(data)

asyncio.run(main())
```
</details>

# Thank the author for the code: 
* **Patreon**: https://www.patreon.com/deviantapi
* **Ko-Fi**: https://ko-fi.com/dezzso
