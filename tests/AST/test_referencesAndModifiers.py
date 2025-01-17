import unittest
from mtgcompiler.frontend.AST.reference import MgName, MgThatReference,MgSelfReference,MgNameReference,MgQualifier
from mtgcompiler.frontend.AST.reference import MgAbilityModifier,MgCombatStatusModifier,MgKeywordStatusModifier,MgTapStatusModifier,MgEffectStatusModifier
from mtgcompiler.frontend.AST.colormana import MgColorTerm
from mtgcompiler.frontend.AST.mtypes import MgType
from mtgcompiler.frontend.AST.expressions import MgDescriptionExpression,MgTypeExpression,MgTargetExpression,MgColorExpression

class TestReferences(unittest.TestCase):
        
        def test_nameReferences(self):
                name = MgName("Keldon Warcaller")
                
                nameref = MgNameReference(nameref=name)
                
                self.assertTrue(nameref.isTraversable())
                self.assertEqual(len(nameref.getTraversalSuccessors()),0)
                self.assertTrue(nameref.hasAntecedent())
                nameref.setAntecedent(name)
                self.assertEqual(nameref.getAntecedent(),name)
                self.assertEqual(nameref.unparseToString().lower(),name.unparseToString().lower())
                
                name = MgName("Arashi, the Sky Asunder")
                nameref = MgNameReference(nameref=name,firstNameOnly=True)
                self.assertTrue(nameref.isFirstNameOnly())
                self.assertEqual(nameref.unparseToString().lower(),"arashi")
                nameref.setFirstNameOnly(False)
                self.assertFalse(nameref.isFirstNameOnly())
                self.assertTrue(nameref.unparseToString().lower(),"arashi, the sky asunder")
        
        def test_selfReferences(self):
                creature_description = MgDescriptionExpression(MgTypeExpression(MgType(MgType.TypeEnum.Creature)))
                targetExpr = MgTargetExpression(creature_description)
                
                selfref = MgSelfReference(reftype=MgSelfReference.SelfEnum.Neutral,antecedent=creature_description)
                
                self.assertTrue(selfref.isTraversable())
                self.assertEqual(len(selfref.getTraversalSuccessors()),0)
                self.assertTrue(selfref.hasAntecedent())
                selfref.setAntecedent(creature_description)
                self.assertEqual(selfref.getAntecedent(),creature_description)
                self.assertTrue(selfref.isNeutral())
                self.assertEqual(selfref.unparseToString().lower(),"itself")
                
                selfref.setNeutral()
                selfref.setMale()
                self.assertTrue(selfref.isMale())
                self.assertEqual(selfref.unparseToString().lower(),"himself")
                
                selfref.setFemale()
                self.assertTrue(selfref.isFemale())
                self.assertEqual(selfref.unparseToString().lower(),"herself")
                
        
        def test_thatReferences(self):
                color_white = MgColorExpression(MgColorTerm(MgColorTerm.ColorTermEnum.White))
                t_enchantment = MgTypeExpression(MgType(MgType.TypeEnum.Enchantment))
                original_enchantment_description = MgDescriptionExpression(color_white,t_enchantment)
                targetExpr = MgTargetExpression(original_enchantment_description)
                
                
                descriptor_enchantment = MgDescriptionExpression(MgTypeExpression(MgType(MgType.TypeEnum.Enchantment)))
                thatref_enchantment = MgThatReference(descriptor=descriptor_enchantment,antecedent=original_enchantment_description)
                
                self.assertTrue(thatref_enchantment.isTraversable())
                self.assertEqual(len(thatref_enchantment.getTraversalSuccessors()),1)
                self.assertTrue(thatref_enchantment.isChild(descriptor_enchantment))
                self.assertEqual(descriptor_enchantment.getParent(),thatref_enchantment)
                self.assertEqual(thatref_enchantment.getDescriptor(),descriptor_enchantment)
                
                self.assertTrue(thatref_enchantment.hasAntecedent())
                self.assertEqual(thatref_enchantment.getAntecedent(),original_enchantment_description)
                thatref_enchantment.setAntecedent(original_enchantment_description)
                
                
                self.assertEqual(thatref_enchantment.getAntecedent(),original_enchantment_description)
                self.assertEqual(thatref_enchantment.unparseToString().lower(),"that enchantment")
                
        def test_itReferences(self):
                pass
                
                
        def test_qualifiers(self):
                pass
        
        def test_modifiers(self):
                triggered = MgAbilityModifier(MgAbilityModifier.AbilityModifierEnum.Triggered)
                ability = MgQualifier(MgQualifier.QualifierEnum.Ability)
                triggered_ability = MgDescriptionExpression(triggered,ability)
                
                self.assertTrue(triggered.isTraversable())
                self.assertEqual(len(triggered.getTraversalSuccessors()),0)
                self.assertEqual(triggered.getModifier(),MgAbilityModifier.AbilityModifierEnum.Triggered)
                self.assertEqual(triggered_ability.unparseToString().lower(),"triggered ability")
                
                blocking = MgCombatStatusModifier(MgCombatStatusModifier.CombatStatusEnum.Blocking)
                creature = MgTypeExpression(MgType(MgType.TypeEnum.Creature))
                blocking_creature = MgDescriptionExpression(blocking,creature)
                self.assertEqual(blocking_creature.unparseToString().lower(),"blocking creature")
                
                enchanted = MgKeywordStatusModifier(MgKeywordStatusModifier.KeywordStatusEnum.Enchanted)
                permanent = MgQualifier(MgQualifier.QualifierEnum.Permanent)
                enchanted_permanent = MgDescriptionExpression(enchanted,permanent)
                self.assertEqual(enchanted_permanent.unparseToString().lower(),"enchanted permanent")
                
                tapped = MgTapStatusModifier(MgTapStatusModifier.TapStatusEnum.Tapped)
                artifact = MgTypeExpression(MgType(MgType.TypeEnum.Artifact))
                tapped_artifact = MgDescriptionExpression(tapped,artifact)
                self.assertEqual(tapped_artifact.unparseToString().lower(),"tapped artifact")
                
                chosen = MgEffectStatusModifier(MgEffectStatusModifier.EffectStatusEnum.Chosen)
                token = MgQualifier(MgQualifier.QualifierEnum.Token)
                tapped_artifact = MgDescriptionExpression(chosen,token)
                self.assertEqual(tapped_artifact.unparseToString().lower(),"chosen token")
                
        
if __name__ == '__main__':
        unittest.main()
