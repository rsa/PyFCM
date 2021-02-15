#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup


def read_file(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as r:
        return r.read()


README = read_file("README.md")
CONTRIB = read_file("CONTRIBUTING.rst")
CHANGES = read_file("CHANGES.rst")
version = read_file("VERSION.txt").strip()

setup(
    name="PyFCM",
    version=version,
    author="/dev/rsa",
    author_email="kris13@bk.ru",
    description=("Python fan control daemon for SBC board"),
    long_description="\n\n".join([README, CONTRIB, CHANGES]),
    license="GPL",
    keywords="fan control gpio",
    url="https://github.com/rsa/PyFCM",
    download_url="https://github.com/rsa/PyFCM/tarball/" + version,
    packages=["FCM"],
    setup_requires=["Opi.GPIO >= 0.4.0","argparse","configparser"],
    zip_safe=False,
    classifiers=[
        "License :: GPL License",
        "Development Status :: 1 - Alfa",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Programming Language :: Python :: 3",
    ]
)
