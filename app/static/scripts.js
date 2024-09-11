var ws;
var clientName;
var client_id = Date.now();

function getCurrentDateTime() {
    var now = new Date();
    return now.toLocaleString();
}

function scrollToBottom() {
    var messages = document.getElementById('messages');
    messages.scrollTop = messages.scrollHeight;  // Faz a rolagem até o fim
}

function storeName() {
    var currentTime = getCurrentDateTime();
    clientName = document.getElementById("clientName").value;
    if (!clientName) {
        alert("Por favor, digite seu nome!");
        return;
    }

    document.getElementById("ws-id").textContent = client_id;
    document.getElementById("ws-name").textContent = clientName;

    ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);

    ws.onopen = function() {
        ws.send(JSON.stringify({ type: 'name', client_id: client_id, name: clientName, timestamp: currentTime }));
    };

    ws.onmessage = function(event) {
        var messages = document.getElementById('messages');
        var message = document.createElement('li');
        var content = document.createTextNode(event.data);
        message.appendChild(content);
        messages.appendChild(message);
        scrollToBottom();
    };

    document.getElementById("chatContainer").style.display = "block";
}

function sendMessage(event) {
    var input = document.getElementById("messageText");
    var currentTime = getCurrentDateTime();

    ws.send(JSON.stringify({
        type: 'message',
        message: input.value,
        timestamp: currentTime
    }));
    input.value = '';
    event.preventDefault();
}

