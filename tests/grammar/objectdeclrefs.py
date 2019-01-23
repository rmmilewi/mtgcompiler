import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestObjectDeclarationsAndReferences(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {"devDefineMissingNames" : True}
                grammar = grammarian.requestGrammar(imports=["base/objectdeclrefs.grm","base/declrefdecorators.grm","base/valueexpressions.grm",
                "base/modifiers.grm","base/characteristics.grm","base/qualifiers.grm","base/typeexpressions.grm","base/colorexpressions.grm","base/entities.grm","base/zones.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="objectdeclref",debug=True)
                
        def test_1(self):
                self._frontend.parse("an elf")
                self._frontend.parse("that elf")
                self._frontend.parse("green elf creatures")
                self._frontend.parse("three 1/1 green elf warrior creatures")
                
        def test_2(self):
                self._frontend.parse("target tapped creature")
                self._frontend.parse("target nonwhite creature")
                self._frontend.parse("target monocolored spell")
        
        def test_3(self):
                self._frontend.parse("a card")
                self._frontend.parse("two cards")
                #self._frontend.parse("a card from your hand")
                
                
                

        
if __name__ == '__main__':
        unittest.main()