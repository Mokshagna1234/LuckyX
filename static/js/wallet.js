document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('wallet-page')) return;

    loadWalletBalance();
    loadWalletHistory();
});

/* ---------------- WALLET BALANCE ---------------- */
function loadWalletBalance() {
    fetch('/wallet/balance/')
        .then(res => {
            if (!res.ok) throw new Error('Wallet API failed');
            return res.json();
        })
        .then(data => {
            document.getElementById('wallet-balance').innerText =
                data.wallet_balance.toFixed(2);
        })
        .catch(err => {
            console.error('WALLET ERROR:', err);
            document.getElementById('wallet-balance').innerText = '0.00';
        });
}

/* ---------------- TRANSACTIONS (TEMP DEMO) ---------------- */
function loadWalletHistory() {
    const list = document.getElementById('wallet-history');
    if (!list) return;

    // TEMP demo data (safe, backend-ready)
    const transactions = [
        { type: 'Credit', amount: 100, time: 'Today' },
        { type: 'Debit', amount: 10, time: 'Draw Entry' },
        { type: 'Credit', amount: 50, time: 'Yesterday' }
    ];

    list.innerHTML = '';

    transactions.forEach(tx => {
        const li = document.createElement('li');
        li.innerHTML = `
            <strong>${tx.type}</strong>
            <span>₹${tx.amount}</span>
            <small>${tx.time}</small>
        `;
        list.appendChild(li);
    });

    if (!transactions.length) {
        list.innerHTML = `<li>No transactions yet</li>`;
    }
}
