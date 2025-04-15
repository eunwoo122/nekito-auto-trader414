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

# ✅ 조건 자동 완화: 2025-04-15 03:14:13.667949

# ✅ 조건 자동 완화: 2025-04-15 03:17:57.212869

# === 조건 자동 진화 결과 (2025-04-15 03:29:18.941106) ===
# 수익률: 2.999, 조건: {'rsi': 30, 'macd_signal': 1.6957675980895155, 'bollinger_width': 0.17691588396627064, 'cci': 123, 'stoch_k': 87, 'volume_mult': 1.6265791029288947}
# 수익률: 2.994, 조건: {'rsi': 10, 'macd_signal': 2.4427395694357292, 'bollinger_width': 0.1466556866424163, 'cci': 59, 'stoch_k': 51, 'volume_mult': 1.5851618463877635}
# 수익률: 2.993, 조건: {'rsi': 26, 'macd_signal': 0.809095498225652, 'bollinger_width': 0.025437395957813774, 'cci': 93, 'stoch_k': 55, 'volume_mult': 1.8319381675660675}

# === 조건 자동 진화 결과 (2025-04-15 04:19:20.024103) ===
# 수익률: 2.999, 조건: {'rsi': 24, 'macd_signal': 1.7902570357058623, 'bollinger_width': 0.07583042267072937, 'cci': -143, 'stoch_k': 10, 'volume_mult': 1.3004258618954765}
# 수익률: 2.995, 조건: {'rsi': 14, 'macd_signal': 1.576796434293121, 'bollinger_width': 0.026911449830251982, 'cci': 117, 'stoch_k': 24, 'volume_mult': 1.1766317461312277}
# 수익률: 2.989, 조건: {'rsi': 28, 'macd_signal': 1.461293669864678, 'bollinger_width': 0.19580175933072227, 'cci': 53, 'stoch_k': 80, 'volume_mult': 1.60000521080164}

# === 조건 자동 진화 결과 (2025-04-15 04:23:18.593473) ===
# 수익률: 2.997, 조건: {'rsi': 15, 'macd_signal': 2.343231254540652, 'bollinger_width': 0.02125999825455132, 'cci': -97, 'stoch_k': 29, 'volume_mult': 0.8040609200023972}
# 수익률: 2.995, 조건: {'rsi': 26, 'macd_signal': 2.0808453088609933, 'bollinger_width': 0.04555639468478233, 'cci': 92, 'stoch_k': 73, 'volume_mult': 1.566212821735708}
# 수익률: 2.995, 조건: {'rsi': 29, 'macd_signal': 1.500450493275668, 'bollinger_width': 0.17902690602321591, 'cci': -137, 'stoch_k': 78, 'volume_mult': 1.6557721941394397}
