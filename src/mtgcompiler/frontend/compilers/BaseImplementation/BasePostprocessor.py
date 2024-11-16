import abc

class BasePostprocessor(metaclass=abc.ABCMeta):
        """This is the abstract base class for all Arbor AST postprocessors."""
        
        def __init__(self,options):
                """
                options: an object that contains options for the postprocessor.
                """
                pass
        
        def postprocess(self,ast):
                """
                Applies post-processing steps to the AST.
                
                ast: The input that will be transformed.
                """
                return NotImplemented