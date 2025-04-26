from flask import Flask, request, jsonify
from bead_prediction import process_and_predict, fetch_weather_data, prepare_data  # 导入预测函数

app = Flask(__name__)

@app.route('/')
def home():
    return "🎉 Flask API is working!"
    
# 预测接口
@app.route('/predict', methods=['GET', 'POST'])  # 支持GET和POST
def predict_route():
    try:
        predictions = process_and_predict()
        predictions_json = predictions.to_dict(orient='records')
        return jsonify(predictions_json)  # 直接返回列表，不要包一层 

    except Exception as e:
        return jsonify({"error": str(e)}), 400
        
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # 默认端口为5000，Azure会自动提供PORT环境变量
    app.run(host='0.0.0.0', port=port)
