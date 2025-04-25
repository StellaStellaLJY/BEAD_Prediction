from flask import Flask, request, jsonify
from bead_prediction import process_and_predict, fetch_weather_data, prepare_data  # 导入预测函数

app = Flask(__name__)

@app.route('/')
def home():
    return "🎉 Flask API is working!"
    
# 预测接口
@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        # 获取 JSON 数据
        data = request.get_json()

        # 调用 bead_prediction 中的预测函数
        predictions = process_and_predict(data)
        
        # 返回预测结果
        return jsonify({"predictions": predictions})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
        
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # 默认端口为5000，Azure会自动提供PORT环境变量
    app.run(host='0.0.0.0', port=port)
