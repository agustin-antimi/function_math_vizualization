import streamlit as st
import sys
sys.path.append("src")

from src.DerivateManager import DerivateManager
import sympy as sp

st.title("Derivative Calculator")

# --- Initialize DerivateManager in session_state ---
if "manager" not in st.session_state:
    st.session_state["manager"] = DerivateManager()

manager: DerivateManager = st.session_state["manager"]

# --- Symbol management section ---
st.subheader("Variables")
st.caption("Manage the variables used for differentiation. Default: x")

current_symbols = manager.symbols
symbol_names = [s.name for s in current_symbols]

# Show current variables as tags
if current_symbols:
    st.markdown("**Current variables:** " + "  ".join(f"`{name}`" for name in symbol_names))

# Two clearly separated columns: one to add, one to remove
col_add, col_remove = st.columns(2)

with col_add:
    st.markdown("**➕ Add a variable**")
    new_symbol = st.text_input("Variable name", placeholder="e.g. y, z, t", key="add_var_input", label_visibility="collapsed")
    if st.button("Add Variable", key="btn_add", use_container_width=True):
        if new_symbol and new_symbol.strip():
            name = new_symbol.strip()
            if name not in symbol_names:
                manager.add_symbols(name)
                st.session_state.pop("derivative_result", None)
                st.rerun()
            else:
                st.warning(f"Variable '{name}' already exists.")
        else:
            st.warning("Enter a variable name first.")

with col_remove:
    st.markdown("**➖ Remove a variable**")
    if symbol_names:
        symbol_to_remove = st.selectbox("Select variable", symbol_names, key="remove_var_select", label_visibility="collapsed")
        if st.button("Remove Variable", key="btn_remove", use_container_width=True):
            manager.remove_symbols(symbol_to_remove)
            st.session_state.pop("derivative_result", None)
            st.rerun()
    else:
        st.warning("No variables to remove.")

st.divider()

# --- Function input ---
function_input = st.text_input(
    "Enter a mathematical function",
    placeholder="e.g. x**2 + 3x + 1, sin(x), e**x",
)

# Calculate button
if st.button("Calculate Derivative", type="primary"):
    if function_input.strip():
        try:
            derivative = manager.calculate_derivative(function_input)

            # Store result in session_state to persist across reruns
            st.session_state["derivative_result"] = derivative
            st.session_state["original_function"] = function_input
            st.session_state["derivative_error"] = None
        except Exception as e:
            st.session_state["derivative_result"] = None
            st.session_state["derivative_error"] = str(e)
    else:
        st.warning("Please enter a function before calculating.")

# --- Display result ---
if st.session_state.get("derivative_result") is not None:
    original = st.session_state["original_function"]
    result = st.session_state["derivative_result"]

    st.divider()
    st.subheader("Result")

    # Build variable list string for display
    sym_names = ", ".join(s.name for s in manager.symbols)

    expr_original = manager.convert_input_to_math_function(original)
    st.latex(rf"f({sym_names}) = {sp.latex(expr_original)}")
    st.latex(rf"f'({sym_names}) = {sp.latex(result)}")

elif st.session_state.get("derivative_error"):
    st.error(f"Error calculating the derivative: {st.session_state['derivative_error']}")
