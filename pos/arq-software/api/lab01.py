import os
import pandas as pd
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route('/upload', methods=['POST'])
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
