import unittest
import mtgcompiler.AST.expressions
from mtgcompiler.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.AST.expressions import MgNumberValue,MgColorExpression,MgTypeExpression,MgModalExpression
from mtgcompiler.AST.expressions import MgManaExpression,MgPTExpression,MgNonExpression,MgAndExpression
from mtgcompiler.AST.expressions import MgOrExpression,MgTargetExpression,MgAllExpression,MgEachExpression
from mtgcompiler.AST.expressions import MgChoiceExpression,MgTapUntapExpression,MgDestroyExpression
from mtgcompiler.AST.reference import MgQualifier

class TestCommonExpressions(unittest.TestCase):
        
        def test_ValueComparisons(self):
                pass
        
        def test_NumberValues(self):
                five_literal = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                self.assertTrue(five_literal.isLiteral())
                self.assertTrue(five_literal.isTraversable())
                self.assertEqual(len(five_literal.getTraversalSuccessors()),0)
                self.assertEqual(five_literal.unparseToString().lower(),"5")
                
                seventytwo_quantity = MgNumberValue(72,MgNumberValue.NumberTypeEnum.Cardinal)
                self.assertTrue(seventytwo_quantity.isQuantity())
                self.assertEqual(seventytwo_quantity.unparseToString().lower(),"seventy-two")
                
                one_frequency = MgNumberValue(1,MgNumberValue.NumberTypeEnum.Frequency)
                self.assertTrue(one_frequency.isFrequency())
                self.assertEqual(one_frequency.unparseToString().lower(),"once")
                
                two_frequency = MgNumberValue(2,MgNumberValue.NumberTypeEnum.Frequency)
                self.assertTrue(two_frequency.isFrequency())
                self.assertEqual(two_frequency.unparseToString().lower(),"twice")
                
                three_frequency = MgNumberValue(3,MgNumberValue.NumberTypeEnum.Frequency)
                self.assertTrue(three_frequency.isFrequency())
                self.assertEqual(three_frequency.unparseToString().lower(),"three times")
                
                four_ordinal = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Ordinal)
                self.assertTrue(four_ordinal.isOrdinal())
                self.assertEqual(four_ordinal.unparseToString().lower(),"fourth")
                
                seventytwo_quantity.setFrequency()
                self.assertTrue(seventytwo_quantity.isFrequency())
                self.assertEqual(seventytwo_quantity.getValue(),72)
                seventytwo_quantity.setValue(73)
                self.assertEqual(seventytwo_quantity.unparseToString().lower(),"seventy-three times")
                
                star_custom = MgNumberValue("*",MgNumberValue.NumberTypeEnum.Custom)
                self.assertTrue(star_custom.isCustom())
                self.assertEqual(star_custom.unparseToString().lower(),"*")
                
        
        def test_ColorExpressions(self):
                multicolored = MgColorTerm(MgColorTerm.ColorTermEnum.Multicolored)
                multicoloredExpr = MgColorExpression(multicolored)
                self.assertEqual(multicoloredExpr.unparseToString().lower(),"multicolored")
                
                red = MgColorTerm(MgColorTerm.ColorTermEnum.Red)
                green = MgColorTerm(MgColorTerm.ColorTermEnum.Green)
                andExpr = MgAndExpression(red,green)
                rgExpr = MgColorExpression(andExpr)
                self.assertEqual(rgExpr.unparseToString().lower(),"red and green")
                
                self.assertTrue(rgExpr.isTraversable())
                self.assertEqual(len(rgExpr.getTraversalSuccessors()),1)
                
                self.assertTrue(rgExpr.isChild(andExpr))
                self.assertEqual(andExpr.getParent(),rgExpr)
                
                white = MgColorTerm(MgColorTerm.ColorTermEnum.White)
                andThenWhite = MgAndExpression(andExpr,white)
                rgExpr.setValue(andThenWhite)
                self.assertEqual(rgExpr.getValue(),andThenWhite)
                self.assertEqual(rgExpr.unparseToString().lower(),"red and green and white")
                
        def test_TypeExpressions(self):
                t_legendary = MgSupertype(MgSupertype.SupertypeEnum.Legendary)
                t_human = MgSubtype(MgSubtype.CreatureSubtypeEnum.Human)
                t_cleric = MgSubtype(MgSubtype.CreatureSubtypeEnum.Cleric)
                
                texpr = MgTypeExpression(t_legendary,t_human,t_cleric)
                
                self.assertTrue(t_legendary.isTraversable())
                self.assertEqual(len(texpr.getTraversalSuccessors()),3)
                
                self.assertTrue(texpr.isChild(t_legendary))
                self.assertEqual(t_legendary.getParent(),texpr)
                
                self.assertEqual(texpr.unparseToString().lower(),"legendary human cleric")
                
                ##test pluralization
                #texpr.setPlural(True)
                #self.assertEqual(texpr.unparseToString().lower(),"legendary human clerics")
                
                #test comma delimitation.
                nonvampire = MgNonExpression(MgSubtype(MgSubtype.CreatureSubtypeEnum.Vampire))
                nonwerewolf = MgNonExpression(MgSubtype(MgSubtype.CreatureSubtypeEnum.Werewolf))
                nonzombie = MgNonExpression(MgSubtype(MgSubtype.CreatureSubtypeEnum.Zombie))
                t_creature = MgType(MgType.TypeEnum.Creature)
                
                commaExpr = MgTypeExpression(nonvampire,nonwerewolf,nonzombie,t_creature)
                commaExpr.setCommaDelimited(True)
                self.assertEqual(commaExpr.unparseToString().lower(),"non-vampire, non-werewolf, non-zombie creature")
                
                
        def test_ManaExpressions(self):
                s0 = MgManaSymbol(cvalue=1)
                s1 = MgManaSymbol(colorv=MgManaSymbol.ManaType.Red)
                s2 = MgManaSymbol(colorv=MgManaSymbol.ManaType.Green)
                s3 = MgManaSymbol(colorv=MgManaSymbol.ManaType.White)
                mexpr = MgManaExpression(s0,s1,s2,s3)
                
                self.assertTrue(mexpr.isTraversable())
                self.assertEqual(len(mexpr.getTraversalSuccessors()),4)
                
                self.assertTrue(mexpr.isChild(s0))
                self.assertEqual(s0.getParent(),mexpr)
                
                self.assertEqual(mexpr.unparseToString(),"{1}{R}{G}{W}")
                
        def test_PowerToughnessExpressions(self):
                one_power = MgNumberValue(1,MgNumberValue.NumberTypeEnum.Literal)
                three_toughness = MgNumberValue(3,MgNumberValue.NumberTypeEnum.Literal)
                one_three = MgPTExpression(one_power,three_toughness)
                
                self.assertTrue(one_three.isTraversable())
                self.assertEqual(len(one_three.getTraversalSuccessors()),2)
                self.assertTrue(one_three.isChild(one_power))
                self.assertEqual(three_toughness.getParent(),one_three)
                self.assertEqual(one_three.unparseToString().lower(),"1/3")
                
        def test_NonExpressions(self):
                t_ferret = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Ferret)
                nonferret = MgNonExpression(t_ferret)
                self.assertEqual(nonferret.unparseToString().lower(),"non-ferret")
                
                self.assertTrue(nonferret.isTraversable())
                self.assertEqual(len(nonferret.getTraversalSuccessors()),1)
                self.assertTrue(nonferret.isChild(t_ferret))
                self.assertEqual(t_ferret.getParent(),nonferret)                
                
                t_legendary = MgSupertype(MgSupertype.SupertypeEnum.Legendary)
                nonlegendary = MgNonExpression(t_legendary)
                t_creature = MgType(MgType.TypeEnum.Creature)
                typeexpr = MgTypeExpression(nonlegendary,t_creature)
                self.assertEqual(typeexpr.unparseToString().lower(),"non-legendary creature")
                
        def test_TargetExpressions(self):
                t_artifact = MgType(MgType.TypeEnum.Artifact)
                t_creature = MgType(MgType.TypeEnum.Creature)
                typeexpr = MgTypeExpression(t_artifact,t_creature)
                
                targetExpr = MgTargetExpression(typeexpr)
                
                self.assertEqual(targetExpr.unparseToString().lower(),"target artifact creature")
                
        def test_ModalExpressions(self):
                pass
                
        def test_UntilExpressions(self):
                pass
                
        def test_AllExpressions(self):
                pass
                
        def test_EachExpressions(self):
                pass
        
        def test_ChoiceExpressions(self):
                pass
                
                

if __name__ == '__main__':
    unittest.main()