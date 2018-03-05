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

def expand(rancher_path):
    env = Environment(loader = FileSystemLoader(rancher_path), trim_blocks=True, lstrip_blocks=True)
    with open('/srv/pillar/%s.sls') % __salt__['grains.get']['environment']) as f:
        config_data = yaml.load(f)

    template = env.get_template('docker-compose.yml')
    output = template.render(config=config_data)
    with open('docker-compose-tmp.yml', 'w') as f:
        f.write(output)

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
    expand(rancher_path)

    if upgrade == "upgrade":
        if confirm == "confirm":
            cmd = 'rancher up -u -c --rancher-file {0}/rancher-compose.yml -f {0}/docker-compose-tmp.yml -d'.format(rancher_path)
        elif confirm == "rollback":
            cmd = 'rancher up -u -r --rancher-file {0}/rancher-compose.yml -f {0}/docker-compose-tmp.yml -d'.format(rancher_path)
        else:
            cmd = 'rancher up -u --rancher-file {0}/rancher-compose.yml -f {0}/docker-compose-tmp.yml -d'.format(rancher_path)
    else:
        cmd = 'rancher up --rancher-file {0}/rancher-compose.yml -f {0}/docker-compose-tmp.yml -d'.format(rancher_path)
    return __salt__['cmd.run'](cmd)

def upgrade(stack, container, confirm=None):
    '''
    option to upgrade just a single container.
    to upgrade the whole stack use rancher.stack
    rancher.upgrade <stack> <container> (confirm or rollback with second command)
    '''
    rancher_path = '/srv/salt/rancher/%s' % (stack)
    expand(rancher_path)

    if confirm == "confirm":
        cmd = 'rancher up -u -c --rancher-file {0}/rancher-compose.yml -f {0}/docker-compose-tmp.yml -d {1}'.format(rancher_path, container)
    elif confirm == "rollback":
        cmd = 'rancher up -u -r --rancher-file {0}/rancher-compose.yml -f {0}/docker-compose-tmp.yml -d {1}'.format(rancher_path, container)
    else:
        cmd = 'rancher up -u --rancher-file {0}/rancher-compose.yml -f {0}/docker-compose-tmp.yml -d {1}'.format(rancher_path, container)
    return __salt__['cmd.run'](cmd)
