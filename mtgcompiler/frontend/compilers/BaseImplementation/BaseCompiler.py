import abc

class BaseCompiler(metaclass=abc.ABCMeta):
        """This is the abstract base class for the facade of the frontend. It encapsulates and provides
        access to the lexer, preprocessor, parser, AST transformer, and postprocessor.
        """
        
        def __init__(self,options):
                """
                options: An object that is passed to the BaseCompiler containing options, parameters, etc.
                that are in turn passed to all the components.
                """
                pass
                
                #self._lexer = self.createLexer(options)
                #self._preprocessor = self.createPreprocessor(options)
                #self._parser = self.createParser(options)
                #self._transformer = self.createTransformer(options)
                #self._postprocessor = self.createPostProcessor(options)
                
                
        def hasLexer(self):
                """
                Checks whether the Lexer has been instantiated. 
                This is usually just a sanity check.
                """
                return self._lexer is not None
                
        def getLexer(self):
                """
                Returns the lexer instance.
                """
                return self._lexer
                
        def hasParser(self):
                """
                Checks whether the Parser has been instantiated. 
                This is usually just a sanity check.
                """
                return self._parser is not None
                
        def getParser(self):
                """
                Returns the Parser instance.
                """
                return self._parser
                
        def hasPreprocessor(self):
                """
                Checks whether the Preprocessor has been instantiated. 
                This is usually just a sanity check.
                """
                return self._preprocessor is not None
                
        def getPreprocessor(self):
                """
                Returns the Preprocessor instance.
                """
                return self._preprocessor
                
        def hasParser(self):
                """
                Checks whether the Parser has been instantiated. 
                This is usually just a sanity check.
                """
                return self._parser is not None
                
        def getParser(self):
                """
                Returns the Parser instance.
                """
                return self._parser
                
        def hasTransformer(self):
                """
                Checks whether the Transformer has been instantiated. 
                This is usually just a sanity check.
                """
                return self._transformer is not None
                
        def getTransformer(self):
                """
                Returns the Transformer instance.
                """
                return self._transformer
                
        def hasPostprocessor(self):
                """
                Checks whether the Postprocessor has been instantiated. 
                This is usually just a sanity check.
                """
                return self._postprocessor is not None
                
        def getPostprocessor(self):
                """
                Returns the Postprocessor instance.
                """
                return self._postprocessor
                
        def compile(self,cardinput,flags):
                """
                Takes a card as input and either returns an AST or produces an error.
                
                cardinput: A card in an appropriate format.
                flags: An object containing implementation-specific flags that control the operation of the compiler.
                """
                return NotImplemented
        
        
                
        
                
        
                 
                