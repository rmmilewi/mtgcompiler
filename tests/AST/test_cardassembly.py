import unittest
from mtgcompiler.AST.reference import MgName
from mtgcompiler.AST.card import MgTypeLine,MgFlavorText,MgTextBox,MgCard
from mtgcompiler.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.AST.expressions import MgDescriptionExpression,MgColorExpression,MgTypeExpression,MgManaExpression,MgPTExpression,MgNonExpression,MgAndExpression,MgOrExpression,MgTargetExpression,MgAllExpression,MgEachExpression,MgChoiceExpression,MgTapUntapExpression,MgDestroyExpression
from mtgcompiler.AST.abilities import MgInstructionSequence,MgSpellAbility
from mtgcompiler.AST.visitors import SimpleGraphingVisitor

class TestMagicCardAssembly(unittest.TestCase):
        
        def test_DoomBlade(self):
                
                #Card name: Doom Blade.
                cardName = MgName("Doom Blade")
                
                #Mana cost: 1B.
                s0 = MgManaSymbol(cvalue=1)
                s1 = MgManaSymbol(colorv=MgManaSymbol.ManaType.Black)
                manaExpr = MgManaExpression(s0,s1)
                
                #Instant.
                t_instant = MgTypeExpression(MgType(MgType.TypeEnum.Instant))
                typeLine = MgTypeLine(types=t_instant)
                
                
                #Destroy target non-black creature.
                c_nonblack = MgColorExpression(MgNonExpression(MgColorTerm(MgColorTerm.ColorTermEnum.Black)))
                t_creature = MgTypeExpression(MgType(MgType.TypeEnum.Creature)) 
                description = MgDescriptionExpression(c_nonblack,t_creature)
                targetExpr = MgTargetExpression(description)
                destroyExpr = MgDestroyExpression(targetExpr)
                instructions = MgInstructionSequence(destroyExpr)
                ability = MgSpellAbility(instructions)
                textBox = MgTextBox(ability)
                
                #The card, all put together
                card = MgCard(**{
                        "name" : cardName,
                        "manaCost" : manaExpr,
                        "typeLine" : typeLine,
                        "textBox" : textBox
                })
                
                print(card.unparseToString().lower())
                visitor = SimpleGraphingVisitor(card)
                visitor.run()
                
                
if __name__ == '__main__':
    unittest.main()
                
                
                
                
                
                
