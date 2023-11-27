
document.addEventListener("DOMContentLoaded", function() {
    const chatMessages = document.getElementById("chat-messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    sendButton.addEventListener("click", function() {
        const userMessage = userInput.value;
        if (userMessage) {
            appendMessage("User", userMessage);
            userInput.value = "";

            // Simulate a response from the chatbot (replace with actual logic)
            setTimeout(() => {
                const botResponse = "This is a sample response from the chatbot.";
                appendMessage("Shopper", botResponse);
            }, 1000);
        }
    });

    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.className = sender === "User" ? "user-message" : "bot-message";
        messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatMessages.appendChild(messageDiv);

        // Scroll to the latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});