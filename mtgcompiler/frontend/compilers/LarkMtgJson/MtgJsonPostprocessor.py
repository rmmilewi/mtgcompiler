from mtgcompiler.frontend.compilers.BaseImplementation.BasePostprocessor import BasePostprocessor

class MtgJsonPostprocessor(BasePostprocessor):
        """The MtgJson postprocessor."""
        
        def __init__(self,options):
                pass #TODO
                
        def postprocess(self,cardobj,flags={}):
                return cardobj