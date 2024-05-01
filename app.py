# app.py
from flask import Flask, request, render_template_string, session, url_for
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# HTML template for the homepage
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #6AD6EA; /* Updated background color */
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        .chat-container {
            width: 100%;
            max-width: 60rem; 
            border-radius: 0.3rem;
            box-shadow: 0 0 1rem rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            height: 90vh;
            max-height: 60rem; /* equivalent to 600px */
        }
        .header {
            font-family: Arial, sans-serif;
            background-color: #002669; /* Updated background color */
            color: white;
            padding: 1rem;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
        }
        .avatar {
            height: 3rem;
            width: 3rem;
            border-radius: 50%;
            margin-right: 1rem;
        }
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            background: #f0f2f5;
        }
        .message {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            padding: 0.5rem;
            border-radius: 1rem;
            background-color: #fff;
            border: 1px solid #ccc;
        }
        .bot {
            color: #555;
        }
        .user {
            color: white; /* Updated text color */
            background-color: #004ACC; /* Updated background color */
            margin-left: auto; /* Align user messages to the right */
        }
        .footer {
            padding: 1rem;
            background: #eceff1;
        }
        form{
            display:flex;
            flex-wrap:wrap;
            gap:1rem;
        }
        input[type="text"] {
            flex: 1;
            min-width:12rem;
            padding: 0.5rem;
            border: 0.18rem solid #6AD6EA;
            border-radius: 0.2rem;
            margin-right: 1rem; /* Add some spacing */
            background: #fff; /* Set background color */
        }
        button {
            padding: 0.68rem 1.25rem;
            background-color: #004ACC;
            color: white;
            border: none;
            border-radius: 0.2rem;
            cursor: pointer;
        }
        button:hover {
            background-color: #002669;
        }
        .chat-heading{
            font-size: 1.5rem;
            padding-left:1rem;
            font-weight:300;
        }
        .img-heading{
            height: 3rem;
            width: 3rem;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <img class="img-heading" src="/static/bot-ava.png" alt="">
            <h1 class="chat-heading">Topper Advisor</h1>
        </div>
        <div class="messages" id="messages">
            {% for message in chat_history %}
                <div class="message {% if message.role == 'bot' %} bot {% else %} user {% endif %}">
                    <img src="{{ message.avatar }}" class="avatar">
                    <p>{{ message.content }}</p>
                </div>
            {% endfor %}
        </div>
        <div class="footer">
            <form action="/" method="post">
                <input type="text" id="input" name="input" placeholder="Ask me anything..." required>
                <button type="submit">Send</button>
            </form>
        </div>
    </div>
    <script>
        const messages = document.getElementById('messages');
        function updateScroll(){
            messages.scrollTop = messages.scrollHeight;
        }
        updateScroll();
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'chat_history' not in session:
        # Initialize chat history with a welcome message
        session['chat_history'] = [
            {'role': 'bot', 'content': "Hello, I'm Topper, your AI Academic Advisor. I'm here to make your elective selection exciting and tailored just for you!", 'avatar': url_for('static', filename='bot-ava.png')},
        ]

    if request.method == 'POST':
        user_input = request.form['input']
        # Example response, you should integrate with OpenAI or another service
        response = "That's really neat bud, I'm not quite set up to handle those types of questions yet. Come back after this coffee. "
        session['chat_history'].append({'role': 'user', 'content': user_input, 'avatar': url_for('static', filename='user-ava.png')})
        session['chat_history'].append({'role': 'bot', 'content': response, 'avatar': url_for('static', filename='bot-ava.png')})
        session.modified = True

    chat_history = session['chat_history']
    return render_template_string(HTML, chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)