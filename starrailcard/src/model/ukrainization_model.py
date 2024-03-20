# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.


from pydantic import BaseModel
from typing import Dict, Union

class UkrainizationModel(BaseModel):
    stats: Dict[str, Union[str, dict, int, None]]
    weapons: Dict[str, Union[str, dict, int, None]]
    avatar: Dict[str, Union[str, dict, int, None]]
    relict_sets: Dict[str, Union[str, dict, int, None]]
    paths: Dict[str, Union[str, dict, int, None]]
    element: Dict[str, Union[str, dict, int, None]]