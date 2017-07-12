🛰

1. `pip install requeriments.txt`
2. Set your `.env` (example in `.env.example`)
2. `huey_consumer tasks.huey`

#### Desktop notifications using `notify-send`
There's an example inside `modules/notify_send.py` to recieve desktop notifications.
Make sure to set up `DBUS_SESSION_BUS_ADDRESS` in your `.env` before running the worker.
From terminal you can add it by running,

```
$ env | grep DBUS >> .env
```


#### Hooks
Add your hook inside `modules` folder, the module class should be called `Hook` and should implement the `on_pass` callback.

```python
# /path/to/iss-notify/modules/example.py

class Hook:
    def on_pass(self, data):
        """
        {'end': {'alt': u'31\xb0',
           'az': u'SSW',
           'datetime': datetime.datetime(2017, 6, 29, 22, 31, 41)},
         'highest': {'alt': u'33\xb0',
           'az': u'SW',
           'datetime': datetime.datetime(2017, 6, 29, 22, 31, 8)},
         'start': {'alt': u'10\xb0',
           'az': u'WNW',
           'datetime': datetime.datetime(2017, 6, 29, 22, 28, 4)}}
        """
        pass
```

#### Supervisor
```
# /etc/supervisor/conf.d/iss.conf

[program:iss]
directory=/path/to/iss-notify
command=huey_consumer tasks.huey
redirect_stderr=true
```
