import streamlit as st
import pandas as pd

st.title("คาดการณ์รายได้และกำไรจากการขายทุเรียน by Nim")

st.write("### ข้อมูลที่คาดการณ์")
col1, col2 = st.columns(2)
price = col1.number_input(
    "ราคาทุเรียนเฉลี่ยต่อกิโลกรัม(บาท)", min_value=0, value=100)
amount = col1.number_input("จำนวนทุเรียน(ลูก)", min_value=0, value=1000)
cost = col2.number_input("ต้นทุน(%)", min_value=0, value=30)
weight = col2.number_input(
    "น้ำหนักทุเรียนโดยเฉลี่ยต่อลูก(กิโลกรัม)", min_value=1, value=3)

# Calculate the earning and profit.
earning = price * amount * weight
profit = earning * (1 - cost / 100)

st.write("### ยินดีด้วย! คุณจะขายทุเรียนได้")
col1, col2 = st.columns(2)
col1.metric(label="รายได้ทั้งหมด", value=f"{earning} บาท")
st.write("แต่เสียใจด้วย รายได้ทั้งหมดเป็นของแม่")
col2.metric(label="กำไรทั้งหมด", value=f"{profit} บาท")
