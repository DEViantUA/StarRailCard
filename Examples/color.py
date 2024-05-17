import asyncio
import starrailcard

async def main():
    async with starrailcard.Card(color = {"1308": ((98,47,104))}) as card:
        await card.create(700649319, style=1)
        
asyncio.run(main())
