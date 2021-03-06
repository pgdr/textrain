#!/usr/bin/env python3

from setuptools import setup

import os

__pgdr = "PG Drange <pgdr@equinor.com>"
__source = "https://github.com/pgdr/ochre"
__webpage = __source
__description = "Words to PDF and so on"


def src(x):
    root = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(root, x))


def _read_file(fname, op):
    with open(src(fname), "r") as fin:
        return op(fin.readlines())


def requirements():
    return []


def readme():
    try:
        return _read_file("README.md", lambda lines: "".join(lines))
    except:
        return __description




REQUIREMENTS = ('pdftotext', 'pdflatex', 'pdftoppm', 'pdfcrop')
for req in REQUIREMENTS:
    msg = 'Missing required tool {}.  Consider apt install it.'.format(req)
    print('Checking for tool {}'.format(req), end=' ... ')
    assert os.system('which ' + req) == 0, msg
    print('ok')

setup(
    name="textrain",
    packages=["textrain"],
    description=__description,
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="PG Drange",
    author_email="pgdr@equinor.com",
    maintainer=__pgdr,
    url=__webpage,
    project_urls={
        "Bug Tracker": "{}/issues".format(__source),
        "Documentation": "{}/blob/master/README.md".format(__source),
        "Source Code": __source,
    },
    license="The unlicense",
    keywords="ocr education tex poppler latex pdflatex",
    version="0.0.2",
    entry_points={
        'console_scripts': [
            'textrain = textrain:main',
        ],
    },
)
