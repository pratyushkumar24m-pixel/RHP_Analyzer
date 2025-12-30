import matplotlib.pyplot as plt
import streamlit as st

def trend_chart(label, years, values):
    fig, ax = plt.subplots()
    ax.plot(years, values, marker="o", linewidth=2)
    ax.set_title(label)
    ax.set_xlabel("Year")
    ax.set_ylabel("Amount (₹ Cr)")
    ax.grid(True)
    st.pyplot(fig)
