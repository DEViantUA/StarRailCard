import asyncio
import starrailcard

async def main():
    async with starrailcard.Card(lang = "en") as card:
        await card.set_lang("ua")
        #Then you can call the main functions creat() and creat_profile()
        
asyncio.run(main())
