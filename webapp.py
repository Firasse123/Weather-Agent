import os
import asyncio
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from llama_index.core.agent.workflow import AgentStream
from main import weather,get_agent
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def api_chat():
    body = request.get_json(silent=True) or {}
    message = body.get('message')
    if not message:
        return jsonify({'error': 'Missing `message` in JSON body'}), 400

    agent, ctx = get_agent()
    try:
        text = asyncio.run(weather(agent, message, ctx))
        return jsonify({'message': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
