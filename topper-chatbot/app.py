import os
from flask import Flask, request, session, url_for, render_template
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Instantiate the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    message = request.json.get("message")
    try:
        completion = client.Completion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        response_text = completion.choices[0].text if completion.choices else "Failed to generate response!"
    except Exception as e:
        response_text = f"An error occurred: {str(e)}"

    return response_text

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'chat_history' not in session:
        session['chat_history'] = [
            {'role': 'bot', 'content': "Hello, I'm Topper, your AI Academic Advisor. I'm here to make your elective selection exciting and tailored just for you!", 'avatar': url_for('static', filename='bot-ava.png')}
        ]

    if request.method == 'POST':
        user_input = request.form['input']
        try:
            completion = client.Completion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            response = completion.choices[0].text if completion.choices else "Sorry, I couldn't generate a response. Please try again."
        except Exception as e:
            response = f"An error occurred: {str(e)}"

        session['chat_history'].append({'role': 'user', 'content': user_input, 'avatar': url_for('static', filename='user-ava.png')})
        session['chat_history'].append({'role': 'bot', 'content': response, 'avatar': url_for('static', filename='bot-ava.png')})
        session.modified = True

    chat_history = session['chat_history']
    return render_template("index.html", chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


