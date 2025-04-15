import os
import random
import datetime

def generate_strategies(n=1000):
    strategies = []
    for _ in range(n):
        strategy = {
            "rsi": random.randint(10, 30),
            "macd_signal": random.uniform(0.5, 2.5),
            "bollinger_width": random.uniform(0.01, 0.2),
            "cci": random.randint(-150, 150),
            "stoch_k": random.randint(10, 90),
            "volume_mult": random.uniform(0.5, 2.0),
        }
        strategies.append(strategy)
    return strategies

def simulate_backtest(strategy):
    # 랜덤 수익률 시뮬레이션
    return {
        "strategy": strategy,
        "profit_ratio": round(random.uniform(-0.5, 3.0), 3),  # -50% ~ +300%
        "trades": random.randint(5, 50)
    }

def backtest_all(strategies):
    return [simulate_backtest(s) for s in strategies]

def select_top(results, top_n=3):
    sorted_results = sorted(results, key=lambda x: x['profit_ratio'], reverse=True)
    return sorted_results[:top_n]

def update_bot_file(top_strategies, filename="nekito_multi_trade_bot.py"):
    with open(filename, "a") as f:
        f.write(f"\n# === 조건 자동 진화 결과 ({datetime.datetime.now()}) ===\n")
        for s in top_strategies:
            f.write(f"# 수익률: {s['profit_ratio']}, 조건: {s['strategy']}\n")

def auto_commit_push():
    os.system("git config --global user.name 'nekito-bot'")
    os.system("git config --global user.email 'bot@nekito.com'")
    os.system("git add nekito_multi_trade_bot.py")
    os.system("git commit -m '🚀 조건 자동 진화 결과 반영' || echo 'No changes'")
    os.system("git push origin main")

if __name__ == "__main__":
    strategies = generate_strategies(1000)
    results = backtest_all(strategies)
    top = select_top(results, top_n=3)
    update_bot_file(top)
    auto_commit_push()
