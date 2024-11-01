import unittest
import lark
import mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonTransformer as MtgJsonTransformer
import mtgcompiler.frontend.compilers.LarkMtgJson.grammar as grammar
import mtgcompiler.frontend.AST.core

class TestMtgJsonTransformer(unittest.TestCase):
    
        @classmethod
        def setUpClass(cls):
            g = grammar.getGrammar()
            cls._parser = lark.Lark(g,start="cardtext",debug=True)
        
        def test_MtgJsonCompiler_isConstructibleWithoutOptions(self):
                transformer = MtgJsonTransformer.MtgJsonTransformer()
                
        def test_MtgJsonCompiler_testTransformerBehaviorOnExamples(self):
                transformer = MtgJsonTransformer.MtgJsonTransformer()
                
                firstStrikeExampleText = "first strike"
                firstStrikeExampleParseTree = self._parser.parse(firstStrikeExampleText)
                self.assertIsInstance(firstStrikeExampleParseTree,lark.tree.Tree)
                firstStrikeExampleAST = transformer.transform(firstStrikeExampleParseTree)
                self.assertIsInstance(firstStrikeExampleAST,mtgcompiler.frontend.AST.core.MgNode)
                
                destroyExampleText = "destroy target blue creature"
                destroyExampleParseTree = self._parser.parse(destroyExampleText)
                destroyExampleAST = transformer.transform(destroyExampleParseTree)
                self.assertIsInstance(destroyExampleAST,mtgcompiler.frontend.AST.core.MgNode)
                
                
                
                