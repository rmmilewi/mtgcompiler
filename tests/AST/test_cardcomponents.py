import unittest
from mtgcompiler.AST.card import MgTypeLine,MgFlavorText
from mtgcompiler.AST.expressions import MgTypeExpression
from mtgcompiler.AST.mtypes import MgSupertype,MgSubtype,MgType

class TestMagicCardComponents(unittest.TestCase):
        def test_TypeLine(self):
                t_legendary = MgSupertype(MgSupertype.SupertypeEnum.Legendary)
                t_creature = MgType(MgType.TypeEnum.Creature)
                t_human = MgSubtype(MgSubtype.CreatureSubtypeEnum.Human)
                t_cleric = MgSubtype(MgSubtype.CreatureSubtypeEnum.Cleric)
                
                texpr_supertypes = MgTypeExpression(t_legendary)
                texpr_types = MgTypeExpression(t_creature)
                texpr_subtypes = MgTypeExpression(t_human,t_cleric)
                
                typeline = MgTypeLine(supertypes=texpr_supertypes,types=texpr_types,subtypes=texpr_subtypes)
                
                self.assertTrue(typeline.isTraversable())
                self.assertEqual(len(typeline.getTraversalSuccessors()),3)
                
                self.assertTrue(typeline.isChild(texpr_types))
                self.assertEqual(texpr_types.getParent(),typeline)
                
                self.assertTrue(typeline.hasSupertype(t_legendary))
                self.assertTrue(typeline.hasType(t_creature))
                self.assertTrue(typeline.hasSubtype(t_human))
                
                self.assertEqual(typeline.unparseToString().lower(),"legendary creature — human cleric")
                
        def testFlavorText(self):
                flavor = "My family protects all families."
                ftext = MgFlavorText(flavor)
                
                self.assertTrue(ftext.isTraversable())
                self.assertEqual(len(ftext.getTraversalSuccessors()),0)
                self.assertEqual(ftext.getFlavor(),flavor)
                
                flavor2 = "It dodges waves of water to prepare for waves of magic."
                ftext.setFlavor(flavor2)
                self.assertEqual(ftext.unparseToString(),flavor2)
                
if __name__ == '__main__':
        unittest.main()