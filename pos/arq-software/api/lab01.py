import os
import functools
import pandas as pd
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
from cachelib.simple import SimpleCache


SECRET_KEY = 'xyz987'
serializer = URLSafeTimedSerializer(SECRET_KEY)


cache = SimpleCache()


app = Flask(__name__)


def generate_token(data, expiration=3600):
    token = serializer.dumps(data)
    cache.set(token, data, timeout=expiration)
    return token


def validate_token(token):
    data = cache.get(token)
    if data is not None:
        return data
    return data


def token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authentication')
        if not token:
            return jsonify({'error': 'token is missing'}), 401
        data = validate_token(token)
        if not data:
            return jsonify({'error': 'token is invalid'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/token', methods=['POST'])
def token():
    data = request.json
    token = generate_token(data)
    return jsonify({'token': token}), 200


    
@app.route('/upload', methods=['POST'])
@token_required
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'no file part'}), 400

    f = request.files['file']

    if f.filename == '':
        return jsonify({'error': 'no selected file'}), 400

    if f.filename.endswith('.csv'):
        f.save(secure_filename(f.filename))
        df = pd.read_csv(f.filename)
        jsonfilename = f.filename.replace('.csv', '.json')
        df.to_json(jsonfilename, orient='records')
        return jsonify(df.head().to_dict(orient='records')), 200
    else:
        return jsonify({'error': 'not a csv file'}), 400


if __name__ == '__main__':
    app.run(debug=True)
