import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, 
    standard_transformations, 
    implicit_multiplication_application
)
from typing import Optional, Any, List, Union, Callable
import numpy as np

class DerivateManager:
    """
    Class to manage and calculate derivatives using SymPy.

    Attributes:
        _symbols (List[sp.Symbol]): The mathematical symbols used for derivation.
    """

    def __init__(self, symbols: Optional[Union[str, List[str]]] = None) -> None:
        """
        Initializes the derivative manager with a list of base symbols.
        Args:
            symbols (str or List[str], optional): The string or list of strings 
                representing the independent variables. Defaults to ["x"].
        """
        if symbols is None:
            symbols = ["x"]
        elif isinstance(symbols, str):
            symbols = [symbols]
            
        # Elimina duplicados y mantiene el orden en 1 línea
        unique_symbols = list(dict.fromkeys(symbols))
        self._symbols = [sp.Symbol(sym) for sym in unique_symbols]

    @property
    def symbols(self) -> List[sp.Symbol]:
        """
        List[sp.Symbol]: Gets the current list of symbols used for derivation.
        """
        return self._symbols.copy()

    @symbols.setter
    def symbols(self, new_values: Union[str, List[str]]) -> None:
        """
        Sets new symbols from a string or list of strings, completely overwriting 
        the old ones while reusing existing SymPy objects when possible.
        Args:
            new_values (str or List[str]): The new values that will define the derivation symbols.
        """
        if isinstance(new_values, str):
            new_values = [new_values]
            
        unique_new_values = list(dict.fromkeys(new_values))
        current_symbols_map = {sym.name: sym for sym in self._symbols}
        self._symbols = [
            current_symbols_map[sym] if sym in current_symbols_map else sp.Symbol(sym) 
            for sym in unique_new_values
        ]

    def add_symbols(self, *new_symbols: str) -> None:
        """
        Adds new symbols to the existing list of derivation symbols without overwriting them.
        
        Args:
            *new_symbols (str): A sequence of new symbol names to add.
        """
        for sym_name in new_symbols:
            # Verify the symbol isnt duplicated
            if not any(existing_sym.name == sym_name for existing_sym in self._symbols):
                self._symbols.append(sp.Symbol(sym_name))      

    def remove_symbols(self, symbols_to_remove: Union[str,List[str]]) -> None:
        """
        Removes symbols from the existing list of derivation symbols.
        
        Args:
            symbols_to_remove (str or List[str]): The values to remove from the list.
        """
        # Filter the current symbols and delete the symbols in the list of symbols_to_remove 
        if isinstance(symbols_to_remove, str):
            symbols_to_remove = [symbols_to_remove]

        self._symbols = [
            sym for sym in self._symbols 
            if sym.name not in symbols_to_remove
        ]            
    
    def convert_input_to_math_function(self, function: str) -> sp.Expr:
        """
        Converts a string representation of a mathematical function into a SymPy expression.
        Supports implicit multiplication (e.g., "2x" is parsed as "2*x").
        """
        transformations = standard_transformations + (implicit_multiplication_application,)
        return parse_expr(function, transformations=transformations)
    
    def calculate_derivative(
        self, function: Optional[str] = None, mixed: bool = False
    ) -> Optional[Union[dict, sp.Expr]]:
        """
        Calculates the derivative of a function with respect to the symbols
        defined in the class.

        By default, computes individual partial derivatives for each symbol
        and returns them as a dictionary. If ``mixed=True``, computes the
        successive mixed partial derivative (∂ⁿf/∂x₁…∂xₙ) instead.

        Args:
            function (str, optional): The mathematical function in text format.
                                      Defaults to None.
            mixed (bool, optional): If True, returns the single mixed partial
                                    derivative with respect to all symbols
                                    (chained). If False, returns a dictionary
                                    mapping each symbol to its individual
                                    partial derivative. Defaults to False.

        Returns:
            Optional[Union[dict, sp.Expr]]:
                - If ``mixed=False``: a dict ``{sp.Symbol: sp.Expr}`` with one
                  partial derivative per symbol.
                - If ``mixed=True``: a single ``sp.Expr`` representing the
                  mixed partial derivative.
                - ``None`` if no function is provided.
        """
        if function is None:
            return None

        expr = self.convert_input_to_math_function(function)

        if mixed:
            return sp.diff(expr, *self._symbols)

        return {sym: sp.diff(expr, sym) for sym in self._symbols}
    
    def evaluate_function(self, function: str, values: dict, as_float: bool = True) -> Any:
        """
        Evaluates a mathematical function at specific values, strictly using the 
        symbols defined in the class instance.

        Args:
            function (str): The mathematical function in text format.
            values (dict): A dictionary mapping variable names to their numerical values. 
                           Must only contain variables defined in the instance.
            as_float (bool, optional): If True, returns a numerical (floating point) result. 
                                       If False, returns the exact symbolic result. Defaults to True.

        Returns:
            Any: The evaluated result.
            
        Raises:
            ValueError: If a variable in 'values' is not defined in the instance's symbols.
        """
        if not function:
            return None
            
        # 1. Obtenemos los nombres de los símbolos válidos de la instancia
        valid_symbol_names = {sym.name for sym in self._symbols}
        
        # 2. Validamos que las variables proporcionadas existan en la instancia
        for key in values.keys():
            if key not in valid_symbol_names:
                raise ValueError(
                    f"The variable '{key}' is not defined in the instance symbols. "
                    f"Available symbols are: {list(valid_symbol_names)}"
                )
                
        expr = self.convert_input_to_math_function(function)
        
        # 3. Construimos el diccionario de sustitución usando los objetos Symbol exactos de la instancia
        subs_dict = {}
        for sym in self._symbols:
            if sym.name in values:
                subs_dict[sym] = values[sym.name]
                
        result = expr.subs(subs_dict)
        
        if as_float:
            return result.evalf()
        return result
    
    def to_numpy_function(self, expr_or_func: Union[str, sp.Expr]) -> Callable:
        """
        Converts a mathematical function or a SymPy expression into a 
        NumPy-compatible function, ideal for array evaluation and plotting.

        Args:
            expr_or_func (str or sp.Expr): The mathematical function in text format or 
                                           the symbolic SymPy expression.

        Returns:
            Callable: A function that accepts NumPy arrays or values as 
                      arguments (in the order of self.symbols).
        """
        # If it's a string, we convert it to a SymPy expression first
        if isinstance(expr_or_func, str):
            expr = self.convert_input_to_math_function(expr_or_func)
        else:
            expr = expr_or_func
            
        # sp.lambdify takes: 
        # 1. The arguments of the function (our symbols)
        # 2. The expression to evaluate
        # 3. The library to use for mathematical operations ("numpy")
        return sp.lambdify(self._symbols, expr, modules="numpy")  

    def solve_for_value(self, function: str, target_value: Union[float, int] = 0) -> List[dict]:
        """
        Finds the values of the variables for which the function equals a specific target value.
        It uses SymPy's Eq and solve methods.

        Args:
            function (str): The mathematical function in text format.
            target_value (float or int, optional): The target value to equate the function to. 
                                                   Defaults to 0 (useful for finding roots or critical points).

        Returns:
            List[dict]: A list of dictionaries where each dictionary represents a solution. 
                        The keys are the SymPy Symbol objects and the values are the solutions.
                        If there are multiple variables, solutions might be in terms of other variables.

        Raises:
            ValueError: If the function contains variables not defined in the instance's symbols.
        """
        if not function:
            return []
            
        # Convert the string to a SymPy expression
        expr = self.convert_input_to_math_function(function)
        
        # 1. Validate that the expression only contains variables defined in _symbols
        expr_symbols = {sym.name for sym in expr.free_symbols}
        valid_symbol_names = {sym.name for sym in self._symbols}
        
        unsupported_symbols = expr_symbols - valid_symbol_names
        if unsupported_symbols:
            raise ValueError(
                f"The function contains variables not defined in the instance symbols: {list(unsupported_symbols)}. "
                f"Available symbols are: {list(valid_symbol_names)}"
            )
            
        # 2. Create the equation: expr == target_value
        equation = sp.Eq(expr, target_value)
        
        # 3. Solve the equation strictly for the symbols defined in the instance
        # dict=True ensures the output is a list of dictionaries mapping symbols to their values
        return sp.solve(equation, self._symbols, dict=True)