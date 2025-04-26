from flask import Flask, request, jsonify
from bead_prediction import process_and_predict, fetch_weather_data, prepare_data

import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🎉 Flask API is working!"

@app.route('/predict', methods=['GET', 'POST'])
def predict_route():
    try:
        predictions = process_and_predict()
        predictions_json = predictions.to_dict(orient='records')
        return jsonify(predictions_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # Azure会提供PORT环境变量
    app.run(host='0.0.0.0', port=port)
