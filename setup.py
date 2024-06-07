import setuptools
import re

with open('starrailcard/__init__.py') as f:
	"""
		Get version from utils.py
		Ref: https://github.com/Rapptz/discord.py/blob/52f3a3496bea13fefc08b38f9ed01641e565d0eb/setup.py#L9
	"""
	version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)

setuptools.setup(
	name="starrailcard",
	version=version,
	author="DeviantUa",
	author_email="deviantapi@gmail.com",
	description= "This Python module provides the ability to create captivating character cards based on player data from Honkai Star Rail, obtained through their unique user identifiers (UIDs). StarRailCard streamlines the process of generating personalized character assembly cards, relying on the information provided by players.",
	long_description=open("README.md", "r", encoding="utf-8").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/DEViantUA/StarRailCard",
	keywords = ["honkai", "cards", "generation", "honkaistarraill","raill", "starraill", "builds", "honkairail", "honkai", "genshin", "build", "api"] ,
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[
		"pydantic",
		"aiohttp",
		"cachetools",
        "Pillow",
        "aiofiles",
        "imageio",
        "moviepy",
        "more-itertools",
        "numpy",
        "beautifulsoup4",
        "anyio"
	],
	python_requires=">=3.9",
	include_package_data=True
)