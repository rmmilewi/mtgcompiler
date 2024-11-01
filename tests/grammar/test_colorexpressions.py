import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestColorExpressions(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {}
                grammar = grammarian.requestGrammar(imports=["base/colorexpressions.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="colorexpression",debug=True)
                
        def test_1(self):
                self._frontend.parse("white")
        
        def test_2(self):
                self._frontend.parse("blue")
        
        def test_3(self):
                self._frontend.parse("black")
        
        def test_4(self):
                self._frontend.parse("red")
        
        def test_5(self):
                self._frontend.parse("green")
        
        def test_6(self):
                self._frontend.parse("monocolored")
        
        def test_7(self):
                self._frontend.parse("multicolored")
        
        def test_8(self):
                self._frontend.parse("colorless")
        
        def test_9(self):
                self._frontend.parse("red and blue")
        
        def test_10(self):
                self._frontend.parse("white or black")
        
        def test_11(self):
                self._frontend.parse("green, white, and red")
                
        def test_12(self):
                self._frontend.parse("nonblue")
        
                
                
if __name__ == '__main__':
        unittest.main()