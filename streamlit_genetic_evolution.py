
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Nekito 자동매매 진화 시스템", layout="wide")

st.title("📈 넥키토 유전 알고리즘 전략 진화")
st.markdown("이 페이지는 자동매매 전략을 유전 알고리즘으로 진화시키는 시스템입니다.")

if st.button("전략 시작"):
    st.success("전략 테스트 시작됨")
    result = np.random.rand(10)
    st.line_chart(result)
