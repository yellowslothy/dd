import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("🧫 세균 키우기 + 죽는 시뮬레이터")

st.markdown("""
이 시뮬레이터는 세균이 자라는 조건과 죽는 조건을 함께 보여줍니다.  
온도, 영양분, 항생제 조건에 따라 세균이 증식하거나 사멸할 수 있습니다.
""")

temperature = st.slider("온도 (℃)", 0, 60, 37)
nutrients = st.slider("영양분 농도 (0=없음, 100=풍부)", 0, 100, 50)
antibiotic = st.selectbox("항생제 사용 여부", ["없음", "사용"])

def calculate_growth_rate(temp, nutrients, antibiotic):
    if temp < 10 or temp > 45:
        temp_effect = -0.5
    else:
        temp_effect = np.exp(-((temp - 37) ** 2) / 50)

    if nutrients < 20:
        nutrient_effect = 0.2
    else:
        nutrient_effect = nutrients / 100

    if antibiotic == "사용":
        antibiotic_effect = 0.3
    else:
        antibiotic_effect = 1.0

    growth_rate = (temp_effect * nutrient_effect * antibiotic_effect)
    return growth_rate

initial_bacteria = 100
hours = np.arange(0, 24, 1)
growth_rate = calculate_growth_rate(temperature, nutrients, antibiotic)
bacteria_count = initial_bacteria * np.exp(growth_rate * hours)
bacteria_count = np.clip(bacteria_count, 0, None)

st.subheader("📈 세균 수 변화 시뮬레이션")
st.write(f"계산된 성장률: `{growth_rate:.3f}`")

fig, ax = plt.subplots()
ax.plot(hours, bacteria_count, color="green" if growth_rate > 0 else "red")
ax.set_xlabel("시간 (시간)")
ax.set_ylabel("세균 수")
ax.set_title("시간에 따른 세균 수 변화")
st.pyplot(fig)

if growth_rate > 0.7:
    st.success("🔥 세균이 폭발적으로 자랍니다!")
elif growth_rate > 0.3:
    st.info("🧫 세균이 안정적으로 자라고 있어요.")
elif growth_rate > 0:
    st.warning("⚠️ 세균이 아주 느리게 자라고 있어요.")
elif growth_rate == 0:
    st.error("😐 세균 수가 유지되고 있습니다 (성장도 사멸도 없음).")
else:
    st.error("☠️ 세균이 죽고 있어요!")
