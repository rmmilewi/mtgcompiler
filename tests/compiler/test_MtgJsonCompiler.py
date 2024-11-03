import unittest
import mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonCompiler as MtgJsonCompiler
import mtgcompiler.frontend.compilers.BaseImplementation as BaseImplementation
import lark


class TestMtgJsonCompiler(unittest.TestCase):
        
        def test_MtgJsonCompiler_isConstructibleWithoutOptions(self):
                compiler = MtgJsonCompiler.MtgJsonCompiler()
                
        def test_MtgJsonCompiler_hasPreprocessorByDefault(self):
                compiler = MtgJsonCompiler.MtgJsonCompiler()
                self.assertTrue(compiler.hasPreprocessor())
                self.assertIsInstance(compiler.getPreprocessor(), BaseImplementation.BasePreprocessor.BasePreprocessor)
                
        def test_MtgJsonCompiler_hasParserByDefault(self):
                compiler = MtgJsonCompiler.MtgJsonCompiler()
                self.assertTrue(compiler.hasParser())      
                
        def test_MtgJsonCompiler_hasPostprocessorByDefault(self):
                compiler = MtgJsonCompiler.MtgJsonCompiler()
                self.assertTrue(compiler.hasPostprocessor())
                self.assertIsInstance(compiler.getPostprocessor(), BaseImplementation.BasePostprocessor.BasePostprocessor)
                
        def test_MtgJsonCompiler_hasTransformerByDefault(self):
                compiler = MtgJsonCompiler.MtgJsonCompiler()
                self.assertTrue(compiler.hasTransformer())
                self.assertIsInstance(compiler.getTransformer(), BaseImplementation.BaseTransformer.BaseTransformer)

        def test_MtgJsonCompiler_canSetParserStartRule(self):
                compiler = MtgJsonCompiler.MtgJsonCompiler(options={"parser.startRule" : "manasymbolexpression"})
                
        def test_MtgJsonCompiler_parserStartRuleMustBeValid(self):
                with self.assertRaises(lark.exceptions.GrammarError):
                    compiler = MtgJsonCompiler.MtgJsonCompiler(options={"parser.startRule" : "nonexistentrule"})
                    
        def testMtgJsonCompiler_canSetLarkDebugMode(self):
            compiler = MtgJsonCompiler.MtgJsonCompiler(options={"parser.larkDebug" : False})
            compiler = MtgJsonCompiler.MtgJsonCompiler(options={"parser.larkDebug" : True})
        
        def test_MtgJsonCompiler_compilerProducesParsedResultsAndAST(self):
                compiler = MtgJsonCompiler.MtgJsonCompiler(options={"parser.startRule" : "manasymbolexpression"})
                result = compiler.compile(textInput="{W}{U}{B}{R}{G}")
                self.assertTrue("parsed_body" in result)
                self.assertTrue("ast" in result)           

                
                
        
if __name__ == '__main__':
    unittest.main()