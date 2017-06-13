🛰

1. `pip install requeriments.txt`
2. `huey_consumer tasks.huey`

##### Modules
Add your module inside `modules` folder, your module should be called `Hook` and should implement the `on_pass` callback

##### On supervisor
```
# /etc/supervisor/conf.d/iss.conf

[program:iss]
directory=/path/to/iss-notify
command=huey_consumer.py tasks.huey
redirect_stderr=true
```
