import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestPlayerDeclarationsAndReferences(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {"devDefineMissingNames" : True}
                grammar = grammarian.requestGrammar(imports=["base/playerdeclrefs.grm","base/declrefdecorators.grm","base/valueexpressions.grm",
                "base/modifiers.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="playerdeclref",debug=True)
                
        def test_1(self):
                self._frontend.parse("you")
                self._frontend.parse("players")
                self._frontend.parse("opponents")
                self._frontend.parse("each player")
                self._frontend.parse("another opponent")
                self._frontend.parse("the team")
                self._frontend.parse("they")
                self._frontend.parse("that owner")
                self._frontend.parse("the controller")
                
        def test_2(self):
                self._frontend.parse("the third player")
                self._frontend.parse("the active player")
                self._frontend.parse("attacking players")
                self._frontend.parse("a defending player")
                self._frontend.parse("each player who STATEMENT")
                self._frontend.parse("its controller")
                self._frontend.parse("their controllers")
                self._frontend.parse("that player's team")
                

        
if __name__ == '__main__':
        unittest.main()