# -*- coding: utf-8 -*-


# app.py
from flask import Flask, request, jsonify
from bead_prediction import process_and_predict, fetch_weather_data, prepare_data  # 导入预测函数

# 初始化 Flask 应用
app = Flask(__name__)

# 根路径，测试用
@app.route('/')
def home():
    return "🎉 Flask API is running!"

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
