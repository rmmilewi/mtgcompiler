import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!
from lark.tree import pydot__tree_to_png #For rendering the parse tree.

class TestEffectStatements(unittest.TestCase):
        
        def makedot(self,tree):
                pydot__tree_to_png(tree, "lark_test.png")
        
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
                self._frontend.parse("prevent all combat damage that would be dealt this turn")
                
        def test_drawdiscard(self):
                self._frontend.parse("draw two cards")
                self._frontend.parse("if you drew a card this turn, draw a card")
                self._frontend.parse("target player draws a card")
                self._frontend.parse("if you draw a card named ~, you gain two life")
                self._frontend.parse("if an opponent drew three or more cards this turn, you gain two life")
                self._frontend.parse("draw a card, then draw cards equal to the number of cards named ~ in all graveyards") #Accumulated Knowledge
                self._frontend.parse("discard a card")
                self._frontend.parse("discard your hand") #One with Nothing
                self._frontend.parse("discard the last card that you drew this turn") #Jandor's Ring, added 'that' for relative clause
                
        def test_castuncast(self):
                self._frontend.parse("you may cast a spell")
                self._frontend.parse("whenever an opponent casts a blue spell during your turn, you may create a 4/4 green elemental creature token")
                #self._frontend.parse("whenever you cast a spell that is both red and white")
                self._frontend.parse("counter target spell")
                self._frontend.parse("~ can not be countered")
                self._frontend.parse("~ can not be countered by spells or abilities")
                
                
        def test_enterleave(self):
                self._frontend.parse("when ~ enters the battlefield, draw a card")
                self._frontend.parse("when ~ leaves the battlefield, draw a card")
                
        def test_choose(self):
                self._frontend.parse("choose artifact, enchantment, instant, sorcery, or planeswalker")
                self._frontend.parse("choose two")
                self._frontend.parse("choose one or both")
                self._frontend.parse("choose a creature type")
                self._frontend.parse("each player chooses a color")
                self._frontend.parse("each player chooses «war» or «peace»")
                self._frontend.parse("if a player chose «cake», you may draw a card")
        
        def test_getgain(self):
                self._frontend.parse("target creature gets -3/-3 until end of turn")
                #self.makedot(self._frontend.parse("except for elves named «john», all elf creatures gets +1/+1 until end of turn"))
                #self._frontend.parse("creatures you control get +1/+1")
                

        
if __name__ == '__main__':
        unittest.main()