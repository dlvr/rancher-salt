# -*- coding: utf-8 -*-
'''
:maintainer: Chris Reed (chris@dlvr.com)
:maturity: new
:requires: none
:platform: all
'''
from __future__ import absolute_import
from jinja2 import Environment, FileSystemLoader
import yaml
import salt
import logging
import cmd
import os

LOG = logging.getLogger(__name__)

def expand(rancher_path, version="latest"):
    env = Environment(loader = FileSystemLoader(rancher_path), trim_blocks=True, lstrip_blocks=True)
    with open('/srv/pillar/%s.sls' % __salt__['grains.get']('environment')) as f:
        config_data = yaml.load(f)

    config_data["tag"] = version

    template = env.get_template('docker-compose.yml')
    template2 = env.get_template('rancher-compose.yml')

    output = template.render(config=config_data)
    output2 = template2.render(config=config_data)

    with open("docker-compose-tmp.yml", "w") as f:
        f.write(output)

    with open("rancher-compose-tmp.yml", "w") as g:
        g.write(output2)

def containers():
    '''
    Lists all running containers in rancher environment
    '''
    return __salt__['cmd.run']('rancher ps')

def stack(stack, upgrade=None, confirm=None):
    '''
    Provision a new stack in rancher:
    rancher.stack <stack name>
    To upgrade the whole stack do:
    rancher.stack upgrade <stack name> (confirm or rollback with a second command)
    '''

    rancher_path = '/srv/salt/rancher/%s' % (stack)
    os.chdir(rancher_path)
    expand(rancher_path)

    if upgrade == "upgrade":
        if confirm == "confirm":
            cmd = 'rancher up -u -c --rancher-file {0}/rancher-compose-tmp.yml -f {0}/docker-compose-tmp.yml -d'.format(rancher_path)
        elif confirm == "rollback":
            cmd = 'rancher up -u -r --rancher-file {0}/rancher-compose-tmp.yml -f {0}/docker-compose-tmp.yml -d'.format(rancher_path)
        else:
            cmd = 'rancher up -u --rancher-file {0}/rancher-compose-tmp.yml -f {0}/docker-compose-tmp.yml -d'.format(rancher_path)
    else:
        cmd = 'rancher up --rancher-file {0}/rancher-compose-tmp.yml -f {0}/docker-compose-tmp.yml -d'.format(rancher_path)
    output = __salt__['cmd.run'](cmd)
    os.remove("%s/docker-compose-tmp.yml" % rancher_path)
    os.remove("%s/rancher-compose-tmp.yml" % rancher_path)
    return output

def upgrade(stack, container, version="latest", confirm=None):
    '''
    option to upgrade just a single container.
    to upgrade the whole stack use rancher.stack
    rancher.upgrade <stack> <container> (confirm or rollback with second command)
    '''
    rancher_path = '/srv/salt/rancher/%s' % (stack)
    os.chdir(rancher_path)
    expand(rancher_path, version)

    if confirm == "confirm":
        cmd = 'rancher up -u -c --rancher-file {0}/rancher-compose-tmp.yml -f {0}/docker-compose-tmp.yml -d {1}'.format(rancher_path, container)
    elif confirm == "rollback":
        cmd = 'rancher up -u -r --rancher-file {0}/rancher-compose-tmp.yml -f {0}/docker-compose-tmp.yml -d {1}'.format(rancher_path, container)
    else:
        cmd = 'rancher up -u --rancher-file {0}/rancher-compose-tmp.yml -f {0}/docker-compose-tmp.yml -d {1}'.format(rancher_path, container)
    output = __salt__['cmd.run'](cmd)
    os.remove("%s/docker-compose-tmp.yml" % rancher_path)
    os.remove("%s/rancher-compose-tmp.yml" % rancher_path)
    return output
