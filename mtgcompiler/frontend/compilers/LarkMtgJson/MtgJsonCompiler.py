from mtgcompiler.frontend.compilers.BaseImplementation.BaseCompiler import BaseCompiler
import mtgcompiler.frontend.compilers.LarkMtgJson.grammar as grammar #TODO: This will change.
#from mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonLexer import MtgJsonLexer
from mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonPreprocessor import MtgJsonPreprocessor
from mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonTransformer import MtgJsonTransformer
from mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonPostprocessor import MtgJsonPostprocessor
#from mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonParser import MtgJsonParser
import cProfile

from lark import Lark

class MtgJsonCompiler(BaseCompiler):
        def __init__(self,options):
                super().__init__(options)
                
                #TODO: This is just a temporary solution until we have a more elegant
                #way of generating the grammar, which is coming shortly.
                g = grammar.getGrammar()
                
                #larkfrontend = Lark(g,start='cardtext',parser='earley',lexer='standard',debug=True)
                #print(larkfrontend.lexer_conf.tokens)
                
                self._larkfrontend = Lark(g,start='cardtext',debug=True)
                self._preprocessor = MtgJsonPreprocessor(options)
                self._transformer = MtgJsonTransformer(options)
                self._postprocessor = MtgJsonPostprocessor(options)
                
                #self._lexer = MtgJsonLexer(options,larklexer=larkfrontend.parser.lexer)
                #self._parser = MtgJsonParser(options,larkparser=larkfrontend.parser.parser)
                
        def _callLarkParse(self,bodytext):
                """Calls the Lark frontend to parse the input."""
                return self._larkfrontend.parse(bodytext)
                
        def compile(self,cardinput,flags):
                
                result = {}
                #Apply the prelex preprocessing step.
                result['parsed_body'] = self._preprocessor.prelex(cardinput,flags)
                
                #Apply the postlex preprocessing step.
                result['parsed_body'] = self._preprocessor.postlex(result['parsed_body'],flags)
                
                #Call the Lark frontend to parse the card text.
                result['parsed_body'] = self._callLarkParse(result['parsed_body'])
                
                #Apply the transformer to generate the AST.
                result = self._transformer.transform(result)
                
                #Apply the postprocessing step
                result = self._postprocessor.postprocess(result,flags)
                
                return result
                
                
                
                #tokenstream = self._lexer.lex(cardinput)
                #print(tokenstream)
                #for token in tokenstream:
                #        print(token.type, token.value)
                #parsetree = self._frontend.parse(cardinput)
                #print(parsetree.pretty())
                
                
                
compiler = MtgJsonCompiler(options=None)

txt = "destroy target blue creature."

cProfile.run(compiler.compile(cardinput=txt,flags=None))

