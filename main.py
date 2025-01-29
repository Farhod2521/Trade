from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import uvicorn
from metatrade5 import get_account_balance, get_trade_history, get_open_positions

app = FastAPI()

# Broker hisoblari (o'zingizning ma'lumotlaringizni qo'shing)
accounts = [
    {"name": "Farhod","login": 313223347, "password": "Farhod_2521", "server": "XMGlobal-MT5 7"},
    {"name": "Islom","login": 98893254, "password": "Farhod_2521", "server": "XMGlobal-MT5 5"},
    {"name": "Sardor","login": 313026727, "password": "Farhod_2521", "server": "XMGlobal-MT5 7"},
]

@app.get("/balances")
async def get_balances():
    balances = []
    for account in accounts:
        balance = get_account_balance(account["login"], account["password"], account["server"])
        balances.append({
            "name": account["name"],  # Ismni ham qaytaramiz
            "login": account["login"],
            "balance": balance
        })
    return balances
@app.get("/open-positions")
def open_positions(login: int):
    # Loginni hisoblash, va tegishli hisobni olish
    account = next((acc for acc in accounts if acc["login"] == login), None)
    if account:
        return get_open_positions(account["login"], account["password"], account["server"])
    else:
        return {"error": "Account not found!"}

@app.get("/trade-history")
async def trade_history(login: int = Query(...)):
    # Loginni hisoblash, va tegishli hisobni olish
    account = next((acc for acc in accounts if acc["login"] == login), None)
    if account:
        return get_trade_history(account["login"], account["password"], account["server"])
    else:
        return {"error": "Account not found!"}

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    with open("index.html", "r") as file:
        return file.read()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
