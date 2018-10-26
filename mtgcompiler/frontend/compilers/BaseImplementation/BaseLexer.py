import abc

class BaseLexer(metaclass=abc.ABCMeta):
        """This is the abstract base class for all Arbor lexers."""
        
        def __init__(self,options):
                """
                options: an object that contains options for the lexer.
                """
                pass
        
        def lex(self,inputstream):
                """
                Lexes the input and returns a token stream.
                
                inputstream: The input that will be lexed.
                """
                return NotImplemented
        