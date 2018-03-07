# rancher-salt
A few assumptions with these states and modules:  
1. Running rancher server 1.26 (latest)  
2. rancher-cli is installed on your salt-master and available globally (usr_local_bin)  
3. Some stuff is hardcoded to how we have our salt and pillar paths setup (e.g. _srv_salt , _srv_pillar). You’ll need to adjust paths for how you have it configured  

## rancher module  
Right now you can make three calls with this module: list, new stack, and upgrade services  

The module is essentially a wrapper for the rancher-cli which needs to be installed on the salt master.  

### Installation  
Create a directory called `_modules` in your salt files root and copy the python script over  
Run `sudo salt-call saltutil.sync_modules` to install it. You should get a return like this:  
```
local:
    - modules.rancher
```

### List containers
`sudo salt-call rancher.containers`
This will list all running containers in your rancher environment
(similar to `docker ps -a`)

### Stack options
The `rancher.stack`  does 2 things:
1. Creates a new stack in rancher
2. Upgrades the **whole** stack of containers (probably don’t want to do regularly)

Create a new stack, named `website`, running 1 container of apache, 1 nginx:  
`sudo salt-call rancher.stack sample-website`

To upgrade the entire stack:  
`sudo salt-call rancher.stack website upgrade`

To confirm or rollback (separate commands from upgrade):  
`sudo salt-call rancher.stack website upgrade confirm/rollback`

### Specific service/container upgrades:  
To upgrade a single container/service, use `rancher.upgrade`. The commands are similar to the stack commands

To upgrade only the nginx container in the stack `website`  
`sudo salt-call rancher.upgrade website nginx`

To confirm or rollback (separate command):  
`sudo salt-call rancher.upgrade website nginx confirm/rollback`  

## Pillar variables  

This module allows environment variables to be passed through to the rancher config. The module imports the .sls as `config`. You then call that in your `docker-compose.yml` as `config.entry`. See the sample-website files for an example.  

This module as-is used the pillar file associated with the "environment" we have configured (like, lab, staging, etc.), with this salt-call `open('/srv/pillar/%s.sls') % __salt__['grains.get']['environment'])`, however you can change this to whatever pillar file or grain.
