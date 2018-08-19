import unittest
import mtgcompiler.AST.expressions
import mtgcompiler.AST.mtypes
from mtgcompiler.AST.colormana import MgManaSymbol

class TestMagicExpressions(unittest.TestCase):
        
        def test_TypeExpressions(self):
                t_legendary = mtgcompiler.AST.mtypes.MgSupertype(mtgcompiler.AST.mtypes.MgSupertype.SupertypeEnum.Legendary)
                t_human = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Human)
                t_cleric = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Cleric)
                
                texpr = mtgcompiler.AST.expressions.MgTypeExpression(t_legendary,t_human,t_cleric)
                
                self.assertTrue(t_legendary.isTraversable())
                self.assertEqual(len(texpr.getTraversalSuccessors()),3)
                
                self.assertTrue(texpr.isChild(t_legendary))
                self.assertEqual(t_legendary.getParent(),texpr)
                
                self.assertEqual(texpr.unparseToString(),"Legendary Human Cleric")
                
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
                

if __name__ == '__main__':
    unittest.main()