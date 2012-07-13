from __future__ import with_statement
from fabric.api import local
import os
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['50.116.21.58']
local_project_path = '/home/devasia/pyserver/directory'
production_project_path = '/srv/webapp/directory'


def restart_supervisor():
    sudo("supervisorctl reload")


def remote_source_update():
    with cd(production_project_path):
        run("git pull")


def push_code():
    local("git push origin master", capture=False)
    remote_source_update()
    restart_supervisor()


def commit_deploy(commit_message):
    local('git add --all && git commit -a -m "%s"' % commit_message,
          capture=False)
    local("git push origin master", capture=False)
    remote_source_update()
    restart_supervisor()
