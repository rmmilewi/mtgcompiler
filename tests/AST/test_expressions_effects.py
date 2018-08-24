import unittest
import mtgcompiler.AST.expressions
from mtgcompiler.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.AST.expressions import MgColorExpression,MgTypeExpression,MgManaExpression,MgPTExpression,MgNonExpression,MgAndExpression,MgOrExpression,MgTargetExpression,MgAllExpression,MgEachExpression,MgChoiceExpression,MgTapUntapExpression,MgDestroyExpression

class TestMagicExpressions(unittest.TestCase):
        
        def test_DestroyExpressions(self):
                t_creature = MgType(MgType.TypeEnum.Creature)
                typeExpr = MgTypeExpression(t_creature)
                typeExpr.setPlural(True)
                allcreatures = MgAllExpression(typeExpr)
                
                destroyExpr = MgDestroyExpression(allcreatures)
                
                self.assertTrue(destroyExpr.isTraversable())
                self.assertEqual(len(destroyExpr.getTraversalSuccessors()),1)
                self.assertTrue(destroyExpr.isChild(allcreatures))
                self.assertEqual(allcreatures.getParent(),destroyExpr)
                
                self.assertEqual(destroyExpr.unparseToString().lower(),"destroy all creatures")
                
        def test_TapUntapExpressions(self):
                t_creature = MgType(MgType.TypeEnum.Creature)
                typeexpr = MgTypeExpression(t_creature)
                targetExpr = MgTargetExpression(typeexpr)
                
                tapExpr = MgTapUntapExpression(targetExpr,tap=True,untap=False)
                
                self.assertTrue(tapExpr.isTraversable())
                self.assertEqual(len(tapExpr.getTraversalSuccessors()),1)
                self.assertTrue(tapExpr.isChild(targetExpr))
                self.assertEqual(targetExpr.getParent(),tapExpr)
                
                self.assertTrue(tapExpr.isTap())
                self.assertFalse(tapExpr.isUntap())
                self.assertEqual(tapExpr.unparseToString().lower(),"tap target creature")
                
                tapExpr.setTap(False)
                tapExpr.setUntap(True)
                self.assertFalse(tapExpr.isTap())
                self.assertTrue(tapExpr.isUntap())
                self.assertEqual(tapExpr.unparseToString().lower(),"untap target creature")
                
                tapExpr.setTap(True)
                self.assertEqual(tapExpr.unparseToString().lower(),"tap or untap target creature")
        