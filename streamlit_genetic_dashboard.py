import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Nekito Genetic Dashboard", layout="wide")
st.title("🧠 넥키토 자동 전략 시각화")

# 사이드바 조건 입력
rsi_min = st.sidebar.slider("RSI 매수 기준 (이하)", 5, 50, 30)
stoch_min = st.sidebar.slider("Stochastic 매수 기준 (이하)", 5, 50, 20)
boll_width = st.sidebar.slider("볼린저밴드 폭 기준", 1.0, 5.0, 2.0)

# 샘플 백테스트 함수
def run_backtest(rsi, stoch, boll):
    np.random.seed(42)
    data = {
        "strategy_id": range(1, 21),
        "rsi": np.random.randint(10, 50, 20),
        "stoch": np.random.randint(5, 50, 20),
        "boll": np.random.uniform(1.5, 4.5, 20),
        "profit": np.random.normal(loc=5, scale=10, size=20),
        "trades": np.random.randint(5, 100, 20),
    }
    df = pd.DataFrame(data)
    filtered = df[(df["rsi"] <= rsi) & (df["stoch"] <= stoch) & (df["boll"] <= boll)]
    return filtered

# 실행 버튼
if st.button("📊 전략 백테스트 실행"):
    result = run_backtest(rsi_min, stoch_min, boll_width)

    if result.empty:
        st.warning("조건을 만족하는 전략이 없습니다.")
    else:
        st.success(f"{len(result)}개 전략 조건 발견됨")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 수익률 히스토그램")
            st.bar_chart(result["profit"])

        with col2:
            st.subheader("📊 거래 수 분포")
            st.bar_chart(result["trades"])

        st.subheader("🧾 전략 조건 요약")
        st.dataframe(result)
