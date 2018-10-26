from mtgcompiler.frontend.compilers.BaseImplementation.BaseCompiler import BaseCompiler
import mtgcompiler.frontend.compilers.LarkMtgJson.grammar as grammar #TODO: This will change.
#from mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonLexer import MtgJsonLexer
from mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonPreprocessor import MtgJsonPreprocessor
#from mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonParser import MtgJsonParser

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
                
                #self._lexer = MtgJsonLexer(options,larklexer=larkfrontend.parser.lexer)
                #self._parser = MtgJsonParser(options,larkparser=larkfrontend.parser.parser)
                
                
        def compile(self,cardinput,flags):
                #tokenstream = self._lexer.lex(cardinput)
                #print(tokenstream)
                #for token in tokenstream:
                #        print(token.type, token.value)
                #parsetree = self._frontend.parse(cardinput)
                #print(parsetree.pretty())
                
                
                
compiler = MtgJsonCompiler(options=None)

txt = "destroy target blue creature."

compiler.compile(cardinput=txt,flags=None)

