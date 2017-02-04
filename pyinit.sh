#!/bin/bash
#make sure pip install scaffold && virtualenv
if [ $# != 1 ]; then
  echo "please your project name"
  exit 1
fi
pyscaffold -p $1 && cd $1 && touch requirements.txt
cat >> setup.py << EOF
from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='$1',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
EOF
virtualenv --python=/usr/local/bin/python3.6 .venv && source .venv/bin/activate
