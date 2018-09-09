import collections
from mtgcompiler.parsers.baseparser import BaseParser
from mtgcompiler.AST.reference import MgName
from mtgcompiler.AST.card import MgTypeLine,MgFlavorText,MgTextBox,MgCard
from mtgcompiler.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.AST.statements import MgKeywordAbilityListStatement

from mtgcompiler.AST.expressions import MgNumberValue,MgPTExpression,MgManaExpression,MgTypeExpression,MgDescriptionExpression,MgNamedExpression
from mtgcompiler.AST.expressions import MgColorExpression,MgAndExpression,MgOrExpression,MgAndOrExpression

from mtgcompiler.AST.abilities import MgReminderText
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
                
                
                def typeline(self,items):
                        return MgTypeLine(supertypes=items[0],types=items[1],subtypes=items[2])
                
                def typelinesupert(self,items):
                        return self.typeexpression(items)
                
                def typelinet(self,items):
                        return self.typeexpression(items)
                        
                def typelinesubt(self,items):
                        return self.typeexpression(items)
                
                def cardtext(self,items):
                        return MgTextBox(*items)
                
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
                        #: "cumulative" "upkeep" costsequence
                        cost = items[0]
                        return MgCumulativeUpkeepAbility(cost)
                def kwflanking(self,items): 
                        #: "flanking"
                        return MgFlankingAbility()
                def kwphasing(self,items): 
                        #: "phasing"
                        return MgPhasingAbility()
                def kwbuyback(self,items): 
                        #: "buyback" costsequence
                        cost = items[0]
                        return MgBuybackAbility(cost)
                def kwshadow(self,items): 
                        #: "shadow"
                        return MgShadowAbility()
                def kwcycling(self,items): 
                        #: "cycling" costsequence
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
                        #: "echo" costsequence
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
                        #: "kicker" costsequence, multikicker
                        cost = items[0]
                        return MgKickerAbility(cost)
                def kwflashback(self,items): 
                        #: "flashback" costsequence
                        cost = items[0]
                        return MgFlashbackAbility(cost)
                def kwmadness(self,items): 
                        #: "madness" costsequence
                        cost = items[0]
                        return MgMadnessAbility(cost)
                def kwfear(self,items): 
                        #: "fear"
                        return MgFearAbility()
                def kwmorph(self,items): 
                        #: "morph" costsequence
                        cost = items[0]
                        return MgMorphAbility(cost)
                def kwmegamorph(self,items): 
                        #: "morph" costsequence
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
                        #: "entwine" costsequence
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
                        #: "ninjutsu" costsequence
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
                        #: "transmute" costsequence
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
                        #: "replicate" costsequence
                        cost = items[0]
                        return MgReplicateAbility(cost)
                def kwforecast(self,items): 
                        #: "forecast" //TODO
                        pass
                def kwgraft(self,items): 
                        #: "graft"
                        return MgGraftAbility()
                def kwrecover(self,items): 
                        #: "recover" costsequence
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
                        #: "aura" "swap" costsequence
                        cost = items[0]
                        return MgAuraSwapAbility(cost)
                def kwdelve(self,items): 
                        #: "delve"
                        return MgDelveAbility()
                def kwfortify(self,items): 
                        #: "fortify" costsequence
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
                        #: "transfigure" costsequence
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
                        #: "evoke" costsequence
                        cost = items[0]
                        return MgEvokeAbility(cost)
                def kwhideaway(self,items): 
                        #: "hideaway"
                        return MgHideawayAbility()
                def kwprowl(self,items): 
                        #: "prowl" costsequence
                        cost = items[0]
                        return MgProwlAbility(cost)
                def kwreinforce(self,items): 
                        #: "reinforce" costsequence
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
                        #: "retrace" costsequence
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
                        #: "unearth" costsequence
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
                        #: "miracle" costsequence
                        cost = items[0]
                        return MgMiracleAbility(cost)
                def kwsoulbond(self,items): 
                        #: "soulbond"
                        return MgSoulbondAbility()
                def kwoverload(self,items): 
                        #: "overload" costsequence
                        cost = items[0]
                        return MgOverloadAbility(cost)
                def kwscavenge(self,items): 
                        #: "scavenge" costsequence
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
                        #: "bestow" costsequence
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
                        #: "outlast" costsequence
                        cost = items[0]
                        return MgOutlastAbility(cost)
                def kwprowess(self,items): 
                        #: "prowess"
                        return MgProwessAbility()
                def kwdash(self,items): 
                        #: "dash" costsequence
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
                        #: "awaken" costsequence
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
                        #: "surge" costsequence
                        cost = items[0]
                        return MgSurgeAbility(cost)
                def kwskulk(self,items): 
                        #: "skulk"
                        return MgSkulkAbility()
                def kwemerge(self,items): 
                        #: "emerge" costsequence
                        cost = items[0]
                        return MgEmergeAbility(cost)
                def kwescalate(self,items): 
                        #: "escalate" costsequence
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
                        #: "embalm" costsequence
                        cost = items[0]
                        return MgEnbalmAbility(cost)
                def kweternalize(self,items): 
                        #: "eternalize" costsequence
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
                
                def remindertext(self,items):
                        text = items[0].value
                        return MgReminderText(text)
                        
                def keywordlist(self,items):
                        flatlst = flatten(items)
                        return MgKeywordAbilityListStatement(*flatlst)
                def keywordsequence(self,items):
                        return items
                def keywordability(self,items):
                        return items[0]
                
                def costsequence(self,items):
                        return items[0]
                        
                def objectname(self,items):
                        return MgName(items[0].value)
                
                def expression(self,items):
                        return items[0]
                        
                def descriptionexpression(self,items):
                        return MgDescriptionExpression(*items)
                
                def namedexpression(self,items):
                        return MgNamedExpression(items[0])
                        
                def typeexpression(self,items):
                        typeobjects = []
                        for item in items:
                                if item.type == "TYPE":
                                        typeobjects.append(MgType(MgType.TypeEnum(item.value)))
                                elif item.type == "SUBTYPESPELL":
                                        typeobjects.append(MgSubtype(MgSubtype.SpellSubtypeEnum(item.value)))
                                elif item.type == "SUBTYPELAND":
                                        typeobjects.append(MgSubtype(MgSubtype.LandSubtypeEnum(item.value)))
                                elif item.type == "SUBTYPEARTIFACT":
                                        typeobjects.append(MgSubtype(MgSubtype.ArtifactSubtypeEnum(item.value)))
                                elif item.type == "SUBTYPEPLANESWALKER":
                                        typeobjects.append(MgSubtype(MgSubtype.PlaneswalkerSubtypeEnum(item.value)))
                                elif item.type == "SUBTYPECREATUREA" or item.type == "SUBTYPECREATUREB":
                                        typeobjects.append(MgSubtype(MgSubtype.CreatureSubtypeEnum(item.value)))
                                elif item.type == "SUBTYPEPLANAR":
                                        typeobjects.append(MgSubtype(MgSubtype.PlanarSubtypeEnum(item.value)))
                                elif item.type == "SUPERTYPE":
                                        typeobjects.append(MgSupertype(MgSupertype.SupertypeEnum(item.value)))
                                else:
                                        raise ValueError("Unrecognized type token: '{0}'".format(item))
                        typeExpr = MgTypeExpression(*typeobjects)
                        return typeExpr
                
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
                
                        typeline: typelinesupert typelinet "—" typelinesubt
                        typelinesupert: SUPERTYPE*
                        typelinet: TYPE*
                        typelinesubt: (SUBTYPESPELL ["s"] | SUBTYPELAND ["s"] SUBTYPELAND | SUBTYPEARTIFACT ["s"]
                        | SUBTYPEPLANESWALKER | SUBTYPECREATUREA | SUBTYPECREATUREB | SUBTYPEPLANAR)*
                
                        cardtext : ability*
                        remindertext : /\(.*?\)/
                        
                        ability : keywordlist remindertext?
                        keywordlist: keywordsequence
                        keywordsequence: keywordability | keywordsequence ("," | ";") keywordability
                        
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
                        kwenchant: "enchant" typeexpression // TODO
                        kwequip: "equip" costsequence  //TODO | "equip" descriptionexpression costsequence
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
                        kwcumulativeupkeep: "cumulative" "upkeep" costsequence
                        kwflanking: "flanking"
                        kwphasing: "phasing"
                        kwbuyback: "buyback" costsequence
                        kwshadow: "shadow"
                        kwcycling: [typeexpression] "cycling" costsequence
                        kwecho: "echo" costsequence
                        kwhorsemanship: "horsemanship"
                        kwfading: "fading" NUMBER
                        kwkicker: "kicker" costsequence -> kicker
                        | "multikicker" costsequence -> multikicker
                        kwflashback: "flashback" costsequence
                        kwmadness: "madness" costsequence
                        kwfear: "fear"
                        kwmorph: "morph" costsequence -> kwmorph
                        | "megamorph" costsequence -> kwmegamorph
                        kwamplify: "amplify" NUMBER
                        kwprovoke: "provoke"
                        kwstorm: "storm"
                        kwaffinity: "affinity" "for" typeexpression
                        kwentwine: "entwine" costsequence
                        kwmodular: "modular" NUMBER
                        kwsunburst: "sunburst"
                        kwbushido: "bushido" NUMBER
                        kwsoulshift: "soulshift" NUMBER
                        kwsplice: "splice" "onto" typeexpression costsequence
                        kwoffering: typeexpression "offering"
                        kwninjutsu: "ninjutsu" costsequence
                        kwepic: "epic"
                        kwconvoke: "convoke"
                        kwdredge: "dredge" NUMBER
                        kwtransmute: "transmute" costsequence
                        kwbloodthirst: "bloodthirst" NUMBER
                        kwhaunt: "haunt"
                        kwreplicate: "replicate" costsequence
                        kwforecast: "forecast"
                        kwgraft: "graft"
                        kwrecover: "recover" costsequence
                        kwripple: "ripple" NUMBER
                        kwsplitsecond: "split" "second"
                        kwsuspend: "suspend" NUMBER
                        kwvanishing: "vanishing" [NUMBER]
                        kwabsorb: "absorb" NUMBER
                        kwauraswap: "aura" "swap" costsequence
                        kwdelve: "delve"
                        kwfortify: "fortify" costsequence
                        kwfrenzy: "frenzy"
                        kwgravestorm: "gravestorm"
                        kwpoisonous: "poisonous" NUMBER
                        kwtransfigure: "transfigure" costsequence
                        kwchampion: "champion" "a"["n"] typeexpression
                        kwchangeling: "changeling"
                        kwevoke: "evoke" costsequence
                        kwhideaway: "hideaway"
                        kwprowl: "prowl" costsequence
                        kwreinforce: "reinforce" costsequence
                        kwconspire: "conspire"
                        kwpersist: "persist"
                        kwwither: "wither"
                        kwretrace: "retrace" costsequence
                        kwdevour: "devour" NUMBER
                        kwexalted: "exalted"
                        kwunearth: "unearth" costsequence
                        kwcascade: "cascade"
                        kwannihilator: "annihilator" NUMBER
                        kwlevelup: "level up" costsequence
                        kwrebound: "rebound"
                        kwtotemarmor: "totem" "armor"
                        kwinfect: "infect"
                        kwbattlecry: "battle" "cry"
                        kwlivingweapon: "living" "weapon"
                        kwundying: "undying"
                        kwmiracle: "miracle" costsequence
                        kwsoulbond: "soulbond"
                        kwoverload: "overload" costsequence
                        kwscavenge: "scavenge" costsequence
                        kwunleash: "unleash"
                        kwcipher: "cipher"
                        kwevolve: "evolve"
                        kwextort: "extort"
                        kwfuse: "fuse"
                        kwbestow: "bestow" costsequence
                        kwtribute: "tribute" NUMBER
                        kwdethrone: "dethrone"
                        kwhiddenagenda: "hidden" "agenda" -> kwhiddenagenda
                        | "double" "agenda" -> kwdoubleagenda
                        kwoutlast: "outlast" costsequence
                        kwprowess: "prowess"
                        kwdash: "dash" costsequence
                        kwexploit: "exploit"
                        kwmenace: "menace"
                        kwrenown: "renown" NUMBER
                        kwawaken: "awaken" costsequence
                        kwdevoid: "devoid"
                        kwingest: "ingest"
                        kwmyriad: "myriad"
                        kwsurge: "surge" costsequence
                        kwskulk: "skulk"
                        kwemerge: "emerge" costsequence
                        kwescalate: "escalate" costsequence
                        kwmelee: "melee"
                        kwcrew: "crew" NUMBER
                        kwfabricate: "fabricate" NUMBER
                        kwpartner: "partner" ["with" objectname]
                        kwundaunted: "undaunted"
                        kwimprovise: "improvise"
                        kwaftermath: "aftermath"
                        kwembalm: "embalm" costsequence
                        kweternalize: "eternalize" costsequence
                        kwafflict: "afflict" NUMBER
                        kwascend: "ascend"
                        kwassist: "assist"
                        
                        costsequence: manaexpression | dashcostexpression
                        
                        //TODO: Add as needed.
                        expression: colorexpression | namedexpression | manaexpression | typeexpression
                        
                        ptexpression: valueexpression "/" valueexpression
                        valueexpression: NUMBER //TODO: Need to account for custom values, variables, etc.
                        dashcostexpression: "—" expression
                        descriptionexpression: expression+
                        
                        namedexpression: "named" objectname
                        targetexpression: "target" expression
                        eachexpression: "each" expression
                        andexpression : expression "and" expression
                        orexpression : expression "or" expression
                        
                        
                        namereference: NAMEREFSYMBOL
                        NAMEREFSYMBOL: "~" //Note: This substitution happens prior to lexing/parsing.
                        
                        //TODO: What about comma-delimited type expressions?
                        typeexpression: (TYPE ["s"] | SUBTYPESPELL ["s"] | SUBTYPELAND ["s"] SUBTYPELAND | SUBTYPEARTIFACT ["s"]
                        | SUBTYPEPLANESWALKER | SUBTYPECREATUREA | SUBTYPECREATUREB | SUBTYPEPLANAR | SUPERTYPE)+
                        
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
                        
                        
                        //TODO: SUBTYPECREATUREA and SUBTYPECREATUREB are split up because having such a long list of alternatives apparently
                        //causes Lark to suffer a recursion depth error. We should see if this is fixable.
                        
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
                        
                        SUPERTYPE: "basic" | "legendary" | "ongoing" | "snow" | "world"
                        
                        
                        colorexpression: colorterm -> colorsingleexpr
                        | colorterm  ("," colorterm ",")* "or" colorterm -> colororexpr
                        | colorterm ("," colorterm ",")* "and" colorterm -> colorandexpr
                        | colorterm ("," colorterm ",")* "and/or" colorterm -> colorandorexpr
                        
                        colorterm: COLORTERM
                        | "non" COLORTERM -> noncolorterm
                        
                        COLORTERM: "white" | "blue" | "black" | "red" | "green" | "monocolored" | "multicolored" | "colorless"
                        
                        objectname: OBJECTNAME
                        OBJECTNAME: WORD ((WS | ",") WORD)* //TODO: commas in names? This is problematic.
                        
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
                        
                        %import common.WORD -> WORD
                        %import common.SIGNED_NUMBER -> NUMBER
                        %import common.WS -> WS
                        %ignore WS
                """, start=startText)
                
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
                        #TODO: There has to be a better way to handle starting at different rules.
                        manaCost = self._miniManaTransformer.transform(self._miniManaParser.parse(cardinput['manaCost']))
                else:
                        manaCost = MgManaExpression()
                        
                #TODO: apparently the MtgJson format doesn't explicitly list color indicators. 
                colorIndicator = None
                
                if 'type' in cardinput:
                        typeLine = self._miniTypelineTransformer.transform(self._miniTypelineParser.parse(cardinput['type']))
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
                        textBox = self._tf.transform(parseTree)
                        #textBox = MgTextBox()
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
                
                
                
                
                
                
                
                
                
                
                