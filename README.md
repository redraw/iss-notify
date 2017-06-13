🛰

1. `pip install requeriments.txt`
2. `huey_consumer tasks.huey`

##### On supervisor
```
# /etc/supervisor/conf.d/iss.conf

[program:iss]
directory=/path/to/iss-notify
command=huey_consumer.py tasks.huey
redirect_stderr=true
```
