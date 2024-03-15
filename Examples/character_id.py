import asyncio
import starrailcard

async def main():
    async with starrailcard.Card(character_id = "1302,1305, 1006") as card:
        print(card)
        
asyncio.run(main())
