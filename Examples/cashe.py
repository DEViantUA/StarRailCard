import asyncio
import starrailcard

async def main():
    async with starrailcard.Card(cashe = {"maxsize": 500, "ttl": 60}) as card:
        print(card)

    #OR

    async with starrailcard.Card(cashe = {"maxsize": 500}) as card:
        print(card)

    #OR

    async with starrailcard.Card(cashe = {"ttl": 60}) as card:
        print(card)
        
asyncio.run(main())
