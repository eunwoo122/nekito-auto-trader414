import logging
import pyupbit
import time
import requests

# 넥키토 실전매매 봇 시작 로깅
logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")
logging.info("🚀넥키토 자동매매 보스 시작됨")

# 실전 체결 여부 설정
real_trade = True

# 업브피트 API 키 설정
ACCESS_KEY = "Fg3A6HBOaPMdMCCCtHS69PJRd2q0xJelalNS0XbyCw"
SECRET_KEY = "7N6QLHJ5AxEXZq0a30buaJznG9Pf3bzrXz3VOAE9x"
upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)

# 텔레그램 설정
TELEGRAM_TOKEN = "7733325333:AABQZQ-KZ0FiNJi6pL87yJ8cCQfLIOYtvhw"
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

symbols = ["KRW-BTC", "KRW-ETH", "KRW-SOL"]
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
                logging.info(f"✅매수 시도: {symbol} - 금액: {amount}원")
                send_telegram(f"✅매수 시도: {symbol} - [{amount}]원")
                if real_trade:
                    upbit.buy_market_order(symbol, amount)
                else:
                    logging.info("[SIMULATION] 실전 체결 모드 OFF - 주문 실행 안 된")

        except Exception as e:
            logging.info(f"❗예외 발생: {e}")
            send_telegram(f"❗예외 발생: {e}")
    time.sleep(60)


# === 조건 자동 진화 결과 (2025-04-15 07:24:11.058010) ===
# 수익률: 2.998, 조건: {'rsi': 17, 'macd_signal': 1.6487440330641685, 'bollinger_width': 0.12198122572141032, 'cci': -89, 'stoch_k': 73, 'volume_mult': 1.01761925012111}
# 수익률: 2.995, 조건: {'rsi': 14, 'macd_signal': 0.8641286640013124, 'bollinger_width': 0.04117633218021087, 'cci': 33, 'stoch_k': 37, 'volume_mult': 1.52060779913698}
# 수익률: 2.992, 조건: {'rsi': 10, 'macd_signal': 0.5683570991044045, 'bollinger_width': 0.13078724708153489, 'cci': -150, 'stoch_k': 82, 'volume_mult': 1.2347730873646854}
