const clickBtn = document.getElementById("clickBtn");
const watchAdBtn = document.getElementById("watchAdBtn");
const balanceDisplay = document.getElementById("balance");

let balance = 0;
const userId = window.Telegram.WebApp.initDataUnsafe.user?.id || Math.floor(Math.random() * 10000);

async function updateBalance() {
    balanceDisplay.textContent = `Баланс: ${balance} монет`;
}

async function sendClick() {
    const response = await fetch("http://localhost:8000/click", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId }),
    });
    const data = await response.json();
    balance = data.balance;
    updateBalance();
}

async function watchAd() {
    // В реальном приложении здесь будет вызов рекламы
    alert("Реклама показана! +10 монет");
    const response = await fetch("http://localhost:8000/watch_ad", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId }),
    });
    const data = await response.json();
    balance = data.balance;
    updateBalance();
}

clickBtn.addEventListener("click", sendClick);
watchAdBtn.addEventListener("click", watchAd);

updateBalance();