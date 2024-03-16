import asyncio
import starrailcard

async with starrailcard.Card() as card:
        data = await card.creat(700649319, style=2)
    for card in data.card:
      card.show() #Model method
      card.card.show() #Pillow method
     
asyncio.run(mains())
