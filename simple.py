import os
import uuid
import redis
import consulate
import json
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    CONSUL_HOST = os.getenv("CONSUL_HOST", "no.host")
    CONSUL_PORT = os.getenv("CONSUL_PORT", 0)
    CONSUL_DC = os.getenv("CONSUL_DC", "nodc")

    consul = consulate.Consul(host=os.environ['CONSUL_HOST'], port=os.environ['CONSUL_PORT'], datacenter=os.environ['CONSUL_DC'])

    data = consul.catalog.service('redis')

    json_str = json.dumps(data)
    resp = json.loads(json_str)

    redis_address = (resp[0]['Address'])
    redis_port = (resp[0]['ServicePort'])

    r_server = redis.Redis(redis_address, redis_port) #this line creates a new Redis object and

    r_server.incr('counter')
    counter = r_server.get('counter')
    return render_template("index.html", CONSUL_HOST=CONSUL_HOST, CONSUL_PORT=CONSUL_PORT, CONSUL_DC=CONSUL_DC, redis_address=redis_address, redis_port=redis_port, counter=counter)

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
