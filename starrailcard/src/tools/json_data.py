# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.

import json
import aiofiles

class JsonManager:
    def __init__(self, file_path):
        self.file_path = file_path

    async def read(self):
        try:
            async with aiofiles.open(self.file_path, mode='r', encoding="utf-8") as file:
                data = await file.read()
                return json.loads(data)
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON file '{self.file_path}'.")
    
    async def write(self, data):
        try:
            async with aiofiles.open(self.file_path, mode='w', encoding="utf-8") as file:
                await file.write(json.dumps(data, indent=4, ensure_ascii=False))
        except Exception as e:
            print(f"Error writing to file '{self.file_path}': {e}")