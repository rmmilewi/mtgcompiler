import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestModifiers(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {"devDefineMissingNames" : True}
                grammar = grammarian.requestGrammar(imports=["base/modifiers.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="modifier",debug=True)
                
        def test_1(self):
                self._frontend.parse("triggered")
        
        def test_2(self):
                self._frontend.parse("tapped")

        def test_3(self):
                self._frontend.parse("attached only to DECLARATIONORREFERENCE")

        def test_4(self):
                self._frontend.parse("under REFERENCEDECORATOR control")

        def test_5(self):
                self._frontend.parse("fortified")

        def test_6(self):
                self._frontend.parse("blocking")
                
if __name__ == '__main__':
        unittest.main()