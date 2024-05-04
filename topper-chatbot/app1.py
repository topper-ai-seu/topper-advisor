import os
import time
from flask import Flask, request, render_template
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
organization = os.getenv("organization")

# Initialize OpenAI client
try:
    client = OpenAI(api_key=api_key, organization=organization)
except OpenAIError as e:
    app.logger.error(f"Failed to initialize OpenAI client: {e}")
    raise

@app.route("/")
def index():
    return render_template("index.html", messages=[])

@app.route("/solve_quadratic", methods=["GET", "POST"])
def solve_quadratic():
    if request.method == "POST":
        try:
            # Create a new thread
            thread = client.beta.threads.create()
            print("Thread ID:", thread.id)

            # Adding a user message to the thread
            user_content = request.form.get('input', 'Default question')
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_content
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
            response_messages = [msg.content[0].text.value for msg in messages.data if msg.role == 'assistant']
            return render_template("index.html", messages=response_messages)

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

if __name__ == "__main__":
    app.run(debug=True)