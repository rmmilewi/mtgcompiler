import abc

class BaseParser(metaclass=abc.ABCMeta):
        """This is the abstract base class for all MtgCompiler parsers."""
        
        
        def parse(self,cardinput):
                """
                Parses a card in whatever format the parser accepts.
                Returns a representation of the card in the MtgCompiler AST format.
                
                cardinput: An input representing a card. The details of that are up
                to the parser implementation.
                """
                return NotImplemented