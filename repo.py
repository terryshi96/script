#! /usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import os
import commands
import datetime

def post_dingtalk(msg):
    print('sending dingtalk message.....')
    os.system("curl %s -H 'Content-Type: application/json' \
        -d '{\"msgtype\": \"text\",\"text\": {\"content\": \" %s \"}}'"%(dingtalk_url, msg))

if __name__ == '__main__':
    dingtalk_url = ''
    arg = sys.argv
    if len(arg) != 4:
        print('lack arguments')
        exit(1)
    base_path = '../'
    project = arg[1]
    project_path = base_path + project
    # create / finish 
    action = arg[2]
    # tab / branch
    keep = arg[3]
    print(project,action,keep)
    current_tmp = commands.getstatusoutput('cd %s && git flow release list'%project_path)
    current = current_tmp[1].strip().strip('*').strip()
    tag = 'v0.1.' + datetime.datetime.now().strftime("%Y%m%d%H%M")
    flag = 1
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
                flag=os.system('cd %s && git checkout develop && git pull && git flow release start %s && git flow release publish %s'%(project_path, tag, tag))
                if flag == 0:
                    post_dingtalk("Project %s release branch has been created\n release/%s"%(project, tag))
        elif action == 'finish':
            print('release ' + current + ' will be finished')
            if keep != 'tag':
                flag=os.system('cd %s && git checkout release/%s && git pull && \
                    git flow release finish -k -n -m %s -p %s && git push && git checkout develop && git branch -d release/%s'%(project_path, current, current, current, current))
            else:
                flag=os.system('cd %s && git checkout release/%s && git pull && \
                    git flow release finish -m %s -p %s'%(project_path, current, current, current))
            if flag == 0:
                post_dingtalk("Project %s release branch release/%s has been finished\n "%(project, tag))
    else:
        os.system('cd %s && pwd && git status'%project_path)
    print('\nDone')


