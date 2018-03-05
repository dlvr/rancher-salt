docker-repo:
  cmd.run:
    - name: 'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -; add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"; apt-get update'
    - unless: 'dpkg -l | grep docker'

install-docker:
  pkg.installed:
    - pkgs:
      - docker-ce: 17.06.2~ce-0~ubuntu
    - skip_verify: True
