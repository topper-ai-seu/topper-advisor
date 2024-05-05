import os
import time
from flask import Flask, request, render_template, session, url_for
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

print("\r\nIn program...\r\n")

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
organization = os.getenv("organization")

print("\r\nCreating open ai client...\r\n")

# Initialize OpenAI client
try:
    client = OpenAI(api_key=api_key, organization=organization)
except OpenAIError as e:
    app.logger.error(f"Failed to initialize OpenAI client: {e}")
    raise

# Define the default route to return the index.html file
@app.route("/")
def index():
    print('In index(), sesssion = ' + str(session))
    if 'chat_history' not in session:
        session['chat_history'] = [
            {'role': 'bot', 'content': "Hello, I'm Topper, your AI Academic Advisor. I'm here to make your elective selection exciting and tailored just for you!", 'avatar': url_for('static', filename='bot-ava.png')}
        ]
    chat_history = session['chat_history']
    return render_template("index.html", chat_history=chat_history)


@app.route('/find_classes', methods=['GET', 'POST'])
def find_classes():
    if request.method == 'POST':
        print("\r\nIn find_classes()...\r\n")
        try:
            # Create a new thread
            thread = client.beta.threads.create()
            print("Thread ID:", thread.id)
        
            # retrieve user input from client submitted form.
            user_input = request.form.get('input', 'Default qestion')
            
            print('Submitting request:' + user_input)
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input
            )

            # Create a run using the new assistant ID
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id
            )

            # Wait for the run to complete and fetch its status
            run = wait_on_run(run, thread)
            print("Run status:", run.status)

            # Retrieve all the messages after the run is completed
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            print('messages = ' + str(messages))
            response_messages = [msg.content[0].text.value for msg in messages.data if msg.role == 'assistant']
            print('response_messages = ' + str(response_messages))
            
            session['chat_history'].append({'role': 'user', 'content': user_input, 'avatar': url_for('static', filename='user-ava.png')})
            session['chat_history'].append({'role': 'bot', 'content': response_messages[0], 'avatar': url_for('static', filename='bot-ava.png')})
            session.modified = True

            chat_history = session['chat_history']
            return render_template("index.html", chat_history=chat_history)
        except OpenAIError as e:
            app.logger.error(f"Error during processing: {e}")
            return str(e), 500
    else:
        # Just show the initial form when the page is accessed via GET
        return render_template("index.html", messages=[])

def wait_on_run(run, thread):
    while run.status in ["queued", "in_progress"]:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        time.sleep(0.5)
    return run

if __name__ == '__main__':
    app.run(debug=True, port=5000)