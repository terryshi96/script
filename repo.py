#! /usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import os
import commands
import datetime

arg = sys.argv
if len(arg) != 4:
    print('lack arguments')
    exit(1)
base_path = '../'
project = arg[1]
project_path = base_path + project
# create / finish 
action = arg[2]
keep = arg[3]
print(project,action,keep)
current_tmp = commands.getstatusoutput('cd %s && git flow release list'%project_path)
current = current_tmp[1].strip().strip('*').strip()
tag = 'v0.1.' + datetime.datetime.now().strftime("%Y%m%d%H%M")
# 判断是否为git flow
if current.find('Not a gitflow-enabled repo yet') == -1:
    print('current release: \n' + current + '\n')
    if action == 'create':
        # 判断是否已有release
        if current.find('No release branches exist') == -1:
            print('please finish the release first')
            exit(1)
        else:
            print('release ' + tag + ' will be created')
            os.system('cd %s && git checkout develop && git pull && git flow release start %s && git flow release publish %s'%(project_path, tag, tag))
    elif action == 'finish':
        print('release ' + current + ' will be finished')
        if keep == 'true':
            os.system('cd %s && git flow release finish -k -m %s -p %s && git checkout develop && git branch -d release/%s'%(project_path, current, current, current))
        else:
            os.system('cd %s && git flow release finish -m %s -p %s'%(project_path, current, current))
else:
    os.system('cd %s && pwd && git status'%project_path)
print('End')


