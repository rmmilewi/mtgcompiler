import abc

class BaseParser(metaclass=abc.ABCMeta):
        """This is the abstract base class for all MtgCompiler parsers."""
        
        def __init__(self,options):
                """
                options: A dictionary that contains options for the parser. 
                """
                
                
                #parseonly: Only parse the input, do not construct an AST.
                if options is not None and "parseonly" in options:
                        self._parseonly = options["parseonly"]
                else:
                        self._parseonly = False
                        
                #rulestextonly: Only parse the rules text
                if options is not None and "rulestextonly" in options:
                        self._rulestextonly = options["rulestextonly"]
                else:
                        self._rulestextonly = False
                        
                #rendertree: for debugging, renders the parse tree of the body
                #text to a png file called lark_test.png
                if options is not None and "renderparsetree" in options:
                        self._renderparsetree = options["renderparsetree"]
                else:
                        self._renderparsetree = False
        
        
        def parse(self,cardinput):
                """
                Parses a card in whatever format the parser accepts.
                Returns a representation of the card in the MtgCompiler AST format.
                
                cardinput: An input representing a card. The details of that are up
                to the parser implementation.
                """
                return NotImplemented