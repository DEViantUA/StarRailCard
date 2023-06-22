# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starrailcard',
 'starrailcard.src',
 'starrailcard.src.generators',
 'starrailcard.src.tools']

package_data = \
{'': ['*'],
 'starrailcard.src': ['assets/*',
                      'assets/Sets/*',
                      'assets/Tallants/*',
                      'assets/bg/*',
                      'assets/const/*',
                      'assets/font/*',
                      'assets/lc/*',
                      'assets/stars/*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0', 'honkairail>=1.0.9,<2.0.0']

setup_kwargs = {
    'name': 'starrailcard',
    'version': '0.0.2',
    'description': 'Module for generating Honkai Star Rail character cards',
    'long_description': '<p align="center">\n <img src="https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/StarRailCardM.png" alt="Баннер"/>\n</p>\n\n____\n\n## StarRailCard\nModule for generating Honkai Star Rail character cards\n:white_medium_square: Ability to generate with or without background.<br>\n:white_medium_square: Ability to set a custom image.<br>\n:white_medium_square: Flexible map settings.\n\n## Installation:\n```\npip install starrailcard\n```\n\n## Launch:\n``` python\nfrom starrailcard import honkaicard \nimport asyncio\n\nasync def mains():\n    while True:\n        async with honkaicard.MiHoMoCard() as hmhm:\n            r = await hmhm.creat(700649319)\n            print(r)\n\nasyncio.run(mains())\n```\n\n## Languages Supported\n| Languege    |  Code   | Languege    |  Code   | Languege    |  Code   |\n|-------------|---------|-------------|---------|-------------|---------|\n|  English    |     en  |  русский    |     ru  |  Chinese    |    chs  |\n|  Tiếng Việt |     vi  |  ไทย        |     th  | Taiwan     |    cht  |\n|  português  |     pt  | 한국어      |     kr  | deutsch    |     de  |\n|  日本語      |     jp  | 中文        |     zh  | español    |     es  |\n|  中文        |     zh  | Indonesian |     id  | français   |     fr  |\n|  Khaenri\'ah  |     kh  | Khaenri\'ah |',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DEViantUA/StarRailCard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
