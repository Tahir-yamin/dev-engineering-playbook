
document.getElementById('run').addEventListener('click', async () => {
    const status = document.getElementById('status');
    status.style.display = 'block';
    status.textContent = 'Injecting...';
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: ['content.js'],
            world: 'MAIN'
        });
        status.textContent = 'Running...';
        status.className = 'success';
    } catch (e) {
        status.textContent = 'Err: ' + e.message;
    }
});
