import sympy as sp

class DerivateManager:
    """
    Class to manage and calculate derivatives of a single variable using SymPy.

    Attributes:
        _symbol (sp.Symbol): The mathematical symbol used for derivation.
    """

    def __init__(self, symbol: str = "x") -> None:
        """
        Initializes the derivative manager with a base symbol.

        Args:
            symbol (str, optional): The string representing the independent 
                variable. Defaults to "x".
        """
        self._symbol = sp.Symbol(symbol)
    
    @property
    def symbol(self) -> sp.Symbol:
        """
        sp.Symbol: Gets the current symbol used for derivation.
        """
        return self._symbol

    @symbol.setter
    def symbol(self, new_value: str) -> None:
        """
        Sets a new symbol from a string input.

        Args:
            new_value (str): The new string value that will define the derivation symbol.
        """
        self._symbol = self._convert_input_to_function(new_value)
    
    def _convert_input_to_function(self, user_input: str = None) -> sp.Expr:
        """
        Converts a text input into a valid SymPy expression or symbol.

        Args:
            user_input (str, optional): The string to be converted.

        Returns:
            sp.Expr: The mathematical expression or symbol interpreted by SymPy.
        """
        # sp.sympify transforms a string into an object that the SymPy library can manipulate.
        return sp.sympify(user_input)
    
    def calculate_derivate_one_variable(self, function: str = None):
        """
        Calculates the first derivative of a function with respect to the configured symbol.

        Args:
            function (str, optional): The mathematical function in text format.

        Returns:
            sp.Expr or None: The derivative expression. Returns None if no
            function is provided in the input.
        """
        if function is None:
            return None
        
        # We need to ensure that the function passed as a string
        # is converted to a SymPy expression before differentiating.
        expr = sp.sympify(function)
        return sp.diff(expr, self._symbol)