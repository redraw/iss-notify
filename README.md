🛰

1. `pip install requeriments.txt`
2. `huey_consumer tasks.huey`

##### Hooks
Add your module inside `modules` folder, your module should be called `Hook` and should implement the `on_pass` callback

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
          'mag': u'-2.5',
         'start': {'alt': u'10\xb0',
           'az': u'WNW',
           'datetime': datetime.datetime(2017, 6, 29, 22, 28, 4)}}
        """
        pass
```

##### Supervisor
```
# /etc/supervisor/conf.d/iss.conf

[program:iss]
directory=/path/to/iss-notify
command=huey_consumer tasks.huey
redirect_stderr=true
```
