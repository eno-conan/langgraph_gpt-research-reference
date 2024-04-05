from flask import Flask, jsonify, request
from backend.langgraph_agent import MasterAgent

backend_app = Flask(__name__)

@backend_app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "Running"}), 200

@backend_app.route('/generate_newspaper', methods=['POST'])
def generate_newspaper():
    # data = request.json
    # {"topics": ["Baseball","NPB","ORIX"], "layout": "layout_1.html"}
    data = {'topics': ['Baseball'], 'layout': 'layout_1.html'}
    master_agent = MasterAgent()
    # newspaper = master_agent.run(data["topics"])
    newspaper = master_agent.run(data["topics"], data["layout"])
    return jsonify({"path": newspaper}), 200

