from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "🎉 Minimal Flask API is working!"

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # 默认端口为5000，Azure会自动提供PORT环境变量
    app.run(host='0.0.0.0', port=port)
