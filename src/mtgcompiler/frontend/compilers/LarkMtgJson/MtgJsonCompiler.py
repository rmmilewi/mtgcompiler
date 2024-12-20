from mtgcompiler.frontend.compilers.BaseImplementation.BaseCompiler import BaseCompiler
import mtgcompiler.frontend.compilers.LarkMtgJson.grammar as grammar #TODO: This will change.
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonPreprocessor import MtgJsonPreprocessor
from mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonTransformer import MtgJsonTransformer
from mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonPostprocessor import MtgJsonPostprocessor
import cProfile
import lark
import re


class MtgJsonCompiler(BaseCompiler):
        def __init__(self,options={}):
                super().__init__(options)
                
                #TODO: This is just a temporary solution until we have a more elegant
                #way of generating the grammar.
                #g = grammar.getGrammar()
                
                """
                grammar = grammarian.requestGrammar(imports=
                [
                "base/common.grm",
                "base/entities.grm",
                "base/statements.grm",
                "base/abilities.grm",
                "base/manasymbolexpressions.grm",
                "base/playerdeclrefs.grm",
                "base/timeexpressions.grm",
                "base/zones.grm",
                "base/characteristics.grm",
                "base/conditionalstmts.grm",
                "base/effectstatements.grm",
                "base/modifiers.grm",
                "base/qualifiers.grm",
                "base/typeexpressions.grm",
                "base/colorexpressions.grm",
                "base/declrefdecorators.grm",
                "base/objectdeclrefs.grm",
                "base/valueexpressions.grm"
                ]
                ,options=options)
                """
                
                #larkfrontend = Lark(g,start='cardtext',parser='earley',lexer='standard',debug=True)
                #print(larkfrontend.lexer_conf.tokens)
                
                if "parser.startRule" in options:
                    startRule = options["parser.startRule"]
                else:
                    startRule = 'cardtext'
                    
                if "parser.larkDebug" in options:
                    larkDebug = options["parser.larkDebug"]
                else:
                    larkDebug = True

                if "parser.larkLexer" in options:
                    larkLexer = options["parser.larkLexer"]
                else:
                    larkLexer = "auto"

                if "parser.larkParser" in options:
                    larkParser = options["parser.larkParser"]
                else:
                    larkParser = "earley"

                if "parser.overrideGrammar" in options:
                    g = options["parser.overrideGrammar"]
                else:
                    g = grammar.getGrammar()

                if "parser.strict" in options:
                    strict = options["parser.strict"]
                else:
                    strict = False

                if "parser.ambiguity" in options:
                    ambiguity = options["parser.ambiguity"]
                else:
                    ambiguity = "resolve"

                try:
                    self._larkfrontend = lark.Lark(g,start=startRule,
                        debug=larkDebug,
                        parser=larkParser,
                        lexer=larkLexer,
                        strict=strict,
                        ambiguity=ambiguity,
                        g_regex_flags=re.X & re.I) #To enable parsing of newline characters and toggling case insensitivity
                except Exception as e:
                    print("MTGJsonCompiler: Failed to instantiate Lark frontend.")
                    raise e
                
                self._parser = self._larkfrontend
                self._preprocessor = MtgJsonPreprocessor(options)
                self._transformer = MtgJsonTransformer(options)
                self._postprocessor = MtgJsonPostprocessor(options)
                
                #self._lexer = MtgJsonLexer(options,larklexer=larkfrontend.parser.lexer)
                #self._parser = MtgJsonParser(options,larkparser=larkfrontend.parser.parser)
                
        def _callLarkParse(self,textInput):
                """Calls the Lark frontend to parse the input."""
                return self._larkfrontend.parse(textInput)
                
        def compile(self,textInput,flags={},name=None):
                result = {}
                #Apply the prelex preprocessing step.
                result['parsed_body'] = self._preprocessor.prelex(textInput,name,flags)
                
                #Apply the postlex preprocessing step.
                result['parsed_body'] = self._preprocessor.postlex(result['parsed_body'],flags)
                
                #Call the Lark frontend to parse the card text.
                result['parsed_body'] = self._callLarkParse(result['parsed_body'])
                
                #Apply the transformer to generate the AST.
                result["ast"] = self._transformer.transform(result['parsed_body'])
                
                #Apply the postprocessing step
                result = self._postprocessor.postprocess(result,flags)
                
                return result
                
                
                
                #tokenstream = self._lexer.lex(cardinput)
                #print(tokenstream)
                #for token in tokenstream:
                #        print(token.type, token.value)
                #parsetree = self._frontend.parse(cardinput)
                #print(parsetree.pretty())

