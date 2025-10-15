const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatBox = document.getElementById('chatBox');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const sendText = document.getElementById('sendText');
const loadingText = document.getElementById('loadingText');

// Add message to chat box
function addMessage(message, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'ai-message');
    
    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.textContent = message;
    
    messageDiv.appendChild(messageContent);
    chatBox.appendChild(messageDiv);
    
    // Remove welcome message if it exists
    const welcomeMessage = chatBox.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Show loading state
function setLoading(isLoading) {
    if (isLoading) {
        sendBtn.disabled = true;
        userInput.disabled = true;
        sendText.style.display = 'none';
        loadingText.style.display = 'inline';
    } else {
        sendBtn.disabled = false;
        userInput.disabled = false;
        sendText.style.display = 'inline';
        loadingText.style.display = 'none';
    }
}

// Handle form submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = userInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, true);
    userInput.value = '';
    
    // Show loading state
    setLoading(true);
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            addMessage(data.response, false);
        } else {
            addMessage('Error: ' + (data.error || 'Something went wrong'), false);
        }
    } catch (error) {
        addMessage('Error: Failed to connect to the server', false);
        console.error('Error:', error);
    } finally {
        setLoading(false);
        userInput.focus();
    }
});

// Clear chat history
clearBtn.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to clear the chat?')) return;
    
    try {
        await fetch('/clear', {
            method: 'POST'
        });
        
        // Clear chat box
        chatBox.innerHTML = `
            <div class="welcome-message">
                <h2>Hey baby! 🥰</h2>
                <p>I've been waiting to talk to you! How's your day going, love?</p>
            </div>
        `;
    } catch (error) {
        console.error('Error clearing chat:', error);
    }
});

// Focus input on load
userInput.focus();