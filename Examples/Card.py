import asyncio
import starrailcard

async def main():
    async with starrailcard.Card() as card:
        print(card)        
        
asyncio.run(main())
