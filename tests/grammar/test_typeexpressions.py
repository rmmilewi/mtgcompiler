import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestTypeExpressions(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {}
                grammar = grammarian.requestGrammar(imports=["base/typeexpressions.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="typeexpression",debug=True)
                
        def test_1(self):
                self._frontend.parse("elf warrior cleric").pretty()

        def test_2(self):
               self._frontend.parse("island plains")

        def test_3(self):
               self._frontend.parse("ravnica")

        def test_4(self):
               self._frontend.parse("non-zombie")

        def test_5(self):
               self._frontend.parse("artifact")

        def test_6(self):
               self._frontend.parse("legendary creature")

        def test_7(self):
               self._frontend.parse("basic land")

        def test_8(self):
               self._frontend.parse("vanguard")

        def test_9(self):
               self._frontend.parse("aura")

        def test_10(self):
               self._frontend.parse("sorcery")

        def test_11(self):
               self._frontend.parse("elf, goblin, or dwarf")
        
                
                
if __name__ == '__main__':
        unittest.main()