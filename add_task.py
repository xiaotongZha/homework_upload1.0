import os

print('input task title')
info=input()
linfo=info.split(' ')
if len(linfo)!=2:
    print("error")
    exit(0)

with open('task.info','r',encoding='utf-8') as f:
    task_list=f.readlines()

if info in task_list:
    print("already exist")
    exit(0)

with open('task.info','a',encoding='utf-8') as f:
    f.write(info+'\n')

os.makedirs(f'report/{linfo[0]}/files/')
open(f'report/{linfo[0]}/cnt.txt','w')
open(f'report/{linfo[0]}/log.txt','w')
