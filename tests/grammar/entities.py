import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestEntityExpressions(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {"devDefineMissingNames" : True}
                grammar = grammarian.requestGrammar(imports=["base/entities.grm","base/playerdeclrefs.grm","base/declrefdecorators.grm","base/valueexpressions.grm",
                "base/modifiers.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="entityexpression",debug=True)
                
        def test_1(self):
                self._frontend.parse("you and an opponent")
                self._frontend.parse("a player and their team")
                self._frontend.parse("your team and/or their team")
                self._frontend.parse("its controller or its owner")
                self._frontend.parse("you, an opponent, and its controller")

        
if __name__ == '__main__':
        unittest.main()