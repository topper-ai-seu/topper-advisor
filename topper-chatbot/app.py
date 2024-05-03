import os
from flask import Flask, request, session, url_for, render_template
from dotenv import load_dotenv
from openai import OpenAI

print("\r\nIn program...\r\n")

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

print("\r\nCreating client...\r\n")


# Instantiate the OpenAI client
connection = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Define the default route to return the index.html file
@app.route("/")
def index():
    print("\r\nIn index()...\r\n")
    if 'chat_history' not in session:
        session['chat_history'] = [
            {'role': 'bot', 'content': "Hello, I'm Topper, your AI Academic Advisor. I'm here to make your elective selection exciting and tailored just for you!", 'avatar': url_for('static', filename='bot-ava.png')}
        ]
    chat_history = session['chat_history']
    return render_template("index.html", chat_history=chat_history)

# # Define the /api route to handle POST requests
# @app.route("/api", methods=["POST"])
# def api():
#     print("\r\nIn api()...\r\n")
#     message = request.json.get("message")
#     print('Submitting request:' + request)
#     try:
#         completion = client.Completion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": message}]
#         )
#         print('Completion: ' + completion)
#         response_text = completion.choices[0].text if completion.choices else "Failed to generate response!"
#     except Exception as e:
#         response_text = f"An error occurred: {str(e)}"

#     return response_text

@app.route('/', methods=['GET', 'POST'])
def home():
    print("\r\nIn home()...\r\n")
    if request.method == 'POST':
        user_input = request.form['input']
        print('Submitting request:' + user_input)
        try:
            completion = connection.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            print('Completion recieved: ' + str(completion))
            if completion.choices:
                response = completion.choices[0].message.content
            else:
                response = "Sorry, I couldn't generate a response. Please try again."
        except Exception as e:
            response = f"An error occurred: {str(e)}"

        session['chat_history'].append({'role': 'user', 'content': user_input, 'avatar': url_for('static', filename='user-ava.png')})
        session['chat_history'].append({'role': 'bot', 'content': response, 'avatar': url_for('static', filename='bot-ava.png')})
        session.modified = True

    chat_history = session['chat_history']
    return render_template("index.html", chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


