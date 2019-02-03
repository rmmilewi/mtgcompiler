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
                self._frontend.parse("players can not lose life")
                self._frontend.parse("you lose 3 life")
                self._frontend.parse("each player loses 2 life")
                self._frontend.parse("an opponent lost life this turn")
        
        def test_sacrifice(self):
                self._frontend.parse("sacrifice a creature")
                self._frontend.parse("you may sacrifice a creature")
                self._frontend.parse("target player sacrifices a creature")
                self._frontend.parse("at the end of turn, if you sacrificed a creature this turn, you may have target opponent sacrifice a creature")
        
        def test_destroy(self):
                self._frontend.parse("destroy target nonblack creature")
                self._frontend.parse("destroy all creatures")
                self._frontend.parse("you gain 2 life for each creature destroyed this way")
                 
        def test_tapuntap(self):
                self._frontend.parse("tap target creature")
                self._frontend.parse("tap a untapped creature")
                self._frontend.parse("untap all creatures")
                
        def test_dealdamage(self):
                self._frontend.parse("~ deals 2 damage to another target creature")
                self._frontend.parse("~ deals 2 damage to any target")
                self._frontend.parse("~ dealt damage this turn")
                self._frontend.parse("~ dealt combat damage equal to 5 this turn")
                self._frontend.parse("it deals that much damage plus 1 to that permanent or player")
                
                
        def test_preventdamage(self):
                self._frontend.parse("prevent the next 2 damage")
                self._frontend.parse("all damage prevented this way")
                self._frontend.parse("prevent that damage")
                self._frontend.parse("prevent the next 1 damage that would be dealt to any target this turn")
                
                

        
if __name__ == '__main__':
        unittest.main()