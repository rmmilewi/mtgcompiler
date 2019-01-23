import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestEffectStatements(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {"devDefineMissingNames" : True}
                grammar = grammarian.requestGrammar(imports=["base/statements.grm","base/conditionalstmts.grm","base/effectstatements.grm",
                "base/entities.grm","base/playerdeclrefs.grm","base/timeexpressions.grm",
                "base/objectdeclrefs.grm","base/declrefdecorators.grm","base/valueexpressions.grm",
                "base/modifiers.grm","base/characteristics.grm","base/qualifiers.grm",
                "base/typeexpressions.grm","base/colorexpressions.grm","base/entities.grm",
                "base/zones.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="earley",start="statement",debug=True)
                
        def test_lifegainloss(self):
                self._frontend.parse("you gain 5 life")
                self._frontend.parse("each player gains 1 life")
                self._frontend.parse("at the beginning of each upkeep, you gain 1 life")
                self._frontend.parse("at the end of turn, if an opponent gained life this turn, you gain 2 life")
                self._frontend.parse("players can not gain life")
                self._frontend.parse("you lose 3 life")
                self._frontend.parse("each player loses 2 life")
                self._frontend.parse("an opponent lost life this turn")
        
        def test_sacrifice(self):
                 self._frontend.parse("sacrifice those lands")
                 self._frontend.parse("you may sacrifice a creature")
                 self._frontend.parse("target player sacrifices a creature")
                
        #def test_destroy(self):
        #        self._frontend.parse("destroy target creature")
                
                

        
if __name__ == '__main__':
        unittest.main()