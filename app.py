from flask import Flask, request, jsonify, render_template
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    # Render the HTML page
    return render_template('index.html')

@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.get_json()
    message = data['message']
    
    # Process the message here by sending it to OpenAI's API
    response = openai.Completion.create(
        engine="text-davinci-003",  # Specify the appropriate engine
        prompt=message,
        max_tokens=150
    )

    # Extracting the text from the response from OpenAI
    bot_response = response.choices[0].text.strip()
    
    # Sending back the response to the front end
    return jsonify({'reply': bot_response})

# The debug=True argument is helpful during development, but should be removed in production
if __name__ == '__main__':
    app.run(debug=True)
