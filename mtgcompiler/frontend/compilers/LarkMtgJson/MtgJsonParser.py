from mtgcompiler.frontend.compilers.BaseImplementation.BaseParser import BaseParser

class MtgJsonParser(BaseParser):
        """The MtgJson lexer. This class wraps the Lark implementation of the lexer,
        helping somewhat to decouple Lark from Arbor."""
        
        def __init__(self,options,larkparser):
                """
                options: an object that contains options for the lexer.
                larkparser: An instance of a Lark parser which is wrapped by this object.
                """
                super().__init__(options)
                self._larkparser = larkparser
                
        def parse(self,cardinput):
                """
                Parses a card in whatever format the parser accepts.
                Returns a parse tree representation of the input.
                
                cardinput: An input representing a card. The details of that are up
                to the parser implementation.
                """
                return self._larkparser.parse(cardinput)