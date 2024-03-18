<p align="center">
 <img src="https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/Examples/image/starRailCardBanner.png" alt="Баннер"/>
</p>

____

## StarRailCard
Welcome to the world of StarRailCard – your magical guide to the universe of Honkai Star Rail! This Python module provides the ability to create captivating character cards based on player data from Honkai Star Rail, obtained through their unique user identifiers (UIDs). StarRailCard streamlines the process of generating personalized character assembly cards, relying on the information provided by players.

1. **Easy Installation:** Set up StarRailCard in just a few simple steps to start using it without any hassle.
2. **Support for Other Programming Languages:** StarRailCard provides support for multiple programming languages, making it accessible to a wide range of developers.
3. **Color Adaptation:** StarRailCard seamlessly adapts its color scheme to match the user's custom images, ensuring a harmonious blend between character cards and background images.
4. **Flexible Configuration:** Customize StarRailCard according to your preferences with flexible configuration options, allowing you to tailor the generation process to your liking.
5. **Multi-Language Support:** With support for all languages available in the game, including Ukrainian, StarRailCard can generate character cards in any language.
6. **Personalized Character Cards:** Create character assembly cards based on specific player data to highlight their uniqueness and individuality.
7. **Animation Support:** StarRailCard supports animated elements, adding extra vitality and dynamism to character cards.
8. **Custom Fonts and Images:** Use custom fonts and character images to create character cards with a unique style.
9. **Instant Data Update and Retrieval:** Get updated character and player profile data instantly, ensuring the information on cards is always up-to-date.
10. **Integration with MiHoMo API Wrapper:** Seamlessly integrate StarRailCard with the MiHoMo API wrapper for quick access to game and character data.



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
