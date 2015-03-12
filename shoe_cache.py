from flask import Flask, request, Response
import redis
import urllib2


backed_image_url = 'http://tucoo.com/logo_class/telecom_logo04/images/Geek.png'

app = Flask(__name__)
r = redis.StrictRedis(host='192.168.1.52', port=6379)

default_upper = 'default_upper'
# /image/?s=A02-B05-C02-H04&upper1=AH5
@app.route('/image/', methods=('GET',))
def cache_image():
    if 's' not in request.args:
        raise Exception('There is not the value of the "s" in the url')
    s = request.args['s']
    upper = request.args.get('upper1', default_upper)
    key = s + ':' + upper
    img_data = r.get(key)
    if not img_data:
        img_data = urllib2.urlopen(backed_image_url).read()
        r.set(key, img_data)
        return Response(img_data, content_type='image/jpeg')
    else:
        return Response(img_data, content_type='image/jpeg')


if __name__ == '__main__':
    app.run()
