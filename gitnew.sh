#! /bin/bash
read -p "are you sure to create branch $1(y)" a
if [[ $a != 'y' ]]; then
  exit 1
fi
git checkout -b $1
git merge $2
git push origin $1
git branch --set-upstream-to=origin/$1
