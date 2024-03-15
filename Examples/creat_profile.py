import asyncio
import starrailcard

async def main():
    async with starrailcard.Card() as card:
        data = await card.creat_profile(700649319)

    print("Settings:")
    print(f"  UID: {data.settings.uid}")
    print(f"  Lang: {data.settings.lang}")
    print(f"  Hide UID: {data.settings.hide_uid}")
    print(f"  Save: {data.settings.save}")
    print(f"  Force Update: {data.settings.force_update}")
    print(f"  Style: {data.settings.style}")
    
    print("\nPlayer:")
    print(f"  UID: {data.player.uid}")
    print(f"  Nickname: {data.player.nickname}")
    print(f"  Level: {data.player.level}")
    print(f"  World Level: {data.player.world_level}")
    print(f"  Friend Count: {data.player.friend_count}")
    print(f"  Avatar ID: {data.player.avatar.id}")
    print(f"  Avatar Name: {data.player.avatar.name}")
    print(f"  Avatar Icon: {data.player.avatar.icon}")
    print(f"  Signature: {data.player.signature}")
    print(f"  Is Display: {data.player.is_display}")
    print("  Space Info:")
    print(f"    Memory Level: {data.player.space_info.memory_data.level}")
    print(f"    Chaos ID: {data.player.space_info.memory_data.chaos_id}")
    print(f"    Chaos Level: {data.player.space_info.memory_data.chaos_level}")
    print(f"    Universe Level: {data.player.space_info.universe_level}")
    print(f"    Light Cone Count: {data.player.space_info.light_cone_count}")
    print(f"    Avatar Count: {data.player.space_info.avatar_count}")
    print(f"    Achievement Count: {data.player.space_info.achievement_count}")
    
    print("\nCharacter Names:")
    for name in data.character_name:
        print(f"  - {name}")
    
    print("\nCharacter IDs:")
    for cid in data.character_id:
        print(f"  - {cid}")

    print(f"\nCard: {data.card}")

asyncio.run(main())
