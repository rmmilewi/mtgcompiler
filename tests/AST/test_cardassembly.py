import unittest
from mtgcompiler.frontend.AST.reference import MgName,MgZone,MgQualifier,MgNameReference
from mtgcompiler.frontend.AST.card import MgTypeLine,MgFlavorText,MgTextBox,MgCard
from mtgcompiler.frontend.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.frontend.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.frontend.AST.expressions import MgDescriptionExpression,MgNumberValue,MgColorExpression,MgChangeZoneExpression
from mtgcompiler.frontend.AST.expressions import MgPossessiveExpression,MgTypeExpression,MgModalExpression,MgControlExpression
from mtgcompiler.frontend.AST.expressions import MgManaExpression,MgPTExpression,MgNonExpression,MgAndExpression
from mtgcompiler.frontend.AST.expressions import MgOrExpression,MgTargetExpression,MgAllExpression,MgEachExpression,MgChoiceExpression
from mtgcompiler.frontend.AST.expressions import MgTapUntapExpression,MgDestroyExpression,MgUncastExpression,MgReturnExpression,MgCardDrawExpression


from mtgcompiler.frontend.AST.abilities import MgStatementSequence,MgSpellAbility
from mtgcompiler.midend.support.inspection import SimpleGraphingVisitor

class TestMagicCardAssembly(unittest.TestCase):
        
        """
        def test_BanisherPriest(self):
                #Card name: Banisher Priest
                cardName = MgName("Banisher Priest")
                
                #Mana cost: 1WW.
                s0 = MgManaSymbol(cvalue=1)
                s1 = MgManaSymbol(colorv=MgManaSymbol.ManaType.White)
                s2 = MgManaSymbol(colorv=MgManaSymbol.ManaType.White)
                manaExpr = MgManaExpression(s0,s1,s2)
                
                #Creature - Human Cleric
                t_creature = MgTypeExpression(MgType(MgType.TypeEnum.Creature))
                t_human = MgTypeExpression(MgType(MgType.SubtypeEnum.Human))
                t_cleric = MgTypeExpression(MgType(MgType.SubtypeEnum.Cleric))
                typeLine = MgTypeLine(types=MgTypeLine(t_creature),subtypes=MgTypeLine(t_human,t_cleric))
                
                
                #exile target creature an opponent controls
                exileEffect = MgExileEffectExpression(
                        subject = MgTargetExpression(MgDescriptionExpression(
                                MgTypeExpression(MgType(MgType.TypeEnum.Creature)),
                                MgControlExpression("an opponent")))                        
                )
                
                #[...] until Banisher Priest leaves the battlefield.
                untilCondition = MgUntilExpression(MgChangeZoneExpression(subject=MgNameReference(),zone=None,entering=False))
                
                subject,zone,entering=True):
                
                #when Banisher Priest enters the battlefield, [...]
                entersTheBattlefield = MgEntersLeavesBattlefieldExpression(MgNameReference,entering=True)
                
                
                #TODO: NOT DONE
        """
                
                
                
        """
        def test_CrypticCommand(self):
                #Card name: Cryptic Command
                cardName = MgName("Cryptic Command")
                
                #Mana cost: 1UUU.
                s0 = MgManaSymbol(cvalue=1)
                s1 = MgManaSymbol(colorv=MgManaSymbol.ManaType.Blue)
                s2 = MgManaSymbol(colorv=MgManaSymbol.ManaType.Blue)
                s3 = MgManaSymbol(colorv=MgManaSymbol.ManaType.Blue)
                manaExpr = MgManaExpression(s0,s1,s2,s3)
                
                #Instant.
                t_instant = MgTypeExpression(MgType(MgType.TypeEnum.Instant))
                typeLine = MgTypeLine(types=t_instant)
                
                #counter target spell
                choice_counterspell = MgStatementSequence(MgStatement(MgUncastExpression(MgTargetExpression(MgDescriptionExpression(
                        MgQualifier(MgQualifier.QualifierEnum.Spell)
                )))))
                
                #Return target permanent to its owner's hand.
                choice_bounce = MgStatementSequence(MgReturnExpression(
                        subject = MgTargetExpression(MgDescriptionExpression(MgQualifier(MgQualifier.QualifierEnum.Permanent))),
                        destination = MgPossessiveExpression(possessive=MgPossessiveExpression.PossessiveEnum.Owner,owned=MgZone(MgZone.ZoneEnum.Hand))
                )))
                
                #Tap all creatures your opponents control.
                choice_tap = MgStatementSequence(MgStatement(MgTapUntapExpression(
                        MgAllExpression(MgDescriptionExpression(MgTypeExpression(MgType(MgType.TypeEnum.Creature)),MgControlExpression("your opponents")))
                        ,tap=True
                )))
                
                #Draw a card.
                choice_draw = MgStatementSequence(MgStatement(MgCardDrawExpression(MgNumberValue(value=1,ntype=MgNumberValue.NumberTypeEnum.Quantity))))
                
                #Choose two
                modalExpr = MgModalExpression(
                        MgNumberValue(value=2,ntype=MgNumberValue.NumberTypeEnum.Quantity),
                        choice_counterspell,choice_bounce,choice_tap,choice_draw
                )
                
                instructions = MgStatementSequence(MgStatement(modalExpr,periodTerminated=False))
                ability = MgSpellAbility(instructions)
                textBox = MgTextBox(ability)
                
                card = MgCard(**{
                        "name" : cardName,
                        "manaCost" : manaExpr,
                        "typeLine" : typeLine,
                        "textBox" : textBox
                })
                
                print(card.unparseToString().lower())
                visitor = SimpleGraphingVisitor()
                visitor.traverse(card)
        """
        
        """
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
                instructions = MgStatementSequence(MgStatement(destroyExpr))
                ability = MgSpellAbility(instructions)
                textBox = MgTextBox(ability)
                
                #The card, all put together
                card = MgCard(**{
                        "name" : cardName,
                        "manaCost" : manaExpr,
                        "typeLine" : typeLine,
                        "textBox" : textBox
                })
                
                #card.unparseToString().lower()
                #print(card.unparseToString().lower())
                #visitor = SimpleGraphingVisitor(card)
                #visitor.run()
        """
                
                
if __name__ == '__main__':
        unittest.main()
                
                
                
                
                
                
