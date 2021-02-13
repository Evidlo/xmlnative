from setuptools import setup
from xmlnative import version
import shutil
import os

setup(
    name='xmlnative',
    version=version.__version__,
    packages=['xmlnative'],
    author="Evan Widloski",
    author_email="evan@evanw.org",
    description="Parse XML into native Python objects",
    long_description=open('README.md').read(),
    long_description_content_type='text/x-markdown',
    license="GPLv3",
    keywords="lxml xml",
    url="https://github.com/evidlo/xmlnative",
    install_requires=[
        "lxml",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
