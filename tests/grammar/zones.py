import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestZones(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {"devDefineMissingNames" : True}
                grammar = grammarian.requestGrammar(imports=["base/zones.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="zonedeclarationexpression",debug=True)
                
        def test_1(self):
                self._frontend.parse("the battlefield")
        
        def test_2(self):
                self._frontend.parse("REFERENCEDECORATOR library")

        def test_3(self):
                self._frontend.parse("DECLARATIONDECORATOR hands")

        def test_4(self):
                self._frontend.parse("outside the game")

        def test_5(self):
                self._frontend.parse("anywhere")
        
        def test_6(self):
                self._frontend.parse("libraries")
        
if __name__ == '__main__':
        unittest.main()