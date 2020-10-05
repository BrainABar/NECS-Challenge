## Introduction
What is needed to get an application running with a load balancer and https

- configure server
  * Updates/Patches
  * Create sudo user/group
  * Create non-sudo user/group
  * Remove root access
    - You can still regain access through cloud-providers client since it connects to a virtual terminal on the host
  * Enable SSH or FTP
  * Restrict ports
  * Find packages first from source, then official repos, last resort 3rd parties due to updates/security concerns
- configure nginx as reverse proxy
  * entry point to restrict overloading of other servers
    - if servers are within cloud-service cluster, overhead should be negligible
  * load balancer can also be handled by this proxy or be used a layer above/below another proxy
    - round robin: passed to next server in list as received
      * weighted: duplicates server within the list by weight (server_1=4, server_2=1, 5 total round robin connections)
    - least connected: tries to pass to least active connections
    - session persistence: sends to previously connected server so that data is easy accessed if previously generated
  * proxy-pass: original headers must be passed to next destination for inspection by application server/web application
    - can be unreliable if multiple layers or untrusted proxy
  * health checks: ensures server is up before creating trying to pass request
- configure gunicorn as application server
  * workers do not share memory so storage like ReDis/NoSQL should be used
  * workers are stored in memory so start up is not added to overhead
  * whitelist ips that need access
- configure flask as web application
  * context starts from request to response
    - allows for pre/post processing
      * ex: stripping headers when receiving payload/adding common response headers before sending request
- configure monitor/logger
  * remote service
  * remote server checking load/status like kubernetes
  * host server to allow for quick recovery if server goes down like supervisor
    - services like docker allow for some process management/scaling but need an application like supervisor/kubernetes
- configure ssl at proxy/application layer
  * 3rd party verifies validity of server, if self-served, many browsers will alert to possible compromise
  * application server, at least with gunicorn needs to be to use `upstream` so that nginx passes traffic along
    - must use socket with gunicorn or configure middleware/custom entry point
      * 104 error, gunicorn responds to initial ssl request and workers terminate connection since they respond right away
  * proxy server, handles ssl and connects with other services using http or desired protocol
- deployment
  * required firewall(ports) opened including able to handle responses to initial connection
  * SeLinux permissions set
  * proper permissions granted, most will start as sudo and revert to non-sudo
    - linked files, if not restricted, can be compromised to run different code
      * used to quickly enable/disable programs/configurations
  * dns records pointed towards cloud-provider
  * cloud-provider records set so domain name can be used

Notes: 
- RedHat/CentOS is much more bare-bones compared to Debian/Ubuntu derivatives

Set up initial server:
```bash
Get the linode-cli (can also use regular ssh)
    > mkdir linode-cli
    > python3 -m pip install virtualenvironment
    > python3 -m virtualenv venv
    > source venv/bin/active
    > python -m pip install linode-cli --upgrade
    > linode-cli configure

Access the server:
    > linode-cli ssh root@<Server_Name>
    > sudo dnf update
    > hostnamectl set-hostname sample-server
    > nano /etc/hosts # add server-ip and hostname under localhost
    > adduser admin
    > passwd admin
    > usermod -aG wheel admin
    > exit
    > linode-cli ssh admin@<Server_Name>
    > mkdir .ssh

Open a new local terminal and create an ssh key if needed and copy to server:
    > ssh-keygen
    > linode-cli linodes list # get servers ip
    > scp ~/.ssh/<filename>.pub admin@<ip-address>:~/.ssh/authorized_keys

Give access to ssh file:
    > sudo chmod 700 ~/.ssh/
    > sudo chmod 600 ~/.ssh/*
    > sudo nano /etc/ssh/sshd_config # Set PermitRootLogin to no and PasswordAuthentication no
    > sudo systemctl restart sshd

Add firewall rules:
    > sudo firewall-cmd --add-service=ssh --zone=public --permanent
    > sudo firewall-cmd --add-service=http --zone=public --permanent
    > sudo firewall-cmd --add-service=https --zone=public --permanent
```
---
Set up NGINX
- Guide to add nginx repo as it is the most updated: https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/#stable_vs_mainline
- CentOS does not come with sites-available/enabled but is included with Ubuntu
```
sudo mkdir /etc/nginx/sites-available
sudo mkdir /etc/nginx/sites-enabled
```
- allows for easier enabling/disabling of sites by linking what is needed from sites-available
  * not needed but makes it easier to distinguish what is active in sites-enabled
```bash
sudo ln -s /etc/nginx/sites-available/<filename>.conf /etc/nginx/sites-enabled/
```
- also able to add file at bottom of nginx.conf
- reload nginx: `sudo nginx -s reload`
- Basic log inspection
```
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```
---

Supervisorctl used to spin up gunicorn application servers
- create log directory/file
```
sudo nano /etc/supervisor/conf.d/<filename>.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl reload sample-program1
sudo supervisorctl reload sample-program2
```
---

Run Flask with reload
```bash
export FLASK_APP=src/app.run.py
export FLASK_ENV=development
flask run -h 0.0.0.0 -p 5000
```

Run GUnicorn with workers
```bash
export FLASK_ENV=testing
gunicorn -w 2 -b 0.0.0.0:5000 --chdir path/to/src/ 'app:create_app()'
```
---
