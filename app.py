from flask import Flask, render_template, jsonify, abort
import os
import pandas as pd
import json

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
SECTIONS = ['PT', 'ED', 'Oven']


def get_subfolders(section):
    section_path = os.path.join(DATA_DIR, section)
    if not os.path.isdir(section_path):
        return []
    return sorted([
        d for d in os.listdir(section_path)
        if os.path.isdir(os.path.join(section_path, d))
    ])


def get_parameters(section, subfolder):
    folder_path = os.path.join(DATA_DIR, section, subfolder)
    if not os.path.isdir(folder_path):
        return []
    return sorted([
        f.replace('.csv', '') for f in os.listdir(folder_path)
        if f.endswith('.csv')
    ])


@app.route('/')
def index():
    section_data = {}
    for s in SECTIONS:
        section_data[s] = get_subfolders(s)
    return render_template('index.html', sections=SECTIONS, section_data=section_data)


@app.route('/dashboard/<section>/<subfolder>')
def dashboard(section, subfolder):
    if section not in SECTIONS:
        abort(404)
    parameters = get_parameters(section, subfolder)
    if not parameters:
        abort(404)
    return render_template(
        'dashboard.html',
        section=section,
        subfolder=subfolder,
        parameters=parameters
    )


@app.route('/api/data/<section>/<subfolder>/<parameter>')
def get_data(section, subfolder, parameter):
    if section not in SECTIONS:
        abort(404)
    csv_path = os.path.join(DATA_DIR, section, subfolder, f'{parameter}.csv')
    if not os.path.isfile(csv_path):
        abort(404)
    try:
        df = pd.read_csv(csv_path)
        df.columns = [c.strip().lower() for c in df.columns]
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        df['difference'] = (df['actual'] - df['forecasted']).round(6)
        return jsonify({
            'timestamps': df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
            'actual': df['actual'].round(6).tolist(),
            'forecasted': df['forecasted'].round(6).tolist(),
            'difference': df['difference'].tolist(),
            'parameter': parameter.replace('_', ' '),
            'subfolder': subfolder.replace('_', ' '),
            'section': section
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
