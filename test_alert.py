from datetime import datetime, timedelta
from tasks import alert


next_pass = {
    'start': {
        'datetime': datetime.utcnow() + timedelta(seconds=5)
    },
    'highest': {
        'datetime': datetime.utcnow() + timedelta(seconds=10),
        'alt': u'30\xb0',
        'az': 'NE'
    },
    'end': {
        'datetime': datetime.utcnow() + timedelta(seconds=15)
    }
}

alert.schedule(args=[next_pass], delay=5)