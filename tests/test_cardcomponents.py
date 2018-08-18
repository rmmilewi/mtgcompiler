import unittest
import mtgcompiler.AST.card
import mtgcompiler.AST.expressions
import mtgcompiler.AST.mtypes

class TestMagicCardComponents(unittest.TestCase):
        def test_TypeLine(self):
                t_legendary = mtgcompiler.AST.mtypes.MgSupertype(mtgcompiler.AST.mtypes.MgSupertype.SupertypeEnum.Legendary)
                t_creature = mtgcompiler.AST.mtypes.MgType(mtgcompiler.AST.mtypes.MgType.TypeEnum.Creature)
                t_human = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Human)
                t_cleric = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Cleric)
                
                texpr_supertypes = mtgcompiler.AST.expressions.MgTypeExpression(t_legendary)
                texpr_types = mtgcompiler.AST.expressions.MgTypeExpression(t_creature)
                texpr_subtypes = mtgcompiler.AST.expressions.MgTypeExpression(t_human,t_cleric)
                
                typeline = mtgcompiler.AST.card.MgTypeLine(supertypes=texpr_supertypes,types=texpr_types,subtypes=texpr_subtypes)
                
                self.assertTrue(typeline.isTraversable())
                self.assertEqual(len(typeline.getTraversalSuccessors()),3)
                
                self.assertTrue(typeline.isChild(texpr_types))
                self.assertEqual(texpr_types.getParent(),typeline)
                
                self.assertTrue(typeline.hasSupertype(t_legendary))
                self.assertTrue(typeline.hasType(t_creature))
                self.assertTrue(typeline.hasSubtype(t_human))
                
                self.assertEqual(typeline.unparseToString(),"Legendary Creature — Human Cleric")
                
if __name__ == '__main__':
        unittest.main()