from mtgcompiler.frontend.compilers.BaseImplementation.BasePreprocessor import BasePreprocessor

class MtgJsonPreprocessor(BasePreprocessor):
        """The MtgJson preprocessor."""
        
        def __init__(self,options):
                pass #TODO
                
                
        def prelex(self,inputobj,flags):
                return inputobj
                
        def postlex(self,inputobj,flags):
                return inputobj