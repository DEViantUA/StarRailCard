import asyncio
import starrailcard

async def mains()
        async with starrailcard.Card() as card:
                data = await card.creat(700649319, style=2)
            for card in data.card:
              await card.get_info(lang = "en")
             
asyncio.run(mains())
