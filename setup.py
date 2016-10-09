from setuptools import setup

setup(
    name="opendank",
    version="0.1",
    description="View images from the WWW in a diashow.",
    url="https://github.com/lnsp/opendank",
    author="the opendank community",
    license="MIT",
    packages=["opendank"],
    install_requires=[
        "praw",
        "requests",
        "pillow",
        "bs4",
    ],
    zip_safe=False)
