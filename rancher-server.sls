include:
  - docker

install-rancher-server:
  cmd.run:
    - name: 'docker run -d --restart=unless-stopped -p 8080:8080 rancher/server'

/usr/bin/rancher:
  file.managed:
    - source: salt://files/usr/bin/rancher