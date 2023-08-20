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
                      'assets/stars/*',
                      'assets/teample_profile/bg/*',
                      'assets/teample_profile/charters/*',
                      'assets/teample_profile/element/*',
                      'assets/teample_tree/*',
                      'assets/teample_tree/artifact/*',
                      'assets/teample_tree/bg/*',
                      'assets/teample_tree/const/*',
                      'assets/teample_tree/lc/*',
                      'assets/teample_tree/skills/*',
                      'assets/teample_two/LC/*',
                      'assets/teample_two/artifact/*',
                      'assets/teample_two/bg/*',
                      'assets/teample_two/path/*',
                      'assets/teample_two/stats/*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0', 'honkairail>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'starrailcard',
    'version': '0.1.5',
    'description': 'Module for generating Honkai Star Rail character cards',
    'long_description': '<p align="center">\n <img src="https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/StarRailCardM.png" alt="Баннер"/>\n</p>\n\n____\n\n## StarRailCard\nModule for generating Honkai Star Rail character cards\n\n* Ability to generate with or without background.<br>\n* Ability to set a custom image.<br>\n* Flexible map settings.\n\n## Installation:\n```\npip install starrailcard\n```\n\n## Launch:\n``` python\nfrom starrailcard import honkaicard \nimport asyncio\n\nasync def mains():\n    async with honkaicard.MiHoMoCard(template=1) as hmhm:\n        r = await hmhm.creat(700649319)\n        print(r)\n\nasyncio.run(mains())\n```\n\n<details>\n<summary>Add image author</summary>\n\n``` python\nfrom starrailcard import honkaicard \nimport asyncio\n\nasync def mains():\n    async with honkaicard.MiHoMoCard(template=1) as hmhm:\n        r = await hmhm.creat(700649319)\n        for key in r.card:\n            cards = await hmhm.add_author(link= "https://www.deviantart.com/dezzso", card= key.card)\n            #cards.save(f"{key.id}.png") #A function to save an image with the author\'s stamp added.\n        print(r)\n\nasyncio.run(mains())\n```\n</details>\n\n\n<details>\n<summary>Create a profile card.</summary>\n\n``` python\nfrom starrailcard import honkaicard \nimport asyncio\n\nasync def mains():\n    async with honkaicard.MiHoMoCard(template=1) as hmhm:\n        r = await hmhm.get_profile(700649319,  card = True)\n        print(r)\n\nasyncio.run(mains())\n```\n</details>\n\n\n## Languages Supported\n| Languege    |  Code   | Languege    |  Code   | Languege    |  Code   |\n|-------------|---------|-------------|---------|-------------|---------|\n|  English    |     en  |  русский    |     ru  |  Chinese    |    chs  |\n|  Tiếng Việt |     vi  |  ไทย        |     th  | Taiwan     |    cht  |\n|  português  |     pt  | 한국어      |     kr  | deutsch    |     de  |\n|  日本語      |     jp  | 中文        |     zh  | español    |     es  |\n|  中文        |     zh  | Indonesian |     id  | français   |     fr  |\n\n\n\n<details>\n<summary>Sample 1 template</summary>\n \n[![Adaptation][3]][3]\n \n[3]: https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/a-18.png\n  \n</details>\n\n\n<details>\n<summary>Sample 2 template</summary>\n \n[![Adaptation][4]][4]\n \n[4]: https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/a-19.png\n \n</details>\n\n\n<details>\n<summary>Sample 3 template</summary>\n \n[![Adaptation][2]][2]\n \n[2]: https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/a-21.png\n \n</details>\n\n\n<details>\n<summary>Sample profile template</summary>\n \n[![Adaptation][1]][1]\n \n[1]: https://raw.githubusercontent.com/DEViantUA/StarRailCard/main/a-22.png\n \n</details>\n',
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
