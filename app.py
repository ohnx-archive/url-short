from flask import Flask, redirect, make_response, request, render_template
import redis
import re
import random

app = Flask(__name__)
# redis config
r = redis.StrictRedis(host='europa.stsosz.io', port=6380, db=0)
p = re.compile("^(https?\:\/\/)?.*\..*\/.*$")
# key generation
# character set
kc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# length
kl = 5
# max tries when generating a random key
mt = 80
# website title
title = "URL shortener"

def jresp(j, val=200):
    resp = make_response(j, val)
    resp.mimetype = 'application/json'
    return resp

@app.route("/json/stats/<key>")
def fetchjson(key):
    url = r.get('key:'+key)
    if url is None:
        return jresp("{\"error\":\"key not found\"}", 400)
    else:
        hits = r.get('hit:'+key)
        return jresp("{\"key\":\""+key+"\",\"url\":\""+url+"\",\"hits\":\""+hits+"\"}")

@app.route("/json/add", methods=['GET', 'POST'])
def addjson():
    # check if value is in post, if not then assume is GET
    if 'url' in request.args:
        url = request.args['url']
    elif 'url' in request.form:
        url = request.form['url']
    else:
        return jresp("{\"error\":\"No url specified\"}", 400)
    if 'key' in request.args:
        key = request.args['key']
    elif 'key' in request.form:
        key = request.form['key']
    else:
        # only try mt amount of times
        for x in range(0, mt):
            key = ''.join(random.choice(kc) for _ in range(kl))
            if r.get('key:'+key) is None:
                break
            if x==mt:
                # didnt get anywhere, return error
                return jresp("{\"error\":\"key could not be generated in sane amount of time\"}", 400)
    # check if key exists
    if not r.get('key:'+key) is None:
        return jresp("{\"error\":\"key already exists\"}", 400)
    if p.match(url):
        r.set('key:'+key, url)
        r.set('hit:'+key,0)
        return jresp("{\"key\":\""+key+"\",\"url\":\""+url+"\",\"hits\":\"0\"}")
    else:
        return jresp("{\"error\":\"URL invalid\"}", 400)

@app.route("/<key>")
def fetch(key):
    url = r.get('key:'+key)
    if url is None:
        return render_template('index.html', title=title)
    r.incr('hit:'+key)
    return redirect(url, code=301)

@app.route("/")
def index():
    return render_template('index.html', title=title)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')