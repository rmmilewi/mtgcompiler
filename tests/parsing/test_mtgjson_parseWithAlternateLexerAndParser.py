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
                                                            "parser.larkLexer" : "basic",
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

        revisedStatementGrammar = """
        
        statementblock : (statement)+ | activationstatement
        
        statement: statementwithouttrailingsubstatements "." | standaloneconditionalstatement "." | compoundstatement "." | modalstatement

        statementwithouttrailingsubstatements: statementexpression
        
        //Period ambiguity resolved: Periods should always occur after each statementwithouttrailingsubstatement, standaloneconditionalstatement, or compoundstatement.
        //Radically simplified the conditional statement logic. Rather than having a separate rule for every conditional term, we have one generic rule for all of them. Note that this means we will have to check the semantics of conditionals at AST construction time to build the AST properly.
        // IS-A and HAS-A relations ("~ IS blue", "~ HAS haste", "creatures you control BECOME dragons in addition to their other types" etc.) previously were classed as statements. They're now considered expressions since they essentially set or compute a value. This simplifies the grammar since it's now easier to determine where a statement should be produced vs. an expression.
        //conditionalstatement with conditionalresult can't exist within a compoundstatement without causing an ambiguity. Fixed by adding compoundconditionalstatement and standaloneconditionalstatement rules.
        //There's an ambiguity with activationstatement: it's unclear whether consecutive sentences in the RHS belong to the activation statement or the surrounding block. Fixed by changing it so an activation statement always takes up the entire block.
        
        
        activationstatement: statementexpression ("," statementexpression)* ":" statementblock 
        modalstatement: "choose" statementexpression DASH (modalchoicestatement)+
        modalchoicestatement: MODALCHOICE statementblock
        
        compoundstatement: (statementwithouttrailingsubstatements | compoundconditionalstatement) ("," (statementwithouttrailingsubstatements | compoundconditionalstatement))* ","? "then" (statementwithouttrailingsubstatements | standaloneconditionalstatement) -> compoundthenstatement
        | (statementwithouttrailingsubstatements | compoundconditionalstatement) ("," (statementwithouttrailingsubstatements | compoundconditionalstatement))* ","? "and" (statementwithouttrailingsubstatements | standaloneconditionalstatement) -> compoundandstatement
        | (statementwithouttrailingsubstatements | compoundconditionalstatement) ("," (statementwithouttrailingsubstatements | compoundconditionalstatement))* ","? "or" (statementwithouttrailingsubstatements | standaloneconditionalstatement) -> compoundorstatement
        
        compoundconditionalstatement: condition statementexpression 
        | statementexpression condition -> compoundconditionalinv
        | conditionalresult postfixexpression -> compoundconditionalresult
        
        standaloneconditionalstatement: "then"? condition statementexpression postfixexpression? "," "then"? (conditionalresult postfixexpression? | standaloneconditionalstatement)
        conditionalresult: statementwithouttrailingsubstatements
        postfixexpression: "instead" | "rather" "than" statementwithouttrailingsubstatements | condition statementexpression | postfixexpression ("and" | "or" | "and/or") postfixexpression

        condition: "only"? "if" -> ifcondition
        | "whenever" -> whenevercondition
        | "when" -> whencondition
        | "as" -> ascondition
        | "as" "long" "as" -> aslongascondition
        | "until" -> untilcondition
        | "after" -> aftercondition
        | "otherwise" -> otherwisecondition
        | "unless" -> unlesscondition
        | "while" -> whilecondition
        | ("during" | "only during") -> duringcondition
        | "except" -> exceptcondition
        | "the" "next" "time" -> thennexttimecondition
        | "before" -> beforecondition
        | "for" "each" "time"? -> beforecondition
        | "at" -> atcondition
        | "as" "an" "additional" "cost" "to"? -> asanadditionalcostcondition
        
        statementexpression: expression
        expression: "TEXT" | beingexpression postfixexpression?
        
        
        //compoundexpression: beingexpression postfixexpression?
        //| statementexpression ("," statementexpression)* ","? "and" statementexpression -> compoundandstatement
        //| statementexpression ("," statementexpression)* ","? "or" statementexpression -> compoundorstatement
        
        beingexpression: statementexpression ("is" | "was" | "are" "each"?) ("still"|"not")? statementexpression -> isexpression
        | statementexpression ("has"|"have"|"had") statementexpression -> hasexpression
        | statementexpression "can" "not"? statementexpression -> canexpression
        | statementexpression "become"["s"] statementexpression -> becomesexpression
        | statementexpression "may" statementexpression -> mayexpression
        | statementexpression "would" statementexpression -> wouldexpression
        | statementexpression (statementexpression? ("do"["es"]? | "did") "not"? statementexpression? | "doing" "so" ) -> doesexpression
        
        DASH: "—"
        MODALCHOICE: "•"
        
        %import common.WS -> WS
        %ignore WS
        """

        compilerUsingPartialGrammar = MtgJsonCompiler.MtgJsonCompiler(
            options={"parser.overrideGrammar": revisedStatementGrammar,
                     "parser.startRule": "statementblock",
                     "parser.ambiguity": "explicit",
                     "parser.larkLexer": "basic",
                     })
        parser = compilerUsingPartialGrammar.getParser()

        statementBlocksToTest = [
            "TEXT.",
            "if TEXT, TEXT.",
            "if TEXT, TEXT instead.",
            "whenever TEXT, TEXT until TEXT.",
            "TEXT : TEXT.",
            "TEXT: TEXT. TEXT. TEXT.",
            "TEXT: TEXT is TEXT until TEXT. TEXT. TEXT. TEXT.",
            "TEXT, TEXT, and TEXT. TEXT.",
            "if TEXT, TEXT except TEXT.",
            "whenever TEXT, TEXT may TEXT. TEXT may TEXT.",
            "whenever TEXT, TEXT if TEXT. if TEXT is TEXT, TEXT. if TEXT is TEXT, TEXT.",
            "at TEXT, TEXT.",
            "whenever TEXT, TEXT unless TEXT.",
            "TEXT. TEXT and TEXT.",
            "TEXT or TEXT.",
            "TEXT. if TEXT is TEXT, TEXT can not TEXT, and if TEXT would TEXT, TEXT instead.", #Carbonize
            "if TEXT would TEXT, TEXT instead.",  # Carbonize Subset
            "choose TEXT — • TEXT.\n• TEXT.", #Abrade
            "when TEXT, TEXT if TEXT.", #Dream Thief
            "if TEXT except TEXT, TEXT. if TEXT, TEXT. if TEXT does not TEXT, TEXT.", #Chains of Mephistopheles
            "TEXT. at TEXT, if TEXT, TEXT. if TEXT, TEXT and TEXT.", #All Hallows' Eve
            "when TEXT, TEXT. then if TEXT, TEXT until TEXT. TEXT may TEXT rather than TEXT.", #Amped Raptor
            "TEXT, TEXT, TEXT: TEXT, TEXT, then TEXT.", #Angel's Herald
            "TEXT can not TEXT, and TEXT can not TEXT. at TEXT, if TEXT, TEXT.", #Arachnus Web
            "TEXT and TEXT. TEXT until TEXT. TEXT if TEXT. while TEXT, TEXT can TEXT only if TEXT are TEXT and only if TEXT is TEXT. if TEXT is TEXT as TEXT, TEXT while TEXT.", #Word of Command
        ]

        shouldOutputVerboseDetails = True

        print("\n-----------------------")
        for statementBlock in statementBlocksToTest:
            try:
                fullParseTimeStart = time.time()
                parseTree = parser.parse(statementBlock)
                fullParseTimeEnd = time.time()
                ambiguities = list(parseTree.find_data("_ambig"))
                statementBlockPrettyPrint = statementBlock.replace('\n', ' ')
                print(f"Statement(s) ({statementBlockPrettyPrint}) took {fullParseTimeEnd-fullParseTimeStart} to parse. The input had {len(ambiguities)} ambiguities.")
                if shouldOutputVerboseDetails and len(ambiguities) > 0:
                    print(parseTree.pretty())
            except Exception as exception:
                firstLineOfException = str(exception).split('\n')[0]
                if shouldOutputVerboseDetails:
                    print(f"Statement(s) ({statementBlock}) produced an exception during parsing: {exception}...")
                else:
                    print(f"Statement(s) ({statementBlock}) produced an exception during parsing: {firstLineOfException}...")
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


if __name__ == '__main__':
    unittest.main()
