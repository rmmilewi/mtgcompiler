import unittest
import mtgcompiler.AST.expressions
from mtgcompiler.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.AST.colormana import MgManaSymbol

class TestMagicExpressions(unittest.TestCase):
        
        def test_TypeExpressions(self):
                t_legendary = MgSupertype(MgSupertype.SupertypeEnum.Legendary)
                t_human = MgSubtype(MgSubtype.CreatureSubtypeEnum.Human)
                t_cleric = MgSubtype(MgSubtype.CreatureSubtypeEnum.Cleric)
                
                texpr = mtgcompiler.AST.expressions.MgTypeExpression(t_legendary,t_human,t_cleric)
                
                self.assertTrue(t_legendary.isTraversable())
                self.assertEqual(len(texpr.getTraversalSuccessors()),3)
                
                self.assertTrue(texpr.isChild(t_legendary))
                self.assertEqual(t_legendary.getParent(),texpr)
                
                self.assertEqual(texpr.unparseToString().lower(),"legendary human cleric")
                
                #test pluralization
                texpr.setPlural(True)
                self.assertEqual(texpr.unparseToString().lower(),"legendary human clerics")
                
                #test comma delimitation.
                nonvampire = mtgcompiler.AST.expressions.MgNonExpression(MgSubtype(MgSubtype.CreatureSubtypeEnum.Vampire))
                nonwerewolf = mtgcompiler.AST.expressions.MgNonExpression(MgSubtype(MgSubtype.CreatureSubtypeEnum.Werewolf))
                nonzombie = mtgcompiler.AST.expressions.MgNonExpression(MgSubtype(MgSubtype.CreatureSubtypeEnum.Zombie))
                t_creature = MgType(MgType.TypeEnum.Creature)
                
                commaExpr = mtgcompiler.AST.expressions.MgTypeExpression(nonvampire,nonwerewolf,nonzombie,t_creature)
                commaExpr.setCommaDelimited(True)
                self.assertEqual(commaExpr.unparseToString().lower(),"non-vampire, non-werewolf, non-zombie creature")
                
                
                
        def test_ManaExpressions(self):
                s0 = MgManaSymbol(cvalue=1)
                s1 = MgManaSymbol(colorv=MgManaSymbol.ManaType.Red)
                s2 = MgManaSymbol(colorv=MgManaSymbol.ManaType.Green)
                s3 = MgManaSymbol(colorv=MgManaSymbol.ManaType.White)
                mexpr = mtgcompiler.AST.expressions.MgManaExpression(s0,s1,s2,s3)
                
                self.assertTrue(mexpr.isTraversable())
                self.assertEqual(len(mexpr.getTraversalSuccessors()),4)
                
                self.assertTrue(mexpr.isChild(s0))
                self.assertEqual(s0.getParent(),mexpr)
                
                self.assertEqual(mexpr.unparseToString(),"{1}{R}{G}{W}")
                
        def test_NonExpressions(self):
                t_ferret = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Ferret)
                nonferret = mtgcompiler.AST.expressions.MgNonExpression(t_ferret)
                self.assertEqual(nonferret.unparseToString(),"non-Ferret")
                
                self.assertTrue(nonferret.isTraversable())
                self.assertEqual(len(nonferret.getTraversalSuccessors()),1)
                self.assertTrue(nonferret.isChild(t_ferret))
                self.assertEqual(t_ferret.getParent(),nonferret)                
                
                t_legendary = MgSupertype(MgSupertype.SupertypeEnum.Legendary)
                nonlegendary = mtgcompiler.AST.expressions.MgNonExpression(t_legendary)
                t_creature = MgType(MgType.TypeEnum.Creature)
                typeexpr = mtgcompiler.AST.expressions.MgTypeExpression(nonlegendary,t_creature)
                self.assertEqual(typeexpr.unparseToString().lower(),"non-legendary creature")
                
        def test_TargetExpressions(self):
                
                t_artifact = MgType(MgType.TypeEnum.Artifact)
                t_creature = MgType(MgType.TypeEnum.Creature)
                typeexpr = mtgcompiler.AST.expressions.MgTypeExpression(t_artifact,t_creature)
                
                targetExpr = mtgcompiler.AST.expressions.MgTargetExpression(typeexpr)
                
                self.assertEqual(targetExpr.unparseToString().lower(),"target artifact creature")
                
        def test_AllExpressions(self):
                pass
                
        def test_EachExpressions(self):
                pass
        
        def test_ChoiceExpressions(self):
                pass
                
        def test_DestroyExpressions(self):
                t_creature = MgType(MgType.TypeEnum.Creature)
                typeExpr = mtgcompiler.AST.expressions.MgTypeExpression(t_creature)
                typeExpr.setPlural(True)
                allcreatures = mtgcompiler.AST.expressions.MgAllExpression(typeExpr)
                
                destroyExpr = mtgcompiler.AST.expressions.MgDestroyExpression(allcreatures)
                
                self.assertTrue(destroyExpr.isTraversable())
                self.assertEqual(len(destroyExpr.getTraversalSuccessors()),1)
                self.assertTrue(destroyExpr.isChild(allcreatures))
                self.assertEqual(allcreatures.getParent(),destroyExpr)
                
                self.assertEqual(destroyExpr.unparseToString().lower(),"destroy all creatures")
                
                

if __name__ == '__main__':
    unittest.main()