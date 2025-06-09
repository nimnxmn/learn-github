import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crypto Radar Chart", layout="wide")
st.title("Crypto Radar Chart")

# เกณฑ์ที่ใช้เปรียบเทียบ
criteria = [
    "MCAP", "Volatility_Week", "Volatility_Month", "Volatility_Quarter",
    "Volatility_Year", "Volume", "Listed_Days", "FDV", "MVRV"
]

# ค่าต่ำสุด-สูงสุด สำหรับ normalize
min_max = {
    "MCAP": (1_000_000_000, 2_500_000_000_000),
    "Volatility_Week": (4, 40),
    "Volatility_Month": (10, 100),
    "Volatility_Quarter": (40, 200),
    "Volatility_Year": (100, 250),
    "Volume": (1_000_000_000, 50_000_000_000),
    "Listed_Days": (100, 5000),
    "FDV": (1_000_000_000, 2_500_000_000_000),
    "MVRV": (0.5, 3.0),
}

# ฟังก์ชัน Normalize (ปรับค่าให้อยู่ในช่วง 0-1)


def normalize(value, min_val, max_val):
    norm = (value - min_val) / (max_val - min_val)
    return norm


# Sidebar: รับข้อมูลจากผู้ใช้
st.sidebar.header("Crypto information")
num_assets = st.sidebar.number_input(
    "Number of crypto to compare", min_value=1, max_value=5, value=2)

assets = {}
for i in range(num_assets):
    st.sidebar.markdown(f"### 🔹 Number {i+1}")
    name = st.sidebar.text_input(
        f"Name of crypto number {i+1}", value=f"crypto {i+1}", key=f"name_{i}")
    values = {}
    for c in criteria:
        val = st.sidebar.number_input(
            f"{c} of {name}", min_value=0.0, step=10.0, format="%.1f", key=f"{c}_{i}")
        values[c] = val
    assets[name] = values

# สร้าง data และชื่อเหรียญ (normalize แล้ว)
data = []
names = []

for name, stats in assets.items():
    norm_values = []
    for c in criteria:
        val = stats[c]
        min_val, max_val = min_max[c]

        norm = normalize(val, min_val, max_val)
        norm_values.append(norm)
    data.append(norm_values)
    names.append(name)

# สร้างมุมของกราฟเรดาร์ (วงกลมแบ่งตามจำนวนเกณฑ์)
num_vars = len(criteria)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # เพิ่มจุดแรกซ้ำที่ท้าย list เพื่อปิดวงกลม

# สร้างกราฟและวาดเรดาร์ชาร์ต
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# วาดข้อมูลแต่ละเหรียญ
for i, d in enumerate(data):
    values = d + d[:1]  # ปิดลูปวงกลม
    ax.plot(angles, values, label=names[i])        # วาดเส้น
    ax.fill(angles, values, alpha=0.1)             # เติมสีพื้น

# ตั้งค่าการแสดงผล
plt.xticks(angles[:-1], criteria, fontsize=4)        # ชื่อแกน
plt.yticks([0.2, 0.5, 1.0], ["20%", "50%", "100%"], color="gray", size=7)
ax.set_title("Crypto Radar Comparison", size=7)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=7)
plt.tight_layout()

st.pyplot(fig)
