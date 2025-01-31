const API_BASE_URL = "https://driven-boxer-partly.ngrok-free.app";  // Ngrok URL

async function fetchBots() {
    const response = await fetch(`${API_BASE_URL}/api/bots`);
    const bots = await response.json();
    const botList = document.getElementById('botList');
    botList.innerHTML = "";
    bots.forEach(bot => {
        const li = document.createElement('li');
        li.innerHTML = `${bot.name} - ${bot.status} 
            <button onclick="startBot(${bot.id})">Start</button>
            <button onclick="stopBot(${bot.id})">Stop</button>`;
        botList.appendChild(li);
    });
}

async function startBot(botId) {
    await fetch(`${API_BASE_URL}/api/start_bot/${botId}`, { method: 'POST' });
    fetchBots();
}

async function stopBot(botId) {
    await fetch(`${API_BASE_URL}/api/stop_bot/${botId}`, { method: 'POST' });
    fetchBots();
}
