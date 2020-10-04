
workers = 1
bind = '0.0.0.0:5050'
user = 'base'
loglevel = 'info'
accesslog = '/var/log/nginx/gunicorn.access.log'
errorlog = '/var/log/nginx/gunicorn.errors.log'
access_log_format = '%({X-Forwarded-Host}i)s - %({X-Real-IP}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
