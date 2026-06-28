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
        return self._symbols

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
    
    def calculate_derivative(self, function: Optional[str] = None) -> Optional[sp.Expr]:
        """
        Calculates the derivative of a function with respect to all the default symbols 
        defined in the class.

        Args:
            function (str, optional): The mathematical function in text format. 
                                      Defaults to None.

        Returns:
            Optional[sp.Expr]: The resulting derivative expression, or None if no function 
                               is provided.
        """
        if function is None:
            return None
        
        expr = self.convert_input_to_math_function(function)
            
        return sp.diff(expr, *self._symbols)
    
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