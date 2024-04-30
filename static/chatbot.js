document.addEventListener('DOMContentLoaded', function() {
  const buttons = document.querySelectorAll('.chatbot-options button');
  const responseDisplay = document.querySelector('.chatbot-response'); // Assuming this is the class of your response display element

  buttons.forEach(function(button) {
    button.addEventListener('click', function(event) {
      sendMessageToServer(event.target.textContent);
    });
  });

  function sendMessageToServer(message) {
    fetch('/process_message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // Update the chatbot content with the reply from the server
      if(responseDisplay) {
        responseDisplay.textContent = data.reply; // Make sure the server sends back a JSON object with a 'reply' key
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      if(responseDisplay) {
        responseDisplay.textContent = 'An error occurred while processing your message.';
      }
    });
  }
});

  