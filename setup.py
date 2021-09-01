"""Setup for aioOmada"""

from setuptools import setup

setup(
    name="aioomada",
    packages=["aioomada"],
    version="27",
    description="An asynchronous Python library for communicating with TP-Link Omada Controller API",
    author="Kevin Stark",
    author_email="kevstar@users.noreply.github.com",
    license="MIT",
    url="https://github.com/kevstark/aioomada",
    download_url="https://github.com/kevstark/aioomada/archive/v27.tar.gz",
    install_requires=["aiohttp"],
    tests_require=["pytest-asyncio", "pytest-aiohttp", "pytest", "aioresponses"],
    keywords=["tplink", "omada", "homeassistant"],
    classifiers=["Natural Language :: English", "Programming Language :: Python :: 3"],
)
