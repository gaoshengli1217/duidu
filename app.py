from flask import Flask, send_from_directory, request, jsonify
import requests
import os

app = Flask(__name__, static_folder='.')

# 通义千问 API 配置
QWEN_API_KEY = 'sk-460aa8cd88764268bd0a42d2ac756df2'
QWEN_API_URL = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/qwen', methods=['POST'])
def qwen_proxy():
    try:
        data = request.json
        request_body = data.get('requestBody', {})
        
        # 调用通义千问 API
        headers = {
            'Authorization': f'Bearer {QWEN_API_KEY}',
            'Content-Type': 'application/json',
            'X-DashScope-SSE': 'disable'
        }
        
        response = requests.post(QWEN_API_URL, json=request_body, headers=headers)
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'data': response.json()
            })
        else:
            return jsonify({
                'success': False,
                'error': f'API调用失败: {response.status_code}'
            }), response.status_code
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
