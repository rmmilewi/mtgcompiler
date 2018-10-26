from mtgcompiler.frontend.compilers.BaseImplementation.BaseLexer import BaseLexer

class MtgJsonLexer(BaseLexer):
        """The MtgJson lexer. This class wraps the Lark implementation of the lexer,
        helping somewhat to decouple Lark from Arbor."""
        
        def __init__(self,options,larklexer):
                """
                options: an object that contains options for the lexer.
                larklexer: An instance of a Lark lexer which is wrapped by this object.
                """
                super().__init__(options)
                self._larklexer = larklexer
                pass
                
        def lex(self,inputstream):
                """
                Lexes the input and returns a token stream.
                
                inputstream: The input that will be lexed.
                """
                
                return self._larklexer.lex(inputstream)