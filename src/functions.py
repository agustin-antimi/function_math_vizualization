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

    This function calculates numerical values for a mathematical function (passed as a string 
    or a SymPy expression) over a large specified range, but sets the initial view (zoom) 
    to a predefined window. The plot features a Cartesian coordinate system.

    Args:
        manager (DerivateManager): The manager instance used to handle parsing/evaluation.
        function (Union[str, sp.Expr]): The mathematical function to plot. Cannot be None.
        x_min (float, optional): The minimum x-value for the generated data. Defaults to -1000.0.
        x_max (float, optional): The maximum x-value for the generated data. Defaults to 1000.0.
        step (float, optional): The step size between x-values. Defaults to 0.05.
        initial_x_view (list[float], optional): The [min, max] range for the initial X-axis view. Defaults to [-10.0, 10.0].
        initial_y_view (list[float], optional): The [min, max] range for the initial Y-axis view. Defaults to [-2.0, 2.0].

    Returns:
        plotly.graph_objects.Figure: The generated Plotly figure object.
    
    Raises:
        ValueError: If the 'function' parameter is None.
    """
    
    # Generate x values
    x = np.arange(x_min, x_max, step)
    
    # Verify the function parameter and evaluate it using function_to_array
    if function is None:
        raise ValueError("The 'function' parameter cannot be None. Please provide a string or a SymPy expression.")
    
    # function_to_array supports str and sympy.Expr
    y = function_to_array(manager, function, x)
    
    # Format the function name for the legend/title depending on its type
    func_name = f"y = {function}" if isinstance(function, str) else f"y = {str(function)}"
    
    # Create the figure and add the trace
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, 
        y=y, 
        mode='lines', 
        name=func_name,
        line=dict(color='blue')
    ))

    # Configure the layout (Cartesian axes crossing at 0,0 and initial zoom)
    fig.update_layout(
        xaxis=dict(
            zeroline=True, 
            zerolinewidth=2, 
            zerolinecolor='black', 
            showgrid=True,
            range=initial_x_view
        ),
        yaxis=dict(
            zeroline=True, 
            zerolinewidth=2, 
            zerolinecolor='black', 
            showgrid=True,
            range=initial_y_view
        ),
        plot_bgcolor='white',
        hovermode="x unified",
        title=f"Interactive Plot: {func_name} (Initial view restricted)"
    )
    
    return fig