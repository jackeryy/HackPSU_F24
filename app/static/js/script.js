document.getElementById('chat-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting normally

    var userInput = document.getElementById('chat-input').value;
    var chatContainer = document.getElementById('chat-container');

    // Display the user's message in the chat
    var userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('chat-message', 'user-message');
    userMessageDiv.textContent = userInput;
    chatContainer.appendChild(userMessageDiv);

    // Send user input to the AI route
    fetch('/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        var botMessageDiv = document.createElement('div');
        botMessageDiv.classList.add('chat-message', 'bot-message');
        botMessageDiv.textContent = data.response;
        chatContainer.appendChild(botMessageDiv);

        // Scroll to the bottom of the chat
        chatContainer.scrollTop = chatContainer.scrollHeight;
    });

    // Clear the input field after submission
    document.getElementById('chat-input').value = '';
});
