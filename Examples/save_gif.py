import asyncio
import starrailcard

async with starrailcard.Card() as card:
        data = await card.creat(700649319, style=2)
    for card in data.card:
        if card.animation:
            card.save_gif(method = "pillow", format= "webp")
      
asyncio.run(mains())
