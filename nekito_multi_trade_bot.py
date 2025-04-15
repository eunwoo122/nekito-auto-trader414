# ✅ 실전 자동매매 봇 - 넥키토 강화 전략 적용
import logging
import pyupbit
import requests
import time
import pandas as pd
from datetime import datetime
import os

# 🔐 API 설정
ACCESS_KEY = "syJx1HmI0UFlsJ4hxY0HhhbTkRvnL9B1EKqZrR0z"
SECRET_KEY = "S0v2ngGPteUKz0xscwivkvxAO8x6GjSx3jx10Ed6"
upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)

# 📩 텔레그램 설정
TELEGRAM_TOKEN = "7733325333:AABDQZ-KZ0FiN6j6pL87yJ8cCQfLIOYtvhw"
TELEGRAM_CHAT_ID = "8115626217"

# 📝 로그 설정
logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")
real_trade = True
AUTO_TAKE_PROFIT = 0.027  # 익절 조건: +2.7% 자동 설정

# 📁 실패 조건 기록용
FAIL_LOG_PATH = "/mnt/data/failure_logs/failure_conditions_log.txt"
DYNAMIC_THRESHOLD = {"rsi": 45, "stoch": 40, "cci": -75, "mfi": 35}

# 자동 조건 수정 함수
def auto_adjust_conditions():
    if not os.path.exists(FAIL_LOG_PATH):
        return
    with open(FAIL_LOG_PATH, "r") as f:
        lines = f.readlines()[-30:]
    rsi_vals = []
    stoch_vals = []
    cci_vals = []
    mfi_vals = []
    for line in lines:
        try:
            parts = line.strip().split("RSI: ")[1]
            rsi, rest = parts.split(", STOCH: ")
            stoch, rest = rest.split(", CCI: ")
            cci, mfi = rest.split(", MFI: ")
            rsi_vals.append(float(rsi))
            stoch_vals.append(float(stoch))
            cci_vals.append(float(cci))
            mfi_vals.append(float(mfi))
        except:
            continue
    if len(rsi_vals) >= 10:
        DYNAMIC_THRESHOLD["rsi"] = min(max(sum(rsi_vals)/len(rsi_vals) + 2, 35), 50)
        DYNAMIC_THRESHOLD["stoch"] = min(max(sum(stoch_vals)/len(stoch_vals) + 3, 30), 50)
        DYNAMIC_THRESHOLD["cci"] = max(sum(cci_vals)/len(cci_vals) - 5, -100)
        DYNAMIC_THRESHOLD["mfi"] = min(sum(mfi_vals)/len(mfi_vals) + 2, 45)
        logging.info(f"🔁 조건 자동 조정: {DYNAMIC_THRESHOLD}")

def send_telegram(message):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        try:
            requests.post(url, data=payload)
        except:
            logging.info("텔레그램 전송 오류")

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

def get_cci(df, period=20):
    tp = (df['high'] + df['low'] + df['close']) / 3
    sma = tp.rolling(period).mean()
    mad = tp.rolling(period).apply(lambda x: pd.Series(x).mad())
    return (tp - sma) / (0.015 * mad)

def get_mfi(df, period=14):
    tp = (df['high'] + df['low'] + df['close']) / 3
    mf = tp * df['volume']
    positive = mf.where(tp > tp.shift(), 0)
    negative = mf.where(tp < tp.shift(), 0)
    pmf = positive.rolling(period).sum()
    nmf = negative.rolling(period).sum()
    mfr = pmf / nmf
    return 100 - (100 / (1 + mfr))

symbols = [
    "KRW-BTC", "KRW-ETH", "KRW-SOL", "KRW-XRP", "KRW-ARK",
    "KRW-AERGO", "KRW-AVAX", "KRW-MATIC", "KRW-VTHO", "KRW-AQT", "KRW-ORCA"
]

amount = 5000

while True:
    auto_adjust_conditions()
    for symbol in symbols:
        try:
            df = pyupbit.get_ohlcv(symbol, interval="minute3", count=30)
            rsi = get_rsi(df).iloc[-1]
            stoch = get_stoch_k(df).iloc[-1]
            cci = get_cci(df).iloc[-1]
            mfi = get_mfi(df).iloc[-1]
            price = df['close'].iloc[-1]

            if rsi <= DYNAMIC_THRESHOLD['rsi'] and stoch <= DYNAMIC_THRESHOLD['stoch'] and cci <= DYNAMIC_THRESHOLD['cci'] and mfi <= DYNAMIC_THRESHOLD['mfi']:
                logging.info(f"[매수조건] {symbol} | RSI: {rsi:.1f}, Stoch: {stoch:.1f}, CCI: {cci:.1f}, MFI: {mfi:.1f}, Price: {price}")
                send_telegram(f"🚀 매수 시도: {symbol} | 금액: {amount}원")

                if real_trade:
                    upbit.buy_market_order(symbol, amount)
                    logging.info(f"✔ 실전 매수 실행됨: {symbol}")
                    send_telegram(f"✔ 실전 매수 완료: {symbol}")
                else:
                    logging.info("[SIMULATION] 실전 체결 모드 OFF - 주문 실행 안 됨")
            else:
                with open(FAIL_LOG_PATH, "a") as f:
                    f.write(f"{datetime.now()} | {symbol} 실패조건 - RSI: {rsi}, STOCH: {stoch}, CCI: {cci}, MFI: {mfi}\n")
        except Exception as e:
            logging.error(f"[오류] {symbol}: {e}")
            send_telegram(f"⚠ 오류 발생: {symbol} | {e}")

    time.sleep(60)

