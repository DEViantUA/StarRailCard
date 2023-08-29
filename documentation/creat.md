### Information about the create method
---

* Generates character cards.
* Returns user information.

### Argument:
* ``uid`` - Custom UID from the game

### Usage example:

```py
from starrailcard import honkaicard 
import asyncio

async def main(uid):
  async with honkaicard.MiHoMoCard() as hmhm
    r = await hmhm.creat(uid)
    print(r)

asyncio.run(main(700649319))
```

### Result:

```py
settings=Settings(uid=700649319, lang='en', hide=False, save=False, background=True)
player=PlayerV2(uid='700649319', nickname='Korzzex', level=66, avatar=Avatar(id='200101', name='March 7th — Welcome', icon='https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/icon/avatar/200101.png'), signature='Описания ещё нет... Скоро...', friend_count=16, world_level=6, birthday=None, space_info=SpaceInfo(pass_area_progress=7, light_cone_count=57, avatar_count=21, achievement_count=265))
card=[Card(id='1209', name='Yanqing', rarity=5, card=<PIL.Image.Image image mode=RGBA size=1924x802 at 0x15816A77AF0>, size=(1924, 802)), Card(id='1105', name='Natasha', rarity=4, card=<PIL.Image.Image image mode=RGBA size=1924x802 at 0x15816AEFD60>, size=(1924, 802)), Card(id='1001', name='March 7th', rarity=4, card=<PIL.Image.Image image mode=RGBA size=1924x802 at 0x15816B26050>, size=(1924, 802)), Card(id='1106', name='Pela', rarity=4, card=<PIL.Image.Image image mode=RGBA size=1924x802 at 0x15816B50310>, size=(1924, 802))]
name='Yanqing, Natasha, March 7th, Pela, '
id='1209, 1105, 1001, 1106, '
```

* ``settings`` - Specified settings during generation.
* ``player`` - User information.
  - ``avatar`` - Profile picture information.
  - ``space_info`` - Contains information about achievements, the number of light cones, characters and the SU.
* ``card`` - List of character cards.
  - ``id`` - Character id.
  - ``name`` - Character name.
  - ``rarity`` - Character rarity.
  - ``card`` - Character card image.
  - ``size`` - Card size.
* ``name`` - Showcase character names.
* ``id`` - Showcase character id.


### How to work with this data?
---

```py
from starrailcard import honkaicard 
import asyncio

async def main(uid):
  async with honkaicard.MiHoMoCard() as hmhm
    r = await hmhm.creat(uid)
    for key in r.card:
      print(f"{key.name} | {key.id}\nRarity: {key.rarity}")
      key.card.show() #Show card image.

asyncio.run(main(700649319))
```
