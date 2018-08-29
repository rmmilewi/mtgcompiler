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
from mtgcompiler.AST.abilities import MgProtectionAbility

class TestKeywordAbilities(unittest.TestCase):
        
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
                
        
        
        
        
if __name__ == '__main__':
        unittest.main()