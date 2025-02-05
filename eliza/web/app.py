"""
Web application for the ELIZA chatbot.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from datetime import datetime
import json
import os
from pathlib import Path
from ..core.chatbot import Eliza

app = Flask(__name__)
socketio = SocketIO(app)
eliza = Eliza()

# Ensure the static and templates directories exist
STATIC_DIR = Path(__file__).parent / 'static'
TEMPLATES_DIR = Path(__file__).parent / 'templates'
STATIC_DIR.mkdir(parents=True, exist_ok=True)
(STATIC_DIR / 'css').mkdir(exist_ok=True)
(STATIC_DIR / 'js').mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/')
def home():
    """Render the main chat interface."""
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Error rendering template: {e}")
        return "Error loading the chat interface", 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('static', filename)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if user_message.lower() in ['quit', 'exit', 'bye']:
            return jsonify({
                'response': 'Goodbye! Take care of yourself.',
                'timestamp': datetime.now().isoformat()
            })
        
        response = eliza.respond(user_message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            'error': 'An error occurred processing your message',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/save-session', methods=['POST'])
def save_session():
    """Save the current chat session."""
    try:
        data = request.json
        session_data = data.get('session', [])
        
        with open('eliza_session.json', 'w') as f:
            json.dump(session_data, f, indent=2)
        
        return jsonify({'status': 'success'})
    except Exception as e:
        app.logger.error(f"Error saving session: {e}")
        return jsonify({'error': 'Failed to save session'}), 500

def main():
    """Main entry point for the web application."""
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    main()
