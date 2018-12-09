import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestQualifiers(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {"devDefineMissingNames" : True}
                grammar = grammarian.requestGrammar(imports=["base/qualifiers.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="qualifier",debug=True)
                
        def test_1(self):
                self._frontend.parse("ability")
        
        def test_2(self):
                self._frontend.parse("abilities")

        def test_3(self):
                self._frontend.parse("card")

        def test_4(self):
                self._frontend.parse("cards")

        def test_5(self):
                self._frontend.parse("effect")
                
if __name__ == '__main__':
        unittest.main()