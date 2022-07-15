from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.13'
DESCRIPTION = 'Streaming video data via networks'
LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

# Setting up
setup(
    name="STRcount",
    version=0.0.1,
    author="Sabiq Chaudhary",
    author_email="<sabiq.work@gmail.com>",
    description="A package to count the number of repeats in a Short Tandem Repeat Expansion from long reads.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'argparse', 
        'logging', 
        'os',
        'pysam',
        'sys',
        'wheel'
    ],
    keywords=['python', 'STR', 'Repeats', 'Tandem Repeats'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)