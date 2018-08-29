import unittest
from mtgcompiler.AST.reference import MgQualifier
from mtgcompiler.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.AST.expressions import MgDescriptionExpression,MgNumberValue,MgColorExpression,MgTypeExpression,MgModalExpression
from mtgcompiler.AST.expressions import MgManaExpression,MgPTExpression,MgNonExpression,MgAndExpression
from mtgcompiler.AST.expressions import MgOrExpression,MgTargetExpression,MgAllExpression,MgEachExpression
from mtgcompiler.AST.expressions import MgChoiceExpression,MgTapUntapExpression,MgDestroyExpression,MgUncastExpression
from  mtgcompiler.AST.expressions import MgCreateTokenExpression
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
                
        def test_UncastExpressions(self):
                
                t_nonenchantment =  MgTypeExpression(MgNonExpression(MgType(MgType.TypeEnum.Enchantment)))
                q_spell = MgQualifier(MgQualifier.QualifierEnum.Spell)
                description = MgDescriptionExpression(t_nonenchantment,q_spell)
                targetExpr = MgTargetExpression(description)
                
                uncastExpr = MgUncastExpression(targetExpr)
                
                self.assertTrue(uncastExpr.isTraversable())
                self.assertEqual(len(uncastExpr.getTraversalSuccessors()),1)
                self.assertTrue(uncastExpr.isChild(targetExpr))
                self.assertEqual(targetExpr.getParent(),uncastExpr)
                
                self.assertEqual(uncastExpr.unparseToString().lower(),"counter target non-enchantment spell")
                
        def test_CreateTokenExpressions(self):
                
                saproling_description = MgDescriptionExpression(
                        MgPTExpression(
                                MgNumberValue(1,MgNumberValue.NumberTypeEnum.Literal),
                                MgNumberValue(1,MgNumberValue.NumberTypeEnum.Literal)
                        ), #1/1
                        MgColorExpression(MgColorTerm(MgColorTerm.ColorTermEnum.Green)), #green
                        MgTypeExpression(MgSubtype(MgSubtype.CreatureSubtypeEnum.Saproling),MgType(MgType.TypeEnum.Creature)), #saproling creature
                        MgQualifier(MgQualifier.QualifierEnum.Token) #token
                )
                three_of_them = MgNumberValue(3,MgNumberValue.NumberTypeEnum.Quantity)
                create_three_saprolings = MgCreateTokenExpression(descriptor=saproling_description,quantity=three_of_them)
                
                self.assertTrue(create_three_saprolings.isTraversable())
                self.assertEqual(len(create_three_saprolings.getTraversalSuccessors()),2)
                self.assertTrue(create_three_saprolings.isChild(saproling_description))
                self.assertEqual(saproling_description.getParent(),create_three_saprolings)
                self.assertTrue(create_three_saprolings.isChild(three_of_them))
                self.assertEqual(three_of_them.getParent(),create_three_saprolings)
                
                self.assertEqual(uncastExpr.unparseToString().lower(),"create three 1/1 green saproling creature token")
                
                
                
                
                
if __name__ == '__main__':
    unittest.main()
        