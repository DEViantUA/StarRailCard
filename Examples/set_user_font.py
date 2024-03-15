import asyncio
import starrailcard

async def main():
    async with starrailcard.Card(user_font = "genshin.ttf") as card:
        await card.set_user_font("C:/Users/Username/Documents/Fonts/genshin.ttf")
        #Then you can call the main functions creat() and creat_profile()
        
asyncio.run(main())
