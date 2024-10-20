import json
from flask import Flask, jsonify, request
from service.utils.api_query import get_ddgs_ai_result
from utils.db import add_user, get_all_users, create_tables, authenticate_user, start_conversation, add_message, get_conversation_history, get_conversation_ids_for_user, delete_table
import os
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

def convert_timestamps(messages):
    for item in messages:
        if 'timestamp' in item and isinstance(item['timestamp'], datetime):
            item['timestamp'] = item['timestamp'].isoformat()
    return sorted(messages, key=lambda message: message['timestamp'])

def get_all_conversation(user_id):
    conv_ids = get_conversation_ids_for_user(user_id)
    # add_message(2, "User","2nd message")
    conv_dict={}
    for conv_id in conv_ids:
        messages = get_conversation_history(conv_id)
        conv_dict[conv_id]= convert_timestamps(messages)
        print(conv_dict)
    return conv_dict


@app.route('/signin', methods=['POST'])
def sign_in():
    # Parse JSON request body
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(username,password)
    success, user_id = authenticate_user(username, password)
    print(success)
    if success:
        conversations= get_all_conversation(user_id)
        response = jsonify({'success': True, 'conversations': conversations, "user_id": user_id})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    

@app.route('/add_message', methods=['POST'])
def add_message_api():
    # Parse JSON request body
    data = request.get_json()
    message = data.get('message')
    conversation_id = data.get('conversationid')
    previous_conv = get_conversation_history(conversation_id)
    message_user_id = add_message(conversation_id, "User",message)
    response_to_input = get_ddgs_ai_result(message, previous_conv)
    message_bot_id = add_message(conversation_id, "AI",response_to_input)
    messages = get_conversation_history(conversation_id)
    if conversation_id and message_user_id and message_bot_id:
        print("conversation_id: ",messages)
        response = jsonify({'success': True, 'conversation': convert_timestamps(messages)})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    
@app.route('/start_conversation', methods=['POST'])
def start_conversation_api():
    # Parse JSON request body
    data = request.get_json()
    user_id = data.get('userid')
    conversation_id = start_conversation(user_id)
    if user_id and conversation_id:
        new_m = add_message(conversation_id, "AI", "Hi there, I am your Search Chatbot. Here to help you with any of your queries")
        conversations= get_all_conversation(user_id)
        response = jsonify({'success': True, 'conversations': conversations})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
#    delete_table("Messages")
#    delete_table("Conversations")
#    create_tables()
   app.run(port=5000)