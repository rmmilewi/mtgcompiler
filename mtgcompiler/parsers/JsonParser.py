import collections
from mtgcompiler.parsers.baseparser import BaseParser
from mtgcompiler.AST.reference import MgName,MgNameReference,MgTapUntapSymbol
from mtgcompiler.AST.card import MgTypeLine,MgFlavorText,MgTextBox,MgCard
from mtgcompiler.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.AST.statements import MgKeywordAbilityListStatement,MgStatementBlock,MgExpressionStatement,MgActivationStatement

from mtgcompiler.AST.expressions import MgNumberValue,MgPTExpression,MgManaExpression,MgTypeExpression,MgDescriptionExpression,MgNamedExpression,MgCostSequenceExpression
from mtgcompiler.AST.expressions import MgColorExpression,MgAndExpression,MgOrExpression,MgAndOrExpression,MgTargetExpression
from mtgcompiler.AST.expressions import MgDestroyExpression,MgExileExpression,MgDealsDamageExpression

from mtgcompiler.AST.abilities import MgReminderText,MgAbilityWord,MgRegularAbility
from mtgcompiler.AST.abilities import MgDeathtouchAbility,MgDefenderAbility,MgDoubleStrikeAbility,MgFirstStrikeAbility,MgTrampleAbility
from mtgcompiler.AST.abilities import MgFlashAbility,MgFlyingAbility,MgHasteAbility,MgIndestructibleAbility,MgReachAbility



from mtgcompiler.AST.abilities import MgHexproofAbility,MgProtectionAbility,MgLandwalkAbility,MgRampageAbility
from mtgcompiler.AST.abilities import MgFadingAbility, MgAmplifyAbility, MgModularAbility, MgBushidoAbility
from mtgcompiler.AST.abilities import MgSoulshiftAbility, MgDredgeAbility, MgBloodthirstAbility, MgGraftAbility
from mtgcompiler.AST.abilities import MgRippleAbility, MgVanishingAbility, MgAbsorbAbility, MgFrenzyAbility
from mtgcompiler.AST.abilities import MgPoisonousAbility, MgDevourAbility, MgAnnihilatorAbility, MgTributeAbility
from mtgcompiler.AST.abilities import MgRenownAbility, MgCrewAbility, MgFabricateAbility, MgAfflictAbility, MgSurveilAbility

from mtgcompiler.AST.abilities import MgCumulativeUpkeepAbility, MgBuybackAbility, MgCyclingAbility, MgKickerAbility, MgMadnessAbility
from mtgcompiler.AST.abilities import MgMorphAbility, MgNinjutsuAbility, MgTransmuteAbility, MgRecoverAbility
from mtgcompiler.AST.abilities import MgAuraSwapAbility, MgTransfigureAbility, MgEvokeAbility, MgMiracleAbility
from mtgcompiler.AST.abilities import MgOverloadAbility, MgScavengeAbility, MgOutlastAbility, MgSurgeAbility
from mtgcompiler.AST.abilities import MgEmergeAbility, MgEscalateAbility, MgEnbalmAbility, MgEternalizeAbility, MgJumpStartAbility

from mtgcompiler.AST.abilities import MgSpliceAbility,MgEnchantAbility,MgEquipAbility,MgBandingAbility,MgAffinityAbility
from mtgcompiler.AST.abilities import MgOfferingAbility,MgForecastAbility,MgSuspendAbility,MgChampionAbility,MgReinforceAbility
from mtgcompiler.AST.abilities import MgHiddenAgendaAbility,MgAwakenAbility,MgPartnerAbility

from lark import Lark #Lexing and parsing!
from lark import Transformer #Converting the parse tree into something useful.
from lark.tree import pydot__tree_to_png #For rendering the parse tree.
from lark.lexer import Token

#Convenience function for flattening lists (of lists)+
def flatten(l):
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

class JsonParser(BaseParser):

        def __init__(self,startText='cardtext'):
                """Calling this constructor causes the Lark parser and the parse-to-AST transformer
                to be instantiated."""
                self._lp,self._tf = self.define_grammar(startText)
                #TODO: There has to be a better way to set different start rules.
                self._miniManaParser,self._miniManaTransformer = self.define_grammar("manaexpression")
                self._miniTypelineParser,self._miniTypelineTransformer = self.define_grammar("typeline")
                
        class JsonTransformer(Transformer):
                
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
                        descriptor = items[0].children[0]
                        return MgEnchantAbility(descriptor)
                def kwequip(self,items):
                        if len(items[0].children) == 1:
                                #Equip <cost>
                                cost = items[0].children[0]
                                return MgEquipAbility(cost)
                        else:
                                #Equip <quality> creature <cost>
                                quality = items[0].children[0]
                                cost = items[0].children[1]
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
                        #: "suspend" NUMBER
                        caliber = int(items[0].value)
                        return MgSuspendAbility(MgNumberValue(caliber,MgNumberValue.NumberTypeEnum.Literal))
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
                        
                #EXPRESSIONS
                def expression(self,items):
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
                        
                        
                        
                #EXPRESSIONS - VALUE EXPRESSIONS
                def valueexpression(self,items):
                        return items[0]
                def valueterm(self,items):
                        return items[0]
                def valuenumber(self,items):
                        return MgNumberValue(items[0].value,MgNumberValue.NumberTypeEnum.Literal)
                        
                #EXPRESSIONS - EFFECT EXPRESSIONS
                def effectexpression(self,items):
                        return items[0]
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
                        
                        #if len(items) == 3:
                        #        subject = items[2]
                        #        damageExpression = items[1]
                        #elif len(items) == 2:
                        #        subject = items[1]
                        #        damageExpression = None
                        #else:
                        #        subject = None
                        #        damageExpression = None
                        return MgDealsDamageExpression(origin,damageExpression,subject,variant)
                        
                def dealsdamagevariantc(self,items):
                        #<origin> deals damage to <subject> <damageExpression>
                        variant = MgDealsDamageExpression.DealsDamageVariantEnum.VariantC
                        origin = items[0]
                        damageExpression = items[2]
                        subject = items[1]
                        return MgDealsDamageExpression(origin,damageExpression,subject,variant)
                
                #REFERENCES
                def referenceterm(self,items):
                        return items[0]
                def namereference(self,items):
                        #This gets bound to the card name later.
                        return MgNameReference(None)
                
                
                #TYPES, DESCRIPTIONS, ETC.      
                def descriptionexpression(self,items):
                        return MgDescriptionExpression(*items)
                
                def namedexpression(self,items):
                        return MgNamedExpression(items[0])
                        
                def typeexpression(self,items):
                        print("TYPE EXPRESSION",items)
                        typeExpr = MgTypeExpression(*items)
                        
                def typeterm(self,items):
                        print("TYPETERM",items)
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
                
                
        def define_grammar(self,startText='cardtext'):                
                larkparser = Lark(r"""
                
                        typeline: typelinesupert typelinet ("—" typelinesubt)?
                        typelinesupert: SUPERTYPE*
                        typelinet: TYPE*
                        typelinesubt: SUBTYPE*
                
                        cardtext : ability*
                        remindertext : /\(.*?\)/
                        
                        ability : keywordlist remindertext?
                        | abilityword? statementblock remindertext? -> regularability
                        abilityword: WORD "—"
                        
                        keywordlist: keywordsequence
                        keywordsequence: keywordability | keywordsequence ("," | ";") keywordability
                        
                        //TODO: Where to place compound statements in all this?
                        statementblock : (compoundstatement | statement) ["."] | statementblock (compoundstatement | statement) ["."]
                        
                        
                        //STATEMENTS
                        
                        statement: expressionstatement
                        | conditionalstatement 
                        | activationstatement
                        | beingstatement
                        | thenstatement
                        | maystatement
                        
                        maystatement: playerterm "may" statement
                        
                        beingstatement: declarationorreference "is" statement -> isstatement
                        | declarationorreference ("has"|"have"|"had") statement -> hasstatement
                        | declarationorreference "isn't" statement -> isntstatement
                        | "it's" statement -> itsstatement
                        | "it's" "not" statement -> itsnotstatement
                        | declarationorreference "can" statement -> canstatement
                        | declarationorreference "can't" statement -> cantstatement
                        
                        thenstatement: "then" statement
                        
                        expressionstatement: expression
                        
                        compoundstatement: statement  ("," statement ",")* "then" statement -> compoundthenstatement
                        | statement ("," statement ",")* "and" statement -> compoundandstatement
                        
                        conditionalstatement: "if" statement "," statement -> ifstatement
                        | statement "if" statement -> ifstatementinv
                        | "whenever" statement "," statement -> wheneverstatement
                        | statement "whenever" statement -> wheneverstatementinv
                        | "when" statement "," statement -> whenstatement
                        | statement "when" statement -> whenstatementinv
                        | "at" statement "," statement -> atstatement
                        | statement "at" statement -> atstatementinv
                        | "as" "long" "as" statement "," statement -> aslongasstatement
                        | statement "as" "long" "as" statement -> aslongasstatementinv
                        | "for" statement "," statement -> forstatement
                        | statement "for" statement -> forstatementinv
                        | "otherwise" "," statement -> otherwisestatement
                        | statement "unless" statement -> unlessstatement
                        | "while" statement "," statement -> whilestatement
                        | "until" timestepexpression "," statement -> untilstatement
                        | statement "until" timestepexpression -> untilstatementinv
                        
                        activationstatement: cost ":" statementblock
                        
                        //KEYWORD ABILITIES
                        
                        keywordability: kwdeathtouch
                        | kwdefender | kwdoublestrike | kwenchant | kwequip | kwfirststrike
                        | kwflash | kwflying | kwhaste | kwhexproof | kwindestructible
                        | kwintimidate | kwlandwalk | kwlifelink | kwprotection | kwreach 
                        | kwshroud | kwtrample | kwvigilance | kwbanding 
                        | kwrampage | kwcumulativeupkeep | kwflanking | kwphasing
                        | kwbuyback | kwshadow | kwcycling | kwecho | kwhorsemanship
                        | kwfading | kwkicker | kwflashback | kwmadness | kwfear
                        | kwmorph | kwamplify |kwprovoke | kwstorm | kwaffinity
                        | kwentwine | kwmodular |kwsunburst | kwbushido | kwsoulshift
                        | kwsplice | kwoffering |kwninjutsu | kwepic | kwconvoke
                        | kwdredge | kwtransmute | kwbloodthirst | kwhaunt | kwreplicate
                        | kwforecast | kwgraft | kwrecover | kwripple | kwsplitsecond
                        | kwsuspend | kwvanishing | kwabsorb | kwauraswap | kwdelve
                        | kwfortify | kwfrenzy | kwgravestorm | kwpoisonous | kwtransfigure
                        | kwchampion | kwchangeling | kwevoke | kwhideaway | kwprowl
                        | kwreinforce | kwconspire | kwpersist | kwwither | kwretrace
                        | kwdevour | kwexalted | kwunearth | kwcascade | kwannihilator
                        | kwlevelup | kwrebound | kwtotemarmor | kwinfect | kwbattlecry
                        | kwlivingweapon | kwundying | kwmiracle | kwsoulbond | kwoverload
                        | kwscavenge | kwunleash |kwcipher | kwevolve | kwextort
                        | kwfuse | kwbestow | kwtribute | kwdethrone | kwhiddenagenda
                        | kwoutlast | kwprowess | kwdash | kwexploit | kwmenace
                        | kwrenown | kwawaken | kwdevoid | kwingest | kwmyriad
                        | kwsurge | kwskulk | kwemerge | kwescalate | kwmelee
                        | kwcrew | kwfabricate | kwpartner | kwundaunted | kwimprovise
                        | kwaftermath | kwembalm | kweternalize | kwafflict | kwascend
                        |kwassist
                        
                        kwdeathtouch: "deathtouch"
                        kwdefender: "defender"
                        kwdoublestrike: "double" "strike"
                        kwenchant: "enchant" typeexpression
                        kwequip: "equip" cost | "equip" descriptionexpression cost
                        kwfirststrike: "first strike"
                        kwflash: "flash"
                        kwflying: "flying"
                        kwhaste: "haste"
                        kwhexproof: "hexproof" | "hexproof" "from" descriptionexpression
                        kwindestructible: "indestructible"
                        kwintimidate: "intimidate"
                        kwlandwalk: typeexpression "walk"
                        kwlifelink: "lifelink"
                        kwprotection: "protection" "from" descriptionexpression ("and" "from" descriptionexpression)*
                        kwreach: "reach"
                        kwshroud: "shroud"
                        kwtrample: "trample"
                        kwvigilance: "vigilance"
                        kwbanding: "banding" | "bands" "with" "other" descriptionexpression
                        kwrampage: "rampage" NUMBER
                        kwcumulativeupkeep: "cumulative" "upkeep" cost
                        kwflanking: "flanking"
                        kwphasing: "phasing"
                        kwbuyback: "buyback" cost
                        kwshadow: "shadow"
                        kwcycling: [typeexpression] "cycling" cost
                        kwecho: "echo" cost
                        kwhorsemanship: "horsemanship"
                        kwfading: "fading" NUMBER
                        kwkicker: "kicker" cost -> kicker
                        | "multikicker" cost -> multikicker
                        kwflashback: "flashback" cost
                        kwmadness: "madness" cost
                        kwfear: "fear"
                        kwmorph: "morph" cost -> kwmorph
                        | "megamorph" cost -> kwmegamorph
                        kwamplify: "amplify" NUMBER
                        kwprovoke: "provoke"
                        kwstorm: "storm"
                        kwaffinity: "affinity" "for" typeexpression
                        kwentwine: "entwine" cost
                        kwmodular: "modular" NUMBER
                        kwsunburst: "sunburst"
                        kwbushido: "bushido" NUMBER
                        kwsoulshift: "soulshift" NUMBER
                        kwsplice: "splice" "onto" typeexpression cost
                        kwoffering: typeexpression "offering"
                        kwninjutsu: "ninjutsu" cost
                        kwepic: "epic"
                        kwconvoke: "convoke"
                        kwdredge: "dredge" NUMBER
                        kwtransmute: "transmute" cost
                        kwbloodthirst: "bloodthirst" NUMBER
                        kwhaunt: "haunt"
                        kwreplicate: "replicate" cost
                        kwforecast: "forecast"
                        kwgraft: "graft"
                        kwrecover: "recover" cost
                        kwripple: "ripple" NUMBER
                        kwsplitsecond: "split" "second"
                        kwsuspend: "suspend" NUMBER
                        kwvanishing: "vanishing" [NUMBER]
                        kwabsorb: "absorb" NUMBER
                        kwauraswap: "aura" "swap" cost
                        kwdelve: "delve"
                        kwfortify: "fortify" cost
                        kwfrenzy: "frenzy"
                        kwgravestorm: "gravestorm"
                        kwpoisonous: "poisonous" NUMBER
                        kwtransfigure: "transfigure" cost
                        kwchampion: "champion" "a"["n"] typeexpression
                        kwchangeling: "changeling"
                        kwevoke: "evoke" cost
                        kwhideaway: "hideaway"
                        kwprowl: "prowl" cost
                        kwreinforce: "reinforce" cost
                        kwconspire: "conspire"
                        kwpersist: "persist"
                        kwwither: "wither"
                        kwretrace: "retrace" cost
                        kwdevour: "devour" NUMBER
                        kwexalted: "exalted"
                        kwunearth: "unearth" cost
                        kwcascade: "cascade"
                        kwannihilator: "annihilator" NUMBER
                        kwlevelup: "level up" cost
                        kwrebound: "rebound"
                        kwtotemarmor: "totem" "armor"
                        kwinfect: "infect"
                        kwbattlecry: "battle" "cry"
                        kwlivingweapon: "living" "weapon"
                        kwundying: "undying"
                        kwmiracle: "miracle" cost
                        kwsoulbond: "soulbond"
                        kwoverload: "overload" cost
                        kwscavenge: "scavenge" cost
                        kwunleash: "unleash"
                        kwcipher: "cipher"
                        kwevolve: "evolve"
                        kwextort: "extort"
                        kwfuse: "fuse"
                        kwbestow: "bestow" cost
                        kwtribute: "tribute" NUMBER
                        kwdethrone: "dethrone"
                        kwhiddenagenda: "hidden" "agenda" -> kwhiddenagenda
                        | "double" "agenda" -> kwdoubleagenda
                        kwoutlast: "outlast" cost
                        kwprowess: "prowess"
                        kwdash: "dash" cost
                        kwexploit: "exploit"
                        kwmenace: "menace"
                        kwrenown: "renown" NUMBER
                        kwawaken: "awaken" cost
                        kwdevoid: "devoid"
                        kwingest: "ingest"
                        kwmyriad: "myriad"
                        kwsurge: "surge" cost
                        kwskulk: "skulk"
                        kwemerge: "emerge" cost
                        kwescalate: "escalate" cost
                        kwmelee: "melee"
                        kwcrew: "crew" NUMBER
                        kwfabricate: "fabricate" NUMBER
                        kwpartner: "partner" ["with" objectname]
                        kwundaunted: "undaunted"
                        kwimprovise: "improvise"
                        kwaftermath: "aftermath"
                        kwembalm: "embalm" cost
                        kweternalize: "eternalize" cost
                        kwafflict: "afflict" NUMBER
                        kwascend: "ascend"
                        kwassist: "assist"
                        
                        //ABILITY COSTS
                        
                        cost: costsequence | dashcostexpression //[TODO]
                        costsequence: ( tapuntapsymbol | manaexpression | effectexpression) ("," (tapuntapsymbol | manaexpression | effectexpression))*
                        dashcostexpression: "—" effectexpression
                        
                        ///VALUE EXPRESSIONS
                        
                        //[TODO: Need to account for custom values, variables, 'equals to' expressions, etc.]
                        valueexpression: valueterm | equaltoexpression | numberofexpression
                        equaltoexpression: eventoreffect? "equal" "to" (valueterm | declarationorreference)
                        numberofexpression: ("a"|"the") "number" "of" declarationorreference
                        valueterm: valuenumber | valuequantity | valuefrequency | valuecustom
                        valuenumber: NUMBER
                        valuequantity: "one" | "two" | "three" | "four" | "five" | "six" //TODO
                        //[TODO: needs another rule to have a different derivation from valuequantity]
                        valuefrequency: "once" | "twice" | valuequantity "times"
                        valuecustom: "X" | "*"
                        
                        
                        //DECLARATIONS AND REFERENCES
                        
                        declarationexpression: definitionexpression -> nakeddeclarationexpression
                        | "any" "target" -> anytargetexpression
                        | "target" definitionexpression -> targetexpression //[TODO: modifiers like 'up to three other target ___'].
                        | "each" definitionexpression -> eachexpression
                        | "all" definitionexpression -> allexpression
                        | "a"["n"] definitionexpression -> indefinitesingularexpression
                        
                        definitionexpression: descriptionexpression
                        | definitionexpression "or" descriptionexpression -> ordefinitionexpression
                        | definitionexpression "and" descriptionexpression -> anddefinitionexpression
                        | definitionexpression "and/or" descriptionexpression -> andordefinitionexpression
                        
                        declarationorreference: referenceterm | declarationexpression
                        
                        descriptionexpression: (colorexpression | namedexpression | manaexpression | typeexpression
                        | ptexpression | qualifier | modifier | locationexpression | valuequantity | controlsexpression)+
                        | playerterm
                        
                        referenceterm: namereference | itreference | thatreference | thisreference | selfreference | thereference | objectname
                        namereference: NAMEREFSYMBOL
                        itreference: "it"
                        thatreference: ("that"|"those") definitionexpression
                        thisreference: "this" definitionexpression
                        selfreference: "itself" | "himself" | "herself"
                        thereference: "the" definitionexpression
                        playerterm: PLAYERTERM | referenceterm
                        possessiveterm: "your" | "their" | referenceterm "'s" //[TODO]
                        
                        
                        ptexpression: valueexpression "/" valueexpression
                        namedexpression: "named" objectname
                        locationexpression: ("in" | "on") (playerpossessiveexpr | "a"["n"] )? zone
                        controlsexpression: playerterm "controls"
                        
                        //EVENT AND EFFECT EXPRESSIONS
                        
                        eventoreffect: eventexpression | effectexpression
                        
                        eventexpression: etbexpression 
                        | ltbexpression
                        | playerdoesexpression
                        
                        playerdoesexpression: playerterm ("do" | "does") -> playerdoesexpression
                        | playerterm ("don't" | "doesn't") -> playerdoesnotexpression
                        
                        etbexpression: declarationorreference "enters" "the" "battlefield"
                        ltbexpression: declarationorreference "leaves" "the" "battlefield"
                        
                        effectexpression: keywordactionexpression
                        | dealsdamageexpression
                        | returnexpression
                        | putinzoneexpression
                        | spendmanaexpression
                        | paylifeexpression
                        | addmanaexpression
                        
                        
                        dealsdamageexpression:  declarationorreference "deals" valueexpression? "damage" ("to" declarationorreference)? -> dealsdamagevarianta
                        | declarationorreference "deals" "damage" valueexpression "to" declarationorreference  -> dealsdamagevariantb
                        | declarationorreference "deals" "damage" "to" declarationorreference  valueexpression -> dealsdamagevariantc
                        
                        returnexpression: playerterm "return"["s"] declarationorreference to possessiveterm? zone //[TODO]
                        
                        putinzoneexpression: "put" descriptionorreference ("onto" | "into") possessiveterm? zone definitionexpression?
                        
                        spendmanaexpression: "spend mana" //[TODO]
                        
                        paylifeexpression: "pay" valueexpression? "life" //[TODO]
                        
                        addmanaexpression: "add" manaexpression
                        
                        keywordactionexpression: basickeywordaction | specialkeywordaction
                        
                        basickeywordaction: activateexpression
                        | attachexpression
                        | castexpression
                        | uncastexpression
                        | createexpression
                        | destroyexpression
                        | discardexpression
                        | doubleexpression
                        | exchangeexpression
                        | exileexpression
                        | fightexpression
                        | playexpression
                        | revealexpression
                        | sacrificeexpression
                        | searchexpression
                        | shuffleexpression
                        | tapuntapexpression
                        
                        attachexpression: "attach" declarationorreference "to" declarationorreference
                        | "unattach" declarationorreference ("from" declarationorreference)? -> unattachexpression
                        | playerterm "attaches" declarationorreference "to" declarationorreference -> playerattachesexpression
                        
                        castexpression: "cast" declarationorreference (castmodifier ("and" castmodifier")?)*
                        castmodifier: "without" "paying" "its" "mana" "cost" -> castwithoutpaying
                        | "as" "though" beingstatement -> castasthough
                        
                        uncastexpression: "counter" declarationorreference
                        createexpression: "create" declarationorreference
                        destroyexpression: "destroy" declarationorreference
                        discardexpression: "discard" declarationorreference
                        doubleexpression: "double" //[TODO]
                        exchangeexpression: "exchange" //[TODO]
                        exileexpression: "exile" declarationorreference
                        fightexpression: "fight" //[TODO]
                        playexpression: "play" declarationorreference
                        revealexpression: "reveal" declarationorreference
                        sacrificeexpression: "sacrifice" declarationorreference
                        | playerterm "sacrifices" declarationorreference -> playersacrificeexpression
                        searchexpression: "search" possessiveterm "library" "for" declarationorreference //[TODO: different zones]
                        shuffleexpression: "shuffle" possessiveterm "library"
                        tapuntapexpression: "tap" declarationorreference -> tapexpression
                        | "untap" declarationorreference -> untapexpression
                        
                        specialkeywordaction: regenerateexpression
                        | scryexpression
                        | fatesealexpression
                        | clashexpression
                        | planeswalkexpression
                        | setinmotionexpression
                        | abandonexpression
                        | proliferateexpression
                        | transformexpression
                        | populateexpression
                        | monstrousexpression
                        | voteexpression
                        | bolsterexpression
                        | manifestexpression
                        | supportexpression
                        | investigateexpression
                        | meldexpression
                        | goadexpression
                        | exertexpression
                        | exploreexpression
                        | assembleexpression
                        
                        regenerateexpression: "regenerate" declarationorreference
                        scryexpression: "scry" valueexpression
                        fatesealexpression: "fateseal" valueexpression
                        planeswalkexpression: playerterm "planeswalk"["s"] "to" PLANE
                        setinmotionexpression: playerterm "set"["s"] declarationorreference "in" "motion"
                        abandonexpression: playerterm? "abandon"["s"] declarationorreference //[Note: Has never been used]
                        proliferateexpression: "proliferate"
                        transformexpression: "transform" declarationorreference
                        populateexpression: "populate"
                        monstrousexpression: declarationorreference "becomes" "monstrous" //[TODO?]
                        bolsterexpression: "bolster" valueexpression
                        manifestexpression: playerterm? "the" "top" valueexpression? "card"["s"] "of" possessiveterm "library"
                        supportexpression: "support" valueexpression
                        investigateexpression: "investigate"
                        meldexpression: "meld" "them" "into" objectname
                        goadexpression: "goad" declarationorreference
                        exertexpression: "exert" declarationorreference
                        exploreexpression: "explore"
                        //[Note: Assemble is an Un-set only keyword action. I might remove this.]
                        assembleexpression: declarationorreference? "assemble"["s"] declarationorreference | assembleexpression valueexpression
                        
                        
                        
                        
                        
                        
                        
                        //TYPE/MANA/COLOR EXPRESSIONS, MODIFIERS, AND MISCELLANEOUS
                        
                        timestepexpression: "end of turn" //[TODO]
                        
                        //TODO: What about comma-delimited type expressions?
                        typeexpression: (typeterm)+
                        
                        typeterm: (TYPE ["s"] | SUBTYPESPELL ["s"] | SUBTYPELAND ["s"] | SUBTYPEARTIFACT ["s"] | SUBTYPEENCHANTMENT ["s"] | SUBTYPEPLANESWALKER | SUBTYPECREATUREA | SUBTYPECREATUREB | SUBTYPEPLANAR | SUPERTYPE)
                        | "non"["-"] typeterm -> nontypeterm
                        
                        TYPE: "planeswalker" | "conspiracy" | "creature" | "enchantment" | "instant"
                        | "land" | "phenomenon" | "plane" | "artifact" | "scheme" | "sorcery"
                        | "tribal" | "vanguard"
                        
                        SUBTYPESPELL : "arcane" | "trap"
                        
                        SUBTYPELAND: "desert" | "forest" | "gate" | "island" | "lair" | "locus"
                        | "mine" | "mountain" | "plains" | "power-plant" | "swamp" | "tower" | "urza's"
                        
                        SUBTYPEARTIFACT: "clue" | "contraption" | "equipment" | "fortification" | "treasure" | "vehicle"
                        
                        SUBTYPEENCHANTMENT: "aura" | "cartouche" | "curse" | "saga" | "shrine"
                        
                        SUBTYPEPLANESWALKER: "ajani" | "aminatou" | "angrath" | "arlinn" | "ashiok" | "bolas" | "chandra"
                        | "dack" | "daretti" | "domri" | "dovin" | "elspeth" | "estrid" | "freyalise" | "garruk" | "gideon"
                        | "huatli" | "jace" | "jaya" | "karn" | "kaya" | "kiora" | "koth" | "liliana" | "nahiri" | "narset"
                        | "nissa" | "nixilis" | "ral" | "rowan" | "saheeli" | "samut" | "sarkhan" | "sorin" | "tamiyo" | "teferi"
                        | "tezzeret" | "tibalt" | "ugin" | "venser" | "vivien" | "vraska" | "will" | "windgrace" | "xenagos"
                        | "yanggu" | "yanling"
                        
                        
                        //[TODO: SUBTYPECREATUREA and SUBTYPECREATUREB are split up because having such a long list of alternatives apparently]
                        //[causes Lark to suffer a recursion depth error. We should see if this is fixable.]
                        
                        SUBTYPECREATUREA: "advisor" | "aetherborn" | "ally" | "angel" | "antelope" | "ape" | "archer" | "archon" 
                        | "artificer" | "assassin" | "assembly-worker" | "atog" | "aurochs" | "avatar" | "azra" | "badger"
                        | "barbarian" | "basilisk" | "bat" | "bear" | "beast" | "beeble" | "berserker" | "bird" | "blinkmoth"
                        | "boar" | "bringer" | "brushwagg" | "camarid" | "camel" | "caribou" | "carrier" | "cat" | "centaur"
                        | "cephalid" | "chimera" | "citizen" | "cleric" | "cockatrice" | "construct" | "coward" | "crab"
                        | "crocodile" | "cyclops" | "dauthi" | "demon" | "deserter" | "devil" | "dinosaur" | "djinn" | "dragon"
                        | "drake" | "dreadnought" | "drone" | "druid" | "dryad" | "dwarf" | "efreet" | "egg" | "elder" | "eldrazi"
                        | "elemental" | "elephant" | "elf" | "elk" | "eye" | "faerie" | "ferret" | "fish" | "flagbearer" | "fox"
                        
                        SUBTYPECREATUREB: "frog" | "fungus" | "gargoyle" | "germ" | "giant" | "gnome" | "goat" | "goblin" | "god" | "golem" | "gorgon"
                        | "graveborn" | "gremlin" | "griffin" | "hag" | "harpy" | "hellion" | "hippo" | "hippogriff" | "homarid" | "homunculus"
                        | "horror" | "horse" | "hound" | "human" | "hydra" | "hyena" | "illusion" | "imp" | "incarnation" | "insect"
                        | "jackal" | "jellyfish" | "juggernaut" | "kavu" | "kirin" | "kithkin" | "knight" | "kobold" | "kor" | "kraken"
                        | "lamia" | "lammasu" | "leech" | "leviathan" | "lhurgoyf" | "licid" | "lizard" | "manticore" | "masticore"
                        | "mercenary" | "merfolk" | "metathran" | "minion" | "minotaur" | "mole" | "monger" | "mongoose" | "monk" 
                        | "monkey" | "moonfolk" | "mutant" | "myr" | "mystic" | "naga" | "nautilus" | "nephilim" | "nightmare" 
                        | "nightstalker" | "ninja" | "noggle" | "nomad" | "nymph" | "octopus" | "ogre" | "ooze" | "orb" | "orc" 
                        | "orgg" | "ouphe" | "ox" | "oyster" | "pangolin" | "pegasus" | "pentavite" | "pest" | "phelddagrif" | "phoenix"
                        | "pilot" | "pincher" | "pirate" | "plant" | "praetor" | "prism" | "processor" | "rabbit" | "rat" | "rebel"
                        | "reflection" | "rhino" | "rigger" | "rogue" | "sable" | "salamander" | "samurai" | "sand" | "saproling" | "satyr"
                        | "scarecrow" | "scion" | "scorpion" | "scout" | "serf" | "serpent" | "servo" | "shade" | "shaman" | "shapeshifter"
                        | "sheep" | "siren" | "skeleton" | "slith" | "sliver" | "slug" | "snake" | "soldier" | "soltari" | "spawn" | "specter"
                        | "spellshaper" | "sphinx" | "spider" | "spike" | "spirit" | "splinter" | "sponge" | "squid" | "squirrel" | "starfish"
                        | "surrakar" | "survivor" | "tetravite" | "thalakos" | "thopter" | "thrull" | "treefolk" | "trilobite" | "triskelavite"
                        | "troll" | "turtle" | "unicorn" | "vampire" | "vedalken" | "viashino" | "volver" | "wall" | "warrior" | "weird"
                        | "werewolf" | "whale" | "wizard" | "wolf" | "wolverine" | "wombat" | "worm" | "wraith" | "wurm" | "yeti" 
                        | "zombie" | "zubera"
                        
                        SUBTYPEPLANAR: "alara" | "arkhos" | "azgol" | "belenon" | "bolas’s meditation realm"
                        | "dominaria" | "equilor" | "ergamon" | "fabacin" | "innistrad" | "iquatana" | "ir" 
                        | "kaldheim" | "kamigawa" | "karsus" | "kephalai" | "kinshala" | "kolbahan" | "kyneth"
                        | "lorwyn" | "luvion" | "mercadia" | "mirrodin" | "moag" | "mongseng" | "muraganda"
                        | "new phyrexia" | "phyrexia" | "pyrulea" | "rabiah" | "rath" | "ravnica" | "regatha"
                        | "segovia" | "serra’s realm" | "shadowmoor" | "shandalar" | "ulgrotha" | "valla"
                        | "vryn" | "wildfire" | "xerex" | "zendikar"
                        
                        SUBTYPE: SUBTYPESPELL | SUBTYPELAND | SUBTYPEARTIFACT | SUBTYPEENCHANTMENT | SUBTYPEPLANESWALKER | SUBTYPECREATUREA | SUBTYPECREATUREB | SUBTYPEPLANAR
                        
                        SUPERTYPE: "basic" | "legendary" | "ongoing" | "snow" | "world"
                        
                        modifier: ABILITYMODIFIER | COMBATSTATUSMODIFIER | KEYWORDSTATUSMODIFIER | TAPPEDSTATUSMODIFIER | EFFECTSTATUSMODIFIER
                        
                        ABILITYMODIFIER: "triggered" | "activated" | "mana"
                        COMBATSTATUSMODIFIER: "attacking" | "defending" | "attacked" | "blocking" | "blocked" | "active"
                        KEYWORDSTATUSMODIFIER: "paired" | "kicked" | "face-up" | "face-down" | "transformed" | "enchanted" | "equipped" | "fortified"
                        TAPPEDSTATUSMODIFIER: "tapped" | "untapped"
                        EFFECTSTATUSMODIFIER: "named" | "chosen" | "revealed" | "returned" | "destroyed" | "exiled" | "died" | "countered" | "sacrificed"
                        
                        qualifier: QUALIFIER["s"]
                        QUALIFIER: ("ability"|"abilities") | "card" | "permanent" | "source" | "spell" | "token" | "effect"
                        zone: ZONE
                        ZONE: "the battlefield" | "graveyard" | "library" | "hand" | "stack" | "exile" | "command zone" | "outside the game"
                        
                        colorexpression: colorterm -> colorsingleexpr
                        | colorterm  ("," colorterm ",")* "or" colorterm -> colororexpr
                        | colorterm ("," colorterm ",")* "and" colorterm -> colorandexpr
                        | colorterm ("," colorterm ",")* "and/or" colorterm -> colorandorexpr
                        
                        colorterm: COLORTERM
                        | "non" COLORTERM -> noncolorterm
                        
                        COLORTERM: "white" | "blue" | "black" | "red" | "green" | "monocolored" | "multicolored" | "colorless"
                        
                        objectname: "'" OBJECTNAME "'" //[TODO: No demarcations around names is difficult also.]
                        OBJECTNAME: WORD ((WS | ",") WORD)* //[TODO: commas in names? This is problematic.]
                        
                        manaexpression: manasymbol+ 
                        manasymbol: "{" manamarkerseq "}"
                        manamarkerseq: manamarker_color -> regularmanasymbol
                        | manamarker_halfmana manamarker_color -> halfmanasymbol
                        | manamarker_color "/" manamarker_phyrexian -> phyrexianmanasymbol
                        | manamarker_color "/" manamarker_color -> hybridmanasymbol
                        | "2" "/" manamarker_color -> alternate2manasymbol
                        | manamarker_snow -> snowmanasymbol
                        | manamarker_colorless -> colorlessmanasymbol
                        | manamarker_x -> xmanasymbol
                        | NUMBER -> genericmanasymbol
                        
                        manamarker_halfmana: "H"i -> halfmarker
                        manamarker_color: "W"i -> whitemarker
                        | "U"i -> bluemarker
                        | "B"i -> blackmarker
                        | "R"i -> redmarker
                        | "G"i -> greenmarker
                        manamarker_snow: "S"i -> snowmarker
                        manamarker_phyrexian: "P"i -> phyrexianmarker
                        manamarker_colorless: "C"i -> colorlessmarker
                        manamarker_x: "X"i -> xmarker
                        
                        NAMEREFSYMBOL: "~" | "~f"
                        PLAYERTERM: "player"["s"] | "opponent"["s"] | "you" | "teammate"["s"] | "your" "team" | "they"
                        
                        tapuntapsymbol: TAPSYMBOL | UNTAPSYMBOL
                        TAPSYMBOL: "{T}"i
                        UNTAPSYMBOL: "{Q}"i
                        
                        %import common.WORD -> WORD
                        %import common.SIGNED_NUMBER -> NUMBER
                        %import common.WS -> WS
                        %ignore WS
                """, start=startText,debug=True)
                
                transformer = JsonParser.JsonTransformer()
                
                #tree = larkparser.parse("first strike, double strike, bushido 5 (this is reminder text)")
                #print(tree)
                #pydot__tree_to_png(tree, "lark_test.png")
                #out = transformer.transform(tree)
                #print(out)
                #quit()
                
                
                return larkparser,transformer
                
        def getLarkParser(self):
                """Get the Lark parser under the hood."""
                return self._lp
                
        def getLarkTransformer(self):
                """Get the transformer that turns parse trees into ASTs."""
                return self._tf
        
        def parse(self,cardinput):
                """The parse method for JsonParser takes a Json dict in MtgJson format.
                For reference, this is an example card in that format:
                
                {'artist': 'Steve Prescott', 
                'cmc': 4, 
                'colorIdentity': ['W'], 
                'colors': ['White'], 
                'flavor': "Thanks to one champion archer, the true borders of Kinsbaile extend an arrow's flight beyond the buildings.",
                'id': '20f7ec0882ea342c284730e7e387c3d517a7c7f7',
                'imageName': 'brigid, hero of kinsbaile',
                'layout': 'normal',
                'manaCost': '{2}{W}{W}',
                'mciNumber': '6',
                'multiverseid': 141829,
                'name': 'Brigid, Hero of Kinsbaile',
                'number': '6',
                'power': '2',
                'rarity': 'Rare',
                'subtypes':['Kithkin', 'Archer'],
                'supertypes': ['Legendary'],
                'text': 'First strike\n{T}: Brigid, Hero of Kinsbaile deals 2 damage to each attacking or blocking creature target player controls.',
                'toughness': '3',
                'type': 'Legendary Creature — Kithkin Archer',
                'types': ['Creature']}
                """
                #TODO: Eventually we'll support non-standard layouts.
                
                
                #Preprocessing step: Replace instances of the card name in the body text
                #with a ~ symbol.
                if 'name' in cardinput and 'text' in cardinput:
                        cardinput['text'] = cardinput['text'].replace(cardinput['name'],'~')
                
                #Preprocessing Step: Convert the typeline and body of the card to lower case.        
                if 'text' in cardinput:
                        cardinput['text'] = cardinput['text'].lower()
                if 'type' in cardinput:
                        cardinput['type'] = cardinput['type'].lower()
                
                
                if 'name' in cardinput:
                        cardName = MgName(cardinput['name'])
                else:
                        cardName = MgName()
                        
                        
                        
                if 'manaCost' in cardinput:
                        manaCost = self._miniManaTransformer.transform(self._miniManaParser.parse(cardinput['manaCost']))
                else:
                        manaCost = MgManaExpression()
                        
                #TODO: apparently the MtgJson format doesn't explicitly list color indicators. 
                colorIndicator = None
                
                if 'type' in cardinput:
                        try:
                                typeLine = self._miniTypelineTransformer.transform(self._miniTypelineParser.parse(cardinput['type']))
                        except Exception as e:
                                print("WTF {0}".format(cardinput['name']))
                                raise e
                else:
                        typeLine = MgTypeLine()
                        
                        
                if 'loyalty' in cardinput:
                        try:
                                loyalty = MgNumberValue(int(cardinput['loyalty']),MgNumberValue.NumberTypeEnum.Literal)
                        except ValueError:
                                loyalty = MgNumberValue(cardinput['loyalty'],MgNumberValue.NumberTypeEnum.Custom)
                else:
                        loyalty = None
                        
                if 'power' in cardinput or 'toughness' in cardinput:
                        try:
                                power = MgNumberValue(int(cardinput['power']),MgNumberValue.NumberTypeEnum.Literal)
                        except ValueError:
                                power = MgNumberValue(cardinput['power'],MgNumberValue.NumberTypeEnum.Custom)
                        try:
                                toughness = MgNumberValue(int(cardinput['toughness']),MgNumberValue.NumberTypeEnum.Literal)
                        except ValueError:
                                toughness = MgNumberValue(cardinput['toughness'],MgNumberValue.NumberTypeEnum.Custom)
                        powerToughness = MgPTExpression(power,toughness)
                else:
                        powerToughness = None
                        
                if 'text' in cardinput:
                        self._lp.start = "cardtext"
                        parseTree = self._lp.parse(cardinput['text'])
                        pydot__tree_to_png(parseTree, "lark_test.png") #TMP
                        textBox = self._tf.transform(parseTree)
                else:
                        textBox = MgTextBox()
                        
                if 'life' in cardinput:
                        try:
                                lifeModifier = MgNumberValue(int(cardinput['life']),MgNumberValue.NumberTypeEnum.Literal)
                        except ValueError:
                                lifeModifier = MgNumberValue(cardinput['life'],MgNumberValue.NumberTypeEnum.Custom)
                else:
                        lifeModifier = None
                        
                if 'hand' in cardinput:
                        try:
                                handModifier = MgNumberValue(int(cardinput['hand']),MgNumberValue.NumberTypeEnum.Literal)
                        except ValueError:
                                handModifier = MgNumberValue(cardinput['hand'],MgNumberValue.NumberTypeEnum.Custom)
                else:
                        handModifier = None
                        
                if 'flavor' in cardinput:
                        flavor = MgFlavorText(cardinput['flavor'])
                else:
                        flavor = None 
                        
                card = MgCard(**{
                        "name" : cardName,
                        "manaCost" : manaCost,
                        "colorIndicator" : colorIndicator,
                        "typeLine" : typeLine,
                        "loyalty" : loyalty,
                        "powerToughness": powerToughness,
                        "textBox" : textBox,
                        "lifeModifier" : lifeModifier,
                        "handModifier" : handModifier,
                        "flavor" : flavor
                })
                
                return card
                
                
                
                
                
                
                
                
                
                
                