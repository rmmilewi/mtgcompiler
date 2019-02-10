import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestCharacteristics(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {"devDefineMissingNames" : True}
                grammar = grammarian.requestGrammar(imports=["base/characteristics.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="characteristicdeclarationexpression",debug=True)
                
        def test_1(self):
                self._frontend.parse("maximum hand size")
        
        def test_2(self):
                self._frontend.parse("card types")

        def test_3(self):
                self._frontend.parse("base toughness")

        def test_4(self):
                self._frontend.parse("power")

        def test_5(self):
                self._frontend.parse("base power")
        
        def test_6(self):
                self._frontend.parse("life modifier")
        
        def test_7(self):
                self._frontend.parse("converted mana cost")
                
        def test_8(self):
                self._frontend.parse("no maximum hand size")
        
if __name__ == '__main__':
        unittest.main()