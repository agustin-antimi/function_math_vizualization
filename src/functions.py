import numpy as np
from DerivateManager import DerivateManager
import matplotlib.pyplot as plt
from typing import Optional, Union
import sympy as sp
import plotly.graph_objects as go

def function_to_array(
    manager: DerivateManager, 
    function: Union[str, sp.Expr], 
    x_values: np.ndarray = np.linspace(-10, 10, 100)
) -> np.ndarray:
    """
    Evaluates a mathematical function over a range of values using a DerivateManager instance.

    Args:
        manager (DerivateManager): The instance of DerivateManager used to parse and convert the function.
        function (str): The mathematical function in text format to be evaluated.
        x_values (np.ndarray, optional): An array of numerical values where the function will be evaluated. 
                                         Defaults to an array from -10 to 10 with 100 points.

    Returns:
        np.ndarray: A NumPy array containing the evaluated results (y-values) corresponding to x_values.
    """
    numpy_function = manager.to_numpy_function(function)
    return numpy_function(x_values)


def _plot_2d(
    manager: DerivateManager,
    function: Union[str, sp.Expr],
    x_min: float = -1000.0,
    x_max: float = 1000.0,
    step: float = 0.05,
    initial_x_view: list[float] = [-5, 5],
    initial_y_view: list[float] = [-5, 5],
) -> go.Figure:
    """
    Internal helper that builds a 2D interactive line plot for a single-variable function.

    Args:
        manager (DerivateManager): The manager instance with exactly one symbol.
        function (Union[str, sp.Expr]): The mathematical function to plot.
        x_min (float): Minimum x-value for generated data.
        x_max (float): Maximum x-value for generated data.
        step (float): Step size between x-values.
        initial_x_view (list[float]): [min, max] range for the initial X-axis view.
        initial_y_view (list[float]): [min, max] range for the initial Y-axis view.

    Returns:
        go.Figure: The generated Plotly figure.
    """
    x = np.arange(x_min, x_max, step)
    y = function_to_array(manager, function, x)

    # Handle constant expressions (lambdify returns a scalar instead of an array)
    y = np.broadcast_to(np.asarray(y, dtype=float), x.shape)

    func_name = f"y = {function}" if isinstance(function, str) else f"y = {str(function)}"

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name=func_name,
        line=dict(color='blue')
    ))

    fig.update_layout(
        xaxis=dict(
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='black',
            showgrid=True,
            range=initial_x_view,
        ),
        yaxis=dict(
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='black',
            showgrid=True,
            range=initial_y_view,
        ),
        plot_bgcolor='white',
        hovermode="x unified",
        title=f"Interactive Plot: {func_name}",
    )

    return fig


def _plot_3d(
    manager: DerivateManager,
    function: Union[str, sp.Expr],
    xy_min: float = -10.0,
    xy_max: float = 10.0,
    step: float = 0.2,
) -> go.Figure:
    """
    Internal helper that builds a 3D interactive surface plot for a two-variable function.

    Args:
        manager (DerivateManager): The manager instance with exactly two symbols.
        function (Union[str, sp.Expr]): The mathematical function to plot.
        xy_min (float): Minimum value for both axes. Defaults to -10.
        xy_max (float): Maximum value for both axes. Defaults to 10.
        step (float): Step size for the meshgrid. Defaults to 0.2.

    Returns:
        go.Figure: The generated Plotly 3D surface figure.
    """
    numpy_function = manager.to_numpy_function(function)

    vals = np.arange(xy_min, xy_max, step)
    X, Y = np.meshgrid(vals, vals)

    # Evaluate: the lambdified function expects (first_symbol, second_symbol)
    Z = numpy_function(X, Y)

    # Handle constant expressions (lambdify returns a scalar instead of an array)
    Z = np.broadcast_to(np.asarray(Z, dtype=float), X.shape)

    sym_names = [s.name for s in manager.symbols]
    func_name = f"f({sym_names[0]}, {sym_names[1]}) = {function}" if isinstance(function, str) else f"f({sym_names[0]}, {sym_names[1]}) = {str(function)}"

    fig = go.Figure()
    fig.add_trace(go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale='Viridis',
        name=func_name,
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title=sym_names[0],
            yaxis_title=sym_names[1],
            zaxis_title="f",
        ),
        title=f"3D Surface Plot: {func_name}",
    )

    return fig


def plot_interactive(
    manager: 'DerivateManager', 
    function: Union[str, sp.Expr] = None,
    x_min: float = -1000.0, 
    x_max: float = 1000.0,
    step: float = 0.05, 
    initial_x_view: list[float] = [-5, 5],
    initial_y_view: list[float] = [-5, 5]
) -> go.Figure:
    """
    Generates and displays an interactive plot for a given mathematical function using Plotly.

    Automatically selects between a 2D line plot (1 variable) and a 3D surface plot
    (2 variables) based on the number of symbols defined in the manager.

    Args:
        manager (DerivateManager): The manager instance used to handle parsing/evaluation.
        function (Union[str, sp.Expr]): The mathematical function to plot. Cannot be None.
        x_min (float, optional): The minimum x-value for generated data (2D only). Defaults to -1000.0.
        x_max (float, optional): The maximum x-value for generated data (2D only). Defaults to 1000.0.
        step (float, optional): The step size between values. Defaults to 0.05.
        initial_x_view (list[float], optional): The [min, max] range for the initial X-axis view (2D only).
        initial_y_view (list[float], optional): The [min, max] range for the initial Y-axis view (2D only).

    Returns:
        plotly.graph_objects.Figure: The generated Plotly figure object.
    
    Raises:
        ValueError: If the 'function' parameter is None or the manager has more than 2 symbols.
    """
    if function is None:
        raise ValueError("The 'function' parameter cannot be None. Please provide a string or a SymPy expression.")

    num_symbols = len(manager.symbols)

    if num_symbols == 1:
        return _plot_2d(
            manager, function,
            x_min=x_min, x_max=x_max, step=step,
            initial_x_view=initial_x_view, initial_y_view=initial_y_view,
        )
    elif num_symbols == 2:
        return _plot_3d(
            manager, function,
            xy_min=initial_x_view[0] if initial_x_view else -10.0,
            xy_max=initial_x_view[1] if initial_x_view else 10.0,
            step=max(step, 0.2),
        )
    else:
        raise ValueError(
            f"Plotting is only supported for 1 or 2 variables. "
            f"The manager has {num_symbols} symbols: {[s.name for s in manager.symbols]}"
        )