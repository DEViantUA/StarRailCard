### Information about the get_profile method
---

* Generates profile cards.
* Returns user information.

### Argument:
* ``uid`` - Custom UID from the game
* ``banner`` - Link to custom banner image. | Type: ``str`` | Default: ``None``
* ``card`` - Generate profile card. | Type: ``bool`` | Default: ``False``

### Usage example:

```py
from starrailcard import honkaicard 
import asyncio

async def main(uid):
  async with honkaicard.MiHoMoCard() as hmhm
    r = await hmhm.get_profile(700649319, banner = "https://i.ibb.co/ZSn53B0/yande-re-1101500-sample-dress-heels-herta-honkai-star-rail-nez39-skirt-lift.jpg", card= True)
    print(r)

asyncio.run(main(700649319))
```

### Result:

```py
settings=Settings(uid=700649319, lang='en', hide=False, save=False, background=True)
player=PlayerV2(uid='700649319', nickname='Korzzex', level=66, avatar=Avatar(id='200101', name='March 7th — Welcome', icon='https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/icon/avatar/200101.png'), signature='Описания ещё нет... Скоро...', friend_count=16, world_level=6, birthday=None, space_info=SpaceInfo(pass_area_progress=7, light_cone_count=57, avatar_count=21, achievement_count=265))
card=<PIL.Image.Image image mode=RGBA size=694x802 at 0x1D8A7E02080>
name='Yanqing, Natasha, March 7th, Pela, '
id='1209, 1105, 1001, 1106, '
```

* ``settings`` - Specified settings during generation.
* ``player`` - User information.
  - ``avatar`` - Profile picture information.
  - ``space_info`` - Contains information about achievements, the number of light cones, characters and the SU.
* ``card`` - Profile card image. | Will be ``None`` if you specify: ``card = False``
* ``name`` - Showcase character names.
* ``id`` - Showcase character id.


### How to work with this data?
---

```py
from starrailcard import honkaicard 
import asyncio

async def main(uid):
  async with honkaicard.MiHoMoCard() as hmhm
    r = await hmhm.get_profile(uid)
    print(f"{r.player.nickname} | {r.player.uid}\nSignature: {r.player.signature}\nWL: {r.player.world_level}\nSU: {r.player.space_info.pass_area_progress}\nAchievement: {r.player.space_info.achievement_count}")
    if not r.card is None:
      r.card.show() #Show card image.

asyncio.run(main(700649319))
```
