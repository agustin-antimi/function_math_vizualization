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

# Clear stale results when the input changes
if function_input != st.session_state.get("original_function", ""):
    st.session_state.pop("derivative_result", None)
    st.session_state.pop("derivative_error", None)

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

    # result is a dict {Symbol: Expr} with one partial derivative per variable
    if isinstance(result, dict):
        for sym, deriv_expr in result.items():
            st.latex(rf"\frac{{\partial f}}{{\partial {sp.latex(sym)}}} = {sp.latex(deriv_expr)}")
    else:
        # Legacy fallback for old session results (single expression)
        st.latex(rf"f'({sym_names}) = {sp.latex(result)}")

    # --- Stationary points (critical points) ---
    st.divider()
    st.subheader("Stationary Points")
    st.caption("Points where all partial derivatives equal zero.")

    try:
        if isinstance(result, dict):
            # Build system of equations: all partial derivatives = 0
            deriv_exprs = list(result.values())
            equations = [sp.Eq(expr, 0) for expr in deriv_exprs]
            solutions = sp.solve(equations, manager.symbols, dict=True)
        else:
            # Single variable: solve f'(x) = 0
            solutions = manager.solve_for_value(str(result), target_value=0)

        if solutions:
            for i, sol in enumerate(solutions):
                point_parts = [rf"{sp.latex(sym)} = {sp.latex(val)}" for sym, val in sol.items()]
                st.latex(rf"P_{{{i+1}}}: \quad " + r", \quad ".join(point_parts))
        else:
            st.info("No stationary points found.")
    except Exception as e:
        st.warning(f"Could not compute stationary points: {e}")
    # --- Evaluate function at specific values ---
    import src.functions as fn

    st.divider()
    st.subheader("Evaluate at a Point")

    sym_names_list = [s.name for s in manager.symbols]

    # Create one number input per variable
    eval_cols = st.columns(len(sym_names_list))
    eval_values = {}
    for i, name in enumerate(sym_names_list):
        with eval_cols[i]:
            eval_values[name] = st.number_input(
                f"{name} =", value=0.0, step=0.1, format="%.4f", key=f"eval_{name}"
            )

    if st.button("Evaluate", key="btn_evaluate"):
        # Evaluate the original function
        try:
            f_val = manager.evaluate_function(original, eval_values)
            point_str = ", ".join(f"{k}={v}" for k, v in eval_values.items())
            st.success(f"f({point_str}) = **{f_val}**")
        except Exception as e:
            st.error(f"Could not evaluate the function: {e}")

        # Evaluate each partial derivative
        if isinstance(result, dict):
            for sym, deriv_expr in result.items():
                try:
                    deriv_str = str(deriv_expr)
                    d_val = manager.evaluate_function(deriv_str, eval_values)
                    point_str = ", ".join(f"{k}={v}" for k, v in eval_values.items())
                    st.success(f"∂f/∂{sym.name}({point_str}) = **{d_val}**")
                except Exception as e:
                    st.error(f"Could not evaluate ∂f/∂{sym.name}: {e}")

    # --- Interactive plots ---
    st.divider()
    st.subheader("Plots")

    # Plot the original function
    num_vars = len(manager.symbols)
    plot_id = f"{original}_{num_vars}"
    try:
        st.markdown(f"**Original function:** $f({sym_names})$")
        fig_original = fn.plot_interactive(manager, original)
        st.plotly_chart(fig_original, use_container_width=True, key=f"plot_orig_{plot_id}")
    except Exception as e:
        st.error(f"Could not plot the original function: {e}")

    # Plot each partial derivative
    if isinstance(result, dict):
        for sym, deriv_expr in result.items():
            try:
                st.markdown(f"**Derivative:** $\\partial f / \\partial {sp.latex(sym)}$")
                fig_deriv = fn.plot_interactive(manager, deriv_expr)
                st.plotly_chart(fig_deriv, use_container_width=True, key=f"plot_d{sym.name}_{plot_id}")
            except Exception as e:
                st.error(f"Could not plot ∂f/∂{sym.name}: {e}")

elif st.session_state.get("derivative_error"):
    st.error(f"Error calculating the derivative: {st.session_state['derivative_error']}")
