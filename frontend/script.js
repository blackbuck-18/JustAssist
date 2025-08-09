document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const backendUrl = 'http://127.0.0.1:8000/chat';

    const sendMessage = () => {
        const text = userInput.value.trim();
        if (text === '') return;

        displayMessage(text, 'user-message');
        userInput.value = '';

        fetch(backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data && data.response) {
                displayMessage(data.response, 'bot-message');
            } else {
                throw new Error("Invalid response format from server");
            }
        })
        .catch(error => {
            console.error('Error connecting to the backend:', error);
            displayMessage('Sorry, there was an error processing your request.', 'bot-message');
        });
    };

    const displayMessage = (text, className) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', className);
        
        const p = document.createElement('p');
        p.textContent = text;
        messageElement.appendChild(p);
        
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    if (sendBtn && userInput && chatBox) {
        sendBtn.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
});