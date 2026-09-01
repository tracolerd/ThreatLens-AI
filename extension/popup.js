document.addEventListener('DOMContentLoaded', async () => {
    const urlElement = document.getElementById('current-url');
    const scanBtn = document.getElementById('scan-btn');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const errorBox = document.getElementById('error-box');
    const errorMessage = document.getElementById('error-message');

    const threatScoreEl = document.getElementById('threat-score');
    const statusBadgeEl = document.getElementById('status-badge');
    const reasonsListEl = document.getElementById('reasons-list');

    let activeTabUrl = '';

    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (tab && tab.url) {
            activeTabUrl = tab.url;
            urlElement.textContent = activeTabUrl;

            if (activeTabUrl.startsWith('chrome://') || activeTabUrl.startsWith('edge://') || activeTabUrl.startsWith('about:')) {
                scanBtn.disabled = true;
                scanBtn.style.opacity = '0.5';
                urlElement.textContent = "Cannot scan internal browser pages.";
            }
        } else {
            urlElement.textContent = "Unable to fetch active URL.";
            scanBtn.disabled = true;
        }
    } catch (err) {
        urlElement.textContent = "Error reading active tab.";
        scanBtn.disabled = true;
    }

    scanBtn.addEventListener('click', async () => {
        if (!activeTabUrl) return;

        scanBtn.classList.add('hidden');
        loadingDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');
        errorBox.classList.add('hidden');

        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/scan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: activeTabUrl })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Server error occurred during scan.');
            }

            const data = await response.json();

            threatScoreEl.textContent = data.threat_score;
            statusBadgeEl.textContent = data.status;
            statusBadgeEl.className = `status-badge status-${data.status}`;

            reasonsListEl.innerHTML = '';
            data.reasons.forEach(reason => {
                const li = document.createElement('li');
                li.textContent = reason;
                reasonsListEl.appendChild(li);
            });

            loadingDiv.classList.add('hidden');
            resultsDiv.classList.remove('hidden');

        } catch (err) {
            loadingDiv.classList.add('hidden');
            scanBtn.classList.remove('hidden');
            errorMessage.textContent = err.message || 'Failed to connect to backend server.';
            errorBox.classList.remove('hidden');
        }
    });
});