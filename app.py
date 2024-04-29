from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.get_json()
    message = data['message']
    # Process the message here
    response = {
        'reply': f"You said: {message}"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)