import asyncio
import starrailcard

cookie = {
    "ltmid_v2": "1awu0nsdd_hy",
    "ltoken_v2": "v2_CXXXXXXnBxOBokYmYyYzBiXXXXXXxIJ686LEGKKjUp6gCMP-XXXXXX",
    "ltuid_v2": "123456789"
}

async def main():
  async with starrailcard.HoYoCard(cookie) as card:
      data = await card.create(700649319)
      print(data)

asyncio.run(main)
