import unittest
import time
import mtgcompiler.midend.support.inspection as inspection
import mtgcompiler.midend.support.binding as binding
import mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonCompiler as MtgJsonCompiler
import pytest
import lark.lexer

class TestGrammarAndParser(unittest.TestCase):

    """
    @classmethod
    def setUpClass(cls):
        compiler = MtgJsonCompiler.MtgJsonCompiler(options={"parser.startRule": "cardtext",
                                                            "parser.larkDebug": True,
                                                            #"parser.larkLexer" : "basic",
                                                            "parser.larkParser" : "earley",
                                                            "parser.strict" : True,
                                                            "parser.ambiguity" : "explicit"
                                                            #"parser.overrideGrammar" : cls.overrideGrammar_tmp()
                                                            })
        parser = compiler.getParser()
        preprocessor = compiler.getPreprocessor()
        cls._parser = parser
        cls._preprocessor = preprocessor
    """""
        

    @pytest.mark.skip(reason="Just doing some experimentation here.")
    def test_WithBasicLexer_RunLexerOnly(self):
        def runLexer(data):
            preprocessed = self._preprocessor.prelex(data['oracle_text'], None, data['name'])
            lexerState = lark.lexer.LexerState(text=preprocessed, line_ctr=lark.lexer.LineCounter(
                b'\n' if isinstance(preprocessed, bytes) else '\n'))
            lexTimeStart = time.time()
            lexerResults = self._parser.parser.lexer.lex(state=lexerState, parser_state=None)
            lexTimeEnd = time.time()
            print(f"{data['name']} took {lexTimeEnd - lexTimeStart} to lex.")
            print(f"Lexer Results for {data['name']}...")
            print("Full Text:",data['oracle_text'])
            for token in lexerResults:
                print(f"(token type: {token.type}) | {token}")

        ragingGoblin = {
            "object": "card",
            "name": "Raging Goblin",
            "oracle_text": "Haste (This creature can attack and {T} as soon as it comes under your control.)"
            }
        #runLexer(ragingGoblin)

        dragonCard = {
            "object": "card",
            "name": "Dragon Card",
            "oracle_text": "If you control a dragon, draw a card."
            }
        #runLexer(dragonCard)

        dragonCard2 = {
            "object": "card",
            "name": "Other Card",
            "oracle_text": "they draw a card."
        }
        #runLexer(dragonCard)


        parseTimeStart = time.time()
        #parseResult = self._parser.parse("if you control a dragon, draw a card.")
        parseResult = self._parser.parse("sacrifice a permanent named target creature")
        parseTimeEnd = time.time()
        print(f"Input text took {parseTimeEnd-parseTimeStart} to parse.")
        print(parseResult.pretty())
        #print(f"{dragonCard['name']} took {parseTimeEnd-parseTimeStart} to parse.")


    def test_periodPlacementForStatements(self):
        statementGrammar = """
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
        | modalstatement

        thenstatement: "then" statement
        insteadstatement: statement "instead"
        maystatement:  playerdeclref? ("may" | "may" "have") statement
        wouldstatement: playerdeclref? "would" statement
        additionalcoststatement: "as" "an" "additional" "cost" "to" statement "," statement
        modalstatement: "choose" valuecardinal DASH (modalchoiceexpression)+
        modalchoiceexpression: MODALCHOICE statementblock

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
        costchangestatement: declarationorreference "cost"["s"] manasymbolexpression "more" "to" ("cast" | "activate") -> costincreasestatement
        | declarationorreference "cost"["s"] manasymbolexpression "less" "to" "cast" -> costreductionstatement
        wherestatement: statement "," "where" statement //[Note: Used in elaborating variables.]

        expressionstatement: (effectexpression | beexpression | valueexpression) timeexpression? //[TODO: Do time expressions need to go here?]
        beexpression: ("be"|"been") modifier valueexpression? ("by" declarationorreference)? timeexpression?//[TODO: Not sure how to categorize this one yet.]
        activationstatement: cost ":" statementblock 

        compoundstatement: statement  ("," statement)* ","? thenstatement -> compoundthenstatement
        | statement ("," statement)* untilstatement -> compounduntilstatement
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
        | "for" "each" genericdeclarationexpression -> forstatementnostatement

        untilstatement: "until" effectexpression -> untileffecthappensstatement
        | "until" timeexpression "," statement -> untiltimestatement
        | statement "until" timeexpression -> untiltimestatementinv

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
        
        //Non-statement related rules...
        declarationorreference: RANDOMTEXT
        timeexpression: RANDOMTEXT
        effectexpression: RANDOMTEXT
        genericdeclarationexpression: RANDOMTEXT
        characteristicexpression: RANDOMTEXT
        manasymbolexpression: RANDOMTEXT
        valueexpression: RANDOMTEXT
        countertype: RANDOMTEXT
        valuecardinal: RANDOMTEXT
        playerdeclref: RANDOMTEXT
        abilitysequencestatement: RANDOMTEXT
        cost: RANDOMTEXT
        modifier: RANDOMTEXT
        DASH: "—"
        MODALCHOICE: "•"
        RANDOMTEXT: "TEXT"
        
        %import common.WS -> WS
        %ignore WS
        """
        compilerUsingPartialGrammar = MtgJsonCompiler.MtgJsonCompiler(
            options={"parser.overrideGrammar": statementGrammar,
                     "parser.startRule": "statementblock",
                     "parser.ambiguity": "explicit"
                     })
        parser = compilerUsingPartialGrammar.getParser()

        statementBlocksToTest = [
            "if TEXT, TEXT instead.",
            "whenever TEXT, TEXT until TEXT.",
            "TEXT: TEXT is TEXT until TEXT.",
            "TEXT. TEXT. TEXT.",
            "TEXT, TEXT, and TEXT. TEXT.",
            "if TEXT, TEXT during TEXT except TEXT after TEXT."
        ]

        for statementBlock in statementBlocksToTest:
            try:
                fullParseTimeStart = time.time()
                parseTree = parser.parse(statementBlock)
                fullParseTimeEnd = time.time()
                print(f"Statement(s) ({statementBlock}) took {fullParseTimeEnd-fullParseTimeStart} to parse")
                ambiguities = list(parseTree.find_data("_ambig"))
                print(f"The input has {len(ambiguities)} ambiguities.")
            except Exception as exception:
                print(f"Encountered an exception when parsing statement(s) ({statementBlock}): {exception}" )
        print("-----------------------")




    @pytest.mark.skip(reason="Just doing some experimentation here.")
    def test_CompareGrammarComplexity(self):
        subsetOfGrammar = """
        sacrificeexpression: "sacrifice" declarationorreference
        declarationorreference: ("a" | "an") typeexpression
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

        SUBTYPEENCHANTMENT: "aura" | "cartouche" | "curse" | "saga" | "shrine" | "case"

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
        
        %import common.UCASE_LETTER -> UCASE_LETTER
        %import common.LCASE_LETTER -> LCASE_LETTER
        %import common.WORD -> WORD
        %import common.SIGNED_NUMBER -> NUMBER
        %import common.WS -> WS
        %ignore WS
        """
        compilerUsingFullGrammar = MtgJsonCompiler.MtgJsonCompiler(options={"parser.startRule": "sacrificeexpression"})
        parserUsingFullGrammar = compilerUsingFullGrammar.getParser()
        compilerUsingPartialGrammar = MtgJsonCompiler.MtgJsonCompiler(options={"parser.overrideGrammar": subsetOfGrammar, "parser.startRule": "sacrificeexpression"})
        parserUsingPartialGrammar = compilerUsingPartialGrammar.getParser()

        expressionsToTest = ["sacrifice a creature","sacrifice a legendary elf power-plant assembly-worker","sacrifice an ajani planeswalker","sacrifice a snow dragon artifact creature"]

        for expression in expressionsToTest:
            fullParseTimeStart = time.time()
            parserUsingFullGrammar.parse(expression)
            fullParseTimeEnd = time.time()

            partialParseTimeStart = time.time()
            parserUsingPartialGrammar.parse(expression)
            partialParseTimeEnd = time.time()

            print(f"Type Expression ({expression}) took {fullParseTimeEnd-fullParseTimeStart} seconds to do a parse with the full grammar, and {partialParseTimeEnd-partialParseTimeStart} seconds with a partial grammar.")

    @classmethod
    def overrideGrammar_tmp(cls):
        return r"""
                typeline.100: typelinesupert typelinet ("—" typelinesubt)?
                typelinesupert.100: SUPERTYPE*
                typelinet.100: TYPE*
                typelinesubt.100: (SUBTYPESPELL | SUBTYPELAND | SUBTYPEARTIFACT | SUBTYPEENCHANTMENT | SUBTYPEPLANESWALKER | SUBTYPECREATUREA | SUBTYPECREATUREB | SUBTYPEPLANAR)*

                //[NOTE.100: Added support for starting reminder text, but what does it attach to?]
                cardtext.100: remindertext? (ability "\n"*)*
                remindertext.100: "(remindertext)"///\(.*?\)/

                ability.100: statementblock remindertext? -> regularability
                | keywordlist remindertext?
                //abilityword.100: WORD+ "—"

                //ability.100: abilityword? statementblock remindertext? -> regularability
                //| keywordlist remindertext?
                //abilityword.100: WORD+ "—"

                keywordlist.100: keywordsequence
                keywordsequence.100: keywordability | keywordsequence ("," | ";") keywordability

                statementblock.100: (statement ["."])+

                //STATEMENTS
                
                statement.100: compoundstatement
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
                | modalstatement

                thenstatement.100: THEN statement
                insteadstatement.100: statement INSTEAD
                maystatement.100:  playerdeclref? (MAY | MAY HAVE) statement
                wouldstatement.100: playerdeclref? "would" statement
                additionalcoststatement.100: AS "an" "additional" "cost" "to" statement "," statement
                modalstatement.100: CHOOSE valuecardinal DASH (modalchoiceexpression)+
                modalchoiceexpression.100: MODALCHOICE statementblock

                dostatement.100: declarationorreference? (DO | DOES) statement? -> dostatement
                | declarationorreference? (DO NOT | DOES NOT) statement? -> dontstatement

                beingstatement.100: isstatement
                | hasstatement
                | isntstatement
                | canstatement
                | becomesstatement
                | costchangestatement
                | wherestatement

                !isstatement.100: declarationorreference (IS | WAS | ARE EACH?) ("still"|NOT)? (declarationorreference | characteristicexpression | statement)
                !hasstatement.100: declarationorreference? ("has"|HAVE|"had") (abilitysequencestatement | characteristicexpression | beexpression | statement)
                | declarationorreference?  ("has"|HAVE|"had") ("a"|valueexpression) countertype "counter"["s"] "on" declarationorreference -> hascounterstatement
                isntstatement.100: declarationorreference? IS NOT statement
                canstatement.100: declarationorreference? CAN statement
                | declarationorreference? CAN NOT statement -> cantstatement
                becomesstatement.100: declarationorreference? "become"["s"] genericdeclarationexpression
                costchangestatement.100: declarationorreference "cost"["s"] manasymbolexpression "more" "to" ("cast" | "activate") -> costincreasestatement
                | declarationorreference "cost"["s"] manasymbolexpression "less" "to" "cast" -> costreductionstatement
                wherestatement.100: statement "," "where" statement //[Note.100: Used in elaborating variables.]

                expressionstatement.100: (effectexpression | beexpression | valueexpression) timeexpression? //[TODO.100: Do time expressions need to go here?]
                beexpression.100: ("be"|"been") modifier valueexpression? ("by" declarationorreference)? timeexpression?//[TODO.100: Not sure how to categorize this one yet.]
                activationstatement.100: cost ".100:" statementblock

                compoundstatement.100: statement  ("," statement)* ","? thenstatement -> compoundthenstatement
                | statement ("," statement)* untilstatement -> compounduntilstatement
                | statement ("," statement)* ","? "and" statement -> compoundandstatement
                | statement ("," statement)* ","? "or" statement -> compoundorstatement

                conditionalstatement.100: ifstatement
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

                ifstatement.100: IF statement "," statement
                | statement ONLY? IF statement -> ifstatementinv

                wheneverstatement.100:  "whenever" statement timeexpression? "," statement 
                | statement "whenever" statement timeexpression? -> wheneverstatementinv

                whenstatement.100:  "when" statement "," statement 
                | statement "when" statement -> whenstatementinv

                atstatement.100:  "at" timeexpression "," statement 
                | statement "at" timeexpression -> atstatementinv

                aslongasstatement.100:  "for"? AS "long" AS statement "," statement
                | statement "for"? AS "long" AS statement -> aslongasstatementinv

                forstatement.100:  "for" EACH (genericdeclarationexpression | "time" statement) ("beyond" "the" "first")? "," statement 
                | statement "for" EACH (genericdeclarationexpression | "time" statement) ("beyond" "the" "first")? -> forstatementinv
                | "for" EACH genericdeclarationexpression -> forstatementnostatement

                untilstatement.100: UNTIL effectexpression -> untileffecthappensstatement
                | UNTIL timeexpression "," statement -> untiltimestatement
                | statement UNTIL timeexpression -> untiltimestatementinv

                afterstatement.100:  AFTER timeexpression "," statement 
                | statement AFTER timeexpression -> afterstatementinv

                otherwisestatement.100: OTHERWISE "," statement

                unlessstatement.100:  statement UNLESS statement

                asstatement.100: AS statement "," statement -> asstatement

                whilestatement.100:  WHILE statement "," statement

                duringstatement.100:  statement DURING timeexpression
                | statement ONLY DURING timeexpression -> exclusiveduringstatement

                exceptstatement.100:  statement "except" (("by"|"for") genericdeclarationexpression | statement)

                ratherstatement.100:  statement RATHER RATHER statement

                nexttimestatement.100: "the" "next" "time" statement timeexpression? "," statement

                beforestatement.100: statement BEFORE (timeexpression | statement)

                //KEYWORD ABILITIES

                abilitysequencestatement.100: (keywordability | quotedabilitystatement) (("," (keywordability | quotedabilitystatement) ",")* ("and" (keywordability | quotedabilitystatement)))?
                quotedabilitystatement.100: "\"" statementblock "\""

                keywordability.100: kwdeathtouch
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
                | kwassist | kwjumpstart | kwmentor | kwafterlife | kwriot | kwspectacle
                | kwescape | kwmutate | kwencore | kwboast | kwforetell | kwdemonstrate
                | kwtimebound | kwdisturb | kwdecayed | kwcleave | kwtraining
                | kwcompleated | kwreconfigure | kwblitz | kwcasualty | kwenlist
                | kwreadahead | kwravenous | kwsquad | kwprototype | kwlivingmetal
                | kwformirrodin | kwtoxic | kwbackup | kwbargain | kwcraft | kwdisguise
                | kwsolve | kwplot | kwsaddle | kwspree | kwfreerunning | kwgift
                | kwoffspring | kwimpending


                kwdeathtouch.100: "deathtouch"
                kwdefender.100: "defender"
                kwdoublestrike.100: "double" "strike"
                kwenchant.100: "enchant" genericdescriptionexpression
                kwequip.100: "equip" cost | "equip" genericdescriptionexpression cost
                kwfirststrike.100: "first strike"
                kwflash.100: "flash"
                kwflying.100: "flying"
                kwhaste.100: "haste"
                kwhexproof.100: "hexproof" | "hexproof" "from" genericdescriptionexpression
                kwindestructible.100: "indestructible"
                kwintimidate.100: "intimidate"
                kwlandwalk.100: typeexpression "walk"
                kwlifelink.100: "lifelink"
                kwprotection.100: "protection" "from" genericdescriptionexpression ("and" "from" genericdescriptionexpression)*
                kwreach.100: "reach"
                kwshroud.100: "shroud"
                kwtrample.100: "trample"
                kwvigilance.100: "vigilance"
                kwbanding.100: "banding" | "bands" WITH "other" genericdescriptionexpression
                kwrampage.100: "rampage" valuenumber
                kwcumulativeupkeep.100: "cumulative" "upkeep" cost
                kwflanking.100: "flanking"
                kwphasing.100: "phasing"
                kwbuyback.100: "buyback" cost
                kwshadow.100: "shadow"
                kwcycling.100: [typeexpression] "cycling" cost
                kwecho.100: "echo" cost
                kwhorsemanship.100: "horsemanship"
                kwfading.100: "fading" valuenumber
                kwkicker.100: "kicker" cost -> kicker
                | "multikicker" cost -> multikicker
                kwflashback.100: "flashback" cost
                kwmadness.100: "madness" cost
                kwfear.100: "fear"
                kwmorph.100: "morph" cost -> kwmorph
                | "megamorph" cost -> kwmegamorph
                kwamplify.100: "amplify" valuenumber
                kwprovoke.100: "provoke"
                kwstorm.100: "storm"
                kwaffinity.100: "affinity" "for" typeexpression
                kwentwine.100: "entwine" cost
                kwmodular.100: "modular" valuenumber
                kwsunburst.100: "sunburst"
                kwbushido.100: "bushido" valuenumber
                kwsoulshift.100: "soulshift" valuenumber
                kwsplice.100: "splice" "onto" typeexpression cost
                kwoffering.100: typeexpression "offering"
                kwninjutsu.100: "ninjutsu" cost
                kwepic.100: "epic"
                kwconvoke.100: "convoke"
                kwdredge.100: "dredge" valuenumber
                kwtransmute.100: "transmute" cost
                kwbloodthirst.100: "bloodthirst" valuenumber
                kwhaunt.100: "haunt"
                kwreplicate.100: "replicate" cost
                kwforecast.100: "forecast" activationstatement
                kwgraft.100: "graft"
                kwrecover.100: "recover" cost
                kwripple.100: "ripple" valuenumber
                kwsplitsecond.100: "split" "second"
                kwsuspend.100: "suspend" valuenumber cost 
                kwvanishing.100: "vanishing" [valuenumber]
                kwabsorb.100: "absorb" valuenumber
                kwauraswap.100: "aura" "swap" cost
                kwdelve.100: "delve"
                kwfortify.100: "fortify" cost
                kwfrenzy.100: "frenzy"
                kwgravestorm.100: "gravestorm"
                kwpoisonous.100: "poisonous" valuenumber
                kwtransfigure.100: "transfigure" cost
                kwchampion.100: "champion" "a"["n"] typeexpression
                kwchangeling.100: "changeling"
                kwevoke.100: "evoke" cost
                kwhideaway.100: "hideaway"
                kwprowl.100: "prowl" cost
                kwreinforce.100: "reinforce" cost
                kwconspire.100: "conspire"
                kwpersist.100: "persist"
                kwwither.100: "wither"
                kwretrace.100: "retrace" cost
                kwdevour.100: "devour" valuenumber
                kwexalted.100: "exalted"
                kwunearth.100: "unearth" cost
                kwcascade.100: "cascade"
                kwannihilator.100: "annihilator" valuenumber
                kwlevelup.100: "level up" cost
                kwrebound.100: "rebound"
                kwtotemarmor.100: "totem" "armor"
                kwinfect.100: "infect"
                kwbattlecry.100: "battle" "cry"
                kwlivingweapon.100: "living" "weapon"
                kwundying.100: "undying"
                kwmiracle.100: "miracle" cost
                kwsoulbond.100: "soulbond"
                kwoverload.100: "overload" cost
                kwscavenge.100: "scavenge" cost
                kwunleash.100: "unleash"
                kwcipher.100: "cipher"
                kwevolve.100: "evolve"
                kwextort.100: "extort"
                kwfuse.100: "fuse"
                kwbestow.100: "bestow" cost
                kwtribute.100: "tribute" valuenumber
                kwdethrone.100: "dethrone"
                kwhiddenagenda.100: "hidden" "agenda" -> kwhiddenagenda
                | "double" "agenda" -> kwdoubleagenda
                kwoutlast.100: "outlast" cost
                kwprowess.100: "prowess"
                kwdash.100: "dash" cost
                kwexploit.100: "exploit"
                kwmenace.100: "menace"
                kwrenown.100: "renown" valuenumber
                kwawaken.100: "awaken" cost
                kwdevoid.100: "devoid"
                kwingest.100: "ingest"
                kwmyriad.100: "myriad"
                kwsurge.100: "surge" cost
                kwskulk.100: "skulk"
                kwemerge.100: "emerge" cost
                kwescalate.100: "escalate" cost
                kwmelee.100: "melee"
                kwcrew.100: "crew" valuenumber
                kwfabricate.100: "fabricate" valuenumber
                kwpartner.100: "partner" [WITH objectname]
                kwundaunted.100: "undaunted"
                kwimprovise.100: "improvise"
                kwaftermath.100: "aftermath"
                kwembalm.100: "embalm" cost
                kweternalize.100: "eternalize" cost
                kwafflict.100: "afflict" valuenumber
                kwascend.100: "ascend"
                kwassist.100: "assist"
                kwjumpstart.100: "jump-start"
                kwmentor.100: "mentor"
                kwafterlife.100: "afterlife" valuenumber
                kwriot.100: "riot"
                kwspectacle.100: "spectacle" cost
                kwescape.100: "escape" cost
                kwcompanion.100: "companion" // TODO.100: this is gonna be bonkers.
                kwmutate.100: "mutate" cost
                kwencore.100: "encore" cost
                kwboast.100: "boast" cost
                kwforetell.100: "foretell" cost
                kwdemonstrate.100: "demonstrate"
                kwtimebound.100: "daybound" -> daybound | "nightbound" -> nightbound
                kwdisturb.100: "disturb" cost
                kwdecayed.100: "decayed"
                kwcleave.100: "cleave" cost // TODO.100: this will be hilarious fun for the AST builder.
                kwtraining.100: "training"
                kwcompleated.100: "compleated"
                kwreconfigure.100: "reconfigure" cost
                kwblitz.100: "blitz" cost
                kwcasualty.100: "casualty" valuenumber
                kwenlist.100: "enlist"
                kwreadahead.100: "read ahead"
                kwravenous.100: "ravenous"
                kwsquad.100: "squad" cost
                kwprototype.100: "prototype" cost
                kwlivingmetal.100: "living metal"
                kwformirrodin.100: "for mirrodin!"
                kwtoxic.100: "toxic" valuenumber
                kwbackup.100: "backup" valuenumber
                kwbargain.100: "bargain"
                kwcraft.100: "craft" WITH declarationorreference cost
                kwdisguise.100: "disguise" cost
                kwsolve.100: "to solve" DASH expressionstatement -> kwtosolve
                | "solved" DASH cost? expressionstatement -> kwsolved
                kwplot.100: "plot" cost
                kwsaddle.100: "saddle" valuenumber
                kwspree.100: "spree" // TODO.100: implement +cost on other lines... this one is weird
                kwfreerunning.100: "freerunning" cost
                kwgift.100: "gift" declarationorreference
                kwoffspring.100: "offspring" cost
                kwimpending.100: "impending" valuenumber cost

                //ABILITY COSTS

                cost.100: costsequence | dashcostexpression
                costsequence.100: (loyaltycost | tapuntapsymbol | manasymbolexpression | effectexpression) ("," (loyaltycost | tapuntapsymbol | manasymbolexpression | effectexpression))*
                // this has ptexpression to account for Prototype keyword ability, e.g..100: Prototype {3}{G} — 3/3
                dashcostexpression.100: DASH ( manasymbolexpression | effectexpression ) ("," (effectexpression))*
                | ( manasymbolexpression | effectexpression ) DASH ptexpression -> dashprototypeexpression

                ///VALUE EXPRESSIONS

                //[TODO.100: Need to account for custom values, variables, 'equals to' expressions, etc.]
                valueexpression.100: valueterm | equaltoexpression | numberofexpression | uptoexpression | thatmanyexpression 
                | ltexpression | lteqexpression | gtexpression | gteqexpression | timesexpression
                ltexpression.100: effectexpression? "less" RATHER (valueexpression | declarationorreference)
                lteqexpression.100: effectexpression? (valueexpression "or" ("less" | "fewer") | "less" RATHER "or" "equal" "to" valueexpression)
                gtexpression.100: effectexpression? "greater" RATHER (valueexpression | declarationorreference)
                | "more" RATHER valueexpression
                gteqexpression.100: effectexpression? (valueexpression "or" ("greater" | "more")  | "greater" RATHER "or" "equal" "to" valueexpression)
                | CARDINAL "or" "more" "times"-> gteqfrequencyexpression
                equaltoexpression.100: effectexpression? "equal" "to" (valueexpression | declarationorreference)
                uptoexpression.100: "up" "to" valueterm
                !thatmanyexpression.100: valuefrequency? "that" ("much"|"many")
                !numberofexpression.100: ("a"|"the"|"any") "number" "of" declarationorreference
                timesexpression.100: "times" statement? //[example.100: the number of times ~ was kicked]
                valueterm.100: valuenumber | valuecardinal | valueordinal | valuefrequency | valuecustom
                valuenumber.100: NUMBER
                valuecardinal.100: CARDINAL
                valueordinal.100: ORDINAL
                valuefrequency.100: FREQUENCY | CARDINAL "times"
                FREQUENCY.100: "once" | "twice"
                CARDINAL.100: "one" | "two" | "three" | "four" | "five" | "six" | "seven" | "eight" | "nine" | "ten" 
                | "eleven" | "twelve" | "thirteen" | "fourteen" | "fifteen" | "sixteen" | "seventeen" | "eighteen" | "nineteen" | "twenty" //[TODO]
                ORDINAL.100: "first" | "second" | "third" | "fourth" | "fifth" //[TODO]
                valuecustom.100: "x" | "*"
                quantityrulemodification.100: "rounded" "up" -> roundedupmod
                | "rounded" "down" -> roundeddownmod
                | "divided" "evenly" -> dividedevenlymod
                | "divided" AS YOU CHOOSE -> dividedfreelymod
                | "plus" valueterm -> plusmod
                | "minus" valueterm -> minusmod


                //DECLARATIONS AND REFERENCES

                declarationorreference.100: genericdeclarationexpression | reference | playerreference | objectreference | anytargetexpression
                genericdeclarationexpression.100: (playerdeclaration | objectdeclaration)
                | declarationorreference ("," declarationorreference ",")* "or" declarationorreference -> orgenericdeclarationexpression
                | declarationorreference ("," declarationorreference ",")* "and" declarationorreference -> andgenericdeclarationexpression
                | declarationorreference ("," declarationorreference ",")* "and/or" declarationorreference -> andorgenericdeclarationexpression

                genericdescriptionexpression.100: objectdescriptionexpression | playerdescriptionexpression

                playerdeclref.100: playerdeclaration | playerreference
                playerdeclaration.100: declarationdecorator* playerdefinition
                playerreference.100: referencedecorator+ playerdefinition
                playerdefinition.100: playerdescriptionexpression
                playerdescriptionexpression.100: playerdescriptionterm (","? playerdescriptionterm)*
                playerdescriptionterm.100: valueordinal | modifier | playerterm | withexpression | withoutexpression | whoexpression
                playerterm.100: PLAYERTERM
                whoexpression.100: "who" statement

                objectdeclref.100: objectdeclaration | objectreference
                objectdeclaration.100: declarationdecorator* objectdefinition
                objectreference.100: referencedecorator+ objectdefinition
                objectdefinition.100: objectdescriptionexpression
                | objectdescriptionexpression ("," objectdescriptionexpression ",")* "or" objectdescriptionexpression -> orobjectdescriptionexpression
                | objectdescriptionexpression ("," objectdescriptionexpression ",")* "and" objectdescriptionexpression -> andobjectdescriptionexpression
                | objectdescriptionexpression ("," objectdescriptionexpression ",")* "and/or" objectdescriptionexpression -> andorobjectdescriptionexpression

                ///[TODO.100: Rewriting objectdescriptionexpression to respect a canonical order because it makes parsing so much faster.]
                //objectdescriptionexpression.100: objectdescriptionterm (","? objectdescriptionterm)*
                objectdescriptionexpression.100: objectpreterm* objectpostterm*
                objectpreterm.100:  colorexpression | namedexpression | manasymbolexpression | typeexpression | ptexpression | valueexpression
                | qualifier | modifier | locationexpression | valuecardinal | additionalexpression | characteristicexpression
                objectpostterm.100: withexpression | withoutexpression | choiceexpression | ofexpression | characteristicexpression | atrandomexpression
                | "that"? dealtdamageexpression | "that" doesnthaveexpression | controlpostfix | ownpostfix | putinzonepostfix | castpostfix | "that" ispostfix | targetspostfix
                | "that" sharepostfix

                //[TODO.100: Mana type declarations. Mana is now a first-class citizen!]
                manadeclref.100: manadeclaration | manareference
                manadeclaration.100: declarationdecorator* manadefinition
                manareference.100: referencedecorator+ manadefinition
                manadefinition.100: manadescriptionexpression
                | manadescriptionexpression ("," manadescriptionexpression ",")* "or" manadescriptionexpression -> ormanadescriptionexpression
                | manadescriptionexpression ("," manadescriptionexpression ",")* "and" manadescriptionexpression -> andmanadescriptionexpression
                | manadescriptionexpression ("," manadescriptionexpression ",")* "and/or" manadescriptionexpression -> andormanadescriptionexpression
                manadescriptionexpression.100: puremanaexpression | textmanaexpression
                puremanaexpression.100: manasymbolexpression
                textmanaexpression.100: valuecardinal "mana" anycolorexpression // E.G. "add one mana of any one color
                productionexpression.100: "produced" "by" declarationorreference -> producedbyexpression
                | "that" declarationorreference COULD "produce" -> couldproduceexpression
                anycolorexpression.100: "of" "any" "color"
                | "of" "any" "one" "color" -> anyonecolorexpression



                declarationdecorator.100: EACH -> eachdecorator
                | "same" -> samedecorator
                | "all" -> alldecorator
                | ["an"]"other" -> otherdecorator
                | "a"["n"] -> indefinitearticledecorator
                | "the" -> definitearticledecorator
                | valueexpression? "target" -> targetdecorator
                | "any" -> anydecorator
                anytargetexpression.100: "any" "target" //Special nullary variant

                reference.100: neutralreference | selfreference | namereference
                neutralreference.100: "it" | "them"
                selfreference.100: "itself" | "himself" | "herself" -> selfreference
                namereference.100: NAMEREFSYMBOL

                referencedecorator.100: ("that" | "those") -> thatreference
                | ("this"|"these") -> thisreference
                | possessiveterm -> possessivereference
                !possessiveterm.100: "its" | "your" | "their" | namereference ("'s"|"'") | objectdeclref ("'s"|"'") 
                | playerdeclref ("'s"|"'") | typeexpression ("'s"|"'") | genericdeclarationexpression ("'s"|"'")

                ptexpression.100: valueexpression "/" valueexpression
                namedexpression.100: "named" (namereference | objectname)
                !locationexpression.100: ("into" | "onto" | "in" | "on" | "from" | "on top of" | "on bottom of")? zonedeclarationexpression
                withexpression.100: WITH (reference | abilitysequencestatement | characteristicexpression | (valueexpression | "a"["n"])? countertype "counter"["s"] "on" reference)
                withoutexpression.100: WITHOUT (reference | abilitysequencestatement | characteristicexpression | (valueexpression | "a"["n"])? countertype "counter"["s"] "on" reference)
                doesnthaveexpression.100: DOES NOT HAVE declarationorreference //[Basically equivalent to 'without']
                dealtdamageexpression.100: "dealt" DAMAGETYPE ("this" "way")? ("by" declarationorreference)? timeexpression?
                choiceexpression.100: "of" possessiveterm "choice"
                ofexpression.100: "of" declarationorreference
                additionalexpression.100: "additional"
                controlpostfix.100: playerdeclref CONTROL["s"]
                | playerdeclref (DO NOT | DOES NOT) CONTROL["s"] -> negativecontrolpostfix
                ownpostfix.100: playerdeclref "own"["s"]
                | playerdeclref (DO NOT | DOES NOT) "own"["s"] -> negativeownpostfix
                castpostfix.100: playerdeclref "cast"
                putinzonepostfix.100: "put" locationexpression zoneplacementmodifier? ("this" "way")?
                targetspostfix.100: "that" "target"["s"] declarationorreference
                atrandomexpression.100: "at" "random" //[TODO.100: Need to find out where to put this.]
                ispostfix.100: isstatement
                sharepostfix.100: "share"["s"] declarationorreference

                //EFFECT EXPRESSIONS


                effectexpression.100: keywordactionexpression
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

                // dealsdamageexpression.100:  declarationorreference? ("deal"["s"]|"dealt") valueexpression? DAMAGETYPE ("to" declarationorreference)? (","? quantityrulemodification)* -> dealsdamagevarianta
                // | valueexpression DAMAGETYPE ("to" declarationorreference)?  (","? quantityrulemodification)* -> dealsdamagevariantaimplied //variant a, implied antecedent
                // | declarationorreference ("deal"["s"]|"dealt") DAMAGETYPE valueexpression ("to" declarationorreference)?  (","? quantityrulemodification)* -> dealsdamagevariantb
                // | declarationorreference ("deal"["s"]|"dealt") DAMAGETYPE ("to" declarationorreference)?  valueexpression  (","? quantityrulemodification)* -> dealsdamagevariantc
                dealsdamageexpression.100: declarationorreference? "deal"["s"] valueexpression? DAMAGETYPE ("to" declarationorreference)? (","? quantityrulemodification)* 
                | valueexpression DAMAGETYPE ("to" declarationorreference)?  (","? quantityrulemodification)*
                preventdamageexpression.100: "prevent" "the" "next" valueexpression DAMAGETYPE "that" "would" "be" "dealt" "to" declarationorreference timeexpression? -> preventdamagevarianta
                | "prevent" "the" "next" valueexpression DAMAGETYPE "that" declarationorreference "would" "deal" "to" declarationorreference timeexpression? -> preventdamagevariantb
                | "prevent" "all" DAMAGETYPE "that" "would" "be" "dealt" ("to" declarationorreference)? timeexpression? -> preventdamagevariantc
                | "prevent" "all" DAMAGETYPE "that" "would" "be" "dealt" "to" "or" "dealt" "by" (declarationorreference)? timeexpression? -> preventdamagevariantd
                | "prevent" "all" DAMAGETYPE "that"? (declarationorreference)? "would" "deal" timeexpression? -> preventdamagevariante
                | "prevent" valueexpression "of" "that" DAMAGETYPE -> preventdamagevariantd 
                | "prevent" "that" DAMAGETYPE -> preventdamagevariante
                | DAMAGETYPE IS "prevented" "this" "way" -> preventdamagevariantf //[TODO.100: There may be a more general is-statement for stuff like 'damage'.]

                returnexpression.100: playerdeclref? "return"["s"] declarationorreference atrandomexpression? ("from" zonedeclarationexpression)? "to" zonedeclarationexpression genericdeclarationexpression? zoneplacementmodifier?//[TODO]

                putinzoneexpression.100: playerdeclref? "put"["s"] (declarationorreference | cardexpression) (locationexpression | "back" | zoneplacementmodifier) (objectdefinition | playerdefinition | zoneplacementmodifier)?
                putcounterexpression.100: playerdeclref? "put"["s"] ("a"|valueexpression) countertype "counter"["s"] "on" declarationorreference
                removecounterexpression.100: playerdeclref? "remove"["s"] ("a"|valueexpression) countertype "counter"["s"] "from" declarationorreference
                spendmanaexpression.100: "spend" "mana" //[TODO.100: this is just a stub]
                paylifeexpression.100: playerdeclref? "pay"["s"] valueexpression? "life"
                addmanaexpression.100: playerdeclref? "add"["s"] manadeclref
                paymanaexpression.100: playerdeclref? "pay"["s"] manadeclref
                payexpression.100: playerdeclref? "pay"["s"] declarationorreference //[TODO.100: This might change. Added for 'rather than pay this spell's mana cost'.]
                gainlifeexpression.100: playerdeclref? "gain"["s"] (valueexpression? "life" | "life" valueexpression)
                | playerdeclref "gained" (valueexpression? "life" | "life" valueexpression) timeexpression?
                loselifeexpression.100: playerdeclref? "lose"["s"] (valueexpression? "life" | "life" valueexpression) 
                | playerdeclref "lost" (valueexpression? "life" | "life" valueexpression) timeexpression?
                getsptexpression.100: declarationorreference? "get"["s"] ptchangeexpression
                diesexpression.100: declarationorreference? "die"["s"] timeexpression?
                gainabilityexpression.100: declarationorreference? "gain"["s"]  abilitysequencestatement
                loseabilityexpression.100: declarationorreference? "lose"["s"] abilitysequencestatement
                lookexpression.100: playerdeclref? ("look"["s"]|"looked") "at" (declarationorreference | cardexpression)
                takeextraturnexpression.100: playerdeclref? "take"["s"] timeexpression
                flipcoinsexpression.100: playerdeclref? "flip"["s"] ("a" | valuecardinal) "coin"["s"]
                !winloseeventexpression.100: playerdeclref? ("lose"|"win")["s"] ("the" "flip" | "the" "game")?
                remainsexpression.100: declarationorreference? "remain"["s"] (modifier | locationexpression)
                assigndamageexpression.100: declarationorreference? "assign"["s"] DAMAGETYPE "to" declarationorreference -> damageredirectionexpression
                | declarationorreference? "assign"["s"] "no" DAMAGETYPE timeexpression -> nodamageassignedexpression
                | declarationorreference? "assign"["s"] DAMAGETYPE valueexpression -> alternatedamageassignmentexpression
                ableexpression.100: declarationorreference? "able" ("to" statement DO "so")?
                changezoneexpression.100: declarationorreference "enter"["s"] locationexpression? genericdeclarationexpression? zoneplacementmodifier? timeexpression? -> enterzoneexpression
                | declarationorreference "leaves" locationexpression -> leavezoneexpression
                skiptimeexpression.100: playerdeclref? "skip"["s"] timeexpression
                switchexpression.100: playerdeclref? "switch"["es"] declarationorreference
                targetsexpression.100: objectdeclref? "target"["s"] declarationorreference?
                shareexpression.100: declarationorreference "share"["s"] declarationorreference


                keywordactionexpression.100: basickeywordaction | specialkeywordaction
                basickeywordaction.100: activateexpression
                | attacksexpression
                | blocksexpression
                | attachexpression
                | castexpression
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
                | millexpression

                activateexpression.100: "activate" declarationorreference
                !attacksexpression.100: declarationorreference? ONLY? "attack"["s"] ONLY? (timeexpression? declarationorreference?| declarationorreference? timeexpression?) "alone"?
                | declarationorreference? "attacked" (timeexpression? declarationorreference?| declarationorreference? timeexpression?) "alone"? -> attackedexpression
                | declarationorreference? "attack"["s"] WITH declarationorreference -> attackswithexpression
                //| "be" "attacked" "by" declarationorreference? timeexpression? -> beattackedexpression
                !blocksexpression.100: declarationorreference? ONLY? "block"["s"] ONLY? (timeexpression? declarationorreference? | declarationorreference? timeexpression?) "alone"?
                | declarationorreference? "blocked" (timeexpression? declarationorreference? | declarationorreference? timeexpression?) "alone"? -> blockedexpression
                //| "be" "blocked" "by" declarationorreference? timeexpression? -> beattackedexpression

                attachexpression.100: "attach" declarationorreference "to" declarationorreference
                | "unattach" declarationorreference ("from" declarationorreference)? -> unattachexpression
                | playerdeclref "attaches" declarationorreference "to" declarationorreference -> playerattachesexpression

                castexpression.100: playerdeclref? "cast"["s"] declarationorreference (castmodifier ("and" castmodifier)?)* timeexpression?
                castmodifier.100: WITHOUT "paying" "its" "mana" "cost" -> castwithoutpaying //[TODO.100: We may be able to fold this into the pay-expression]
                | AS "though" beingstatement -> castasthough
                chooseexpression.100: playerdeclref? (CHOOSE["s"]|"chose") declarationorreference ("from" "it")? atrandomexpression? //[TODO]
                controlsexpression.100: playerdeclref? (CONTROL["s"] | "controlled") genericdeclarationexpression
                gaincontrolexpression.100: playerdeclref? ("gain"["s"] | "gained") CONTROL "of" declarationorreference

                uncastexpression.100: "counter" declarationorreference
                createexpression.100: playerdeclref? "create"["s"] declarationorreference
                destroyexpression.100: "destroy" declarationorreference
                drawexpression.100: playerdeclref? (DRAW["s"]|"drew") cardexpression //[("a" CARD | valueexpression CARD["s"] | "cards"["s"] valueexpression)]
                discardexpression.100: playerdeclref? ("discard"["s"] | "discarded") (declarationorreference | "a" CARD | valueexpression CARD["s"] | CARD["s"] valueexpression) "at random"?
                doubleexpression.100: "double" //[TODO]
                exchangeexpression.100: "exchange" characteristicexpression //[TODO]
                exileexpression.100: "exile" declarationorreference
                fightexpression.100: declarationorreference? "fight"["s"] declarationorreference?
                playexpression.100: playerdeclref? ("play"["s"] | "played") declarationorreference timeexpression?
                revealexpression.100: playerdeclref? ("reveal"["s"] | "revealed") (cardexpression | declarationorreference)
                sacrificeexpression.100: playerdeclref? ("sacrifice"["s"] | "sacrificed") declarationorreference
                searchexpression.100: playerdeclref? ("search"["es"] | "searched") zonedeclarationexpression? "for" declarationorreference
                // used to be mandatory to specify a zone for shuffling, now default deck shuffling doesn't specify it.
                shuffleexpression.100: playerdeclref? ("shuffle"["s"] | "shuffled") zonedeclarationexpression? 
                tapuntapexpression.100: "tap" declarationorreference? -> tapexpression
                | "untap" declarationorreference? -> untapexpression
                millexpression.100: "mill" valueexpression CARD["s"]

                specialkeywordaction.100: regenerateexpression
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
                | surveilexpression
                | conniveexpression
                | monstrosityexpression
                | adaptexpression
                | amassexpression
                | learnexpression
                | ventureexpression
                | convertexpression
                | incubateexpression
                | theringtemptsexpression
                | timetravelexpression
                | discoverexpression
                | cloakexpression
                | collectevidenceexpression
                | suspectexpression
                | forageexpression
                | manifestdreadexpression

                regenerateexpression.100: "regenerate" declarationorreference
                scryexpression.100: "scry" valueexpression
                fatesealexpression.100: "fateseal" valueexpression
                clashexpression.100: playerdeclref? "clash" WITH playerdeclref
                detainexpression.100: "detain" objectdeclref
                planeswalkexpression.100: playerdeclref "planeswalk"["s"] "to" SUBTYPEPLANAR
                setinmotionexpression.100: playerdeclref "set"["s"] declarationorreference "in" "motion"
                abandonexpression.100: playerterm? "abandon"["s"] declarationorreference //[Note.100: Has never been used]
                proliferateexpression.100: "proliferate"
                transformexpression.100: "transform" declarationorreference
                populateexpression.100: "populate"
                voteexpression.100: playerdeclref "vote"["s"] "for" (objectname "or" objectname | declarationorreference) //[TODO]
                bolsterexpression.100: "bolster" valueexpression
                manifestexpression.100: playerdeclref? "manifest"["s"] cardexpression
                supportexpression.100: "support" valueexpression
                investigateexpression.100: "investigate"
                meldexpression.100: "meld" "them" "into" objectname
                goadexpression.100: "goad" declarationorreference
                exertexpression.100: playerdeclref? "exert"["s"] declarationorreference
                exploreexpression.100: declarationorreference? "explores"
                //[This one below is a bit weird because it's not 'becomes turned face up', it's 'is turned face up'.]
                //[It's a passive construction, but it's not a modifier like face-up.]
                !turnfaceexpression.100: playerdeclref? "turn"["s"] declarationorreference "face" ("down" | "up")
                | "turned" "face" ("down" | "up") -> turnedfaceexpression
                cycleexpression.100: playerdeclref? ("cycle"["s"] | "cycled") declarationorreference? 

                levelupexpression.100: ("level" levelrangeexpression ptexpression ability*)
                levelrangeexpression.100: NUMBER "-" NUMBER | NUMBER "+"
                surveilexpression.100: "surveil" valueexpression
                conniveexpression.100: "connive" valueexpression
                monstrosityexpression.100: "monstrosity" valueexpression
                adaptexpression.100: "adapt" valueexpression
                amassexpression.100: "amass" typeterm? valueexpression
                learnexpression.100: "learn"
                ventureexpression.100: "venture into the dungeon"
                convertexpression.100: "convert" namereference
                incubateexpression.100: "incubate" valueexpression
                theringtemptsexpression.100: "the ring tempts you"
                timetravelexpression.100: "time travel" valuefrequency?
                discoverexpression.100: "discover" valueexpression
                # // TODO.100: not sure this works, e.g. "cloak the top card of your library"
                cloakexpression.100: "cloak" declarationorreference 
                collectevidenceexpression.100: "collect evidence" valueexpression
                suspectexpression.100: "suspect" reference
                forageexpression.100: "forage"
                manifestdreadexpression.100: "manifest dread"


                //TYPE/MANA/COLOR EXPRESSIONS, MODIFIERS, AND MISCELLANEOUS

                timeexpression.100: startendspecifier? timeterm ("of" timeexpression)? ("on" possessiveterm timemodifier* PHASE)?
                startendspecifier.100: "the"? "beginning" "of" -> timebeginmodifier
                | "the"? "end" "of" -> timeendmodifier
                timeterm.100: (referencedecorator* | declarationdecorator*) possessiveterm* timemodifier* (PHASE | STEP | TURN | GAME |  "one")
                timemodifier.100: "next" valuecardinal? -> nexttimemodifier
                | "additional" -> additionaltimemodifier
                | valuecardinal? "extra" -> extratimemodifier
                PHASE.100: "beginning phase" | ("precombat" | "postcombat")? "main phase" | ("combat" | "combat phase") | "ending phase"
                STEP.100: "untap step" | ("upkeep step" | "upkeep") | "draw step" | "beginning of combat" | "declare attackers step"
                | "declare blockers step" | "combat damage step" | "end of combat" | "end step" | "cleanup step" | "step"
                TURN.100: "turn"
                GAME.100: "game" 

                //[TODO.100: What about comma-delimited type expressions?]
                typeexpression.100: (typeterm)+ | typeterm ("," typeterm)+
                | typeterm ("," typeterm ",")* "or" typeterm -> ortypeexpression

                typeterm.100: (TYPE ["s"] | SUBTYPESPELL ["s"] | SUBTYPELAND ["s"] | SUBTYPEARTIFACT ["s"] | SUBTYPEENCHANTMENT ["s"] | SUBTYPEPLANESWALKER | SUBTYPECREATUREA ["s"] | SUBTYPECREATUREB ["s"] | SUBTYPEPLANAR | SUPERTYPE)
                | "non"["-"] typeterm -> nontypeterm

                TYPE.100: "planeswalker" | "conspiracy" | "creature" | "enchantment" | "instant"
                | "land" | "phenomenon" | "plane" | "artifact" | "scheme" | "sorcery"
                | "tribal" | "vanguard"

                SUBTYPESPELL.100: "arcane" | "trap"

                SUBTYPELAND.100: "desert" | "forest" | "gate" | "island" | "lair" | "locus"
                | "mine" | "mountain" | "plains" | "power-plant" | "swamp" | "tower" | "urza's"

                SUBTYPEARTIFACT.100: "clue" | "contraption" | "equipment" | "fortification" | "treasure" | "vehicle"

                SUBTYPEENCHANTMENT.100: "aura" | "cartouche" | "curse" | "saga" | "shrine" | "case"

                SUBTYPEPLANESWALKER.100: "ajani" | "aminatou" | "angrath" | "arlinn" | "ashiok" | "bolas" | "chandra"
                | "dack" | "daretti" | "domri" | "dovin" | "elspeth" | "estrid" | "freyalise" | "garruk" | "gideon"
                | "huatli" | "jace" | "jaya" | "karn" | "kaya" | "kiora" | "koth" | "liliana" | "nahiri" | "narset"
                | "nissa" | "nixilis" | "ral" | "rowan" | "saheeli" | "samut" | "sarkhan" | "sorin" | "tamiyo" | "teferi"
                | "tezzeret" | "tibalt" | "ugin" | "venser" | "vivien" | "vraska" | "will" | "windgrace" | "xenagos"
                | "yanggu" | "yanling"


                //[TODO.100: SUBTYPECREATUREA and SUBTYPECREATUREB are split up because having such a long list of alternatives apparently]
                //[causes Lark to suffer a recursion depth error. We should see if this is fixable.]

                SUBTYPECREATUREA.100: "advisor" | "aetherborn" | ("ally"|"allies") | "angel" | "antelope" | "ape" | "archer" | "archon" 
                | "artificer" | "assassin" | "assembly-worker" | "atog" | "aurochs" | "avatar" | "azra" | "badger"
                | "barbarian" | "basilisk" | "bat" | "bear" | "beast" | "beeble" | "berserker" | "bird" | "blinkmoth"
                | "boar" | "bringer" | "brushwagg" | "camarid" | "camel" | "caribou" | "carrier" | "cat" | "centaur"
                | "cephalid" | "chimera" | "citizen" | "cleric" | "cockatrice" | "construct" | "coward" | "crab"
                | "crocodile" | "cyclops" | "dauthi" | "demon" | "deserter" | "devil" | "dinosaur" | "djinn" | "dragon"
                | "drake" | "dreadnought" | "drone" | "druid" | "dryad" | ("dwarf"|"dwarves") | "efreet" | "egg" | "elder" | "eldrazi"
                | "elemental" | "elephant" | ("elf"|"elves") | "elk" | "eye" | "faerie" | "ferret" | "fish" | "flagbearer" | "fox"

                SUBTYPECREATUREB.100: "frog" | "fungus" | "gargoyle" | "germ" | "giant" | "gnome" | "goat" | "goblin" | "god" | "golem" | "gorgon"
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

                SUBTYPEPLANAR.100: "alara" | "arkhos" | "azgol" | "belenon" | "bolas’s meditation realm"
                | "dominaria" | "equilor" | "ergamon" | "fabacin" | "innistrad" | "iquatana" | "ir" 
                | "kaldheim" | "kamigawa" | "karsus" | "kephalai" | "kinshala" | "kolbahan" | "kyneth"
                | "lorwyn" | "luvion" | "mercadia" | "mirrodin" | "moag" | "mongseng" | "muraganda"
                | "new phyrexia" | "phyrexia" | "pyrulea" | "rabiah" | "rath" | "ravnica" | "regatha"
                | "segovia" | "serra’s realm" | "shadowmoor" | "shandalar" | "ulgrotha" | "valla"
                | "vryn" | "wildfire" | "xerex" | "zendikar"

                subtype.100: SUBTYPESPELL | SUBTYPELAND | SUBTYPEARTIFACT | SUBTYPEENCHANTMENT | SUBTYPEPLANESWALKER | SUBTYPECREATUREA | SUBTYPECREATUREB | SUBTYPEPLANAR

                SUPERTYPE.100: "basic" | "legendary" | "ongoing" | "snow" | "world"

                DAMAGETYPE.100: "damage" | "combat damage" | "noncombat damage"

                modifier.100: ABILITYMODIFIER | COMBATSTATUSMODIFIER | KEYWORDSTATUSMODIFIER | TAPPEDSTATUSMODIFIER | EFFECTSTATUSMODIFIER
                | controlmodifier | attachmentmodifier

                ABILITYMODIFIER.100: "triggered" | "activated" | "mana" | "loyalty"
                COMBATSTATUSMODIFIER.100: "attacking" | "defending" | "attacked" | "blocking" | "blocked" | "active"
                KEYWORDSTATUSMODIFIER.100: "paired" | "kicked" | "face-up" | "face-down" | "transformed" | "enchanted" | "equipped"
                | "fortified" | "monstrous" | "regenerated" | "suspended" | "flipped" | "suspected" // TODO.100: ensure 'suspected' works properly
                TAPPEDSTATUSMODIFIER.100: "tapped" | "untapped"
                EFFECTSTATUSMODIFIER.100: "named" | "chosen" | "chosen at random" | "revealed" | "returned" | "destroyed" | "exiled" | "died" | "countered" | "sacrificed"
                | "the target of a spell or ability" | "prevented" | "created"
                controlmodifier.100: "under" referencedecorator+ CONTROL
                attachmentmodifier.100: "attached" (ONLY? "to" declarationorreference)? -> attachedmodifier
                | "unattached" ("from" declarationorreference)? -> unattachedmodifier

                qualifier.100: QUALIFIER["s"]
                | "non" QUALIFIER -> nonqualifier
                QUALIFIER.100: ("ability"|"abilities") | CARD | "permanent" | "source" | "spell" | "token" | "effect"

                characteristicexpression.100: characteristicterms 
                | (characteristicterms (valueexpression|ptexpression) | (valueexpression|ptexpression) characteristicterms) -> characteristicvaluecompexpr

                characteristicterms.100: characteristicterm
                | possessiveterm+ characteristicterm -> characteristicpossessiveexpr
                | "the" characteristicterm -> characteristicthereference
                | characteristicterm  ("," characteristicterm ",")* "or" characteristicterm -> characteristicorexpr
                | characteristicterm  ("," characteristicterm ",")* "and" characteristicterm -> characteristicandexpr
                | characteristicterm  ("," characteristicterm ",")* "and/or" characteristicterm -> characteristicandorexpr
                | "no" characteristicterm -> nocharacteristicexpr //[example.100: no maximum hand size]

                characteristicterm.100: modifier* characteristic
                characteristic.100: OBJECTCHARACTERISTIC | PLAYERCHARACTERISTIC
                PLAYERCHARACTERISTIC.100: "maximum hand size" | "life total"["s"] | "life" | "cards in hand"
                # OBJECTCHARACTERISTIC.100: CARD? "name" | "mana cost" | "converted mana cost" | "color"["s"] | "color indicator" | "type"["s"] | "card type"["s"] | "subtype"["s"] | "supertype"["s"]
                # | "rules text" | "abilities" | "power" | "toughness" | "base power" | "base toughness" | "loyalty" | "hand modifier" | "life modifier"
                OBJECTCHARACTERISTIC.100: CARD? "name" | "mana value" | "color"["s"] | "color indicator" | "type"["s"] | "card type"["s"] | "subtype"["s"] | "supertype"["s"]
                | "rules text" | "abilities" | "power" | "toughness" | "base power" | "base toughness" | "loyalty" | "hand modifier" | "life modifier"

                //[TODO.100: Not quite done, there are expressions like 'a number of cards equal to [...]'. There's some overlapping responsibilities with descriptions involving cards, maybe.]
                !cardexpression.100: ("the" "top" | "the" "bottom")? (valueterm | thatmanyexpression | "a")? CARD["s"] ("from" "the" "top" | "from" "the" "bottom")? ("of" zonedeclarationexpression)?  

                zonedeclarationexpression.100: (declarationdecorator* | referencedecorator*) zone
                zoneplacementmodifier.100: "in" "any" "order" -> anyorderplacement
                | "in" "a" "random" "order" -> randomorderplacement
                | ORDINAL "from" "the" "top" -> fromtopplacement
                | ORDINAL "from" "the" "bottom" -> frombottomplacement
                zone.100: ZONE
                ZONE.100: "the battlefield" | "graveyard"["s"] | ("library"|"libraries") | "hand"["s"] | "stack" | "exile" | "command zone" | "outside the game" | "anywhere"

                colorexpression.100: colorterm -> colorsingleexpr
                | colorterm  ("," colorterm ",")* "or" colorterm -> colororexpr
                | colorterm ("," colorterm ",")* "and" colorterm -> colorandexpr
                | colorterm ("," colorterm ",")* "and/or" colorterm -> colorandorexpr

                colorterm.100: COLORTERM
                | "non" COLORTERM -> noncolorterm

                COLORTERM.100: "white" | "blue" | "black" | "red" | "green" | "monocolored" | "multicolored" | "colorless"

                objectname.0: "objectname" //OBJECTNAME //[TODO.100: No demarcations around names is difficult also. Need preprocessor help here.]
                //OBJECTNAME.0: NAMEWORD ((WS | ",") NAMEWORD)* //[TODO.100: commas in names? This is problematic. Need preprocessor help here.]
                //NAMEWORD.100: UCASE_LETTER (LCASE_LETTER)*
                //NAMEWORD.0: (UCASE_LETTER | LCASE_LETTER)+

                countertype.100: ptchangeexpression //| WORD

                loyaltycost.100: "[" (PLUS | PWMINUS)? valueterm "]"
                //[NOTE.100: Both Scryfall and Mtgjson use a long dash, not a short dash, to indicate a minus on a planeswalker ability]
                PWMINUS.100: "−"
                ptchangeexpression.100: (PLUS | MINUS) valueterm "/" (PLUS | MINUS) valueterm
                PLUS.100: "+"
                MINUS.100: "-"

                manaspecificationexpression.100: valueterm "mana" manaspecifier+
                manaspecifier.100: anycolorexpression //[TODO.100: Need to add the rest of these]

                manasymbolexpression.100: manasymbol+
                | manasymbolexpression "or" manasymbolexpression -> ormanaexpression
                manasymbol.100: "{" manamarkerseq "}"
                manamarkerseq.100: manamarker_color -> regularmanasymbol
                | manamarker_halfmana manamarker_color -> halfmanasymbol
                | manamarker_color "/" manamarker_phyrexian -> phyrexianmanasymbol
                | manamarker_color "/" manamarker_color -> hybridmanasymbol
                | "2" "/" manamarker_color -> alternate2manasymbol
                | manamarker_snow -> snowmanasymbol
                | manamarker_colorless -> colorlessmanasymbol
                | manamarker_x -> xmanasymbol
                | NUMBER -> genericmanasymbol

                manamarker_halfmana.100: "H"i -> halfmarker
                manamarker_color.100: "W"i -> whitemarker
                | "U"i -> bluemarker
                | "B"i -> blackmarker
                | "R"i -> redmarker
                | "G"i -> greenmarker
                manamarker_snow.100: "S"i -> snowmarker
                manamarker_phyrexian.100: "P"i -> phyrexianmarker
                manamarker_colorless.100: "C"i -> colorlessmarker
                manamarker_x.100: "X"i -> xmarker

                DASH.100: "—"
                MODALCHOICE.100: "•"

                NAMEREFSYMBOL.100: "~" | "~f"
                PLAYERTERM.100: "player"["s"] | "opponent"["s"] | YOU |  "teammate"["s"] | "team"["s"] | "they" | "controller"["s"] | "owner"["s"]

                tapuntapsymbol.100: TAPSYMBOL | UNTAPSYMBOL
                TAPSYMBOL.100: "{T}"i
                UNTAPSYMBOL.100: "{Q}"i
                
                IF.100: "if"
                THEN.100: "then"
                MAY.100: "may"
                HAVE.100: "have"
                IS.100: "is"
                WAS.100: "was"
                ARE.100: "are"
                EACH.100: "each"
                WHILE.100: "while"
                AFTER.100: "after"
                UNLESS.100: "unless"
                CAN.100: "can"
                INSTEAD.100: "instead"
                CHOOSE.100: "choose"
                NOT.100: "not"
                DO.100: "do"
                DOES.100: "does"
                UNTIL.100: "until"
                OTHERWISE.100: "otherwise"
                AS.100: "as"
                DURING.100: "during"
                WITH.100: "with"
                WITHOUT.100: "without"
                COULD.100: "could"
                ONLY.100: "only"
                RATHER.100: "rather"
                THAN.100: "than"
                BEFORE.100: "before"
                DRAW.100: "draw"
                CARD.100: "card"
                YOU.100: "you"
                CONTROL.100: "control"
                

                //%import common.UCASE_LETTER -> UCASE_LETTER
                //%import common.LCASE_LETTER -> LCASE_LETTER
                //%import common.WORD -> WORD
                %import common.SIGNED_NUMBER -> NUMBER
                %import common.WS -> WS
                %ignore WS
                """


if __name__ == '__main__':
    unittest.main()
