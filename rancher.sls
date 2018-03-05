include:
  - docker

install-rancher-agent:
  cmd.run:
    {% if grains['environment'] == 'lab' %}
    - name: 'docker run --rm --privileged -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/rancher:/var/lib/rancher rancher/agent:v1.2.6 http://rancher-url/v1...'
    {% elif grains['environment'] == 'staging' %}
    - name: 'docker run --rm --privileged -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/rancher:/var/lib/rancher rancher/agent:v1.2.6 http://rancher-url/v1...'
    {% endif %}
    - unless: 'docker ps | grep rancher'
