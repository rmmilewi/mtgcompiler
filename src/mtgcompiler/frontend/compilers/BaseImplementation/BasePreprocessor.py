import abc

class BasePreprocessor(metaclass=abc.ABCMeta):
        """This is the abstract base class for all Arbor lexers."""
        
        def __init__(self,options):
                """
                options: an object that contains options for the lexer.
                """
                pass
        
        def prelex(self,inputobj):
                """
                Calls methods that preprocess the input prior to lexing. This step operates
                on the raw text.
                """
                return NotImplemented
                
        def postlex(self,inputstream):
                """
                Calls methods that preprocess the input after lexing. This step operates on
                the token stream.
                """
                return NotImplemented