
import os
import datetime

def modify_conditions():
    # 조건 예시: 단순 주석 추가 (실제로는 전략 조건 코드 자동 수정 영역)
    with open("nekito_multi_trade_bot.py", "a") as f:
        f.write(f"\n# ✅ 조건 자동 완화: {datetime.datetime.now()}\n")

def auto_commit_push():
    os.system("git config --global user.name 'nekito-bot'")
    os.system("git config --global user.email 'bot@nekito.com'")
    os.system("git add nekito_multi_trade_bot.py")
    os.system("git commit -m '🔁 조건 자동 완화 커밋' || echo 'No changes'")
    os.system("git push origin main")

if __name__ == "__main__":
    modify_conditions()
    auto_commit_push()
