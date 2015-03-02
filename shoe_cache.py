from flask import Flask, request
import redis


app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379)

default_upper = 'default_upper'
# /image/?s=A02-B05-C02-H04&upper1=AH5
@app.route('/image/', methods=('GET',))
def cache_image():
    if 's' not in request.args:
        raise Exception('There is not the value of the "s" in the url')
    s = request.args['s']
    upper = request.args.get('upper1', default_upper)
    key = str.join(s, ':', upper)
    image = r.get(key)
    if not image:
        return image
    else:
        r.set(key, key)
        return key

    return 'Hello World' + request.args['name'].get('upper1', default_upper)


if __name__ == '__main__':
    app.run()
