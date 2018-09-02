import unittest
from mtgcompiler.AST.reference import MgName,MgZone,MgQualifier,MgNameReference
from mtgcompiler.AST.card import MgTypeLine,MgFlavorText,MgTextBox,MgCard
from mtgcompiler.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.AST.expressions import MgDescriptionExpression,MgNumberValue,MgColorExpression,MgEntersLeavesBattlefieldExpression
from mtgcompiler.AST.expressions import MgPossessiveExpression,MgTypeExpression,MgModalExpression,MgControlExpression
from mtgcompiler.AST.expressions import MgManaExpression,MgPTExpression,MgNonExpression,MgAndExpression
from mtgcompiler.AST.expressions import MgOrExpression,MgTargetExpression,MgAllExpression,MgEachExpression,MgChoiceExpression
from mtgcompiler.AST.expressions import MgTapUntapExpression,MgDestroyExpression,MgUncastExpression,MgReturnExpression,MgCardDrawExpression
from mtgcompiler.AST.visitors import SimpleGraphingVisitor

from mtgcompiler.AST.abilities import MgStatement,MgStatementSequence,MgSpellAbility
from mtgcompiler.AST.abilities import MgHexproofAbility,MgProtectionAbility,MgLandwalkAbility,MgRampageAbility
from mtgcompiler.AST.abilities import MgFadingAbility, MgAmplifyAbility, MgModularAbility, MgBushidoAbility
from mtgcompiler.AST.abilities import MgSoulshiftAbility, MgDredgeAbility, MgBloodthirstAbility, MgGraftAbility
from mtgcompiler.AST.abilities import MgRippleAbility, MgVanishingAbility, MgAbsorbAbility, MgFrenzyAbility
from mtgcompiler.AST.abilities import MgPoisonousAbility, MgDevourAbility, MgAnnihilatorAbility, MgTributeAbility
from mtgcompiler.AST.abilities import MgRenownAbility, MgCrewAbility, MgFabricateAbility, MgAfflictAbility, MgSurveilAbility


class TestKeywordAbilities(unittest.TestCase):
        
        def test_Rampage(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Rampage = MgRampageAbility(five)
                
                self.assertTrue(Rampage.isTraversable())
                self.assertEqual(len(Rampage.getTraversalSuccessors()),1)
                self.assertTrue(Rampage.isChild(five))
                self.assertEqual(five.getParent(),Rampage)
                self.assertEqual(Rampage.getCaliber(),five)
                self.assertEqual(Rampage.unparseToString().lower(),"rampage 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Rampage.setCaliber(four)
                self.assertEqual(Rampage.getCaliber(),four)
                self.assertTrue(Rampage.isChild(four))
                self.assertEqual(four.getParent(),Rampage)
                self.assertEqual(Rampage.unparseToString().lower(),"rampage 4")
        
        def test_Fading(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Fading = MgFadingAbility(five)
                
                self.assertTrue(Fading.isTraversable())
                self.assertEqual(len(Fading.getTraversalSuccessors()),1)
                self.assertTrue(Fading.isChild(five))
                self.assertEqual(five.getParent(),Fading)
                self.assertEqual(Fading.getCaliber(),five)
                self.assertEqual(Fading.unparseToString().lower(),"fading 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Fading.setCaliber(four)
                self.assertEqual(Fading.getCaliber(),four)
                self.assertTrue(Fading.isChild(four))
                self.assertEqual(four.getParent(),Fading)
                self.assertEqual(Fading.unparseToString().lower(),"fading 4")
        
        def test_Amplify(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Amplify = MgAmplifyAbility(five)
                
                self.assertTrue(Amplify.isTraversable())
                self.assertEqual(len(Amplify.getTraversalSuccessors()),1)
                self.assertTrue(Amplify.isChild(five))
                self.assertEqual(five.getParent(),Amplify)
                self.assertEqual(Amplify.getCaliber(),five)
                self.assertEqual(Amplify.unparseToString().lower(),"amplify 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Amplify.setCaliber(four)
                self.assertEqual(Amplify.getCaliber(),four)
                self.assertTrue(Amplify.isChild(four))
                self.assertEqual(four.getParent(),Amplify)
                self.assertEqual(Amplify.unparseToString().lower(),"amplify 4")
        def test_Modular(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Modular = MgModularAbility(five)
                
                self.assertTrue(Modular.isTraversable())
                self.assertEqual(len(Modular.getTraversalSuccessors()),1)
                self.assertTrue(Modular.isChild(five))
                self.assertEqual(five.getParent(),Modular)
                self.assertEqual(Modular.getCaliber(),five)
                self.assertEqual(Modular.unparseToString().lower(),"modular 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Modular.setCaliber(four)
                self.assertEqual(Modular.getCaliber(),four)
                self.assertTrue(Modular.isChild(four))
                self.assertEqual(four.getParent(),Modular)
                self.assertEqual(Modular.unparseToString().lower(),"modular 4")
        def test_Bushido(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Bushido = MgBushidoAbility(five)
                
                self.assertTrue(Bushido.isTraversable())
                self.assertEqual(len(Bushido.getTraversalSuccessors()),1)
                self.assertTrue(Bushido.isChild(five))
                self.assertEqual(five.getParent(),Bushido)
                self.assertEqual(Bushido.getCaliber(),five)
                self.assertEqual(Bushido.unparseToString().lower(),"bushido 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Bushido.setCaliber(four)
                self.assertEqual(Bushido.getCaliber(),four)
                self.assertTrue(Bushido.isChild(four))
                self.assertEqual(four.getParent(),Bushido)
                self.assertEqual(Bushido.unparseToString().lower(),"bushido 4")
        def test_Soulshift(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Soulshift = MgSoulshiftAbility(five)
                
                self.assertTrue(Soulshift.isTraversable())
                self.assertEqual(len(Soulshift.getTraversalSuccessors()),1)
                self.assertTrue(Soulshift.isChild(five))
                self.assertEqual(five.getParent(),Soulshift)
                self.assertEqual(Soulshift.getCaliber(),five)
                self.assertEqual(Soulshift.unparseToString().lower(),"soulshift 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Soulshift.setCaliber(four)
                self.assertEqual(Soulshift.getCaliber(),four)
                self.assertTrue(Soulshift.isChild(four))
                self.assertEqual(four.getParent(),Soulshift)
                self.assertEqual(Soulshift.unparseToString().lower(),"soulshift 4")
        def test_Dredge(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Dredge = MgDredgeAbility(five)
                
                self.assertTrue(Dredge.isTraversable())
                self.assertEqual(len(Dredge.getTraversalSuccessors()),1)
                self.assertTrue(Dredge.isChild(five))
                self.assertEqual(five.getParent(),Dredge)
                self.assertEqual(Dredge.getCaliber(),five)
                self.assertEqual(Dredge.unparseToString().lower(),"dredge 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Dredge.setCaliber(four)
                self.assertEqual(Dredge.getCaliber(),four)
                self.assertTrue(Dredge.isChild(four))
                self.assertEqual(four.getParent(),Dredge)
                self.assertEqual(Dredge.unparseToString().lower(),"dredge 4")
        def test_Bloodthirst(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Bloodthirst = MgBloodthirstAbility(five)
                
                self.assertTrue(Bloodthirst.isTraversable())
                self.assertEqual(len(Bloodthirst.getTraversalSuccessors()),1)
                self.assertTrue(Bloodthirst.isChild(five))
                self.assertEqual(five.getParent(),Bloodthirst)
                self.assertEqual(Bloodthirst.getCaliber(),five)
                self.assertEqual(Bloodthirst.unparseToString().lower(),"bloodthirst 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Bloodthirst.setCaliber(four)
                self.assertEqual(Bloodthirst.getCaliber(),four)
                self.assertTrue(Bloodthirst.isChild(four))
                self.assertEqual(four.getParent(),Bloodthirst)
                self.assertEqual(Bloodthirst.unparseToString().lower(),"bloodthirst 4")
        def test_Graft(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Graft = MgGraftAbility(five)
                
                self.assertTrue(Graft.isTraversable())
                self.assertEqual(len(Graft.getTraversalSuccessors()),1)
                self.assertTrue(Graft.isChild(five))
                self.assertEqual(five.getParent(),Graft)
                self.assertEqual(Graft.getCaliber(),five)
                self.assertEqual(Graft.unparseToString().lower(),"graft 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Graft.setCaliber(four)
                self.assertEqual(Graft.getCaliber(),four)
                self.assertTrue(Graft.isChild(four))
                self.assertEqual(four.getParent(),Graft)
                self.assertEqual(Graft.unparseToString().lower(),"graft 4")
        def test_Ripple(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Ripple = MgRippleAbility(five)
                
                self.assertTrue(Ripple.isTraversable())
                self.assertEqual(len(Ripple.getTraversalSuccessors()),1)
                self.assertTrue(Ripple.isChild(five))
                self.assertEqual(five.getParent(),Ripple)
                self.assertEqual(Ripple.getCaliber(),five)
                self.assertEqual(Ripple.unparseToString().lower(),"ripple 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Ripple.setCaliber(four)
                self.assertEqual(Ripple.getCaliber(),four)
                self.assertTrue(Ripple.isChild(four))
                self.assertEqual(four.getParent(),Ripple)
                self.assertEqual(Ripple.unparseToString().lower(),"ripple 4")
        def test_Vanishing(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Vanishing = MgVanishingAbility(five)
                
                self.assertTrue(Vanishing.isTraversable())
                self.assertEqual(len(Vanishing.getTraversalSuccessors()),1)
                self.assertTrue(Vanishing.isChild(five))
                self.assertEqual(five.getParent(),Vanishing)
                self.assertEqual(Vanishing.getCaliber(),five)
                self.assertEqual(Vanishing.unparseToString().lower(),"vanishing 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Vanishing.setCaliber(four)
                self.assertEqual(Vanishing.getCaliber(),four)
                self.assertTrue(Vanishing.isChild(four))
                self.assertEqual(four.getParent(),Vanishing)
                self.assertEqual(Vanishing.unparseToString().lower(),"vanishing 4")
        def test_Absorb(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Absorb = MgAbsorbAbility(five)
                
                self.assertTrue(Absorb.isTraversable())
                self.assertEqual(len(Absorb.getTraversalSuccessors()),1)
                self.assertTrue(Absorb.isChild(five))
                self.assertEqual(five.getParent(),Absorb)
                self.assertEqual(Absorb.getCaliber(),five)
                self.assertEqual(Absorb.unparseToString().lower(),"absorb 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Absorb.setCaliber(four)
                self.assertEqual(Absorb.getCaliber(),four)
                self.assertTrue(Absorb.isChild(four))
                self.assertEqual(four.getParent(),Absorb)
                self.assertEqual(Absorb.unparseToString().lower(),"absorb 4")
        def test_Frenzy(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Frenzy = MgFrenzyAbility(five)
                
                self.assertTrue(Frenzy.isTraversable())
                self.assertEqual(len(Frenzy.getTraversalSuccessors()),1)
                self.assertTrue(Frenzy.isChild(five))
                self.assertEqual(five.getParent(),Frenzy)
                self.assertEqual(Frenzy.getCaliber(),five)
                self.assertEqual(Frenzy.unparseToString().lower(),"frenzy 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Frenzy.setCaliber(four)
                self.assertEqual(Frenzy.getCaliber(),four)
                self.assertTrue(Frenzy.isChild(four))
                self.assertEqual(four.getParent(),Frenzy)
                self.assertEqual(Frenzy.unparseToString().lower(),"frenzy 4")
        def test_Poisonous(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Poisonous = MgPoisonousAbility(five)
                
                self.assertTrue(Poisonous.isTraversable())
                self.assertEqual(len(Poisonous.getTraversalSuccessors()),1)
                self.assertTrue(Poisonous.isChild(five))
                self.assertEqual(five.getParent(),Poisonous)
                self.assertEqual(Poisonous.getCaliber(),five)
                self.assertEqual(Poisonous.unparseToString().lower(),"poisonous 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Poisonous.setCaliber(four)
                self.assertEqual(Poisonous.getCaliber(),four)
                self.assertTrue(Poisonous.isChild(four))
                self.assertEqual(four.getParent(),Poisonous)
                self.assertEqual(Poisonous.unparseToString().lower(),"poisonous 4")
        def test_Devour(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Devour = MgDevourAbility(five)
                
                self.assertTrue(Devour.isTraversable())
                self.assertEqual(len(Devour.getTraversalSuccessors()),1)
                self.assertTrue(Devour.isChild(five))
                self.assertEqual(five.getParent(),Devour)
                self.assertEqual(Devour.getCaliber(),five)
                self.assertEqual(Devour.unparseToString().lower(),"devour 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Devour.setCaliber(four)
                self.assertEqual(Devour.getCaliber(),four)
                self.assertTrue(Devour.isChild(four))
                self.assertEqual(four.getParent(),Devour)
                self.assertEqual(Devour.unparseToString().lower(),"devour 4")
        def test_Annihilator(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Annihilator = MgAnnihilatorAbility(five)
                
                self.assertTrue(Annihilator.isTraversable())
                self.assertEqual(len(Annihilator.getTraversalSuccessors()),1)
                self.assertTrue(Annihilator.isChild(five))
                self.assertEqual(five.getParent(),Annihilator)
                self.assertEqual(Annihilator.getCaliber(),five)
                self.assertEqual(Annihilator.unparseToString().lower(),"annihilator 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Annihilator.setCaliber(four)
                self.assertEqual(Annihilator.getCaliber(),four)
                self.assertTrue(Annihilator.isChild(four))
                self.assertEqual(four.getParent(),Annihilator)
                self.assertEqual(Annihilator.unparseToString().lower(),"annihilator 4")
        def test_Tribute(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Tribute = MgTributeAbility(five)
                
                self.assertTrue(Tribute.isTraversable())
                self.assertEqual(len(Tribute.getTraversalSuccessors()),1)
                self.assertTrue(Tribute.isChild(five))
                self.assertEqual(five.getParent(),Tribute)
                self.assertEqual(Tribute.getCaliber(),five)
                self.assertEqual(Tribute.unparseToString().lower(),"tribute 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Tribute.setCaliber(four)
                self.assertEqual(Tribute.getCaliber(),four)
                self.assertTrue(Tribute.isChild(four))
                self.assertEqual(four.getParent(),Tribute)
                self.assertEqual(Tribute.unparseToString().lower(),"tribute 4")
        def test_Renown(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Renown = MgRenownAbility(five)
                
                self.assertTrue(Renown.isTraversable())
                self.assertEqual(len(Renown.getTraversalSuccessors()),1)
                self.assertTrue(Renown.isChild(five))
                self.assertEqual(five.getParent(),Renown)
                self.assertEqual(Renown.getCaliber(),five)
                self.assertEqual(Renown.unparseToString().lower(),"renown 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Renown.setCaliber(four)
                self.assertEqual(Renown.getCaliber(),four)
                self.assertTrue(Renown.isChild(four))
                self.assertEqual(four.getParent(),Renown)
                self.assertEqual(Renown.unparseToString().lower(),"renown 4")
        def test_Crew(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Crew = MgCrewAbility(five)
                
                self.assertTrue(Crew.isTraversable())
                self.assertEqual(len(Crew.getTraversalSuccessors()),1)
                self.assertTrue(Crew.isChild(five))
                self.assertEqual(five.getParent(),Crew)
                self.assertEqual(Crew.getCaliber(),five)
                self.assertEqual(Crew.unparseToString().lower(),"crew 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Crew.setCaliber(four)
                self.assertEqual(Crew.getCaliber(),four)
                self.assertTrue(Crew.isChild(four))
                self.assertEqual(four.getParent(),Crew)
                self.assertEqual(Crew.unparseToString().lower(),"crew 4")
        def test_Fabricate(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Fabricate = MgFabricateAbility(five)
                
                self.assertTrue(Fabricate.isTraversable())
                self.assertEqual(len(Fabricate.getTraversalSuccessors()),1)
                self.assertTrue(Fabricate.isChild(five))
                self.assertEqual(five.getParent(),Fabricate)
                self.assertEqual(Fabricate.getCaliber(),five)
                self.assertEqual(Fabricate.unparseToString().lower(),"fabricate 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Fabricate.setCaliber(four)
                self.assertEqual(Fabricate.getCaliber(),four)
                self.assertTrue(Fabricate.isChild(four))
                self.assertEqual(four.getParent(),Fabricate)
                self.assertEqual(Fabricate.unparseToString().lower(),"fabricate 4")
        def test_Afflict(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Afflict = MgAfflictAbility(five)
                
                self.assertTrue(Afflict.isTraversable())
                self.assertEqual(len(Afflict.getTraversalSuccessors()),1)
                self.assertTrue(Afflict.isChild(five))
                self.assertEqual(five.getParent(),Afflict)
                self.assertEqual(Afflict.getCaliber(),five)
                self.assertEqual(Afflict.unparseToString().lower(),"afflict 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Afflict.setCaliber(four)
                self.assertEqual(Afflict.getCaliber(),four)
                self.assertTrue(Afflict.isChild(four))
                self.assertEqual(four.getParent(),Afflict)
                self.assertEqual(Afflict.unparseToString().lower(),"afflict 4")
        def test_Surveil(self):
                five = MgNumberValue(5,MgNumberValue.NumberTypeEnum.Literal)
                Surveil = MgSurveilAbility(five)
                
                self.assertTrue(Surveil.isTraversable())
                self.assertEqual(len(Surveil.getTraversalSuccessors()),1)
                self.assertTrue(Surveil.isChild(five))
                self.assertEqual(five.getParent(),Surveil)
                self.assertEqual(Surveil.getCaliber(),five)
                self.assertEqual(Surveil.unparseToString().lower(),"surveil 5")
                
                four = MgNumberValue(4,MgNumberValue.NumberTypeEnum.Literal)
                Surveil.setCaliber(four)
                self.assertEqual(Surveil.getCaliber(),four)
                self.assertTrue(Surveil.isChild(four))
                self.assertEqual(four.getParent(),Surveil)
                self.assertEqual(Surveil.unparseToString().lower(),"surveil 4")
        
        
        def test_Protection(self):
                #Protection from Red
                red = MgColorExpression(MgColorTerm(MgColorTerm.ColorTermEnum.Red))
                pro_red = MgProtectionAbility(red)
                
                self.assertTrue(pro_red.isTraversable())
                self.assertEqual(len(pro_red.getTraversalSuccessors()),1)
                self.assertTrue(pro_red.isChild(red))
                self.assertEqual(red.getParent(),pro_red)
                self.assertEqual(pro_red.unparseToString().lower(),"protection from red")
                
                #Protection from instant spell[s] and from sorcery spell[s]
                #Note that the default unparsing routine does not do pluralization,
                #though it's expected of a dedicated unparser.
                
                instant_spells = MgDescriptionExpression(
                        MgTypeExpression(MgType(MgType.TypeEnum.Instant)),
                        MgQualifier(MgQualifier.QualifierEnum.Spell)
                )
                
                sorcery_spells = MgDescriptionExpression(
                        MgTypeExpression(MgType(MgType.TypeEnum.Sorcery)),
                        MgQualifier(MgQualifier.QualifierEnum.Spell)
                )
                
                pro_instantAndSorcery = MgProtectionAbility(instant_spells,sorcery_spells)
                
                self.assertEqual(len(pro_instantAndSorcery.getTraversalSuccessors()),2)
                self.assertTrue(pro_instantAndSorcery.isChild(instant_spells))
                self.assertEqual(instant_spells.getParent(),pro_instantAndSorcery)
                self.assertEqual(pro_instantAndSorcery.unparseToString().lower(),"protection from instant spell and from sorcery spell")
                
                
        def test_Hexproof(self):
                hexproof = MgHexproofAbility()
                
                self.assertTrue(hexproof.isTraversable())
                self.assertFalse(hexproof.hasQualitySpecifier())
                self.assertEqual(len(hexproof.getTraversalSuccessors()),0)
                self.assertEqual(hexproof.unparseToString().lower(),"hexproof")
                
                
                black = MgColorExpression(MgColorTerm(MgColorTerm.ColorTermEnum.Black))
                hexproof_from_black = MgHexproofAbility(quality=black)
                
                self.assertTrue(hexproof_from_black.isTraversable())
                self.assertTrue(hexproof_from_black.hasQualitySpecifier())
                self.assertEqual(len(hexproof_from_black.getTraversalSuccessors()),1)
                self.assertTrue(hexproof_from_black.isChild(black))
                self.assertEqual(black.getParent(),hexproof_from_black)
                self.assertEqual(hexproof_from_black.unparseToString().lower(),"hexproof from black")
                
                
                green = MgColorExpression(MgColorTerm(MgColorTerm.ColorTermEnum.Green))
                hexproof_from_black.setQualitySpecifier(green)
                self.assertEqual(hexproof_from_black.getQualitySpecifier(),green)
                self.assertTrue(hexproof_from_black.isChild(green))
                self.assertEqual(green.getParent(),hexproof_from_black)
                self.assertEqual(hexproof_from_black.unparseToString().lower(),"hexproof from green")
                
                
                
        def test_Landwalk(self):
                t_island_expr = MgTypeExpression(MgSubtype(MgSubtype.LandSubtypeEnum.Island))
                islandwalk = MgLandwalkAbility(landtype=t_island_expr)
                
                self.assertTrue(islandwalk.isTraversable())
                self.assertTrue(islandwalk.hasLandType())
                self.assertEqual(len(islandwalk.getTraversalSuccessors()),1)
                self.assertTrue(islandwalk.isChild(t_island_expr))
                self.assertEqual(t_island_expr.getParent(),islandwalk)
                self.assertEqual(islandwalk.unparseToString().lower(),"islandwalk")
                
                
                t_nonbasic_land_expr = MgTypeExpression(
                        MgNonExpression(MgSupertype(MgSupertype.SupertypeEnum.Basic)),
                        MgType(MgType.TypeEnum.Land)
                )
                
                nonbasiclandwalk = MgLandwalkAbility(landtype=t_nonbasic_land_expr)
                self.assertEqual(nonbasiclandwalk.unparseToString().lower(),"non-basic landwalk")
                
                #Used when talking about landwalk abilities in general.
                landwalk  = MgLandwalkAbility()
                self.assertEqual(landwalk.unparseToString().lower(),"landwalk")
                
                t_lair_expr = MgTypeExpression(MgSubtype(MgSubtype.LandSubtypeEnum.Lair))
                landwalk.setLandType(t_lair_expr)
                self.assertEqual(landwalk.getLandType(),t_lair_expr)
                self.assertTrue(landwalk.isChild(t_lair_expr))
                self.assertEqual(t_lair_expr.getParent(),landwalk)
                self.assertEqual(landwalk.unparseToString().lower(),"lairwalk")
                
                
                
                
        
        
if __name__ == '__main__':
        unittest.main()