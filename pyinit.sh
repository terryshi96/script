#!/bin/bash
#make sure pip install scaffold
if [ $# != 1 ]; then
  echo "please your project name"
fi
pyscaffold -p $1 && cd $1 && touch requirements.txt
cd $1 && pyvenv .venv && source .venv/bin/activate
