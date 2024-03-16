import asyncio
import starrailcard

async def main():
    async with starrailcard.Card() as card:
            data = await card.creat_profile(700649319)
        key_id = data.get_charter()
        key_name = data.get_charter(name = True)
        key_setting = data.get_charter(setting = True)
        print(f"ID KEY: {key_id}")
        print(f"Name KEY: {key_name}")
        print(f"ID KEY SETTING: {key_setting}")
        
     
asyncio.run(main())
