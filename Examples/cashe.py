import asyncio
import starrailcard

async def main():
    async with starrailcard.MiHoMoCard(cashe = {"maxsize": 500, "ttl": 60}) as card:
        print(card)

    #OR

    async with starrailcard.MiHoMoCard(cashe = {"maxsize": 500}) as card:
        print(card)

    #OR

    async with starrailcard.MiHoMoCard(cashe = {"ttl": 60}) as card:
        print(card)
        
asyncio.run(main())
