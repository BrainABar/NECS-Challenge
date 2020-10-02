# NECS-Challenge
Creating basic web service with reverse proxy and load balancing

Set up initial server:
```bash
Get the linode-cli (can allow use regular ssh)
    > mkdir linode-cli
    > python3 -m pip install virtualenvironment
    > python3 -m virtualenv venv
    > source venv/bin/active
    > python -m pip install linode-cli --upgrade
    > linode-cli configure
    > linode-cli ssh root@<Server_Name>
    > apt update && apt upgrade
    > hostnamectl set-hostname personal-server
    > nano /etc/hosts # add server-ip and hostname under localhost
    > adduser admin
    > passwd admin
    > usermod -aG wheel admin
    > exit
    > linode-cli ssh admin@<Server_Name>
    > mkdir .ssh

Open a new local terminal and create an ssh key on local machine:
    > ssh-keygen
    > linode-cli linodes list # get servers ip
    > scp ~/.ssh/<filename>.pub admin@<ip-address>:~/.ssh/authorized_keys

Give access to ssh file:
    > sudo chmod 700 ~/.ssh/
    > sudo chmod 600 ~/.ssh/*
    > sudo nano /etc/ssh/sshd_config # Set PermitRootLogin to no and PasswordAuthentication no
    > sudo systemctl restart sshd

Add firewall rules:
    // Allow loopback connections
    > sudo iptables -A INPUT -i lo -j ACCEPT
    // Allow responses
    > sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    // Allow SSH
    > sudo iptables -A INPUT -p tcp --dport ssh -j ACCEPT
    // Allow HTTP/HTTPS
    > sudo iptables -A INPUT -p tcp -m multiport --dports 80,443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
    //Set default rules
    > sudo iptables -P INPUT DROP
    > sudo iptables -P OUTPUT ACCEPT
    > sudo iptables -P FORWARD DROP
```

Run Flask with reload
```bash
export FLASK_APP=src/app.run.py
export FLASK_ENV=development
flask run -h 0.0.0.0 -p 5000
```

Run GUnicorn with workers
```bash
export FLASK_ENV=testing
gunicorn -w 2 -b 0.0.0.0:5000 --chdir src/ 'app:create_app()'
```