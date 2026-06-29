import streamlit as st
import sys
sys.path.append("src")

from src.DerivateManager import DerivateManager

st.title("Function Math Visualizer")
st.markdown("A tool for computing and visualizing derivatives of mathematical functions.")

# --- Initialize DerivateManager in session_state ---
if "manager" not in st.session_state:
    st.session_state["manager"] = DerivateManager()

manager: DerivateManager = st.session_state["manager"]

# --- Display current variables ---
st.subheader("Active Variables")

current_symbols = manager.symbols

if current_symbols:
    symbol_names = ", ".join(f"`{s.name}`" for s in current_symbols)
    st.markdown(f"The derivative manager is configured with **{len(current_symbols)}** variable(s): {symbol_names}")
else:
    st.warning("No variables defined. Go to **Derivative Calculator** to add variables.")

st.info("You can manage variables and compute derivatives in the **Derivative Calculator** page from the sidebar.")