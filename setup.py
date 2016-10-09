from setuptools import setup

setup(
    name="opendank",
    version="0.1",
    description="View images from the WWW in a diashow.",
    url="https://github.com/lnsp/opendank",
    download_url="https://github.com/lnsp/opendank/tarball/0.1",
    author="the opendank community",
    author_email="lennart@mooxmirror.io",
    license="MIT",
    packages=["opendank"],
    keywords=["memes", "www", "diashow"],
    classifiers=[],
    install_requires=[
        "praw",
        "requests",
        "pillow",
        "bs4",
    ],
    scripts=["bin/opendank"],
    zip_safe=False)
