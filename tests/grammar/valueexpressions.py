import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestValueExpressions(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {}
                grammar = grammarian.requestGrammar(imports=["base/valueexpressions.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="valueexpression",debug=True)
                
        def test_1(self):
                self._frontend.parse("three thousand nine hundred thirty five")
                
        def test_2(self):
                self._frontend.parse("thirteen times")
        
        def test_3(self):
                self._frontend.parse("twice")
        
        def test_4(self):
                self._frontend.parse("eighth")
        
        def test_5(self):
                self._frontend.parse("fourth")
        
        def test_6(self):
                self._frontend.parse("ninetieth")
        
        def test_7(self):
                self._frontend.parse("ninety first")
        
        def test_8(self):
                self._frontend.parse("one million one hundred thousand")
        
        def test_9(self):
                self._frontend.parse("5")
        
        def test_10(self):
                self._frontend.parse("-3")
        
        def test_11(self):
                self._frontend.parse("*")
        
        def test_12(self):
                self._frontend.parse("x")
        
        def test_13(self):
                self._frontend.parse("equal to five")
        
        def test_14(self):
                self._frontend.parse("three or greater")
        
        def test_15(self):
                self._frontend.parse("less than or equal to 7")
        
        def test_16(self):
                self._frontend.parse("up to thirty times")
        
        def test_17(self):
                self._frontend.parse("that much")
        
        def test_18(self):
                self._frontend.parse("that many")
        
        def test_19(self):
                self._frontend.parse("three times that much")
        
        def test_20(self):
                self._frontend.parse("two plus three")
        
        def test_21(self):
                self._frontend.parse("fifteen times that much rounded down")
        
                

if __name__ == '__main__':
        unittest.main()