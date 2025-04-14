
import pyupbit
import time
import requests

# 업비트 API 키 설정
ACCESS_KEY = "여기에_너의_ACCESS_KEY"
SECRET_KEY = "여기에_너의_SECRET_KEY"
upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)

# 텔레그램 설정 (옵션)
TELEGRAM_TOKEN = "여기에_텔레그램_봇_토큰"
TELEGRAM_CHAT_ID = "여기에_챗_ID"

def send_telegram(message):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"[텔레그램 오류] {e}")

def get_rsi(df, period=14):
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def get_stoch_k(df, period=14):
    low_min = df['low'].rolling(window=period).min()
    high_max = df['high'].rolling(window=period).max()
    return 100 * ((df['close'] - low_min) / (high_max - low_min))

symbols = [
    "KRW-BTC", "KRW-ETH", "KRW-USDT", "KRW-XRP", "KRW-BNB",
    "KRW-SOL", "KRW-USDC", "KRW-DOGE", "KRW-TRX", "KRW-ADA"
]

positions = {symbol: {"entry": None, "volume": None} for symbol in symbols}
buy_krw = 1000  # 종목당 매수 금액

print("🚀 Nekito 다중 종목 실전 자동매매 시작")
send_telegram("🚀 Nekito 다중 종목 자동매매 시작됨!")

while True:
    for symbol in symbols:
        try:
            df = pyupbit.get_ohlcv(symbol, interval="minute5", count=100)
            df['rsi'] = get_rsi(df)
            df['stoch_k'] = get_stoch_k(df)
            rsi = df['rsi'].iloc[-1]
            stoch_k = df['stoch_k'].iloc[-1]
            price = df['close'].iloc[-1]
            vol = df['volume'].iloc[-1]
            vol_avg = df['volume'].rolling(10).mean().iloc[-1]

            print(f"[{symbol}] RSI: {rsi:.1f}, Stoch: {stoch_k:.1f}, Price: {price}")

            # 매수 조건
            if positions[symbol]["entry"] is None and rsi < 35 and stoch_k < 20 and vol > vol_avg:
                order = upbit.buy_market_order(symbol, buy_krw)
                time.sleep(1)
                balance = upbit.get_balances()
                for b in balance:
                    if b['currency'] in symbol:
                        positions[symbol]["volume"] = float(b['balance'])
                        break
                positions[symbol]["entry"] = price
                msg = f"📈 [매수 체결] {symbol} 진입가: {price:.2f}"
                print(msg)
                send_telegram(msg)

            # 익절 조건
            if positions[symbol]["entry"] and price >= positions[symbol]["entry"] * 1.10:
                upbit.sell_market_order(symbol, positions[symbol]["volume"])
                msg = f"✅ [익절 매도] {symbol} 현재가: {price:.2f} / 수익률 +10%"
                print(msg)
                send_telegram(msg)
                positions[symbol] = {"entry": None, "volume": None}

            # 손절 조건
            if positions[symbol]["entry"] and price <= positions[symbol]["entry"] * 0.98:
                upbit.sell_market_order(symbol, positions[symbol]["volume"])
                msg = f"❌ [손절 매도] {symbol} 현재가: {price:.2f} / 손실률 -2%"
                print(msg)
                send_telegram(msg)
                positions[symbol] = {"entry": None, "volume": None}

        except Exception as e:
            print(f"[{symbol} 오류] {e}")
            send_telegram(f"[{symbol} 오류] {e}")
        time.sleep(1)

    time.sleep(60)
