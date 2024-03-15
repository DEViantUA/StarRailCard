import asyncio
import starrailcard

async def main():
    async with starrailcard.Card(user_font = "genshin.ttf") as card:
        print(card)
    #OR
    async with starrailcard.Card(user_font = "C:/Users/Username/Documents/Fonts/genshin.ttf") as card:
        print(card)
      
asyncio.run(main())
