import abc

class BaseTransformer(metaclass=abc.ABCMeta):
        """This is the abstract base class for all Arbor AST transformers."""
        
        def __init__(self,options):
                """
                options: an object that contains options for the transformer.
                """
                pass
        
        def transform(self,parsetree):
                """
                Returns a representation of the card in the MtgCompiler AST format.
                
                parsetree: The input that will be transformed.
                """
                return NotImplemented