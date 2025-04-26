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
        # 直接调用 process_and_predict，不需要从请求中获取数据
        predictions = process_and_predict()  # 没有传递数据，只需要调用函数
        
        # 将 DataFrame 转换为 JSON 格式（可以根据需求进一步调整数据结构）
        predictions_json = predictions.to_dict(orient='records')  # 将 DataFrame 转换为列表的字典
        
        # 返回预测结果
        return jsonify({"predictions": predictions_json})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
        
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # 默认端口为5000，Azure会自动提供PORT环境变量
    app.run(host='0.0.0.0', port=port)
