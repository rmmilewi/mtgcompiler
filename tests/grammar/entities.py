import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestEntityExpressions(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {"devDefineMissingNames" : True}
                grammar = grammarian.requestGrammar(imports=["base/entities.grm","base/playerdeclrefs.grm","base/objectdeclrefs.grm",
                "base/declrefdecorators.grm","base/valueexpressions.grm","base/modifiers.grm","base/characteristics.grm","base/qualifiers.grm",
                "base/typeexpressions.grm","base/colorexpressions.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="earley",start="entityexpression",debug=True)
                
        def test_players(self):
                self._frontend.parse("you")
                self._frontend.parse("you and an opponent")
                self._frontend.parse("a player and their team")
                self._frontend.parse("your team and/or their team")
                self._frontend.parse("its controller or its owner")
                self._frontend.parse("you, an opponent, and its controller")
                
        def test_objects(self):
                self._frontend.parse("an elf and a goblin")
                self._frontend.parse("target artifact or enchantment")
                self._frontend.parse("all creatures and all lands")
                self._frontend.parse("target creature, target enchantment, and target artifact")
                
        
        def test_objectsandplayers(self):
                self._frontend.parse("target creature and its controller")

        
if __name__ == '__main__':
        unittest.main()