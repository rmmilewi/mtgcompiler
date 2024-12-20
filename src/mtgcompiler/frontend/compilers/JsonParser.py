import collections, pickle
# from mtgcompiler.parsers.baseparser import BaseParser
from mtgcompiler.frontend.AST.reference import MgNameReference,MgThisReference
from mtgcompiler.frontend.AST.reference import MgName,MgTapUntapSymbol,MgZone,MgQualifier
from mtgcompiler.frontend.AST.reference import MgAbilityModifier,MgCombatStatusModifier,MgKeywordStatusModifier, \
    MgEffectStatusModifier
from mtgcompiler.frontend.AST.card import MgTypeLine,MgFlavorText,MgTextBox,MgCard
from mtgcompiler.frontend.AST.mtypes import MgSupertype,MgSubtype,MgType
from frontend.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.frontend.AST.statements import MgKeywordAbilityListStatement,MgStatementBlock,MgExpressionStatement,MgActivationStatement
from mtgcompiler.frontend.AST.statements import MgAbilitySequenceStatement,MgQuotedAbilityStatement
from mtgcompiler.frontend.AST.statements import MgWhenStatement

from mtgcompiler.frontend.AST.expressions import MgNumberValue,MgPTExpression,MgManaExpression,MgTypeExpression,MgDescriptionExpression
from mtgcompiler.frontend.AST.expressions import MgNamedExpression,MgCostSequenceExpression,MgWithExpression,MgIndefiniteSingularExpression
from mtgcompiler.frontend.AST.expressions import MgColorExpression,MgAndExpression,MgOrExpression,MgAndOrExpression,MgTargetExpression,MgDeclarationExpression
from mtgcompiler.frontend.AST.expressions import MgDestroyExpression, MgDealsDamageExpression,MgChangeZoneExpression,MgSacrificeExpression
from mtgcompiler.frontend.AST.expressions import MgAnyColorSpecifier,MgManaSpecificationExpression,MgAddManaExpression,MgCreateTokenExpression

from mtgcompiler.frontend.AST.abilities import MgReminderText,MgAbilityWord,MgRegularAbility
from mtgcompiler.frontend.AST.abilities import MgDeathtouchAbility,MgDefenderAbility,MgDoubleStrikeAbility,MgFirstStrikeAbility,MgTrampleAbility
from mtgcompiler.frontend.AST.abilities import MgFlashAbility,MgFlyingAbility,MgHasteAbility,MgIndestructibleAbility,MgReachAbility



from mtgcompiler.frontend.AST.abilities import MgHexproofAbility,MgProtectionAbility,MgLandwalkAbility,MgRampageAbility
from mtgcompiler.frontend.AST.abilities import MgFadingAbility, MgAmplifyAbility, MgModularAbility, MgBushidoAbility
from mtgcompiler.frontend.AST.abilities import MgSoulshiftAbility, MgDredgeAbility, MgBloodthirstAbility, MgGraftAbility
from mtgcompiler.frontend.AST.abilities import MgRippleAbility, MgVanishingAbility, MgAbsorbAbility, MgFrenzyAbility
from mtgcompiler.frontend.AST.abilities import MgPoisonousAbility, MgDevourAbility, MgAnnihilatorAbility, MgTributeAbility
from mtgcompiler.frontend.AST.abilities import MgRenownAbility, MgCrewAbility, MgFabricateAbility

from mtgcompiler.frontend.AST.abilities import MgCumulativeUpkeepAbility, MgBuybackAbility, MgCyclingAbility, MgKickerAbility, MgMadnessAbility
from mtgcompiler.frontend.AST.abilities import MgMorphAbility, MgNinjutsuAbility, MgTransmuteAbility, MgRecoverAbility
from mtgcompiler.frontend.AST.abilities import MgAuraSwapAbility, MgTransfigureAbility, MgEvokeAbility, MgMiracleAbility
from mtgcompiler.frontend.AST.abilities import MgOverloadAbility, MgScavengeAbility, MgOutlastAbility, MgSurgeAbility
from mtgcompiler.frontend.AST.abilities import MgEmergeAbility, MgEscalateAbility, MgEnbalmAbility, MgEternalizeAbility

from mtgcompiler.frontend.AST.abilities import MgSpliceAbility,MgEnchantAbility,MgEquipAbility,MgBandingAbility,MgAffinityAbility
from mtgcompiler.frontend.AST.abilities import MgOfferingAbility, MgSuspendAbility,MgChampionAbility,MgReinforceAbility
from mtgcompiler.frontend.AST.abilities import MgHiddenAgendaAbility,MgAwakenAbility,MgPartnerAbility

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

class JsonParser():
        """A parser implementation supporting the mtgjson card format."""

        def __init__(self,options):
                """Calling this constructor causes the Lark parser and the parse-to-AST transformer
                to be instantiated.
                
                options: A dictionary that contains options for the parser. See BaseParser for details.
                """
                #super().__init__(options)
                self.options = options
                self._lp,self._tf = self.define_grammar('cardtext')
                #TODO: There has to be a better way to set different start rules.
                if self._rulestextonly == False:
                        self._miniManaParser,self._miniManaTransformer = self.define_grammar("manaexpression")
                        self._miniTypelineParser,self._miniTypelineTransformer = self.define_grammar("typeline")
                
        @classmethod
        def saveToPickle(cls,parser,path="parser.pickle"):
                """Pickle the parser. This is for testing purposes, right now."""
                with open(path,'wb') as outfile:
                        pickle.dump(obj=parser,file=outfile)
        
        @classmethod
        def loadFromPickle(cls,path="parser.pickle"):
                """Unpickle the parser. This is for testing purposes, right now."""
                with open(path,'rb') as infile:
                        return pickle.load(infile)
                
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
                def anycolorspecifier(self,items):
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
                
                
        def define_grammar(self,startText='cardtext'):                
                larkparser = Lark(r"""
                
                        typeline: typelinesupert typelinet ("—" typelinesubt)?
                        typelinesupert: SUPERTYPE*
                        typelinet: TYPE*
                        typelinesubt: (SUBTYPESPELL | SUBTYPELAND | SUBTYPEARTIFACT | SUBTYPEENCHANTMENT | SUBTYPEPLANESWALKER | SUBTYPECREATUREA | SUBTYPECREATUREB | SUBTYPEPLANAR)*
                
                        //[NOTE: Added support for starting reminder text, but what does it attach to?]
                        cardtext : remindertext? ability? ("\n" ability)* //[TODO: Do we need to explicitly recognize newlines? We might in order to separate distinct abilities.]
                        remindertext : /\(.*?\)/
                        
                        ability : abilityword? statementblock remindertext? -> regularability
                        | keywordlist remindertext?
                        abilityword: WORD "—"
                        
                        keywordlist: keywordsequence
                        keywordsequence: keywordability | keywordsequence ("," | ";") keywordability
                        
                        //statementblock : statement ["."] | statementblock statement ["."]
                        statementblock : (statement ["."])+
                        
                        //STATEMENTS
                        
                        statement: compoundstatement
                        | expressionstatement
                        | conditionalstatement 
                        | activationstatement
                        | beingstatement
                        | dostatement
                        | thenstatement
                        | insteadstatement
                        | maystatement
                        | wouldstatement
                        | additionalcoststatement
                        
                        thenstatement: "then" statement
                        insteadstatement: statement "instead"
                        maystatement:  playerdeclref? ("may" | "may" "have") statement
                        wouldstatement: playerdeclref? "would" statement
                        additionalcoststatement: "as" "an" "additional" "cost" "to" statement "," statement
                        
                        dostatement: declarationorreference? ("do" | "does") statement? -> dostatement
                        | declarationorreference? ("do" "not" | "does" "not") statement? -> dontstatement
                        
                        beingstatement: isstatement
                        | hasstatement
                        | isntstatement
                        | canstatement
                        | becomesstatement
                        | costchangestatement
                        | wherestatement
                        
                        !isstatement: declarationorreference ("is" | "was" | "are" "each"?) ("still"|"not")? (declarationorreference | characteristicexpression | statement)
                        !hasstatement: declarationorreference? ("has"|"have"|"had") (abilitysequencestatement | characteristicexpression | beexpression | statement)
                        | declarationorreference?  ("has"|"have"|"had") ("a"|valueexpression) countertype "counter"["s"] "on" declarationorreference -> hascounterstatement
                        isntstatement: declarationorreference? "is" "not" statement
                        canstatement: declarationorreference? "can" statement
                        | declarationorreference? "can" "not" statement -> cantstatement
                        becomesstatement: declarationorreference? "become"["s"] genericdeclarationexpression
                        costchangestatement: declarationorreference "cost"["s"] manaexpression "more" "to" "cast" -> costincreasestatement
                        | declarationorreference "cost"["s"] manaexpression "less" "to" "cast" -> costreductionstatement
                        wherestatement: statement "," "where" statement //[Note: Used in elaborating variables.]
                        
                        expressionstatement: (effectexpression | beexpression | valueexpression) timeexpression? //[TODO: Do time expressions need to go here?]
                        beexpression: ("be"|"been") modifier valueexpression? timeexpression?//[TODO: Not sure how to categorize this one yet.]
                        activationstatement: cost ":" statementblock
                        
                        compoundstatement: statement  ("," statement)* ","? "then" statement -> compoundthenstatement
                        | statement ("," statement)* ","? "and" statement -> compoundandstatement
                        | statement ("," statement)* ","? "or" statement -> compoundorstatement
                        
                        conditionalstatement: ifstatement
                        | wheneverstatement
                        | whenstatement
                        | atstatement
                        | aslongasstatement
                        | forstatement
                        | untilstatement
                        | afterstatement
                        | otherwisestatement
                        | unlessstatement
                        | asstatement
                        | whilestatement
                        | duringstatement
                        | exceptstatement
                        | ratherstatement
                        | nexttimestatement
                        | beforestatement
                        
                        ifstatement: "if" statement "," statement
                        | statement "only"? "if" statement -> ifstatementinv
                        
                        wheneverstatement:  "whenever" statement timeexpression? "," statement 
                        | statement "whenever" statement timeexpression? -> wheneverstatementinv
                        
                        whenstatement:  "when" statement "," statement 
                        | statement "when" statement -> whenstatementinv
                        
                        atstatement:  "at" timeexpression "," statement 
                        | statement "at" timeexpression -> atstatementinv
                        
                        aslongasstatement:  "for"? "as" "long" "as" statement "," statement
                        | statement "for"? "as" "long" "as" statement -> aslongasstatementinv
                        
                        forstatement:  "for" "each" (genericdeclarationexpression | "time" statement) ("beyond" "the" "first")? "," statement 
                        | statement "for" "each" (genericdeclarationexpression | "time" statement) ("beyond" "the" "first")? -> forstatementinv
                        
                        untilstatement:  "until" timeexpression "," statement 
                        | statement "until" timeexpression -> untilstatementinv
                        
                        afterstatement:  "after" timeexpression "," statement 
                        | statement "after" timeexpression -> afterstatementinv
                        
                        otherwisestatement: "otherwise" "," statement
                        
                        unlessstatement:  statement "unless" statement
                        
                        asstatement: "as" statement "," statement -> asstatement
                        
                        whilestatement:  "while" statement "," statement
                        
                        duringstatement:  statement "during" timeexpression
                        | statement "only" "during" timeexpression -> exclusiveduringstatement
                        
                        exceptstatement:  statement "except" (("by"|"for") genericdeclarationexpression | statement)
                        
                        ratherstatement:  statement "rather" "than" statement
                        
                        nexttimestatement: "the" "next" "time" statement timeexpression? "," statement
                        
                        beforestatement: statement "before" (timeexpression | statement)
                        
                        //KEYWORD ABILITIES
                        
                        abilitysequencestatement: (keywordability | quotedabilitystatement) (("," (keywordability | quotedabilitystatement) ",")* ("and" (keywordability | quotedabilitystatement)))?
                        quotedabilitystatement: "\"" statementblock "\""
                        
                        keywordability: kwdeathtouch
                        | kwdefender | kwdoublestrike | kwenchant | kwequip | kwfirststrike
                        | kwflash | kwflying | kwhaste | kwhexproof | kwindestructible
                        | kwintimidate | kwlandwalk | kwlifelink | kwprotection | kwreach 
                        | kwshroud | kwtrample | kwvigilance | kwbanding 
                        | kwrampage | kwcumulativeupkeep | kwflanking | kwphasing
                        | kwbuyback | kwshadow | kwcycling | kwecho | kwhorsemanship
                        | kwfading | kwkicker | kwflashback | kwmadness | kwfear
                        | kwmorph | kwamplify | kwprovoke | kwstorm | kwaffinity
                        | kwentwine | kwmodular | kwsunburst | kwbushido | kwsoulshift
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
                        | kwassist
                        
                        kwdeathtouch: "deathtouch"
                        kwdefender: "defender"
                        kwdoublestrike: "double" "strike"
                        kwenchant: "enchant" genericdescriptionexpression
                        kwequip: "equip" cost | "equip" genericdescriptionexpression cost
                        kwfirststrike: "first strike"
                        kwflash: "flash"
                        kwflying: "flying"
                        kwhaste: "haste"
                        kwhexproof: "hexproof" | "hexproof" "from" genericdescriptionexpression
                        kwindestructible: "indestructible"
                        kwintimidate: "intimidate"
                        kwlandwalk: typeexpression "walk"
                        kwlifelink: "lifelink"
                        kwprotection: "protection" "from" genericdescriptionexpression ("and" "from" genericdescriptionexpression)*
                        kwreach: "reach"
                        kwshroud: "shroud"
                        kwtrample: "trample"
                        kwvigilance: "vigilance"
                        kwbanding: "banding" | "bands" "with" "other" genericdescriptionexpression
                        kwrampage: "rampage" valuenumber
                        kwcumulativeupkeep: "cumulative" "upkeep" cost
                        kwflanking: "flanking"
                        kwphasing: "phasing"
                        kwbuyback: "buyback" cost
                        kwshadow: "shadow"
                        kwcycling: [typeexpression] "cycling" cost
                        kwecho: "echo" cost
                        kwhorsemanship: "horsemanship"
                        kwfading: "fading" valuenumber
                        kwkicker: "kicker" cost -> kicker
                        | "multikicker" cost -> multikicker
                        kwflashback: "flashback" cost
                        kwmadness: "madness" cost
                        kwfear: "fear"
                        kwmorph: "morph" cost -> kwmorph
                        | "megamorph" cost -> kwmegamorph
                        kwamplify: "amplify" valuenumber
                        kwprovoke: "provoke"
                        kwstorm: "storm"
                        kwaffinity: "affinity" "for" typeexpression
                        kwentwine: "entwine" cost
                        kwmodular: "modular" valuenumber
                        kwsunburst: "sunburst"
                        kwbushido: "bushido" valuenumber
                        kwsoulshift: "soulshift" valuenumber
                        kwsplice: "splice" "onto" typeexpression cost
                        kwoffering: typeexpression "offering"
                        kwninjutsu: "ninjutsu" cost
                        kwepic: "epic"
                        kwconvoke: "convoke"
                        kwdredge: "dredge" valuenumber
                        kwtransmute: "transmute" cost
                        kwbloodthirst: "bloodthirst" valuenumber
                        kwhaunt: "haunt"
                        kwreplicate: "replicate" cost
                        kwforecast: "forecast" activationstatement
                        kwgraft: "graft"
                        kwrecover: "recover" cost
                        kwripple: "ripple" valuenumber
                        kwsplitsecond: "split" "second"
                        kwsuspend: "suspend" valuenumber cost 
                        kwvanishing: "vanishing" [valuenumber]
                        kwabsorb: "absorb" valuenumber
                        kwauraswap: "aura" "swap" cost
                        kwdelve: "delve"
                        kwfortify: "fortify" cost
                        kwfrenzy: "frenzy"
                        kwgravestorm: "gravestorm"
                        kwpoisonous: "poisonous" valuenumber
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
                        kwdevour: "devour" valuenumber
                        kwexalted: "exalted"
                        kwunearth: "unearth" cost
                        kwcascade: "cascade"
                        kwannihilator: "annihilator" valuenumber
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
                        kwtribute: "tribute" valuenumber
                        kwdethrone: "dethrone"
                        kwhiddenagenda: "hidden" "agenda" -> kwhiddenagenda
                        | "double" "agenda" -> kwdoubleagenda
                        kwoutlast: "outlast" cost
                        kwprowess: "prowess"
                        kwdash: "dash" cost
                        kwexploit: "exploit"
                        kwmenace: "menace"
                        kwrenown: "renown" valuenumber
                        kwawaken: "awaken" cost
                        kwdevoid: "devoid"
                        kwingest: "ingest"
                        kwmyriad: "myriad"
                        kwsurge: "surge" cost
                        kwskulk: "skulk"
                        kwemerge: "emerge" cost
                        kwescalate: "escalate" cost
                        kwmelee: "melee"
                        kwcrew: "crew" valuenumber
                        kwfabricate: "fabricate" valuenumber
                        kwpartner: "partner" ["with" objectname]
                        kwundaunted: "undaunted"
                        kwimprovise: "improvise"
                        kwaftermath: "aftermath"
                        kwembalm: "embalm" cost
                        kweternalize: "eternalize" cost
                        kwafflict: "afflict" valuenumber
                        kwascend: "ascend"
                        kwassist: "assist"
                        
                        //ABILITY COSTS
                        
                        cost: costsequence | dashcostexpression
                        costsequence: (loyaltycost | tapuntapsymbol | manaexpression | effectexpression) ("," (loyaltycost | tapuntapsymbol | manaexpression | effectexpression))*
                        dashcostexpression: DASH ( manaexpression | effectexpression )
                        
                        ///VALUE EXPRESSIONS
                        
                        //[TODO: Need to account for custom values, variables, 'equals to' expressions, etc.]
                        valueexpression: valueterm | equaltoexpression | numberofexpression | uptoexpression | thatmanyexpression 
                        | ltexpression | lteqexpression | gtexpression | gteqexpression | timesexpression
                        ltexpression: effectexpression? "less" "than" (valueexpression | declarationorreference)
                        lteqexpression: effectexpression? (valueexpression "or" ("less" | "fewer") | "less" "than" "or" "equal" "to" valueexpression)
                        gtexpression: effectexpression? "greater" "than" (valueexpression | declarationorreference)
                        | "more" "than" valueexpression
                        gteqexpression: effectexpression? (valueexpression "or" ("greater" | "more")  | "greater" "than" "or" "equal" "to" valueexpression)
                        | CARDINAL "or" "more" "times"-> gteqfrequencyexpression
                        equaltoexpression: effectexpression? "equal" "to" (valueexpression | declarationorreference)
                        uptoexpression: "up" "to" valueterm
                        !thatmanyexpression: valuefrequency? "that" ("much"|"many")
                        !numberofexpression: ("a"|"the"|"any") "number" "of" declarationorreference
                        timesexpression: "times" statement? //[example: the number of times ~ was kicked]
                        valueterm: valuenumber | valuecardinal | valueordinal | valuefrequency | valuecustom
                        valuenumber: NUMBER
                        valuecardinal: CARDINAL
                        valueordinal: ORDINAL
                        valuefrequency: FREQUENCY | CARDINAL "times"
                        FREQUENCY: "once" | "twice"
                        CARDINAL: "one" | "two" | "three" | "four" | "five" | "six" | "seven" | "eight" | "nine" | "ten" 
                        | "eleven" | "twelve" | "thirteen" | "fourteen" | "fifteen" | "sixteen" | "seventeen" | "eighteen" | "nineteen" | "twenty" //[TODO]
                        ORDINAL: "first" | "second" | "third" | "fourth" | "fifth" //[TODO]
                        valuecustom: "x" | "*"
                        quantityrulemodification: "rounded" "up" -> roundedupmod
                        | "rounded" "down" -> roundeddownmod
                        | "divided" "evenly" -> dividedevenlymod
                        | "divided as you choose" -> dividedfreelymod
                        | "plus" valueterm -> plusmod
                        | "minus" valueterm -> minusmod
                        
                        
                        //DECLARATIONS AND REFERENCES
                        
                        declarationorreference: genericdeclarationexpression | reference | playerreference | objectreference | anytargetexpression
                        genericdeclarationexpression: (playerdeclaration | objectdeclaration)
                        | declarationorreference "or" declarationorreference -> orgenericdeclarationexpression
                        | declarationorreference "and" declarationorreference -> andgenericdeclarationexpression
                        | declarationorreference "and/or" declarationorreference -> andorgenericdeclarationexpression
                        
                        genericdescriptionexpression: objectdescriptionexpression | playerdescriptionexpression
                        
                        playerdeclref: playerdeclaration | playerreference
                        playerdeclaration: declarationdecorator* playerdefinition
                        playerreference: referencedecorator+ playerdefinition
                        playerdefinition: playerdescriptionexpression
                        playerdescriptionexpression : playerdescriptionterm (","? playerdescriptionterm)*
                        playerdescriptionterm: valueordinal | modifier | playerterm | withexpression | withoutexpression | whoexpression
                        playerterm: PLAYERTERM
                        whoexpression: "who" statement
                        
                        objectdeclref: objectdeclaration | objectreference
                        objectdeclaration: declarationdecorator* objectdefinition
                        objectreference: referencedecorator+ objectdefinition
                        objectdefinition: objectdescriptionexpression
                        | objectdescriptionexpression "or" objectdescriptionexpression -> ordefinitionexpression
                        | objectdescriptionexpression "and" objectdescriptionexpression -> anddefinitionexpression
                        | objectdescriptionexpression "and/or" objectdescriptionexpression -> andordefinitionexpression
                        objectdescriptionexpression: objectdescriptionterm (","? objectdescriptionterm)*
                        
                        objectdescriptionterm: colorexpression | namedexpression | manaexpression | typeexpression | ptexpression | valueexpression
                        | qualifier | modifier | locationexpression | valuecardinal | withexpression | withoutexpression |
                        | choiceexpression | ofexpression | characteristicexpression | additionalexpression | atrandomexpression
                        | "that"? dealtdamageexpression | "that" doesnthaveexpression | controlpostfix | ownpostfix | putinzonepostfix | castpostfix | "that" ispostfix | targetspostfix
                        | "that" sharepostfix
                        
                        
                        
                        
                        declarationdecorator: "each" -> eachdecorator
                        | "all" -> alldecorator
                        | ["an"]"other" -> otherdecorator
                        | "a"["n"] -> indefinitearticledecorator
                        | "the" -> definitearticledecorator
                        | valueexpression? "target" -> targetdecorator
                        | "any" -> anydecorator
                        anytargetexpression: "any" "target" //Special nullary variant
                        
                        reference: neutralreference | selfreference | namereference
                        neutralreference: "it" | "them"
                        selfreference: "itself" | "himself" | "herself" -> selfreference
                        namereference: NAMEREFSYMBOL
                        
                        referencedecorator: ("that" | "those") -> thatreference
                        | ("this"|"these") -> thisreference
                        | possessiveterm -> possessivereference
                        !possessiveterm: "its" | "your" | "their" | namereference ("'s"|"'") | objectdeclref ("'s"|"'") | playerdeclref ("'s"|"'") | typeexpression ("'s"|"'") | genericdeclarationexpression ("'s"|"'")
                        
                        ptexpression: valueexpression "/" valueexpression
                        namedexpression: "named" (namereference | objectname)
                        !locationexpression: ("into" | "onto" | "in" | "on" | "from" | "on top of" | "on bottom of")? zonedeclarationexpression
                        withexpression: "with" (reference | abilitysequencestatement | characteristicexpression | (valueexpression | "a"["n"])? countertype "counter"["s"] "on" reference)
                        withoutexpression: "without" (reference | abilitysequencestatement | characteristicexpression | (valueexpression | "a"["n"])? countertype "counter"["s"] "on" reference)
                        doesnthaveexpression: "does" "not" "have" declarationorreference //[Basically equivalent to 'without']
                        dealtdamageexpression: "dealt" DAMAGETYPE ("this" "way")? ("by" declarationorreference)? timeexpression?
                        choiceexpression: "of" possessiveterm "choice"
                        ofexpression: "of" declarationorreference
                        additionalexpression: "additional"
                        controlpostfix: playerdeclref "control"["s"]
                        | playerdeclref ("do" "not" | "does" "not") "control"["s"] -> negativecontrolpostfix
                        ownpostfix: playerdeclref "own"["s"]
                        | playerdeclref ("do" "not" | "does" "not") "own"["s"] -> negativeownpostfix
                        castpostfix: playerdeclref "cast"
                        putinzonepostfix: "put" locationexpression zoneplacementmodifier? ("this" "way")?
                        targetspostfix: "that" "target"["s"] declarationorreference
                        atrandomexpression: "at" "random" //[TODO: Need to find out where to put this.]
                        ispostfix: isstatement
                        sharepostfix: "share"["s"] declarationorreference
                        
                        
                        //EFFECT EXPRESSIONS
                        
                        
                        effectexpression: keywordactionexpression
                        | dealsdamageexpression
                        | preventdamageexpression
                        | returnexpression
                        | putinzoneexpression
                        | putcounterexpression
                        | removecounterexpression
                        | spendmanaexpression
                        | paylifeexpression
                        | addmanaexpression
                        | paymanaexpression
                        | payexpression
                        | gainlifeexpression
                        | loselifeexpression
                        | getsptexpression
                        | diesexpression
                        | gainabilityexpression
                        | loseabilityexpression
                        | lookexpression
                        | takeextraturnexpression
                        | flipcoinsexpression
                        | winloseeventexpression
                        | remainsexpression
                        | assigndamageexpression
                        | ableexpression
                        | changezoneexpression
                        | skiptimeexpression
                        | switchexpression
                        | targetsexpression
                        | shareexpression
                        
                        dealsdamageexpression:  declarationorreference? ("deal"["s"]|"dealt") valueexpression? DAMAGETYPE ("to" declarationorreference)? (","? quantityrulemodification)* -> dealsdamagevarianta
                        | valueexpression DAMAGETYPE ("to" declarationorreference)?  (","? quantityrulemodification)* -> dealsdamagevariantaimplied //variant a, implied antecedent
                        | declarationorreference ("deal"["s"]|"dealt") DAMAGETYPE valueexpression ("to" declarationorreference)?  (","? quantityrulemodification)* -> dealsdamagevariantb
                        | declarationorreference ("deal"["s"]|"dealt") DAMAGETYPE ("to" declarationorreference)?  valueexpression  (","? quantityrulemodification)* -> dealsdamagevariantc
                        preventdamageexpression: "prevent" "the" "next" valueexpression DAMAGETYPE "that" "would" "be" "dealt" "to" declarationorreference timeexpression? -> preventdamagevarianta
                        | "prevent" "the" "next" valueexpression DAMAGETYPE "that" declarationorreference "would" "deal" "to" declarationorreference timeexpression? -> preventdamagevariantb
                        | "prevent" "all" DAMAGETYPE "that" "would" "be" "dealt" ("to" declarationorreference)? timeexpression? -> preventdamagevariantc
                        | "prevent" valueexpression "of" "that" DAMAGETYPE -> preventdamagevariantd 
                        | "prevent" "that" DAMAGETYPE -> preventdamagevariante
                        | DAMAGETYPE "is" "prevented" "this" "way" -> preventdamagevariantf //[TODO: There may be a more general is-statement for stuff like 'damage'.]
                        
                        returnexpression: playerdeclref? "return"["s"] declarationorreference atrandomexpression? ("from" zonedeclarationexpression)? "to" zonedeclarationexpression genericdeclarationexpression? zoneplacementmodifier?//[TODO]
                        
                        putinzoneexpression: playerdeclref? "put"["s"] (declarationorreference | cardexpression) (locationexpression | "back" | zoneplacementmodifier) (objectdefinition | playerdefinition | zoneplacementmodifier)?
                        putcounterexpression: playerdeclref? "put"["s"] ("a"|valueexpression) countertype "counter"["s"] "on" declarationorreference
                        removecounterexpression: playerdeclref? "remove"["s"] ("a"|valueexpression) countertype "counter"["s"] "from" declarationorreference
                        spendmanaexpression: "spend" "mana" //[TODO: this is just a stub]
                        paylifeexpression: playerdeclref? "pay"["s"] valueexpression? "life"
                        addmanaexpression: playerdeclref? "add"["s"] (manaexpression|manaspecificationexpression)
                        paymanaexpression: playerdeclref? "pay"["s"] (manaexpression|manaspecificationexpression)
                        payexpression: playerdeclref? "pay"["s"] declarationorreference //[TODO: This might change. Added for 'rather than pay this spell's mana cost'.]
                        gainlifeexpression: playerdeclref? "gain"["s"] (valueexpression? "life" | "life" valueexpression)
                        | playerdeclref "gained" (valueexpression? "life" | "life" valueexpression) timeexpression?
                        loselifeexpression: playerdeclref? "lose"["s"] (valueexpression? "life" | "life" valueexpression) 
                        | playerdeclref "lost" (valueexpression? "life" | "life" valueexpression) timeexpression?
                        getsptexpression: declarationorreference? "get"["s"] ptchangeexpression
                        diesexpression: declarationorreference? "die"["s"] timeexpression?
                        gainabilityexpression: declarationorreference? "gain"["s"]  abilitysequencestatement
                        loseabilityexpression: declarationorreference? "lose"["s"] abilitysequencestatement
                        lookexpression: playerdeclref? ("look"["s"]|"looked") "at" (declarationorreference | cardexpression)
                        takeextraturnexpression: playerdeclref? "take"["s"] timeexpression
                        flipcoinsexpression: playerdeclref? "flip"["s"] ("a" | valuecardinal) "coin"["s"]
                        !winloseeventexpression: playerdeclref? ("lose"|"win")["s"] ("the" "flip" | "the" "game")?
                        remainsexpression: declarationorreference? "remain"["s"] (modifier | locationexpression)
                        assigndamageexpression: declarationorreference? "assign"["s"] DAMAGETYPE "to" declarationorreference -> damageredirectionexpression
                        | declarationorreference? "assign"["s"] "no" DAMAGETYPE timeexpression -> nodamageassignedexpression
                        | declarationorreference? "assign"["s"] DAMAGETYPE valueexpression -> alternatedamageassignmentexpression
                        ableexpression: declarationorreference? "able" ("to" statement "do" "so")?
                        changezoneexpression: declarationorreference "enter"["s"] locationexpression genericdeclarationexpression? zoneplacementmodifier? timeexpression? -> enterzoneexpression
                        | declarationorreference "leaves" locationexpression -> leavezoneexpression
                        skiptimeexpression: playerdeclref? "skip"["s"] timeexpression
                        switchexpression: playerdeclref? "switch"["es"] declarationorreference
                        targetsexpression: objectdeclref? "target"["s"] declarationorreference?
                        shareexpression: declarationorreference "share"["s"] declarationorreference
                        
                        
                        keywordactionexpression: basickeywordaction | specialkeywordaction
                        basickeywordaction: activateexpression
                        | attacksexpression
                        | blocksexpression
                        | attachexpression
                        | castexpression
                        | modalexpression
                        | chooseexpression
                        | controlsexpression
                        | gaincontrolexpression
                        | uncastexpression
                        | createexpression
                        | destroyexpression
                        | drawexpression
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
                        
                        activateexpression: "activate" declarationorreference
                        !attacksexpression: declarationorreference? "only"? "attack"["s"] "only"? (timeexpression? declarationorreference?| declarationorreference? timeexpression?) "alone"?
                        | declarationorreference? "attacked" (timeexpression? declarationorreference?| declarationorreference? timeexpression?) "alone"? -> attackedexpression
                        !blocksexpression: declarationorreference? "only"? "block"["s"] "only"? (timeexpression? declarationorreference? | declarationorreference? timeexpression?) "alone"?
                        | playerdeclref? "blocked" (timeexpression? declarationorreference?| declarationorreference? timeexpression?) "alone"? -> blockedexpression
                        attachexpression: "attach" declarationorreference "to" declarationorreference
                        | "unattach" declarationorreference ("from" declarationorreference)? -> unattachexpression
                        | playerdeclref "attaches" declarationorreference "to" declarationorreference -> playerattachesexpression
                        
                        castexpression: playerdeclref? "cast"["s"] declarationorreference (castmodifier ("and" castmodifier)?)* timeexpression?
                        castmodifier: "without" "paying" "its" "mana" "cost" -> castwithoutpaying //[TODO: We may be able to fold this into the pay-expression]
                        | "as" "though" beingstatement -> castasthough
                        chooseexpression: playerdeclref? ("choose"["s"]|"chose") declarationorreference ("from" "it")? atrandomexpression? //[TODO]
                        modalexpression: "choose" valuecardinal DASH (modalchoiceexpression)+
                        modalchoiceexpression: MODALCHOICE statementblock
                        controlsexpression: playerdeclref? ("control"["s"] | "controlled") genericdeclarationexpression
                        gaincontrolexpression: playerdeclref? ("gain"["s"] | "gained") "control" "of" declarationorreference
                        
                        uncastexpression: "counter" declarationorreference
                        createexpression: playerdeclref? "create"["s"] objectdeclaration
                        destroyexpression: "destroy" declarationorreference
                        drawexpression: playerdeclref? ("draw"["s"]|"drew") cardexpression //[("a" "card" | valueexpression "card"["s"] | "cards"["s"] valueexpression)]
                        discardexpression: playerdeclref? ("discard"["s"] | "discarded") (declarationorreference | "a" "card" | valueexpression "card"["s"] | "card"["s"] valueexpression) "at random"?
                        doubleexpression: "double" //[TODO]
                        exchangeexpression: "exchange" //[TODO]
                        exileexpression: "exile" declarationorreference
                        fightexpression: declarationorreference? "fight"["s"] declarationorreference?
                        playexpression: playerdeclref? ("play"["s"] | "played") declarationorreference timeexpression?
                        revealexpression: playerdeclref? ("reveal"["s"] | "revealed") (cardexpression | declarationorreference)
                        sacrificeexpression: playerdeclref? ("sacrifice"["s"] | "sacrificed") declarationorreference
                        searchexpression: playerdeclref? ("search"["es"] | "searched") zonedeclarationexpression? "for" declarationorreference
                        shuffleexpression: playerdeclref? ("shuffle"["s"] | "shuffled") zonedeclarationexpression
                        tapuntapexpression: "tap" declarationorreference? -> tapexpression
                        | "untap" declarationorreference? -> untapexpression
                        
                        specialkeywordaction: regenerateexpression
                        | scryexpression
                        | fatesealexpression
                        | clashexpression
                        | detainexpression
                        | planeswalkexpression
                        | setinmotionexpression
                        | abandonexpression
                        | proliferateexpression
                        | transformexpression
                        | populateexpression
                        | voteexpression
                        | bolsterexpression
                        | manifestexpression
                        | supportexpression
                        | investigateexpression
                        | meldexpression
                        | goadexpression
                        | exertexpression
                        | exploreexpression
                        | turnfaceexpression
                        | cycleexpression
                        | levelupexpression~2
                        
                        regenerateexpression: "regenerate" declarationorreference
                        scryexpression: "scry" valueexpression
                        fatesealexpression: "fateseal" valueexpression
                        clashexpression: playerdeclref? "clash" "with" playerdeclref
                        detainexpression: "detain" objectdeclref
                        planeswalkexpression: playerdeclref "planeswalk"["s"] "to" SUBTYPEPLANAR
                        setinmotionexpression: playerdeclref "set"["s"] declarationorreference "in" "motion"
                        abandonexpression: playerterm? "abandon"["s"] declarationorreference //[Note: Has never been used]
                        proliferateexpression: "proliferate"
                        transformexpression: "transform" declarationorreference
                        populateexpression: "populate"
                        voteexpression: playerdeclref "vote"["s"] "for" (objectname "or" objectname | declarationorreference) //[TODO]
                        bolsterexpression: "bolster" valueexpression
                        manifestexpression: playerdeclref? "manifest"["s"] cardexpression
                        supportexpression: "support" valueexpression
                        investigateexpression: "investigate"
                        meldexpression: "meld" "them" "into" objectname
                        goadexpression: "goad" declarationorreference
                        exertexpression: playerdeclref? "exert"["s"] declarationorreference
                        exploreexpression: declarationorreference? "explores"
                        //[This one below is a bit weird because it's not 'becomes turned face up', it's 'is turned face up'.]
                        //[It's a passive construction, but it's not a modifier like face-up.]
                        !turnfaceexpression: playerdeclref? "turn"["s"] declarationorreference "face" ("down" | "up")
                        | "turned" "face" ("down" | "up") -> turnedfaceexpression
                        cycleexpression: playerdeclref? ("cycle"["s"] | "cycled") declarationorreference? 
                        
                        levelupexpression: ("level" levelrangeexpression ptexpression ability*)
                        levelrangeexpression: NUMBER "-" NUMBER | NUMBER "+"
                        
                        
                        //TYPE/MANA/COLOR EXPRESSIONS, MODIFIERS, AND MISCELLANEOUS
                        
                        timeexpression: startendspecifier? timeterm ("of" timeexpression)?
                        startendspecifier: "the"? "beginning" "of" -> timebeginmodifier
                        | "the"? "end" "of" -> timeendmodifier
                        timeterm: (referencedecorator* | declarationdecorator*) possessiveterm* timemodifier* (PHASE | STEP | TURN | GAME |  "one")
                        timemodifier: "next" valuecardinal? -> nexttimemodifier
                        | "additional" -> additionaltimemodifier
                        | valuecardinal? "extra" -> extratimemodifier
                        PHASE: "beginning phase" | ("precombat" | "postcombat")? "main phase" | ("combat" | "combat phase") | "ending phase"
                        STEP: "untap step" | ("upkeep step" | "upkeep") | "draw step" | "beginning of combat" | "declare attackers step"
                        | "declare blockers step" | "combat damage step" | "end of combat" | "end step" | "cleanup step" | "step"
                        TURN: "turn"
                        GAME: "game" 
                        
                        //[TODO: What about comma-delimited type expressions?]
                        typeexpression: (typeterm)+ | typeterm ("," typeterm)+
                        | typeterm ("," typeterm ",")* "or" typeterm -> ortypeexpression
                        
                        typeterm: (TYPE ["s"] | SUBTYPESPELL ["s"] | SUBTYPELAND ["s"] | SUBTYPEARTIFACT ["s"] | SUBTYPEENCHANTMENT ["s"] | SUBTYPEPLANESWALKER | SUBTYPECREATUREA ["s"] | SUBTYPECREATUREB ["s"] | SUBTYPEPLANAR | SUPERTYPE)
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
                        
                        SUBTYPECREATUREA: "advisor" | "aetherborn" | ("ally"|"allies") | "angel" | "antelope" | "ape" | "archer" | "archon" 
                        | "artificer" | "assassin" | "assembly-worker" | "atog" | "aurochs" | "avatar" | "azra" | "badger"
                        | "barbarian" | "basilisk" | "bat" | "bear" | "beast" | "beeble" | "berserker" | "bird" | "blinkmoth"
                        | "boar" | "bringer" | "brushwagg" | "camarid" | "camel" | "caribou" | "carrier" | "cat" | "centaur"
                        | "cephalid" | "chimera" | "citizen" | "cleric" | "cockatrice" | "construct" | "coward" | "crab"
                        | "crocodile" | "cyclops" | "dauthi" | "demon" | "deserter" | "devil" | "dinosaur" | "djinn" | "dragon"
                        | "drake" | "dreadnought" | "drone" | "druid" | "dryad" | ("dwarf"|"dwarves") | "efreet" | "egg" | "elder" | "eldrazi"
                        | "elemental" | "elephant" | ("elf"|"elves") | "elk" | "eye" | "faerie" | "ferret" | "fish" | "flagbearer" | "fox"
                        
                        SUBTYPECREATUREB: "frog" | "fungus" | "gargoyle" | "germ" | "giant" | "gnome" | "goat" | "goblin" | "god" | "golem" | "gorgon"
                        | "graveborn" | "gremlin" | "griffin" | "hag" | "harpy" | "hellion" | "hippo" | "hippogriff" | "homarid" | "homunculus"
                        | "horror" | "horse" | "hound" | "human" | "hydra" | "hyena" | "illusion" | "imp" | "incarnation" | "insect"
                        | "jackal" | "jellyfish" | "juggernaut" | "kavu" | "kirin" | "kithkin" | "knight" | "kobold" | "kor" | "kraken"
                        | "lamia" | "lammasu" | "leech" | "leviathan" | "lhurgoyf" | "licid" | "lizard" | "manticore" | "masticore"
                        | ("mercenary"|"mercenaries") | "merfolk" | "metathran" | "minion" | "minotaur" | "mole" | "monger" | "mongoose" | "monk" 
                        | "monkey" | "moonfolk" | "mutant" | "myr" | "mystic" | "naga" | "nautilus" | "nephilim" | "nightmare" 
                        | "nightstalker" | "ninja" | "noggle" | "nomad" | "nymph" | ("octopus"|"octopuses") | "ogre" | "ooze" | "orb" | "orc" 
                        | "orgg" | "ouphe" | "ox" | "oyster" | "pangolin" | "pegasus" | "pentavite" | "pest" | "phelddagrif" | "phoenix"
                        | "pilot" | "pincher" | "pirate" | "plant" | "praetor" | "prism" | "processor" | "rabbit" | "rat" | "rebel"
                        | "reflection" | "rhino" | "rigger" | "rogue" | "sable" | "salamander" | "samurai" | "sand" | "saproling" | "satyr"
                        | "scarecrow" | "scion" | "scorpion" | "scout" | "serf" | "serpent" | "servo" | "shade" | "shaman" | "shapeshifter"
                        | "sheep" | "siren" | "skeleton" | "slith" | "sliver" | "slug" | "snake" | "soldier" | "soltari" | "spawn" | "specter"
                        | "spellshaper" | "sphinx" | "spider" | "spike" | "spirit" | "splinter" | "sponge" | "squid" | "squirrel" | "starfish"
                        | "surrakar" | "survivor" | "tetravite" | "thalakos" | "thopter" | "thrull" | "treefolk" | "trilobite" | "triskelavite"
                        | "troll" | "turtle" | "unicorn" | "vampire" | "vedalken" | "viashino" | "volver" | "wall" | "warrior" | "weird"
                        | ("werewolf"|"werewolves") | "whale" | "wizard" | ("wolf"|"wolves") | "wolverine" | "wombat" | "worm" | "wraith" | "wurm" | "yeti" 
                        | "zombie" | "zubera"
                        
                        SUBTYPEPLANAR: "alara" | "arkhos" | "azgol" | "belenon" | "bolas’s meditation realm"
                        | "dominaria" | "equilor" | "ergamon" | "fabacin" | "innistrad" | "iquatana" | "ir" 
                        | "kaldheim" | "kamigawa" | "karsus" | "kephalai" | "kinshala" | "kolbahan" | "kyneth"
                        | "lorwyn" | "luvion" | "mercadia" | "mirrodin" | "moag" | "mongseng" | "muraganda"
                        | "new phyrexia" | "phyrexia" | "pyrulea" | "rabiah" | "rath" | "ravnica" | "regatha"
                        | "segovia" | "serra’s realm" | "shadowmoor" | "shandalar" | "ulgrotha" | "valla"
                        | "vryn" | "wildfire" | "xerex" | "zendikar"
                        
                        subtype: SUBTYPESPELL | SUBTYPELAND | SUBTYPEARTIFACT | SUBTYPEENCHANTMENT | SUBTYPEPLANESWALKER | SUBTYPECREATUREA | SUBTYPECREATUREB | SUBTYPEPLANAR
                        
                        SUPERTYPE: "basic" | "legendary" | "ongoing" | "snow" | "world"
                        
                        DAMAGETYPE: "damage" | "combat damage" | "noncombat damage"
                        
                        modifier: ABILITYMODIFIER | COMBATSTATUSMODIFIER | KEYWORDSTATUSMODIFIER | TAPPEDSTATUSMODIFIER | EFFECTSTATUSMODIFIER
                        | controlmodifier | attachmentmodifier
                        
                        ABILITYMODIFIER: "triggered" | "activated" | "mana" | "loyalty"
                        COMBATSTATUSMODIFIER: "attacking" | "defending" | "attacked" | "blocking" | "blocked" | "active"
                        KEYWORDSTATUSMODIFIER: "paired" | "kicked" | "face-up" | "face-down" | "transformed" | "enchanted" | "equipped"
                        | "fortified" | "monstrous" | "regenerated" | "suspended" | "flipped"
                        TAPPEDSTATUSMODIFIER: "tapped" | "untapped"
                        EFFECTSTATUSMODIFIER: "named" | "chosen" | "chosen at random" | "revealed" | "returned" | "destroyed" | "exiled" | "died" | "countered" | "sacrificed"
                        | "the target of a spell or ability" | "prevented" | "created"
                        controlmodifier: "under" referencedecorator+ "control"
                        attachmentmodifier: "attached" ("only"? "to" declarationorreference)? -> attachedmodifier
                        | "unattached" ("from" declarationorreference)? -> unattachedmodifier
                        
                        qualifier: QUALIFIER["s"]
                        QUALIFIER: ("ability"|"abilities") | "card" | "permanent" | "source" | "spell" | "token" | "effect"
                        
                        characteristicexpression: characteristicterms 
                        | (characteristicterms (valueexpression|ptexpression) | (valueexpression|ptexpression) characteristicterms) -> characteristicvaluecompexpr
                        
                        characteristicterms: characteristicterm
                        | possessiveterm+ characteristicterm -> characteristicpossessiveexpr
                        | "the" characteristicterm -> characteristicthereference
                        | characteristicterm  ("," characteristicterm ",")* "or" characteristicterm -> characteristicorexpr
                        | characteristicterm  ("," characteristicterm ",")* "and" characteristicterm -> characteristicandexpr
                        | characteristicterm  ("," characteristicterm ",")* "and/or" characteristicterm -> characteristicandorexpr
                        | "no" characteristicterm -> nocharacteristicexpr //[example: no maximum hand size]
                        
                        characteristicterm: modifier* characteristic
                        characteristic: OBJECTCHARACTERISTIC | PLAYERCHARACTERISTIC
                        PLAYERCHARACTERISTIC: "maximum hand size" | "life total" | "life" | "cards in hand"
                        OBJECTCHARACTERISTIC: "card"? "name" | "mana cost" | "converted mana cost" | "color"["s"] | "color indicator" | "type"["s"] | "card type"["s"] | "subtype"["s"] | "supertype"["s"]
                        | "rules text" | "abilities" | "power" | "toughness" | "base power" | "base toughness" | "loyalty" | "hand modifier" | "life modifier"
                        
                        //[TODO: Not quite done, there are expressions like 'a number of cards equal to [...]'. There's some overlapping responsibilities with descriptions involving cards, maybe.]
                        !cardexpression: ("the" "top" | "the" "bottom")? (valueterm | thatmanyexpression | "a")? "card"["s"] ("from" "the" "top" | "from" "the" "bottom")? ("of" zonedeclarationexpression)?  
                        
                        zonedeclarationexpression: (declarationdecorator* | referencedecorator*) zone
                        zoneplacementmodifier: "in" "any" "order" -> anyorderplacement
                        | "in" "a" "random" "order" -> randomorderplacement
                        | ORDINAL "from" "the" "top" -> fromtopplacement
                        | ORDINAL "from" "the" "bottom" -> frombottomplacement
                        zone: ZONE
                        ZONE: "the battlefield" | "graveyard"["s"] | ("library"|"libraries") | "hand"["s"] | "stack" | "exile" | "command zone" | "outside the game" | "anywhere"
                        
                        colorexpression: colorterm -> colorsingleexpr
                        | colorterm  ("," colorterm ",")* "or" colorterm -> colororexpr
                        | colorterm ("," colorterm ",")* "and" colorterm -> colorandexpr
                        | colorterm ("," colorterm ",")* "and/or" colorterm -> colorandorexpr
                        
                        colorterm: COLORTERM
                        | "non" COLORTERM -> noncolorterm
                        
                        COLORTERM: "white" | "blue" | "black" | "red" | "green" | "monocolored" | "multicolored" | "colorless"
                        
                        objectname: OBJECTNAME //[TODO: No demarcations around names is difficult also.]
                        OBJECTNAME: NAMEWORD ((WS | ",") NAMEWORD)* //[TODO: commas in names? This is problematic.]
                        NAMEWORD: UCASE_LETTER (LCASE_LETTER)*
                        
                        countertype: ptchangeexpression | WORD
                        
                        loyaltycost: (PLUS | PWMINUS)? valueterm
                        //[NOTE: Both Scryfall and Mtgjson use a long dash, not a short dash, to indicate a minus on a planeswalker ability]
                        PWMINUS: "−"
                        ptchangeexpression: (PLUS | MINUS) valueterm "/" (PLUS | MINUS) valueterm
                        PLUS: "+"
                        MINUS: "-"
                        
                        manaspecificationexpression: valueterm "mana" manaspecifier+
                        manaspecifier: anycolorspecifier //[TODO: Need to add the rest of these]
                        
                        anycolorspecifier: "of" "any" "color" -> anycolorspecifier
                        | "of" "any" "one" "color" -> anyonecolorspecifier
                        
                        manaexpression: manasymbol+
                        | manaexpression "or" manaexpression -> ormanaexpression
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
                        
                        DASH: "—"
                        MODALCHOICE: "•"
                        
                        NAMEREFSYMBOL: "~" | "~f"
                        PLAYERTERM: "player"["s"] | "opponent"["s"] | "you" |  "teammate"["s"] | "team"["s"] | "they" | "controller"["s"] | "owner"["s"]
                        
                        tapuntapsymbol: TAPSYMBOL | UNTAPSYMBOL
                        TAPSYMBOL: "{T}"i
                        UNTAPSYMBOL: "{Q}"i
                        
                        %import common.UCASE_LETTER -> UCASE_LETTER
                        %import common.LCASE_LETTER -> LCASE_LETTER
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
                
                
        #TODO: This will probably be split off into a separate preprocessor class.
        def preprocess(self,cardinput):
                #Preprocessing step: Replace instances of the card name in the body text
                #with a ~ symbol.
                #TODO: First name only references need to be replaced with '~f'
                if 'name' in cardinput and 'text' in cardinput:
                        cardinput['text'] = cardinput['text'].replace(cardinput['name'],'~')
                        
                #Preprocessing Step: Convert the typeline and body of the card to lower case.        
                if 'text' in cardinput:
                        cardinput['text'] = cardinput['text'].lower()
                if 'type' in cardinput:
                        cardinput['type'] = cardinput['type'].lower()
                        
                #Preprocessing step: A minority of cards both on Mtgjson and Scryfall use 'his or her', which should be 'their' now.
                if 'text' in cardinput:
                        cardinput['text'] = cardinput['text'].replace("his or her","their")
                        
                #Preprocessing step: Expand pronoun-related contractions.
                if 'text' in cardinput:
                        cardinput['text'] = cardinput['text'].replace("it's","it is")
                        cardinput['text'] = cardinput['text'].replace("you're","you are")
                        cardinput['text'] = cardinput['text'].replace("they're","they are")
                        cardinput['text'] = cardinput['text'].replace("you've","you have")
                        cardinput['text'] = cardinput['text'].replace("isn't","is not")
                        cardinput['text'] = cardinput['text'].replace("aren't","are not")
                        cardinput['text'] = cardinput['text'].replace("don't","do not")
                        cardinput['text'] = cardinput['text'].replace("doesn't","does not")
                        cardinput['text'] = cardinput['text'].replace("can't","can not")
                        
                        
                #Preprocessing step: Some 20-or-so cards use 'each' before a verb to emphasize that a subject is plural
                #For our purposes, this is just syntactic sugar, so we will remove it. Examples include:
                #       * "You and that player each draw a card"
                #       * "Up to X target creatures each gain [...]"
                #       * "Those players each discard two cards at random."
                #Only a couple of effects use this wording. If I'm missing any, I'll go back and add them here later.
                if 'text' in cardinput:
                        cardinput['text'] = cardinput['text'].replace("each get","get")
                        cardinput['text'] = cardinput['text'].replace("each gain","gain")
                        cardinput['text'] = cardinput['text'].replace("each lose","lose")
                        cardinput['text'] = cardinput['text'].replace("each draw","draw")
                        cardinput['text'] = cardinput['text'].replace("each discard","discard")
                        cardinput['text'] = cardinput['text'].replace("each sacrifice","sacrifice")
                
                        
                return cardinput
                        
                
                
        
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
                                        
                cardinput = self.preprocess(cardinput)
                
                
                if 'name' in cardinput:
                        cardName = MgName(cardinput['name'])
                else:
                        cardName = MgName()
                        
                        
                        
                if 'manaCost' in cardinput and self._rulestextonly == False:
                        parsedManaCost = self._miniManaParser.parse(cardinput['manaCost'])
                        if not self._parseonly:
                                manaCost = self._miniManaTransformer.transform(parsedManaCost)
                        else:
                                manaCost = MgManaExpression()
                else:
                        manaCost = MgManaExpression()
                        
                #TODO: apparently the MtgJson format doesn't explicitly list color indicators. 
                colorIndicator = None
                
                if 'type' in cardinput and self._rulestextonly == False:
                        try:
                                parsedTypeLine = self._miniTypelineParser.parse(cardinput['type'])
                                if not self._parseonly:
                                        typeLine = self._miniTypelineTransformer.transform(parsedTypeLine)
                                else:
                                        typeLine = MgTypeLine()
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
                        parseTree = self._lp.parse(cardinput['text'])
                        if self._renderparsetree:
                                pydot__tree_to_png(parseTree, "lark_test.png")
                                print(parseTree.pretty()) #TMP
                        if not self._parseonly:
                                textBox = self._tf.transform(parseTree)
                        else:
                                textBox = MgTextBox()
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
                        
                if not self._parseonly:
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
                else:
                        return None
                
                
                
                
                
                
                
                
                
                
                
