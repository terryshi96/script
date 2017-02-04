#!/bin/bash
#make sure pip install scaffold && virtualenv
if [ $# != 1 ]; then
  echo "please your project name"
  exit 1
fi
pyscaffold -p $1 && cd $1 && touch requirements.txt
virtualenv --python=/usr/local/bin/python3.6 .venv && source .venv/bin/activate
