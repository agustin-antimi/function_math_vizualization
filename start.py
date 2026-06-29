import streamlit as st

st.set_page_config(page_title="Function Math Vizualizer", page_icon="📐", layout="centered")

pg = st.navigation([
    st.Page("pages/welcome_page.py", title="Home", default=True),
    st.Page("pages/calculator_vizualizator.py", title="Derivative Calculator"),
])

pg.run()