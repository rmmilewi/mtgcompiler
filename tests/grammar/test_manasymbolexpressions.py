import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestManaSymbolExpressions(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {}
                grammar = grammarian.requestGrammar(imports=["base/manasymbolexpressions.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="manasymbolexpression",debug=True)
                
        def test_1(self):
                self._frontend.parse("{W}")
        
        def test_2(self):
                self._frontend.parse("{U}")
        
        def test_3(self):
                self._frontend.parse("{B}")
        
        def test_4(self):
                self._frontend.parse("{R}")
        
        def test_5(self):
                self._frontend.parse("{G}")
        
        def test_6(self):
                self._frontend.parse("{0}")
        
        def test_7(self):
                self._frontend.parse("{8}")
        
        def test_8(self):
                self._frontend.parse("{X}")
        
        def test_9(self):
                self._frontend.parse("{∞}")
        
        def test_10(self):
                self._frontend.parse("{G/W}")
        
        def test_11(self):
                self._frontend.parse("{W/U}")
        
        def test_12(self):
                self._frontend.parse("{U/B}")
        
        def test_13(self):
                self._frontend.parse("{B/R}")
        
        def test_14(self):
                self._frontend.parse("{R/G}")
        
        def test_15(self):
                self._frontend.parse("{W/B}")
        
        def test_16(self):
                self._frontend.parse("{U/R}")
        
        def test_17(self):
                self._frontend.parse("{B/G}")
        
        def test_18(self):
                self._frontend.parse("{G/U}")
        
        def test_19(self):
                self._frontend.parse("{R/W}")
        
        def test_20(self):
                self._frontend.parse("{S}")
        
        def test_21(self):
                self._frontend.parse("{U/P}")
        
        def test_22(self):
                self._frontend.parse("{HW}")
        
        def test_23(self):
                self._frontend.parse("{R/2}")
                
        def test_23(self):
                self._frontend.parse("{R}{G}{B}{3}")
                
                
if __name__ == '__main__':
        unittest.main()
        