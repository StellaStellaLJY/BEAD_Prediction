# -*- coding: utf-8 -*-


# app.py

from flask import Flask, request, jsonify
from bead_prediction import predict  # 导入预测函数

# 初始化 Flask 应用
app = Flask(__name__)

# 根路径，测试用
@app.route('/')
def home():
    return "🎉 Flask API is running!"

# 预测接口
@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        # 获取 JSON 数据
        data = request.get_json()

        # 调用 bead_prediction 中的预测函数
        predictions = predict(data)
        
        # 返回预测结果
        return jsonify({"predictions": predictions})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 主程序入口（仅本地测试时用，Azure 会自动调用）
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
