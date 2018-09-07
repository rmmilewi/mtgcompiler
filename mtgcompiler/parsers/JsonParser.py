from mtgcompiler.parsers.baseparser import BaseParser
from mtgcompiler.AST.reference import MgName
from mtgcompiler.AST.card import MgTypeLine,MgFlavorText,MgTextBox,MgCard
from mtgcompiler.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.AST.expressions import MgNumberValue,MgPTExpression,MgManaExpression,MgTypeExpression


from mtgcompiler.AST.abilities import MgDeathtouchAbility,MgDefenderAbility,MgDoubleStrikeAbility,MgFirstStrikeAbility
from mtgcompiler.AST.abilities import MgFlashAbility,MgFlyingAbility,MgHasteAbility,MgIndestructibleAbility


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

class JsonParser(BaseParser):

        def __init__(self,startText='cardtext'):
                """Calling this constructor causes the Lark parser and the parse-to-AST transformer
                to be instantiated."""
                self._lp,self._tf = self.define_grammar(startText)
                
                
        class JsonTransformer(Transformer):
                def kwdeathtouch(self,items): 
                        return MgDeathtouchAbility()
                def kwdefender(self,items): 
                        return MgDefenderAbility()
                def kwdoublestrike(self,items): 
                        return MgDoubleStrikeAbility()
                def kwenchant(self,items): 
                        print("HAI")
                        print(items)
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
                                return MgEquipAbility(quality=quality,cost=cost) #TODO
                                
                def kwfirststrike(self,items): 
                        return MgFirstStrikeAbility()
                def kwflash(self,items): 
                        return MgFlashAbility()
                def kwflying(self,items): 
                        return MgFlyingAbility()
                def kwhaste(self,items): 
                        return MgHasteAbility()
                def kwhexproof(self,items): 
                        return MgHexproofAbility()
                def kwindestructible(self,items): 
                        return MgIndestructibleAbility()
                def kwintimidate(self,items): 
                        return MgIntimidateAbility()
                def kwlandwalk(self,items): 
                        #TODO
                        return MgLandwalkAbility()
                def kwlifelink(self,items): 
                        return MgLifelinkAbility()
                def kwprotection(self,items): 
                        #TODO
                        return MgProtectionAbility()
                def kwreach(self,items): 
                        return MgReachAbility()
                def kwshroud(self,items): 
                        return MgShroudAbility()
                def kwtrample(self,items): 
                        return MgTrampleAbility()
                def kwvigilance(self,items): 
                        return MgVigilanceAbility()
                def kwbanding(self,items): 
                        #: "banding" | "bands" "with" "other" // TODO 
                        return MgBandingAbility()
                def kwrampage(self,items): 
                        #: "rampage" NUMBER
                        return items
                def kwcumulativeupkeep(self,items): 
                        #: "cumulative" "upkeep" costsequence
                        pass
                def kwflanking(self,items): 
                        #: "flanking"
                        pass
                def kwphasing(self,items): 
                        #: "phasing"
                        pass
                def kwbuyback(self,items): 
                        #: "buyback" costsequence
                        pass
                def kwshadow(self,items): 
                        #: "shadow"
                        pass
                def kwcycling(self,items): 
                        #: "cycling" costsequence
                        pass
                def kwecho(self,items): 
                        #: "echo" costsequence
                        pass
                def kwhorsemanship(self,items): 
                        #: "horsemanship"
                        pass
                def kwfading(self,items): 
                        #: "fading" NUMBER
                        pass
                def kwkicker(self,items): 
                        #: "kicker" costsequence
                        pass
                def kwflashback(self,items): 
                        #: "flashback"
                        pass
                def kwmadness(self,items): 
                        #: "madness"
                        pass
                def kwfear(self,items): 
                        #: "fear"
                        pass
                def kwmorph(self,items): 
                        #: "morph"
                        pass
                def kwamplify(self,items): 
                        #: "amplify" NUMBER
                        pass
                def kwprovoke(self,items): 
                        #: "provoke"
                        pass
                def kwstorm(self,items): 
                        #: "storm"
                        pass
                def kwaffinity(self,items): 
                        #: "affinity" "for" // TODO
                        pass
                def kwentwine(self,items): 
                        #: "entwine" costsequence
                        pass
                def kwmodular(self,items): 
                        #: "modular"
                        pass
                def kwsunburst(self,items): 
                        #: "sunburst"
                        pass
                def kwbushido(self,items): 
                        #: "bushido" NUMBER
                        pass
                def kwsoulshift(self,items): 
                        #: "soulshift" NUMBER
                        pass
                def kwsplice(self,items): 
                        #: "splice" "onto" // TODO
                        pass
                def kwoffering(self,items): 
                        #: "offering" // TODO
                        pass
                def kwninjutsu(self,items): 
                        #: "ninjutsu" costsequence
                        pass
                def kwepic(self,items): 
                        #: "epic"
                        pass
                def kwconvoke(self,items): 
                        #: "convoke"
                        pass
                def kwdredge(self,items): 
                        #: "dredge" NUMBER
                        pass
                def kwtransmute(self,items): 
                        #: "transmute" costsequence
                        pass
                def kwbloodthirst(self,items): 
                        #: "bloodthirst" NUMBER
                        pass
                def kwhaunt(self,items): 
                        #: "haunt"
                        pass
                def kwreplicate(self,items): 
                        #: "replicate"
                        pass
                def kwforecast(self,items): 
                        #: "forecast"
                        pass
                def kwgraft(self,items): 
                        #: "graft"
                        pass
                def kwrecover(self,items): 
                        #: "recover" costsequence
                        pass
                def kwripple(self,items): 
                        #: "ripple" NUMBER
                        pass
                def kwsplitsecond(self,items): 
                        #: "split" "second"
                        pass
                def kwsuspend(self,items): 
                        #: "suspend" NUMBER
                        pass
                def kwvanishing(self,items): 
                        #: "vanishing" [NUMBER]
                        pass
                def kwabsorb(self,items): 
                        #: "absorb" NUMBER
                        pass
                def kwauraswap(self,items): 
                        #: "aura" "swap" costsequence
                        pass
                def kwdelve(self,items): 
                        #: "delve"
                        pass
                def kwfortify(self,items): 
                        #: "fortify"
                        pass
                def kwfrenzy(self,items): 
                        #: "frenzy"
                        pass
                def kwgravestorm(self,items): 
                        #: "gravestorm"
                        pass
                def kwpoisonous(self,items): 
                        #: "poisonous" NUMBER
                        pass
                def kwtransfigure(self,items): 
                        #: "transfigure" costsequence
                        pass
                def kwchampion(self,items): 
                        #: "champion" "a"["n"] // TODO
                        pass
                def kwchangeling(self,items): 
                        #: "changeling"
                        pass
                def kwevoke(self,items): 
                        #: "evoke" costsequence
                        pass
                def kwhideaway(self,items): 
                        #: "hideaway"
                        pass
                def kwprowl(self,items): 
                        #: "prowl" costsequence
                        pass
                def kwreinforce(self,items): 
                        #: "reinforce" costsequence
                        pass
                def kwconspire(self,items): 
                        #: "conspire"
                        pass
                def kwpersist(self,items): 
                        #: "persist"
                        pass
                def kwwither(self,items): 
                        #: "wither"
                        pass
                def kwretrace(self,items): 
                        #: "retrace" costsequence
                        pass
                def kwdevour(self,items): 
                        #: "devour" NUMBER
                        pass
                def kwexalted(self,items): 
                        #: "exalted"
                        pass
                def kwunearth(self,items): 
                        #: "unearth" costsequence
                        pass
                def kwcascade(self,items): 
                        #: "cascade"
                        pass
                def kwannihilator(self,items): 
                        #: "annihilator" NUMBER
                        pass
                def kwlevelup(self,items): 
                        #: "level up" // TODO
                        pass
                def kwrebound(self,items): 
                        #: "rebound"
                        pass
                def kwtotemarmor(self,items): 
                        #: "totem" "armor"
                        pass
                def kwinfect(self,items): 
                        #: "infect"
                        pass
                def kwbattlecry(self,items): 
                        #: "battle" "cry"
                        pass
                def kwlivingweapon(self,items): 
                        #: "living" "weapon"
                        pass
                def kwundying(self,items): 
                        #: "undying"
                        pass
                def kwmiracle(self,items): 
                        #: "miracle" costsequence
                        pass
                def kwsoulbond(self,items): 
                        #: "soulbond"
                        pass
                def kwoverload(self,items): 
                        #: "overload" costsequence
                        pass
                def kwscavenge(self,items): 
                        #: "scavenge" costsequence
                        pass
                def kwunleash(self,items): 
                        #: "unleash"
                        pass
                def kwcipher(self,items): 
                        #: "cipher"
                        pass
                def kwevolve(self,items): 
                        #: "evolve"
                        pass
                def kwextort(self,items): 
                        #: "extort"
                        pass
                def kwfuse(self,items): 
                        #: "fuse"
                        pass
                def kwbestow(self,items): 
                        #: "bestow" costsequence
                        pass
                def kwtribute(self,items): 
                        #: "tribute" NUMBER
                        pass
                def kwdethrone(self,items): 
                        #: "dethrone"
                        pass
                def kwhiddenagenda(self,items): 
                        #: "hidden" "agenda" | "double" "agenda"
                        pass
                def kwoutlast(self,items): 
                        #: "outlast" costsequence
                        pass
                def kwprowess(self,items): 
                        #: "prowess"
                        pass
                def kwdash(self,items): 
                        #: "dash" costsequence
                        pass
                def kwexploit(self,items): 
                        #: "exploit"
                        pass
                def kwmenace(self,items): 
                        #: "menace"
                        pass
                def kwrenown(self,items): 
                        #: "renown" NUMBER
                        pass
                def kwawaken(self,items): 
                        #: "awaken" costsequence
                        pass
                def kwdevoid(self,items): 
                        #: "devoid"
                        pass
                def kwingest(self,items): 
                        #: "ingest"
                        pass
                def kwmyriad(self,items): 
                        #: "myriad"
                        pass
                def kwsurge(self,items): 
                        #: "surge" costsequence
                        pass
                def kwskulk(self,items): 
                        #: "skulk"
                        pass
                def kwemerge(self,items): 
                        #: "emerge" costsequence
                        pass
                def kwescalate(self,items): 
                        #: "escalate" costsequence
                        pass
                def kwmelee(self,items): 
                        #: "melee"
                        pass
                def kwcrew(self,items): 
                        #: "crew" NUMBER
                        pass
                def kwfabricate(self,items): 
                        #: "fabricate" NUMBER
                        pass
                def kwpartner(self,items): 
                        #: "partner" | "partner" "with" // TODO
                        pass
                def kwundaunted(self,items): 
                        #: "undaunted"
                        pass
                def kwimprovise(self,items): 
                        #: "improvise"
                        pass
                def kwaftermath(self,items): 
                        #: "aftermath"
                        pass
                def kwembalm(self,items): 
                        #: "embalm" costsequence
                        pass
                def kweternalize(self,items): 
                        #: "eternalize" costsequence
                        pass
                def kwafflict(self,items): 
                        #: "afflict" NUMBER
                        pass
                def kwascend(self,items): 
                        #: "ascend"
                        pass
                def kwassist(self,items): 
                        #: "assist"
                        pass
                        
                        
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
                                        raise ValueError("Unrecognized type token: {0}".format(item))
                        typeExpr = MgTypeExpression(*typeobjects)
                        return typeExpr
                
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
                
                        cardtext : (ability remindertext?)*
                        remindertext : /\(.*?\)/ -> reminder
                        
                        ability : keywordsequence
                        keywordsequence: keywordability | keywordability "," keywordsequence
                        
                        keywordability: kwdeathtouch
                        |kwdefender 
                        |kwdoublestrike 
                        |kwenchant 
                        |kwequip 
                        |kwfirststrike
                        |kwflash
                        |kwflying
                        |kwhaste
                        |kwhexproof
                        |kwindestructible
                        |kwintimidate
                        |kwlandwalk
                        |kwlifelink
                        |kwprotection
                        |kwreach
                        |kwshroud
                        |kwtrample
                        |kwvigilance
                        |kwbanding
                        |kwrampage
                        |kwcumulativeupkeep
                        |kwflanking
                        |kwphasing
                        |kwbuyback
                        |kwshadow
                        |kwcycling
                        |kwecho
                        |kwhorsemanship
                        |kwfading
                        |kwkicker
                        |kwflashback
                        |kwmadness
                        |kwfear
                        |kwmorph
                        |kwamplify
                        |kwprovoke
                        |kwstorm
                        |kwaffinity
                        |kwentwine
                        |kwmodular
                        |kwsunburst
                        |kwbushido
                        |kwsoulshift
                        |kwsplice
                        |kwoffering
                        |kwninjutsu
                        |kwepic
                        |kwconvoke
                        |kwdredge
                        |kwtransmute
                        |kwbloodthirst
                        |kwhaunt
                        |kwreplicate
                        |kwforecast
                        |kwgraft
                        |kwrecover
                        |kwripple
                        |kwsplitsecond
                        |kwsuspend
                        |kwvanishing
                        |kwabsorb
                        |kwauraswap
                        |kwdelve
                        |kwfortify
                        |kwfrenzy
                        |kwgravestorm
                        |kwpoisonous
                        |kwtransfigure
                        |kwchampion
                        |kwchangeling
                        |kwevoke
                        |kwhideaway
                        |kwprowl
                        |kwreinforce
                        |kwconspire
                        |kwpersist
                        |kwwither
                        |kwretrace
                        |kwdevour
                        |kwexalted
                        |kwunearth
                        |kwcascade
                        |kwannihilator
                        |kwlevelup
                        |kwrebound
                        |kwtotemarmor
                        |kwinfect
                        |kwbattlecry
                        |kwlivingweapon
                        |kwundying
                        |kwmiracle
                        |kwsoulbond
                        |kwoverload
                        |kwscavenge
                        |kwunleash
                        |kwcipher
                        |kwevolve
                        |kwextort
                        |kwfuse
                        |kwbestow
                        |kwtribute
                        |kwdethrone
                        |kwhiddenagenda
                        |kwoutlast
                        |kwprowess
                        |kwdash
                        |kwexploit
                        |kwmenace
                        |kwrenown
                        |kwawaken
                        |kwdevoid
                        |kwingest
                        |kwmyriad
                        |kwsurge
                        |kwskulk
                        |kwemerge
                        |kwescalate
                        |kwmelee
                        |kwcrew
                        |kwfabricate
                        |kwpartner
                        |kwundaunted
                        |kwimprovise
                        |kwaftermath
                        |kwembalm
                        |kweternalize
                        |kwafflict
                        |kwascend
                        |kwassist
                        
                        kwdeathtouch: "deathtouch"
                        kwdefender: "defender"
                        kwdoublestrike: "double" "strike"
                        kwenchant: "enchant" typeexpression // TODO
                        kwequip: "equip" costsequence  //TODO | "equip" descriptionexpr costsequence
                        kwfirststrike: "first strike"
                        kwflash: "flash"
                        kwflying: "flying"
                        kwhaste: "haste"
                        kwhexproof: "hexproof"
                        kwindestructible: "indestructible"
                        kwintimidate: "intimidate"
                        kwlandwalk: "walk" // TODO
                        kwlifelink: "lifelink"
                        kwprotection: "protection" "from" // TODO
                        kwreach: "reach"
                        kwshroud: "shroud"
                        kwtrample: "trample"
                        kwvigilance: "vigilance"
                        kwbanding: "banding" | "bands" "with" "other" // TODO 
                        kwrampage: "rampage" NUMBER
                        kwcumulativeupkeep: "cumulative" "upkeep" costsequence
                        kwflanking: "flanking"
                        kwphasing: "phasing"
                        kwbuyback: "buyback" costsequence
                        kwshadow: "shadow"
                        kwcycling: "cycling" costsequence
                        kwecho: "echo" costsequence
                        kwhorsemanship: "horsemanship"
                        kwfading: "fading" NUMBER
                        kwkicker: "kicker" costsequence
                        kwflashback: "flashback"
                        kwmadness: "madness"
                        kwfear: "fear"
                        kwmorph: "morph"
                        kwamplify: "amplify" NUMBER
                        kwprovoke: "provoke"
                        kwstorm: "storm"
                        kwaffinity: "affinity" "for" // TODO
                        kwentwine: "entwine" costsequence
                        kwmodular: "modular"
                        kwsunburst: "sunburst"
                        kwbushido: "bushido" NUMBER
                        kwsoulshift: "soulshift" NUMBER
                        kwsplice: "splice" "onto" // TODO
                        kwoffering: "offering" // TODO
                        kwninjutsu: "ninjutsu" costsequence
                        kwepic: "epic"
                        kwconvoke: "convoke"
                        kwdredge: "dredge" NUMBER
                        kwtransmute: "transmute" costsequence
                        kwbloodthirst: "bloodthirst" NUMBER
                        kwhaunt: "haunt"
                        kwreplicate: "replicate"
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
                        kwfortify: "fortify"
                        kwfrenzy: "frenzy"
                        kwgravestorm: "gravestorm"
                        kwpoisonous: "poisonous" NUMBER
                        kwtransfigure: "transfigure" costsequence
                        kwchampion: "champion" "a"["n"] // TODO
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
                        kwlevelup: "level up" // TODO
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
                        kwhiddenagenda: "hidden" "agenda" | "double" "agenda"
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
                        kwpartner: "partner" | "partner" "with" // TODO
                        kwundaunted: "undaunted"
                        kwimprovise: "improvise"
                        kwaftermath: "aftermath"
                        kwembalm: "embalm" costsequence
                        kweternalize: "eternalize" costsequence
                        kwafflict: "afflict" NUMBER
                        kwascend: "ascend"
                        kwassist: "assist"
                        
                        costsequence: manaexpression | "-" expression // TODO
                        
                        //TODO: Add as needed.
                        expression: manaexpression | typeexpression 
                        typeexpression: (TYPE | SUBTYPESPELL | SUBTYPELAND | SUBTYPEARTIFACT | SUBTYPEPLANESWALKER | SUBTYPECREATUREA
                        | SUBTYPECREATUREB | SUBTYPEPLANAR | SUPERTYPE)+
                        
                        
                        TYPE: "artifact" | "conspiracy" | "creature" | "enchantment" | "instant"
                        | "land" | "phenomenon" | "plane" | "planeswalker" | "scheme" | "sorcery"
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
                        
                        manamarker_halfmana: "H" -> halfmarker
                        manamarker_color: "W" -> whitemarker
                        | "U" -> bluemarker
                        | "B" -> blackmarker
                        | "R" -> redmarker
                        | "G" -> greenmarker
                        manamarker_snow: "S" -> snowmarker
                        manamarker_phyrexian: "P" -> phyrexianmarker
                        manamarker_colorless: "C" -> colorlessmarker
                        manamarker_x: "X" -> xmarker
                        
                        
                        %import common.SIGNED_NUMBER -> NUMBER
                        %import common.WS
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
                
                if 'name' in cardinput:
                        cardName = MgName(cardinput['name'])
                else:
                        cardName = MgName()
                        
                if 'manaCost' in cardinput:
                        self._lp.start = "manaexpression"
                        manaCost = self._tf.transform(self._lp.parse(cardinput['manaCost']))
                else:
                        manaCost = MgManaExpression()
                        
                #TODO: apparently the MtgJson format doesn't explicitly list color indicators. 
                colorIndicator = None
                
                if 'type' in cardinput:
                        if 'supertypes' in cardinput:
                                supertypes = MgTypeExpression() #TODO
                        else:
                                supertypes = MgTypeExpression()
                        if 'types' in cardinput:
                                types = MgTypeExpression() #TODO
                        else:
                                types = MgTypeExpression()
                        if 'subtypes' in cardinput:
                                subtypes = MgTypeExpression() #TODO
                        else:
                                subtypes = MgTypeExpression()
                        typeLine = MgTypeLine(supertypes=supertypes,types=types,subtypes=subtypes)
                else:
                        typeLine = MgTypeLine()
                        
                        
                if 'loyalty' in cardinput:
                        loyalty = None #TODO
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
                        self._lp.parse(cardinput['text'])
                        textBox = MgTextBox() #TODO
                else:
                        textBox = MgTextBox()
                        
                if 'life' in cardinput:
                        lifeModifier = None #TODO
                else:
                        lifeModifier = None
                        
                if 'hand' in cardinput:
                        handModifier = None #TODO
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
                
                
                
                
                
                
                
                
                
                
                