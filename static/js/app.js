let currentDrawId = null;
let timerInterval = null;

/* ---------------- CSRF ---------------- */
function getCSRFToken() {
    let cookieValue = null;
    document.cookie.split(';').forEach(cookie => {
        cookie = cookie.trim();
        if (cookie.startsWith('csrftoken=')) {
            cookieValue = cookie.substring('csrftoken='.length);
        }
    });
    return cookieValue;
}

/* ---------------- DRAW ---------------- */
function loadDraw() {
    if (!document.getElementById('home-page')) return;
    fetch('/draw/current/')
        .then(res => {
            if (!res.ok) throw new Error('Draw API failed');
            return res.json();
        })
        .then(draw => {
            console.log('DRAW DATA:', draw);
            console.log('END TIME:', draw.end_time);

            currentDrawId = draw.id;

            const total = 50;
            const left = total - draw.tickets_sold;

            document.getElementById('tickets-left').innerText = left;

            const percent = ((total - left) / total) * 100;
            document.getElementById('progress-fill').style.width = percent + '%';

            startTimer(draw.end_time);
        })
        .catch(err => {
            console.error('DRAW ERROR:', err);
        });
}



/* ---------------- TIMER (MM:SS) ---------------- */
function startTimer(endTime) {
    if (timerInterval) clearInterval(timerInterval);

    const minEl = document.getElementById('timer-min');
    const secEl = document.getElementById('timer-sec');

    timerInterval = setInterval(() => {
        const diff = new Date(endTime) - new Date();

        if (diff <= 0) {
            clearInterval(timerInterval);
            minEl.innerText = '00';
            secEl.innerText = '00';
            return;
        }

        const mins = Math.floor(diff / 60000);
        const secs = Math.floor((diff % 60000) / 1000);

        minEl.innerText = mins.toString().padStart(2, '0');
        secEl.innerText = secs.toString().padStart(2, '0');
    }, 1000);
}



/* ---------------- BUY ---------------- */
function joinDraw() {
    const tickets = document.getElementById('ticket-count').value;

    fetch(`/draw/join/${currentDrawId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ tickets })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('message').innerText =
            data.message || data.error;
    });
}

/* ---------------- LIVE WINNERS (SIMULATION) ---------------- */
const sampleWinners = [
    'JAC204', 'SAM918', 'RIT552', 'MAX777',
    'ALX301', 'NIK889', 'DEV432'
];

function addWinner() {
    const ul = document.getElementById('winners');
    if (!ul) return;

    const id = sampleWinners[Math.floor(Math.random() * sampleWinners.length)];

    const li = document.createElement('li');
    li.classList.add('winner-new');

    li.innerHTML = `
        <div class="winner-avatar">${id[0]}</div>
        <div class="winner-info">
            <div class="winner-id">${id}</div>
            <div class="winner-amount">Won ₹450</div>
        </div>
    `;

    ul.prepend(li);

    setTimeout(() => li.classList.remove('winner-new'), 1200);

    if (ul.children.length>3) {
        ul.removeChild(ul.lastChild);
    }
}

if (document.getElementById('home-page')) {

    /* Initial fake winners */
    for (let i = 0; i < 3; i++) addWinner();

    /* Add new winner every 60 seconds */
    setInterval(addWinner, 60000);
}

/* ---------------- MINI TIMER FOR DRAW CARDS ---------------- */
function startMiniTimer(card, endTime) {
    const minEl = card.querySelector('.timer-min');
    const secEl = card.querySelector('.timer-sec');

    if (!minEl || !secEl) return;

    setInterval(() => {
        const diff = new Date(endTime) - new Date();

        if (diff <= 0) {
            minEl.innerText = '00';
            secEl.innerText = '00';
            return;
        }

        const mins = Math.floor(diff / 60000);
        const secs = Math.floor((diff % 60000) / 1000);

        minEl.innerText = String(mins).padStart(2, '0');
        secEl.innerText = String(secs).padStart(2, '0');
    }, 1000);
}


function loadDrawQueue() {
    fetch('/draw/queue/')
        .then(res => {
            if (!res.ok) throw new Error('Queue API failed');
            return res.json();
        })
        .then(draws => {
            const container = document.getElementById('draw-list');
            if (!container) return;

            container.innerHTML = '';

            draws.forEach(draw => {
                const left = draw.total_tickets - draw.tickets_sold;
                const percent = Math.min(
                    (draw.tickets_sold / draw.total_tickets) * 100,
                    100
                );

                const card = document.createElement('div');
                card.className = 'lux-draw';

                card.innerHTML = `
                    <div class="lux-top">
                        <div>
                            <span class="lux-live ${draw.status.toLowerCase()}">
                                ${draw.status}
                            </span>
                            <div class="lux-prize">Win ₹${draw.prize}</div>
                        </div>
                        <div class="lux-timer">
                            <span class="timer-min">--</span>:<span class="timer-sec">--</span>
                        </div>
                    </div>

                    <div class="lux-progress-wrap">
                        <div class="lux-progress-bar">
                            <div class="lux-progress-fill" style="width:${percent}%"></div>
                        </div>
                        <div class="lux-progress-text">${left} tickets left</div>
                    </div>

                    <div class="lux-buy">
                          <div class="lux-price">₹${draw.ticket_price} <span>/ ticket</span></div>

                            <div class="lux-action">
                                     ${
                                        window.IS_AUTHENTICATED
                                                ? `<button>BUY NOW</button>`
                                                   : `<div class="lux-login-hint">Login to participate</div>`
                                                    }
                            </div>
                    </div>
                `;

                container.appendChild(card);
                startMiniTimer(card, draw.end_time);
            });
        })
        .catch(err => console.error('DRAW QUEUE ERROR:', err));
}

document.addEventListener('DOMContentLoaded', () => {

    /* DRAW PAGE */
    const drawList = document.getElementById('draw-list');
    if (drawList) {
        console.log('DRAW PAGE → loading queue');
        loadDrawQueue();
        return;
    }

    /* HOME PAGE */
    const ticketsLeft = document.getElementById('tickets-left');
    if (ticketsLeft) {
        console.log('HOME PAGE → loading single draw');
        loadDraw();
    }

});

