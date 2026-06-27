import sympy as sp
from typing import Optional, Any, List, Union

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

    def remove_symbols(self, *symbols_to_remove: str) -> None:
        """
        Removes symbols from the existing list of derivation symbols.
        
        Args:
            *symbols_to_remove (str): A sequence of symbol names to remove.
        """
        # Filter the current symbols and delete the symbols in the list of symbols_to_remove 
        self._symbols = [
            sym for sym in self._symbols 
            if sym.name not in symbols_to_remove
        ]            
    
    def calculate_derivative(self, function: Optional[str] = None, *variables: str) -> Any:
        """
        Calculates the derivative of a function. 
        If specific variables are provided, it derives with respect to them.
        Otherwise, it derives with respect to all the symbols defined in the class.

        Args:
            function (str, optional): The mathematical function in text format.
            *variables (str): A sequence of variable names to derive with respect to.
                              If none are provided, the class's default symbols are used.

        Returns:
            sp.Expr or None: The resulting derivative expression, or None if inputs are invalid.
        """
        if function is None:
            return None
        
        expr = sp.sympify(function)
        
        # Determinamos qué variables usar
        if variables:
            # Si el usuario mandó variables en el método, usamos esas
            sym_vars = [sp.Symbol(var) for var in variables]
        else:
            # Si no, usamos las que están configuradas en la clase
            sym_vars = self._symbols
            
        return sp.diff(expr, *sym_vars)