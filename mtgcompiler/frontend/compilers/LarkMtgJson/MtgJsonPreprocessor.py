from mtgcompiler.frontend.compilers.BaseImplementation.BasePreprocessor import BasePreprocessor

class MtgJsonPreprocessor(BasePreprocessor):
        """The MtgJson preprocessor."""
        
        def __init__(self,options):
                pass #TODO
                
                
        def prelex(self,inputobj,flags,name):
                if name is not None:
                    if "," in name:
                        splitName = name.split(",")
                        inputobj = inputobj.replace(name,"~f")
                        inputobj = inputobj.replace(splitName[0],"~")
                    else:
                        inputobj = inputobj.replace(name,"~")
                return inputobj
                
        def postlex(self,inputobj,flags):
                return inputobj