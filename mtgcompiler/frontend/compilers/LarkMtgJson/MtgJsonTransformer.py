
from mtgcompiler.frontend.compilers.BaseImplementation.BaseTransformer import BaseTransformer
from lark import Transformer as LarkTransformer, \
        Transformer  # The Lark class responsible for converting the parse tree into something useful.

#TODO: I'm gonna restructure all these imports, because this is just getting really messy.
from mtgcompiler.frontend.AST.reference import MgNameReference,MgThisReference
from mtgcompiler.frontend.AST.reference import MgName,MgTapUntapSymbol,MgZone,MgQualifier
from mtgcompiler.frontend.AST.reference import MgAbilityModifier,MgCombatStatusModifier,MgKeywordStatusModifier,MgTapStatusModifier,MgEffectStatusModifier
from mtgcompiler.frontend.AST.card import MgTypeLine,MgFlavorText,MgTextBox,MgCard
from mtgcompiler.frontend.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.frontend.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.frontend.AST.statements import MgKeywordAbilityListStatement,MgStatementBlock,MgExpressionStatement,MgActivationStatement
from mtgcompiler.frontend.AST.statements import MgAbilitySequenceStatement,MgQuotedAbilityStatement
from mtgcompiler.frontend.AST.statements import MgWhenStatement

from mtgcompiler.frontend.AST.expressions import MgNumberValue,MgPTExpression,MgManaExpression,MgTypeExpression,MgDescriptionExpression
from mtgcompiler.frontend.AST.expressions import MgNamedExpression,MgCostSequenceExpression,MgWithExpression,MgIndefiniteSingularExpression
from mtgcompiler.frontend.AST.expressions import MgColorExpression,MgAndExpression,MgOrExpression,MgAndOrExpression,MgTargetExpression,MgDeclarationExpression
from mtgcompiler.frontend.AST.expressions import MgDestroyExpression,MgExileExpression,MgDealsDamageExpression,MgChangeZoneExpression,MgSacrificeExpression
from mtgcompiler.frontend.AST.expressions import MgAnyColorSpecifier,MgManaSpecificationExpression,MgAddManaExpression,MgCreateTokenExpression

from mtgcompiler.frontend.AST.abilities import MgReminderText,MgAbilityWord,MgRegularAbility
from mtgcompiler.frontend.AST.abilities import MgDeathtouchAbility,MgDefenderAbility,MgDoubleStrikeAbility,MgFirstStrikeAbility,MgTrampleAbility
from mtgcompiler.frontend.AST.abilities import MgFlashAbility,MgFlyingAbility,MgHasteAbility,MgIndestructibleAbility,MgReachAbility



from mtgcompiler.frontend.AST.abilities import MgHexproofAbility,MgProtectionAbility,MgLandwalkAbility,MgRampageAbility
from mtgcompiler.frontend.AST.abilities import MgFadingAbility, MgAmplifyAbility, MgModularAbility, MgBushidoAbility
from mtgcompiler.frontend.AST.abilities import MgSoulshiftAbility, MgDredgeAbility, MgBloodthirstAbility, MgGraftAbility
from mtgcompiler.frontend.AST.abilities import MgRippleAbility, MgVanishingAbility, MgAbsorbAbility, MgFrenzyAbility
from mtgcompiler.frontend.AST.abilities import MgPoisonousAbility, MgDevourAbility, MgAnnihilatorAbility, MgTributeAbility
from mtgcompiler.frontend.AST.abilities import MgRenownAbility, MgCrewAbility, MgFabricateAbility, MgAfflictAbility, MgSurveilAbility

from mtgcompiler.frontend.AST.abilities import MgCumulativeUpkeepAbility, MgBuybackAbility, MgCyclingAbility, MgKickerAbility, MgMadnessAbility
from mtgcompiler.frontend.AST.abilities import MgMorphAbility, MgNinjutsuAbility, MgTransmuteAbility, MgRecoverAbility
from mtgcompiler.frontend.AST.abilities import MgAuraSwapAbility, MgTransfigureAbility, MgEvokeAbility, MgMiracleAbility
from mtgcompiler.frontend.AST.abilities import MgOverloadAbility, MgScavengeAbility, MgOutlastAbility, MgSurgeAbility
from mtgcompiler.frontend.AST.abilities import MgEmergeAbility, MgEscalateAbility, MgEnbalmAbility, MgEternalizeAbility, MgJumpStartAbility

from mtgcompiler.frontend.AST.abilities import MgSpliceAbility,MgEnchantAbility,MgEquipAbility,MgBandingAbility,MgAffinityAbility
from mtgcompiler.frontend.AST.abilities import MgOfferingAbility,MgForecastAbility,MgSuspendAbility,MgChampionAbility,MgReinforceAbility
from mtgcompiler.frontend.AST.abilities import MgHiddenAgendaAbility,MgAwakenAbility,MgPartnerAbility

from lark.lexer import Token

#Convenience function for flattening lists (of lists)+
def flatten(l):
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


class MtgJsonTransformer(BaseTransformer):
        """The MtgJson transformer. This class wraps the Lark implementation of the transformer,
        helping somewhat to decouple Lark from Arbor."""
        
        def __init__(self,options):
                """
                options: an object that contains options for the transformer.
                """
                super().__init__(options)
                self._larktf = MtgJsonTransformer.LarkTransformer()
                pass #TODO: Handling various options in here.
                
        def transform(self,parseTree):
                """
                parsedText: A parse tree from Lark
                output - an Arbor abstract syntax tree (AST) derived from the parse tree.
                """
                ast = self._larktf.transform(parseTree) #Calls the Lark transformer which traverses the parsetree.
                return ast

        class LarkTransformer(Transformer):
                #CARDS
                def typeline(self,items):
                        linefeatures = {}
                        linefeatures["supertypes"] = MgTypeExpression()
                        linefeatures["types"] = MgTypeExpression()
                        linefeatures["subtypes"] = MgTypeExpression()
                        for item in items:
                                subfield,expr = item
                                linefeatures[subfield] = expr
        
                        return MgTypeLine(supertypes=linefeatures["supertypes"],types=linefeatures["types"],subtypes=linefeatures["subtypes"])

                def typelinesupert(self,items):
                        items = [self.typeterm([item]) for item in items]
                        return ("supertypes",self.typeexpression(items))

                def typelinet(self,items):
                        items = [self.typeterm([item]) for item in items]
                        return ("types",self.typeexpression(items))
        
                def typelinesubt(self,items):
                        items = [self.typeterm([item]) for item in items]
                        return ("subtypes",self.typeexpression(items))

                def cardtext(self,items):
                        return MgTextBox(*items)
        
                #ABILITIES
        
                def ability(self,items):
                        #Either there is a single node representing an ability or sequence of keyword abilities,
                        #or there is an additional node for the reminder text.
                        if len(items) == 1:
                                return items[0]
                        else:
                                abilityOrSeq = items[0]
                                reminderText = items[1]
                                if type(abilityOrSeq) == MgKeywordAbilityListStatement:
                                        #The reminder text is attached to the final keyword ability in a sequence
                                        #of keyword abilities.
                                        abilityOrSeq.getAbilityAtIndex(-1).setReminderText(reminderText)
                                else:
                                        abilityOrSeq.setReminderText(reminderText)
                        return abilityOrSeq
        
                def regularability(self,items):
                        #abilityword? stmtblock remindertext?
                        abilityWord = None
                        statementBlock = None
                        reminderText = None
                        if len(items) == 3:
                                #ability word, then statement block, then reminder text
                                abilityWord = items[0]
                                statementBlock = items[1]
                                reminderText = items[2]
                        elif len(items) == 2:
                                if type(items[0]) == MgAbilityWord:
                                        #ability word, then statement block
                                        abilityWord = items[0]
                                        statementBlock = items[1]
                                else:
                                        #statement block, then reminder text
                                        statementBlock = items[0]
                                        reminderText = items[1]
                        else:
                                #Just the statement block, no ability word or reminder text.
                                statementBlock = items[0]
                        
                        return MgRegularAbility(stmtblock=statementBlock,abilityWord=abilityWord,reminderText=reminderText)
        
                def abilityword(self,items):
                        text = items[0].value
                        return MgAbilityWord(text)
                def remindertext(self,items):
                        text = items[0].value
                        return MgReminderText(text)
        
        
                #ABILITIES - KEYWORD ABILITIES
        
                def keywordlist(self,items):
                        flatlst = flatten(items)
                        return MgKeywordAbilityListStatement(*flatlst)
                def keywordsequence(self,items):
                        return items
                def keywordability(self,items):
                        return items[0]
        
        

                def kwdeathtouch(self,items): 
                        return MgDeathtouchAbility()
                def kwdefender(self,items): 
                        return MgDefenderAbility()
                def kwdoublestrike(self,items): 
                        return MgDoubleStrikeAbility()
                def kwenchant(self,items): 
                        descriptor = items[0]
                        return MgEnchantAbility(descriptor)
                def kwequip(self,items):
                        if len(items[0].children) == 1:
                                #Equip <cost>
                                cost = items[0]
                                return MgEquipAbility(cost)
                        else:
                                #Equip <quality> creature <cost>
                                quality = items[0]
                                cost = items[1]
                                return MgEquipAbility(quality=quality,cost=cost)
                
                def kwfirststrike(self,items): 
                        return MgFirstStrikeAbility()
                def kwflash(self,items): 
                        return MgFlashAbility()
                def kwflying(self,items): 
                        return MgFlyingAbility()
                def kwhaste(self,items): 
                        return MgHasteAbility()
                def kwhexproof(self,items): 
                        if len(items) == 1:
                                #hexproof from quality
                                return MgHexproofAbility(quality=items[0])
                        else:
                                #regular hexproof
                                return MgHexproofAbility()
                def kwindestructible(self,items): 
                        return MgIndestructibleAbility()
                def kwintimidate(self,items): 
                        return MgIntimidateAbility()
                def kwlandwalk(self,items): 
                        typeExpr = items[0]
                        return MgLandwalkAbility(typeExpr)
                def kwlifelink(self,items): 
                        return MgLifelinkAbility()
                def kwprotection(self,items):
                        return MgProtectionAbility(*items)
                def kwreach(self,items): 
                        return MgReachAbility()
                def kwshroud(self,items): 
                        return MgShroudAbility()
                def kwtrample(self,items): 
                        return MgTrampleAbility()
                def kwvigilance(self,items): 
                        return MgVigilanceAbility()
                def kwbanding(self,items): 
                        #: "banding" | "bands" "with" "other"
                        if len(items) == 1:
                                #Bands with other.
                                return MgBandingAbility(quality=items[0])
                        else:
                                #Regular banding
                                return MgBandingAbility()
                def kwrampage(self,items): 
                        #: "rampage" NUMBER
                        caliber = int(items[0].value)
                        return MgRampageAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwcumulativeupkeep(self,items): 
                        #: "cumulative" "upkeep" cost
                        cost = items[0]
                        return MgCumulativeUpkeepAbility(cost)
                def kwflanking(self,items): 
                        #: "flanking"
                        return MgFlankingAbility()
                def kwphasing(self,items): 
                        #: "phasing"
                        return MgPhasingAbility()
                def kwbuyback(self,items): 
                        #: "buyback" cost
                        cost = items[0]
                        return MgBuybackAbility(cost)
                def kwshadow(self,items): 
                        #: "shadow"
                        return MgShadowAbility()
                def kwcycling(self,items): 
                        #: "cycling" cost
                        if len(items) == 2:
                                #typecycling
                                typeExpr = items[0]
                                cost = items[1]
                                return MgCyclingAbility(cost=cost,cyclingType=typeExpr)
                        else:
                                #regular cycling
                                cost = items[0]
                                return MgCyclingAbility(cost)
                def kwecho(self,items): 
                        #: "echo" cost
                        cost = items[0]
                        return MgEchoAbility(cost)
                def kwhorsemanship(self,items): 
                        #: "horsemanship"
                        return MgHorsemanshipAbility()
                def kwfading(self,items): 
                        #: "fading" NUMBER
                        caliber = int(items[0].value)
                        return MgFadingAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwkicker(self,items): 
                        #: "kicker" cost, multikicker
                        cost = items[0]
                        return MgKickerAbility(cost)
                def kwflashback(self,items): 
                        #: "flashback" cost
                        cost = items[0]
                        return MgFlashbackAbility(cost)
                def kwmadness(self,items): 
                        #: "madness" cost
                        cost = items[0]
                        return MgMadnessAbility(cost)
                def kwfear(self,items): 
                        #: "fear"
                        return MgFearAbility()
                def kwmorph(self,items): 
                        #: "morph" cost
                        cost = items[0]
                        return MgMorphAbility(cost)
                def kwmegamorph(self,items): 
                        #: "morph" cost
                        cost = items[0]
                        return MgMorphAbility(cost,isMega=True)
                def kwamplify(self,items): 
                        #: "amplify" NUMBER
                        caliber = int(items[0].value)
                        return MgAmplifyAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwprovoke(self,items): 
                        #: "provoke"
                        return MgProvokeAbility()
                def kwstorm(self,items): 
                        #: "storm"
                        return MgStormAbility()
                def kwaffinity(self,items): 
                        #: "affinity" "for" typeexpression
                        if len(items) == 1:
                                return MgAffinityAbility(items[0])
                def kwentwine(self,items): 
                        #: "entwine" cost
                        cost = items[0]
                        return MgEntwineAbility(cost)
                def kwmodular(self,items): 
                        #: "modular" NUMBER
                        caliber = int(items[0].value)
                        return MgModularAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwsunburst(self,items): 
                        #: "sunburst"
                        return MgSunburstAbility()
                def kwbushido(self,items): 
                        #: "bushido" NUMBER
                        caliber = int(items[0].value)
                        return MgBushidoAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
        
                def kwsoulshift(self,items): 
                        #: "soulshift" NUMBER
                        caliber = int(items[0].value)
                        return MgSoulshiftAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwsplice(self,items): 
                        #: "splice" "onto" typeexpression cost
                        return MgSpliceAbility(cost=items[1],spliceType=items[0])
                def kwoffering(self,items): 
                        #: type "offering"
                        typeExpr = items[0]
                        return MgOfferingAbility(typeExpr)
                def kwninjutsu(self,items): 
                        #: "ninjutsu" cost
                        cost = items[0]
                        return MgNinjutsuAbility(cost)
                def kwepic(self,items): 
                        #: "epic"
                        return MgEpicAbility()
                def kwconvoke(self,items): 
                        #: "convoke"
                        return MgConvokeAbility()
                def kwdredge(self,items): 
                        #: "dredge" NUMBER
                        caliber = int(items[0].value)
                        return MgDredgeAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwtransmute(self,items): 
                        #: "transmute" cost
                        cost = items[0]
                        return MgTransmuteAbility(cost)
                def kwbloodthirst(self,items): 
                        #: "bloodthirst" NUMBER
                        caliber = int(items[0].value)
                        return MgBloodthirstAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwhaunt(self,items): 
                        #: "haunt"
                        return MgHauntAbility()
                def kwreplicate(self,items): 
                        #: "replicate" cost
                        cost = items[0]
                        return MgReplicateAbility(cost)
                def kwforecast(self,items): 
                        #: "forecast" //TODO
                        pass
                def kwgraft(self,items): 
                        #: "graft"
                        return MgGraftAbility()
                def kwrecover(self,items): 
                        #: "recover" cost
                        cost = items[0]
                        return MgRecoverAbility(cost)
                def kwripple(self,items): 
                        #: "ripple" NUMBER
                        caliber = int(items[0].value)
                        return MgRippleAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwsplitsecond(self,items): 
                        #: "split" "second"
                        return MgSplitSecondAbility()
                def kwsuspend(self,items): 
                        #: "suspend" NUMBER cost
                        caliber = int(items[0].value)
                        cost = items[1]
                        return MgSuspendAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal),cost)
                def kwvanishing(self,items): 
                        #: "vanishing" [NUMBER]
                        if len(items) == 1:
                                caliber = int(items[0].value)
                                return MgVanishingAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                        else:
                                return MgVanishingAbility()
                def kwabsorb(self,items): 
                        #: "absorb" NUMBER
                        caliber = int(items[0].value)
                        return MgAbsorbAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwauraswap(self,items): 
                        #: "aura" "swap" cost
                        cost = items[0]
                        return MgAuraSwapAbility(cost)
                def kwdelve(self,items): 
                        #: "delve"
                        return MgDelveAbility()
                def kwfortify(self,items): 
                        #: "fortify" cost
                        cost = items[0]
                        return MgFortifyAbility(cost)
                def kwfrenzy(self,items): 
                        #: "frenzy"
                        return MgFrenzyAbility()
                def kwgravestorm(self,items): 
                        #: "gravestorm"
                        return MgGravestormAbility()
                def kwpoisonous(self,items): 
                        #: "poisonous" NUMBER
                        caliber = int(items[0].value)
                        return MgPoisonousAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwtransfigure(self,items): 
                        #: "transfigure" cost
                        cost = items[0]
                        return MgTransfigureAbility(cost)
                def kwchampion(self,items): 
                        #: "champion" "a"["n"]
                        typeExpr = items[0]
                        return MgChampionAbility(typeExpr)
                def kwchangeling(self,items): 
                        #: "changeling"
                        return MgChangelingAbility()
                def kwevoke(self,items): 
                        #: "evoke" cost
                        cost = items[0]
                        return MgEvokeAbility(cost)
                def kwhideaway(self,items): 
                        #: "hideaway"
                        return MgHideawayAbility()
                def kwprowl(self,items): 
                        #: "prowl" cost
                        cost = items[0]
                        return MgProwlAbility(cost)
                def kwreinforce(self,items): 
                        #: "reinforce" cost
                        cost = items[0]
                        return MgReinforceAbility(cost)
                def kwconspire(self,items): 
                        #: "conspire"
                        return MgConspireAbility()
                def kwpersist(self,items): 
                        #: "persist"
                        return MgPersistAbility()
                def kwwither(self,items): 
                        #: "wither"
                        return MgWitherAbility()
                def kwretrace(self,items): 
                        #: "retrace" cost
                        cost = items[0]
                        return MgRetraceAbility(cost)
                def kwdevour(self,items): 
                        #: "devour" NUMBER
                        caliber = int(items[0].value)
                        return MgDevourAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwexalted(self,items): 
                        #: "exalted"
                        return MgExaltedAbility()
                def kwunearth(self,items): 
                        #: "unearth" cost
                        cost = items[0]
                        return MgUnearthAbility(cost)
                def kwcascade(self,items): 
                        #: "cascade"
                        return MgCascadeAbility()
                def kwannihilator(self,items): 
                        #: "annihilator" NUMBER
                        caliber = int(items[0].value)
                        return MgAnnihilatorAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwlevelup(self,items): 
                        #: "level up"
                        cost = items[0]
                        return MgLevelUpAbility(cost)
                def kwrebound(self,items): 
                        #: "rebound"
                        return MgReboundAbility()
                def kwtotemarmor(self,items): 
                        #: "totem" "armor"
                        return MgTotemArmorAbility()
                def kwinfect(self,items): 
                        #: "infect"
                        return MgInfectAbility()
                def kwbattlecry(self,items): 
                        #: "battle" "cry"
                        return MgBattleCryAbility()
                def kwlivingweapon(self,items): 
                        #: "living" "weapon"
                        return MgLivingWeaponAbility()
                def kwundying(self,items): 
                        #: "undying"
                        return MgUndyingAbility()
                def kwmiracle(self,items): 
                        #: "miracle" cost
                        cost = items[0]
                        return MgMiracleAbility(cost)
                def kwsoulbond(self,items): 
                        #: "soulbond"
                        return MgSoulbondAbility()
                def kwoverload(self,items): 
                        #: "overload" cost
                        cost = items[0]
                        return MgOverloadAbility(cost)
                def kwscavenge(self,items): 
                        #: "scavenge" cost
                        cost = items[0]
                        return MgScavengeAbility(cost)
                def kwunleash(self,items): 
                        #: "unleash"
                        return MgUnleashAbility()
                def kwcipher(self,items): 
                        #: "cipher"
                        return MgCipherAbility()
                def kwevolve(self,items): 
                        #: "evolve"
                        return MgEvolveAbility()
                def kwextort(self,items): 
                        #: "extort"
                        return MgExtortAbility()
                def kwfuse(self,items): 
                        #: "fuse"
                        return MgFuseAbility()
                def kwbestow(self,items): 
                        #: "bestow" cost
                        cost = items[0]
                        return MgBestowAbility(cost)
                def kwtribute(self,items): 
                        #: "tribute" NUMBER
                        caliber = int(items[0].value)
                        return MgTributeAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwdethrone(self,items): 
                        #: "dethrone"
                        return MgDethroneAbility()
                def kwhiddenagenda(self,items): 
                        #: "hidden" "agenda" | "double" "agenda"
                       return MgHiddenAgendaAbility(isDoubleAgenda=False)
                def kwdoubleagenda(self,items): 
                        #: "hidden" "agenda" | "double" "agenda"
                       return MgHiddenAgendaAbility(isDoubleAgenda=True)
                def kwoutlast(self,items): 
                        #: "outlast" cost
                        cost = items[0]
                        return MgOutlastAbility(cost)
                def kwprowess(self,items): 
                        #: "prowess"
                        return MgProwessAbility()
                def kwdash(self,items): 
                        #: "dash" cost
                        cost = items[0]
                        return MgDashAbility(cost)
                def kwexploit(self,items): 
                        #: "exploit"
                        return MgExploitAbility()
                def kwmenace(self,items): 
                        #: "menace"
                        return MgMenaceAbility()
                def kwrenown(self,items): 
                        #: "renown" NUMBER
                        caliber = int(items[0].value)
                        return MgRenownAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwawaken(self,items): 
                        #: "awaken" cost
                        cost = items[0]
                        return MgAwakenAbility(cost)
                def kwdevoid(self,items): 
                        #: "devoid"
                        return MgDevoidAbility()
                def kwingest(self,items): 
                        #: "ingest"
                        return MgIngestAbility()
                def kwmyriad(self,items): 
                        #: "myriad"
                        return MgMyriadAbility()
                def kwsurge(self,items): 
                        #: "surge" cost
                        cost = items[0]
                        return MgSurgeAbility(cost)
                def kwskulk(self,items): 
                        #: "skulk"
                        return MgSkulkAbility()
                def kwemerge(self,items): 
                        #: "emerge" cost
                        cost = items[0]
                        return MgEmergeAbility(cost)
                def kwescalate(self,items): 
                        #: "escalate" cost
                        cost = items[0]
                        return MgEscalateAbility(cost)
                def kwmelee(self,items): 
                        #: "melee"
                        return MgMeleeAbility()
                def kwcrew(self,items): 
                        #: "crew" NUMBER
                        caliber = int(items[0].value)
                        return MgCrewAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwfabricate(self,items): 
                        #: "fabricate" NUMBER
                        caliber = int(items[0].value)
                        return MgFabricateAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwpartner(self,items): 
                        #: "partner" | "partner" "with" name
                        if len(items) == 1:
                                return MgPartnerAbility(partnerName=items[0])
                        else:
                                return MgPartnerAbility()
                def kwundaunted(self,items): 
                        #: "undaunted"
                        return MgUndauntedAbility()
                def kwimprovise(self,items): 
                        #: "improvise"
                        return MgImproviseAbility()
                def kwaftermath(self,items): 
                        #: "aftermath"
                        return MgAftermathAbility()
                def kwembalm(self,items): 
                        #: "embalm" cost
                        cost = items[0]
                        return MgEnbalmAbility(cost)
                def kweternalize(self,items): 
                        #: "eternalize" cost
                        cost = items[0]
                        return MgEternalizeAbility(cost)
                def kwafflict(self,items): 
                        #: "afflict" NUMBER
                        caliber = int(items[0].value)
                        return MgRippleAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
                def kwascend(self,items): 
                        #: "ascend"
                        return MgAscendAbility()
                def kwassist(self,items): 
                        #: "assist"
                        return MgAssistAbility()

                #STATEMENTS
                def statement(self,items):
                        return items[0]

                def statementblock(self,items):
                        return MgStatementBlock(*items)

                def expressionstatement(self,items):
                        expression = items[0]
                        return MgExpressionStatement(expression)
        
                def activationstatement(self,items):
                        cost = items[0]
                        instructions = items[1]
                        return MgActivationStatement(cost=cost,instructions=instructions)
         
                def abilitysequencestatement(self,items):
                        return MgAbilitySequenceStatement(*items)
                def quotedabilitystatement(self,items):
                        return MgQuotedAbilityStatement(items[0])
        
                #STATEMENTS - BEING STATEMENTS

                def hasstatement(self,items):
                         return items #TODO
        
                #STATEMENTS - CONDITIONAL STATEMENTS

                def whenstatement(self,items):
                        conditional = items[0]
                        consequence = items[1]
                        inverted=False
                        return MgWhenStatement(conditional,consequence,inverted)
                def whenstatementinv(self,items):
                        conditional = items[1]
                        consequence = items[0]
                        inverted=True
                        return MgWhenStatement(conditional,consequence,inverted)
        
        
        

        
                #EXPRESSIONS
                def effectexpression(self,items):
                        return items[0]

        
                #EXPRESSIONS - UNARY OPERATIONS
                def unaryop(self,items):
                        return items[0]
                def targetexpression(self,items):
                        subject = items[0]
                        return MgTargetExpression(subject)
                def anytargetexpression(self,items):
                        #Nullary variant of target expression
                        return MgTargetExpression(isAny=True)
                def withexpression(self,items):
                        return MgWithExpression(items[0])
                def indefinitesingularexpression(self,items):
                        return MgIndefiniteSingularExpression(items[0])
        
        
                #EXPRESSIONS - VALUE EXPRESSIONS
                def valueexpression(self,items):
                        return items[0]
                def valueterm(self,items):
                        return items[0]
                def valuenumber(self,items):
                        return MgNumberValue(items[0].value,MgNumberValue.NumberTypeEnum.Literal)
        
                #EXPRESSIONS - EVENT AND EFFECT EXPRESSIONS

                def eventexpression(self,items):
                        return items[0]
        
        
                def createexpression(self,items):
                        if len(items) == 2:
                                quantity = items[0]
                                declaration = items[1]
                                return MgCreateTokenExpression(declaration,quantity)
                        else:
                                declaration = items[0]
                                return MgCreateTokenExpression(declaration)

                def enterzoneexpression(self,items):
                        subject = items[0]
                        if len(items) == 3:
                                possessiveterm = items[1] #TODO: Deal with possessive constructions.
                                zone = items[2]
                                return MgChangeZoneExpression(subject=subject,zone=zone,entering=True)
                        else:
                                zone = items[1]
                                return MgChangeZoneExpression(subject=subject,zone=zone,entering=True)
                
                def leavezoneexpression(self,items):
                        subject = items[0]
                        if len(items) == 3:
                                possessiveterm = items[1] #TODO: Deal with possessive constructions.
                                zone = items[2]
                                return MgChangeZoneExpression(subject=subject,zone=zone,entering=False)
                        else:
                                zone = items[1]
                                return MgChangeZoneExpression(subject=subject,zone=zone,entering=False)


                def effectexpression(self,items):
                        return items[0]
        
                def keywordactionexpression(self,items):
                        return items[0]
                def basickeywordaction(self,items):
                        return items[0]
                def specialkeywordaction(self,items):
                        return items[0]
        
        
                def addmanaexpression(self,items):
                        if len(items) == 1:
                                manaexpr = items[0]
                                return MgAddManaExpression(manaexpr)
                        else:
                                playerexpr = items[0]
                                manaexpr = items[1]
                                return MgAddManaExpression(manaexpr,playerexpr)
        
        
        
                def destroyexpression(self,items):
                        return MgDestroyExpression(items[0])
                def dealsdamagevarianta(self,items):
                        #<origin> deals <damageExpression>? damage to <subject>?
                        origin = items[0]
                        variant = MgDealsDamageExpression.DealsDamageVariantEnum.VariantA
                        if len(items) == 3:
                                subject = items[2]
                                damageExpression = items[1]
                        elif len(items) == 2:
                                subject = items[1]
                                damageExpression = None
                        else:
                                subject = None
                                damageExpression = None
                        return MgDealsDamageExpression(origin,damageExpression,subject,variant)
        
                def dealsdamagevariantb(self,items):
                        #<origin> deals damage <damageExpression> to <subject>
                        origin = items[0]
                        damageExpression = items[1]
                        subject = items[2]
                        variant = MgDealsDamageExpression.DealsDamageVariantEnum.VariantB
                        return MgDealsDamageExpression(origin,damageExpression,subject,variant)
        
                def dealsdamagevariantc(self,items):
                        #<origin> deals damage to <subject> <damageExpression>
                        variant = MgDealsDamageExpression.DealsDamageVariantEnum.VariantC
                        origin = items[0]
                        damageExpression = items[2]
                        subject = items[1]
                        return MgDealsDamageExpression(origin,damageExpression,subject,variant)
        
        
                def sacrificeexpression(self,items):
                        if len(items) == 2:
                                controller = items[0]
                                subject = items[1]
                                return MgSacrificeExpression(subject=subject,controller=controller)
                        else:
                                subject = items[0]
                                return MgSacrificeExpression(subject=subject)
        

                #REFERENCES
                def referenceterm(self,items):
                        return items[0]
                def namereference(self,items):
                        #Note: the antecedent is determined during binding.
                        return MgNameReference(None)
                def thisreference(self,items):
                        #Note: the antecedent is determined during binding.
                        return MgThisReference(items[0])


                #TYPES, DECLARATIONS, ETC.

                def zone(self,items):
                        zone = items[0]
                        return MgZone(MgZone.ZoneEnum(zone.value))

                def declarationorreference(self,items):
                        return items[0]

                def declarationexpression(self,items):
                        definition = items[0]
                        return MgDeclarationExpression(definition)
        
                def nakeddeclarationexpression(self,items):
                        return items[0]
        
                def definitionexpression(self,items):
                        return items[0]

                def descriptionexpression(self,items):
                        return MgDescriptionExpression(*items)

                def namedexpression(self,items):
                        return MgNamedExpression(items[0])
        
        
                def qualifier(self,items):
                        return MgQualifier(MgQualifier.QualifierEnum(items[0].value))

                def modifier(self,items):
                        item = items[0]
                        if item.type == "ABILITYMODIFIER":
                                return MgAbilityModifier(MgAbilityModifier.AbilityModifierEnum(item.value))
                        elif item.type == "COMBATSTATUSMODIFIER":
                                return MgCombatStatusModifier(MgCombatStatusModifier.CombatStatusEnum(item.value))
                        elif item.type == "KEYWORDSTATUSMODIFIER":
                                return MgKeywordStatusModifier(MgKeywordStatusModifier.KeywordStatusEnum(item.value))
                        elif item.type == "TAPPEDSTATUSMODIFIER":
                                return MgTappedStatusModifier(MgTappedStatusModifier.TappedStatusEnum(item.value))
                        elif item.type == "EFFECTSTATUSMODIFIER":
                                return MgEffectStatusModifier(MgEffectStatusModifier.EffectStatusEnum(item.value))
                        else:
                                raise ValueError("Unrecognized entity modifier token: '{0}'".format(item))
        
                def typeexpression(self,items):
                        typeExpr = MgTypeExpression(*items)
                        return typeExpr
        
                def typeterm(self,items):
                        item = items[0]
                        if item.type == "TYPE":
                                return MgType(MgType.TypeEnum(item.value))
                        elif item.type == "SUBTYPESPELL":
                                return MgSubtype(MgSubtype.SpellSubtypeEnum(item.value))
                        elif item.type == "SUBTYPELAND":
                                return MgSubtype(MgSubtype.LandSubtypeEnum(item.value))
                        elif item.type == "SUBTYPEARTIFACT":
                                return MgSubtype(MgSubtype.ArtifactSubtypeEnum(item.value))
                        elif item.type == "SUBTYPEENCHANTMENT":
                                return MgSubtype(MgSubtype.EnchantmentSubtypeEnum(item.value))
                        elif item.type == "SUBTYPEPLANESWALKER":
                                return MgSubtype(MgSubtype.PlaneswalkerSubtypeEnum(item.value))
                        elif item.type == "SUBTYPECREATUREA" or item.type == "SUBTYPECREATUREB":
                                return MgSubtype(MgSubtype.CreatureSubtypeEnum(item.value))
                        elif item.type == "SUBTYPEPLANAR":
                                return MgSubtype(MgSubtype.PlanarSubtypeEnum(item.value))
                        elif item.type == "SUPERTYPE":
                                return MgSupertype(MgSupertype.SupertypeEnum(item.value))
                        else:
                                raise ValueError("Unrecognized type token: '{0}'".format(item))
                def nontypeterm(self,items):
                        typeterm = items[0]
                        return MgNonExpression(typeterm)

                def colorsingleexpr(self,items):
                        return MgColorExpression(*items)

                def colororexpr(self,items):
                        #Note: Internally, 'red, white, or green' is represented as 'red OR white OR green'
                        lhs = None
                        for item in items:
                                if lhs == None:
                                        lhs = item
                                else:
                                        lhs = MgOrExpression(lhs,item)
                        return MgColorExpression(lhs)
        
                def colorandexpr(self,items):
                        #Note: Internally, 'red, white, and green' is represented as 'red AND white AND green'
                        lhs = None
                        for item in items:
                                if lhs == None:
                                        lhs = item
                                else:
                                        lhs = MgAndExpression(lhs,item)
                        return MgColorExpression(lhs)

                def colorandorexpr(self,items):
                        #Note: Internally, 'red, white, and/or green' is represented as 'red AND/OR white AND/OR green'
                        lhs = None
                        for item in items:
                                if lhs == None:
                                        lhs = item
                                else:
                                        lhs = MgAndOrExpression(lhs,item)
                        return MgColorExpression(lhs)

                def colorterm(self,items):
                        return MgColorTerm(MgColorTerm.ColorTermEnum(items[0].value))
        
                def noncolorterm(self,items):
                        return MgNonExpression(MgColorTerm(MgColorTerm.ColorTermEnum(items[0].value)))
        
                def cost(self,items):
                        return items[0]
                def costsequence(self,items):
                        return MgCostSequenceExpression(*items)
                def tapuntapsymbol(self,items):
                        if items[0].type == "TAPSYMBOL":
                                return MgTapUntapSymbol(isTap=True)
                        else:
                                return MgTapUntapSymbol(isTap=False)
        
                def objectname(self,items):
                        return MgName(items[0].value)
        
                def valueexpression(self,items):
                        return items[0]
        
                def valuecardinal(self,items):
                        return MgNumberValue(w2n.word_to_num(items[0].value),MgNumberValue.NumberTypeEnum.Cardinal)
        
        
        
                def manaspecificationexpression(self,items):
                        quantity = items[0]
                        specifiers = items[1:]
                        return MgManaSpecificationExpression(quantity,*specifiers)
                def manaspecifier(self,items):
                        return items[0]
                def anycolorexpression(self,items):
                        return MgAnyColorSpecifier(anyOneColor=False)
                def anyonecolorspecifier(self,items):
                        #"of any one color" variant
                        return MgAnyColorSpecifier(anyOneColor=True)

                def manaexpression(self,items):
                        manaExpr = MgManaExpression(*items)
                        return manaExpr

                def manasymbol(self,items):
                        subtree = items[0] #A mana symbol should only have one child: a marker sequence.


                        colorEnum = None #The flags indicating color/colorlessness
                        modifierEnum = None #modifiers like phyrexian, snow, etc.
                        cvalue = -1 #The value of the symbol. This is used when the mana is generic or variable (e.g. 5, X).

                        #Here we apply any modifier flags that the AST cares about.
                        if subtree.data == "halfmanasymbol":
                                modifier = MgManaSymbol.ManaModifier.Half
                        elif subtree.data == "phyrexianmanasymbol": 
                                modifier = MgManaSymbol.ManaModifier.Phyrexian
                        elif subtree.data == "alternate2manasymbol":
                                modifier = MgManaSymbol.ManaModifier.AlternateTwo
                        elif subtree.data == "snowmanasymbol": 
                                modifier = MgManaSymbol.ManaModifier.Snow
                        elif subtree.data == "xmanasymbol":
                                cvalue = "X" #TODO: This doesn't cover the infinity symbol.
        
        
                        def updateColorEnum(colorEnum,flag):
                                #Updates the color enum with an additional flag.
                                #It's easier to write this once in an inner function
                                #than to spell it out every single time.
                                if colorEnum is None:
                                        colorEnum = flag
                                else:
                                        colorEnum = colorEnum | flag
        
                                return colorEnum #Return the updated version.
        
        
                        for child in subtree.children:
                                if type(child) == Token and child.type == "NUMBER":
                                        cvalue = int(child.value) #This is a generic mana symbol
                                else:
                                        childAlias = child.data
                                        if childAlias == "whitemarker":
                                                colorEnum = updateColorEnum(colorEnum,MgManaSymbol.ManaType.White)
                                        elif childAlias == "bluemarker":
                                                colorEnum = updateColorEnum(colorEnum,MgManaSymbol.ManaType.Blue)
                                        elif childAlias == "blackmarker":
                                                colorEnum = updateColorEnum(colorEnum,MgManaSymbol.ManaType.Black)
                                        elif childAlias == "redmarker":
                                                colorEnum = updateColorEnum(colorEnum,MgManaSymbol.ManaType.Red)
                                        elif childAlias == "greenmarker":
                                                colorEnum = updateColorEnum(colorEnum,MgManaSymbol.ManaType.Green)
                                        elif childAlias == "colorlessmarker":
                                                colorEnum = updateColorEnum(colorEnum,MgManaSymbol.ManaType.Colorless)

                        return MgManaSymbol(colorv=colorEnum,modifiers=modifierEnum,cvalue=cvalue)
        