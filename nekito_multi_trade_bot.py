import logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info("✅ 넥키토 자동매매 봇 시작됨")

import pyupbit
import time
import requests

# 업비트 API 키 설정
ACCESS_KEY = "Fg3A6HBQaP4bMQCCCHS69PJRd2q0xJe1aNS0XbyC"
SECRET_KEY = "7N6QLHJ5AxEXzQa30buajZnG9F3bsrZx3VQAE9x"
upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)

# 텔레그램 설정 (선택)
TELEGRAM_TOKEN = "7733325333:AAEQzQX-kZQFiNJi6pL87YJ8cCQtIOYtvhw"
TELEGRAM_CHAT_ID = "8115626217"

def send_telegram(message):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"텔레그램 오류: {e}")

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
    return (df['close'] - low_min) / (high_max - low_min) * 100

symbols = ["KRW-BTC", "KRW-ETH", "KRW-SOL"]  # 감시 종목
amount = 5000

while True:
    for symbol in symbols:
        try:
            df = pyupbit.get_ohlcv(symbol, interval="minute1", count=20)
            rsi = get_rsi(df).iloc[-1]
            stoch = get_stoch_k(df).iloc[-1]
            price = df['close'].iloc[-1]

            logging.info(f"[{symbol}] RSI: {rsi:.1f}, Stoch: {stoch:.1f}, Price: {price}")

            if rsi < 30 and stoch < 20:
                logging.info(f"📈 매수 시도: {symbol} - 금액: {amount}원")
                send_telegram(f"📈 매수 시도: {symbol} - {amount}원")
                # 실전 매수
                upbit.buy_market_order(symbol, amount)

        except Exception as e:
            logging.info(f"❗ 예외 발생: {e}")
            send_telegram(f"❗ 예외 발생: {e}")
    time.sleep(60)

# ✅ 조건 자동 완화: 2025-04-15 03:03:18.765890
