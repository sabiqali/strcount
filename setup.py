from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

VERSION = '0.0.6'
DESCRIPTION = 'A package to count the number of repeats in a Short Tandem Repeat Expansion from long reads.'
LONG_DESCRIPTION = long_description
# Setting up
setup(
    name="STRcount",
    version="0.0.6",
    author="Sabiq Chaudhary",
    author_email="<sabiq.work@gmail.com>",
    description="A package to count the number of repeats in a Short Tandem Repeat Expansion from long reads.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=requirements,
    keywords=['python', 'STR', 'Repeats', 'Tandem Repeats'],
    entry_points ={
            'console_scripts': [
                'STRcount = STRcount.STRcount:main'
            ]
        },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    scripts=['src/STRcount/STRcount.py']
)