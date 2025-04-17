document.addEventListener('DOMContentLoaded', function () {
    const messageInput = document.querySelector('.message-input');
    const sendButton = document.querySelector('.send-button');
    const chatContainer = document.querySelector('.chat-container');
    const welcomeContainer = document.querySelector('.welcome-container');
    const exampleCards = document.querySelectorAll('.example-card');
    const resetButton = document.getElementById('resetChat');
    const newChatButton = document.querySelector('.new-chat');

    function addMessage(text, isUser) {
        welcomeContainer.style.display = 'none';
        chatContainer.style.display = 'flex';

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';

        const avatar = document.createElement('div');
        avatar.className = `avatar ${isUser ? 'user-avatar' : 'bot-avatar'}`;
        avatar.textContent = isUser ? 'U' : 'S';

        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.textContent = text;

        messageContent.appendChild(avatar);
        messageContent.appendChild(messageText);
        messageDiv.appendChild(messageContent);
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function sendMessage() {
        const text = messageInput.value.trim();
        if (text) {
            addMessage(text, true);
            messageInput.value = '';
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: text }),
                });
                const data = await response.json();
                addMessage(data.response, false);
            } catch (err) {
                addMessage('Oops! Something went wrong.', false);
            }
        }
    }

    sendButton.addEventListener('click', sendMessage);

    messageInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    exampleCards.forEach(card => {
        card.addEventListener('click', function () {
            const text = this.querySelector('.example-text').textContent;
            messageInput.value = text;
            sendMessage();
        });
    });

    function resetChat() {
        chatContainer.style.display = 'none';
        welcomeContainer.style.display = 'flex';
        while (chatContainer.children.length > 1) {
            chatContainer.removeChild(chatContainer.lastChild);
        }
    }

    resetButton.addEventListener('click', resetChat);
    newChatButton.addEventListener('click', resetChat);

    messageInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});
