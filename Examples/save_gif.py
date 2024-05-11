import asyncio
import starrailcard

async def main():
        async with starrailcard.Card() as card:
            data = await card.create(700649319, style=2)
            for card in data.card:
                if card.animation:
                    card.save_gif(method = "pillow", format= "webp")
      
asyncio.run(main())
