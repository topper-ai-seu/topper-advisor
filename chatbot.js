document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.chatbot-options button');
    buttons.forEach(function(button) {
      button.addEventListener('click', function(event) {
        sendMessageToServer(event.target.textContent);
      });
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
      // Handle the response data by updating the chatbot content
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }
  