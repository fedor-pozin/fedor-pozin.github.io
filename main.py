from fastapi import FastAPI, Request
import sqlite3
import uvicorn

app = FastAPI()

# Подключаем базу данных
conn = sqlite3.connect('clicker.db', check_same_thread=False)
cursor = conn.cursor()

# Создаем таблицу пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0,
    last_ad_watch TIMESTAMP
)
''')
conn.commit()


@app.post("/click")
async def handle_click(request: Request):
    data = await request.json()
    user_id = data["user_id"]

    # Увеличиваем баланс на 1 за клик
    cursor.execute("INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, 0)", (user_id,))
    cursor.execute("UPDATE users SET balance = balance + 1 WHERE user_id = ?", (user_id,))
    conn.commit()

    return {"balance": cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]}


from fastapi import HTTPException  # Добавьте в импорты


@app.post("/watch_ad")
async def watch_ad(request: Request):
    try:
        data = await request.json()
        user_id = data.get("user_id")  # Используем .get() вместо []

        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")

        cursor.execute("INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, 0)", (user_id,))
        cursor.execute("UPDATE users SET balance = balance + 10 WHERE user_id = ?", (user_id,))
        conn.commit()

        balance = cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        return {"balance": balance}

    except Exception as e:
        print("Error:", e)  # Логируем ошибку
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)