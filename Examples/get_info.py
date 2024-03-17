import asyncio
import starrailcard

async def main():
        async with starrailcard.Card() as card:
                data = await card.creat(700649319, style=2)
            for card in data.card:
              info = await card.get_info(lang = "en")
              print(info)
             
asyncio.run(main())
