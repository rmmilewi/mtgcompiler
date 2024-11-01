import unittest
from mtgcompiler.frontend.AST.reference import MgQualifier,MgNameReference,MgDamageType
from mtgcompiler.frontend.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.frontend.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.frontend.AST.expressions import MgDescriptionExpression,MgNumberValue,MgColorExpression,MgTypeExpression,MgModalExpression
from mtgcompiler.frontend.AST.expressions import MgManaExpression,MgPTExpression,MgNonExpression,MgAndExpression
from mtgcompiler.frontend.AST.expressions import MgOrExpression,MgTargetExpression,MgAllExpression,MgEachExpression
from mtgcompiler.frontend.AST.expressions import MgChoiceExpression,MgTapUntapExpression,MgDestroyExpression,MgUncastExpression
from  mtgcompiler.frontend.AST.expressions import MgCreateTokenExpression,MgDealsDamageExpression
class TestMagicExpressions(unittest.TestCase):
        
        def test_DestroyExpressions(self):
                t_creature = MgType(MgType.TypeEnum.Creature)
                typeExpr = MgTypeExpression(t_creature)
                allcreatures = MgAllExpression(typeExpr)
                
                destroyExpr = MgDestroyExpression(allcreatures)
                
                self.assertTrue(destroyExpr.isTraversable())
                self.assertEqual(len(destroyExpr.getTraversalSuccessors()),1)
                self.assertTrue(destroyExpr.isChild(allcreatures))
                self.assertEqual(allcreatures.getParent(),destroyExpr)
                
                self.assertEqual(destroyExpr.unparseToString().lower(),"destroy all creature")
                
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
                
        def test_DealsDamageExpressions(self):
                nameref = MgNameReference(None)
                one = MgNumberValue(1,MgNumberValue.NumberTypeEnum.Literal)
                any_target = MgTargetExpression(isAny=True)
                damageType = MgDamageType(damageType=MgDamageType.DamageTypeEnum.RegularDamage)
                
                damageexpr_0 = MgDealsDamageExpression(origin=nameref,damageType=damageType,damageExpression=one,subject=any_target)
                
                self.assertTrue(damageexpr_0.isTraversable())
                self.assertEqual(len(damageexpr_0.getTraversalSuccessors()),2)
                self.assertTrue(damageexpr_0.isChild(any_target))
                self.assertEqual(any_target.getParent(),damageexpr_0)
                
                self.assertEqual(damageexpr_0.getOrigin(),nameref)
                self.assertTrue(damageexpr_0.hasDamageExpression())
                self.assertEqual(damageexpr_0.getDamageExpression(),one)
                self.assertTrue(damageexpr_0.hasSubject())
                self.assertEqual(damageexpr_0.getSubject(),any_target)
                
                self.assertEqual(damageexpr_0.unparseToString().lower(),"~ deal(s) 1 damage to any target")
                
                
                
                
        def test_CreateTokenExpressions(self):
                
                saproling_description = MgDescriptionExpression(
                        #1/1
                        MgPTExpression(
                                MgNumberValue(1,MgNumberValue.NumberTypeEnum.Literal),
                                MgNumberValue(1,MgNumberValue.NumberTypeEnum.Literal)
                        ),
                        #green
                        MgColorExpression(MgColorTerm(MgColorTerm.ColorTermEnum.Green)), 
                        #saproling creature
                        MgTypeExpression(MgSubtype(MgSubtype.CreatureSubtypeEnum.Saproling),MgType(MgType.TypeEnum.Creature)),
                        #token
                        MgQualifier(MgQualifier.QualifierEnum.Token)
                )
                three_of_them = MgNumberValue(3,MgNumberValue.NumberTypeEnum.Cardinal)
                create_three_saprolings = MgCreateTokenExpression(descriptor=saproling_description,quantity=three_of_them)
                
                self.assertTrue(create_three_saprolings.isTraversable())
                self.assertEqual(len(create_three_saprolings.getTraversalSuccessors()),2)
                self.assertTrue(create_three_saprolings.isChild(saproling_description))
                self.assertEqual(saproling_description.getParent(),create_three_saprolings)
                self.assertTrue(create_three_saprolings.isChild(three_of_them))
                self.assertEqual(three_of_them.getParent(),create_three_saprolings)
                
                self.assertEqual(create_three_saprolings.unparseToString().lower(),"create three 1/1 green saproling creature token")
                
                
                
                
                
if __name__ == '__main__':
    unittest.main()
        