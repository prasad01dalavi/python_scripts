from flask import Flask, make_response, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from mongoengine import *


connect('mongodb')  # Connect to Mongo Database
app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10/second"]  # 10 requests per second by any user
)


class RequestStats(Document):
    user_id = IntField()
    rps = IntField()

class RateLimiter:
    def configure_global_limits(self, rps):
        # set global limit to request per second
        pass

    def configure_limit(self, user_id, rps):
        # set limit for specified user id to requests per second
        pass 


def get_rps():
    user_id = request.args.get('user_id')
    rps = RequestStats.objects(user_id=user_id).get().rps
    print(f'[INFO] User ID: {user_id} | RPS: {rps}')
    return f"{rps}/second"


@app.route('/api')
@limiter.limit(limit_value=get_rps)
def api():
    print(f'[INFO] Request from host: {get_remote_address()}')
    return 'This is response from the API!'


@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
            jsonify(error="Ratelimit exceeded %s" % e.description), 429
    )

if __name__ == '__main__':
    app.run(debug=True)
