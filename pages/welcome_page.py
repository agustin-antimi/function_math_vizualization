import streamlit as st
import sys
sys.path.append("src")

from src.DerivateManager import DerivateManager

st.title("Function Math Visualizer")

st.markdown("""
Welcome to **Function Math Visualizer**, an interactive tool for working with
mathematical functions and their derivatives.

### What is this project?

This application lets you explore calculus concepts visually and symbolically.
You can type any mathematical function, compute its derivative instantly, and
see the result rendered in clean LaTeX notation.

### Features

- **Symbolic differentiation** — compute derivatives of any function using
  [SymPy](https://www.sympy.org) under the hood.
- **Multi-variable support** — add or remove variables to differentiate with
  respect to more than one independent variable.
- **LaTeX rendering** — results are displayed in standard mathematical notation.
- **Interactive plots** — visualize functions and their derivatives on
  interactive graphs powered by Plotly.

### How to use it

1. Go to the **Derivative Calculator** page from the sidebar.
2. Configure your variables (default is `x`). You can add more like `y` or `t`.
3. Enter a function (e.g. `x**2 + 3x + 1`, `sin(x)`, `e**x`).
4. Click **Calculate Derivative** and see the result below.
""")

# --- Show active variables ---
if "manager" not in st.session_state:
    st.session_state["manager"] = DerivateManager()

manager: DerivateManager = st.session_state["manager"]
current_symbols = manager.symbols

st.divider()
st.subheader("Active Variables")

if current_symbols:
    symbol_names = ", ".join(f"`{s.name}`" for s in current_symbols)
    st.markdown(f"The derivative manager has **{len(current_symbols)}** variable(s) configured: {symbol_names}")
else:
    st.warning("No variables defined. Go to **Derivative Calculator** to add variables.")