import bottle
from bottle import Bottle, request, response
from services import OneSignal
from main import redis

app = Bottle()


@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = 'iss.now.sh'


@app.get('/')
def root():
    return 'ok'


@app.post('/subscribe')
def subscribe():
    player_id = request.params.get('playerId')

    device = OneSignal().get_device(player_id)

    if device:
        location = device['tags'].get('location')

        if location:
            # add location
            redis.sadd('iss:locations', location)

            # add player/device
            players = 'iss:location:%s:players' % location
            redis.sadd(players, player_id)

    return {
        'status': 'ok'
    }


@app.post('/unsubscribe')
def unsubscribe():
    player_id = request.params.get('playerId')

    device = OneSignal().get_device(player_id)

    if location:
        location = device['tags'].get('location')

        if location:
            # remove player/device
            players = 'iss:location:%s:players' % location
            redis.srem(players, player_id)

            # untrack location if no more players in the location
            if not redis.exists(players):
                redis.srem('iss:locations', location)

    return {
        'status': 'ok'
    }


app.run(host='0.0.0.0', port=8000)