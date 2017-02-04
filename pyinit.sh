#!/bin/bash
#make sure pip install scaffold && virtualenv
if [ $# != 1 ]; then
  echo "please your project name"
  exit 1
fi
pyscaffold -p $1 && cd $1 && touch requirements.txt
cat > setup.py << EOF
from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

install_requires=[
    # -*- Extra requirements: -*-
],

long_desc="""\
""",

setup(name='$1',
      version=version,
      description="",
      long_description=long_desc,
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      classifiers=[],
      )
#python setup.py sdist --formats=zip,gztar && python setup.py  register && python  setup.py sdist upload
EOF
virtualenv --python=/usr/local/bin/python3.6 .venv && source .venv/bin/activate
