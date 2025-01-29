import MetaTrader5 as mt5
from datetime import datetime

def get_account_balance(login, password, server):
    if not mt5.initialize(login=login, password=password, server=server):
        print(f"MT5 initialize failed for account {login}")
        return None

    account_info = mt5.account_info()
    if account_info is None:
        print(f"Failed to get account info for {login}")
        mt5.shutdown()
        return None

    balance = account_info.balance
    mt5.shutdown()
    return balance

def get_open_positions(login, password, server):
    print(f"📢 Ulanish MT5 hisobiga: {login}")

    # MT5 ga yangi login bilan ulanish
    if not mt5.initialize(login=login, password=password, server=server):
        print(f"❌ MT5 initialize ishlamadi! Hisob {login} uchun.")
        return []

    positions = mt5.positions_get()
    
    if positions is None or len(positions) == 0:
        print("❌ Ochiq bitimlar topilmadi!")
        error = mt5.last_error()
        print(f"⚠️ MT5 Xato kodi: {error}")
        mt5.shutdown()
        return []

    trades = []
    for position in positions:
        trades.append({
            "order": position.ticket,
            "symbol": position.symbol,
            "lots": position.volume,
            "price": position.price_open,
            "profit": position.profit,
            "time": datetime.fromtimestamp(position.time).strftime('%Y-%m-%d %H:%M:%S')
        })
    
    mt5.shutdown()
    return trades

def get_trade_history(login, password, server):
    print(f"📢 Ulanish MT5 hisobiga: {login}")

    if not mt5.initialize(login=login, password=password, server=server):
        print(f"❌ MT5 initialize ishlamadi! Hisob {login} uchun.")
        return []

    # ✅ 2025-01-01 dan hozirgacha
    start = datetime(2025, 1, 1)
    end = datetime.now()

    print(f"📢 Tarix so‘rovi: {start} dan {end} gacha")

    history = mt5.history_deals_get(start, end)
    
    if history is None:
        print("❌ `history_deals_get` bo‘sh natija qaytardi!")
        mt5.shutdown()
        return []
    
    print(f"✅ {len(history)} ta savdo tarixi topildi!")

    trades = []
    for deal in history:
        if deal.ticket > 0:  # Xato yoki bekor qilingan savdolarni chiqarib tashlash
            trades.append({
                "order": deal.ticket,
                "symbol": deal.symbol,
                "lots": deal.volume,
                "price": deal.price,
                "profit": deal.profit,
                "time": datetime.fromtimestamp(deal.time).strftime('%Y-%m-%d %H:%M:%S')  # Savdo vaqti
            })
    
    mt5.shutdown()
    return trades
