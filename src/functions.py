import numpy as np
from DerivateManager import DerivateManager

def function_to_array(
    manager: DerivateManager, 
    function: str, 
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

