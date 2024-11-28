import unittest
import time,os
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


    def test_improveStatementLevelOfGrammar(self):
        """
        //Period ambiguity resolved: Periods should always occur after each statementwithouttrailingsubstatement, standaloneconditionalstatement, or compoundstatement.
        //Radically simplified the conditional statement logic. Rather than having a separate rule for every conditional term, we have one generic rule for all of them. Note that this means we will have to check the semantics of conditionals at AST construction time to build the AST properly.
        // IS-A and HAS-A relations ("~ IS blue", "~ HAS haste", "creatures you control BECOME dragons in addition to their other types" etc.) previously were classed as statements. They're now considered expressions since they essentially set or compute a value. This simplifies the grammar since it's now easier to determine where a statement should be produced vs. an expression.
        //conditionalstatement with conditionalresult can't exist within a compoundstatement without causing an ambiguity. Fixed by adding compoundconditionalstatement and standaloneconditionalstatement rules.
        //There was an ambiguity with activationstatement: it's unclear whether consecutive sentences in the RHS belong to the activation statement or the surrounding block. Fixed by changing it so an activation statement always takes up the entire block.
        """

        revisedStatementGrammar = """
        cardtext: ability (NEWLINE+ ability)*

        ability: (abilityworddecorator | remindertextdecorator)? statementblock remindertextdecorator? -> regularability
        //| keywordlist remindertextdecorator?
        abilityworddecorator: WORD+ DASH
        remindertextdecorator: /\(.*?\)/
        
        statementblock : (statement)+ | activationstatement
        
        statement: statementwithouttrailingsubstatements "." | standaloneconditionalstatement "." | compoundstatement "." | modalstatement

        statementwithouttrailingsubstatements: statementexpression
        
        activationstatement: statementexpression ("," statementexpression)* ":" statementblock 
        modalstatement:  "choose" statementexpression DASH modalchoicestatement (NEWLINE modalchoicestatement)+
        modalchoicestatement: MODALCHOICE abilityworddecorator? statementblock remindertextdecorator?
        
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
        %import common.NEWLINE -> NEWLINE
        %import common.WORD -> WORD
        %ignore WS
        """

        compilerUsingPartialGrammar = MtgJsonCompiler.MtgJsonCompiler(
            options={"parser.overrideGrammar": revisedStatementGrammar,
                     "parser.startRule": "cardtext",
                     "parser.ambiguity": "explicit",
                     "parser.larkLexer": "basic",
                     })
        parser = compilerUsingPartialGrammar.getParser()

        statementBlocksToTest = [
            "TEXT.",
            "if TEXT, TEXT.",
            "if TEXT, TEXT. (Reminder Text Here.)",
            "choose TEXT — • Foil Their Scheme — TEXT.\n• Learn Their Secrets — TEXT then TEXT.",
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
            "TEXT and TEXT. TEXT. TEXT if TEXT. while TEXT, TEXT can TEXT only if TEXT are TEXT and only if TEXT is TEXT. if TEXT is TEXT as TEXT, TEXT while TEXT.", #Word of Command
            "TEXT: TEXT.\n TEXT: TEXT."
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

    def test_improveDeclarationLevelOfGrammar(self):
        revisedDeclarationGrammar = """
        abilitysequencestatement: "ABILITYSEQUENCESTATEMENT"
        beingexpression: "BEINGEXPRESSION"
        effectexpression: "EFFECTEXPRESSION"
        statement: "STATEMENT"
        
        //
        
        //DECLARATIONS AND REFERENCES
        declarationorreference: genericdeclarationexpression | reference | playerreference | objectreference | anytargetexpression
        genericdeclarationexpression: (playerdeclaration | objectdeclaration)
        | declarationorreference ("," declarationorreference ",")* "or" declarationorreference -> orgenericdeclarationexpression
        | declarationorreference ("," declarationorreference ",")* "and" declarationorreference -> andgenericdeclarationexpression
        | declarationorreference ("," declarationorreference ",")* "and/or" declarationorreference -> andorgenericdeclarationexpression
        
        genericdescriptionexpression: objectdescriptionexpression | playerdescriptionexpression
        
        playerdeclref: playerdeclaration | playerreference
        playerdeclaration: declarationdecorator* playerdefinition
        playerreference: referencedecorator+ playerdefinition
        playerdefinition: playerdescriptionexpression
        playerdescriptionexpression : playerdescriptionterm (","? playerdescriptionterm)*
        playerdescriptionterm: valueordinal | modifier | playerterm | withexpression | withoutexpression //| whoexpression
        playerterm: PLAYERTERM
        //whoexpression: "who" statementexpression
        
        objectdeclref: objectdeclaration | objectreference
        objectdeclaration: declarationdecorator* objectdefinition
        objectreference: referencedecorator+ objectdefinition
        objectdefinition: objectdescriptionexpression
        | objectdescriptionexpression ("," objectdescriptionexpression ",")* "or" objectdescriptionexpression -> orobjectdescriptionexpression
        | objectdescriptionexpression ("," objectdescriptionexpression ",")* "and" objectdescriptionexpression -> andobjectdescriptionexpression
        | objectdescriptionexpression ("," objectdescriptionexpression ",")* "and/or" objectdescriptionexpression -> andorobjectdescriptionexpression
        
        ///[TODO: Rewriting objectdescriptionexpression to respect a canonical order because it makes parsing so much faster.]
        //objectdescriptionexpression: objectdescriptionterm (","? objectdescriptionterm)*
        objectdescriptionexpression: objectpreterm+ objectpostterm*
        objectpreterm:  colorexpression  | manasymbolexpression | typeexpression | ptexpression | valueexpression
        | qualifier | modifier | locationexpression | valuecardinal | additionalexpression | characteristicexpression
        objectpostterm: withexpression | withoutexpression | choiceexpression | ofexpression | characteristicexpression | atrandomexpression
        | "that"? dealtdamageexpression | "that" doesnthaveexpression | controlpostfix | ownpostfix | putinzonepostfix | castpostfix | targetspostfix
        | "that" sharepostfix | namedexpression | "that" beingexpression 
        
        //[TODO: Mana type declarations. Mana is now a first-class citizen!]
        manadeclref: manadeclaration | manareference
        manadeclaration: declarationdecorator* manadefinition
        manareference: referencedecorator+ manadefinition
        manadefinition: manadescriptionexpression
        | manadescriptionexpression ("," manadescriptionexpression ",")* "or" manadescriptionexpression -> ormanadescriptionexpression
        | manadescriptionexpression ("," manadescriptionexpression ",")* "and" manadescriptionexpression -> andmanadescriptionexpression
        | manadescriptionexpression ("," manadescriptionexpression ",")* "and/or" manadescriptionexpression -> andormanadescriptionexpression
        manadescriptionexpression: puremanaexpression | textmanaexpression
        puremanaexpression: manasymbolexpression
        // E.G. "add one mana of any one color" or "add six {g}"
        textmanaexpression: valuecardinal (("mana" anycolorexpression) | manasymbolexpression )
        productionexpression: "produced" "by" declarationorreference -> producedbyexpression
        | "that" declarationorreference "could" "produce" -> couldproduceexpression
        anycolorexpression: "of" "any" "color"
        | "of" "any" "one" "color" -> anyonecolorexpression
        
        
        
        declarationdecorator: "each" -> eachdecorator
        | "same" -> samedecorator
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
        !possessiveterm: "its" | "your" | "their" | namereference ("'s"|"'") | objectdeclref ("'s"|"'")
        | playerdeclref ("'s"|"'") | typeexpression ("'s"|"'") | genericdeclarationexpression ("'s"|"'")
        
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
        //ispostfix: isstatement
        sharepostfix: "share"["s"] declarationorreference
                
                
                
        //TYPE/MANA/COLOR EXPRESSIONS, MODIFIERS, AND MISCELLANEOUS
        timeexpression: startendspecifier? timeterm ("of" timeexpression)? ("on" possessiveterm timemodifier* PHASE)?
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
        
        SUBTYPESPELL : "arcane" | "trap" | "adventure"
        
        SUBTYPELAND: "desert" | "forest" | "gate" | "island" | "lair" | "locus"
        | "mine" | "mountain" | "plains" | "power-plant" | "swamp" | "tower" | "urza's"
        
        SUBTYPEARTIFACT: "clue" | "contraption" | "equipment" | "fortification" | "treasure" | "vehicle" | "food"
        
        SUBTYPEENCHANTMENT: "aura" | "cartouche" | "curse" | "saga" | "shrine" | "rune" | "shard" | "case"
        
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
        | "zombie" | "zubera" | "mouse"
        
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
        | "fortified" | "monstrous" | "regenerated" | "suspended" | "flipped" | "suspected" // TODO: ensure 'suspected' works properly
        TAPPEDSTATUSMODIFIER: "tapped" | "untapped"
        EFFECTSTATUSMODIFIER: "named" | "chosen" | "chosen at random" | "revealed" | "returned" | "destroyed" | "exiled" | "died" | "countered" | "sacrificed"
        | "the target of a spell or ability" | "prevented" | "created"
        controlmodifier: "under" referencedecorator+ "control"
        attachmentmodifier: "attached" ("only"? "to" declarationorreference)? -> attachedmodifier
        | "unattached" ("from" declarationorreference)? -> unattachedmodifier
        
        qualifier: QUALIFIER["s"]
        | "non" QUALIFIER -> nonqualifier
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
        PLAYERCHARACTERISTIC: "maximum hand size" | "life total"["s"] | "life" | "cards in hand"
        # OBJECTCHARACTERISTIC: "card"? "name" | "mana cost" | "converted mana cost" | "color"["s"] | "color indicator" | "type"["s"] | "card type"["s"] | "subtype"["s"] | "supertype"["s"]
        # | "rules text" | "abilities" | "power" | "toughness" | "base power" | "base toughness" | "loyalty" | "hand modifier" | "life modifier"
        OBJECTCHARACTERISTIC: "card"? "name" | "mana value" | "color"["s"] | "color indicator" | "type"["s"] | "card type"["s"] | "subtype"["s"] | "supertype"["s"]
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
        
        objectname: OBJECTNAME //[TODO: No demarcations around names is difficult also. Need preprocessor help here.]
        OBJECTNAME: "OBJECTNAME" //[TODO: Temporarily commenting this out] //NAMEWORD ((WS | ",") NAMEWORD)* //[TODO: commas in names? This is problematic. Need preprocessor help here.]
        //NAMEWORD: (UCASE_LETTER | LCASE_LETTER)+
        
        countertype: ptchangeexpression //| WORD //[TODO: Should we enumerate all the common counter types?]
        
        loyaltycost: "[" (PLUS | PWMINUS)? valueterm "]"
        //[NOTE: Both Scryfall and Mtgjson use a long dash, not a short dash, to indicate a minus on a planeswalker ability]
        PWMINUS: "−"
        ptchangeexpression: (PLUS | MINUS) valueterm "/" (PLUS | MINUS) valueterm
        PLUS: "+"
        MINUS: "-"
        
        manaspecificationexpression: valueterm "mana" manaspecifier+
        manaspecifier: anycolorexpression //[TODO: Need to add the rest of these]
        
        manasymbolexpression: manasymbol+
        | manasymbolexpression "or" manasymbolexpression -> ormanaexpression
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
        | "divided" "as" "you" "choose" -> dividedfreelymod
        | "plus" valueterm -> plusmod
        | "minus" valueterm -> minusmod
        
        DASH: "—"
        MODALCHOICE: "•"
        
        NAMEREFSYMBOL: "~" | "~f"
        PLAYERTERM: "player"["s"] | "opponent"["s"] | "you" |  "teammate"["s"] | "team"["s"] | "they" | "controller"["s"] | "owner"["s"]
        
        tapuntapsymbol: TAPSYMBOL | UNTAPSYMBOL
        TAPSYMBOL: "{T}"i
        UNTAPSYMBOL: "{Q}"i
        
        %import common.UCASE_LETTER -> UCASE_LETTER
        %import common.LCASE_LETTER -> LCASE_LETTER
        //%import common.WORD -> WORD
        %import common.NEWLINE -> NEWLINE
        %import common.SIGNED_NUMBER -> NUMBER
        %import common.WS -> WS
        %ignore WS
        """

        compilerUsingPartialGrammar = MtgJsonCompiler.MtgJsonCompiler(
            options={"parser.overrideGrammar": revisedDeclarationGrammar,
                     "parser.startRule": "declarationorreference",
                     "parser.ambiguity": "explicit",
                     "parser.larkLexer": "basic",
                     })
        parser = compilerUsingPartialGrammar.getParser()

        declarationsToTest = [
            "their hand",
            "that player",
            "creatures you control",
            "{W}{W}{1}",
            "{G} or {U}",
            "all blue creatures, black creatures, and white creatures",
            "two 1/1 green elf creature tokens",
            "the exiled card",
            "a teammate's life total",
            "abilities of permanents you control",
            "this turn",
            "combat damage",
            "each draw step",
            "the battlefield",
            "seven cards in hand",
            "a spell on the stack",
            "multicolored enchantments",
            "the name of the player",
            "an artifact under their control",
            "a creature with a +1/+1 counter on it"
        ]

        shouldOutputVerboseDetails = False

        def getLexerResults(card):
            lexerState = lark.lexer.LexerState(text=cardsToTest[0], line_ctr=lark.lexer.LineCounter(
                b'\n' if isinstance(cardsToTest[0], bytes) else '\n'))
            lexTimeStart = time.time()
            lexerResults = parser.parser.lexer.lex(state=lexerState, parser_state=None)
            lexTimeEnd = time.time()
            print(f"Card ({card}) took {lexTimeEnd - lexTimeStart} to lex.")
            for token in lexerResults:
                print(f"(token type: {token.type}) | {token}")

        print("\n-----------------------")
        for declaration in declarationsToTest:
            try:
                fullParseTimeStart = time.time()
                parseTree = parser.parse(declaration)
                fullParseTimeEnd = time.time()
                ambiguities = list(parseTree.find_data("_ambig"))
                declarationPrettyPrint = declaration.replace('\n', ' ')
                print(
                    f"Declaration ({declarationPrettyPrint}) took {fullParseTimeEnd - fullParseTimeStart} to parse. The input had {len(ambiguities)} ambiguities.")
                if shouldOutputVerboseDetails and len(ambiguities) > 0:
                    print(parseTree.pretty())
            except Exception as exception:
                firstLineOfException = str(exception).split('\n')[0]
                if shouldOutputVerboseDetails:
                    print(f"Declaration ({declaration}) produced an exception during parsing: {exception}...")
                else:
                    print(
                        f"Declaration ({declaration}) produced an exception during parsing: {firstLineOfException}...")
        print("-----------------------")

    def test_integratingStatementLevelChangesToGrammar(self):
        integratedGrammar = """"""
        revisedGrammarDirectory = "tests/parsing/revisedgrammar/"
        for fileName in os.listdir(revisedGrammarDirectory):
            filePath = os.path.join(revisedGrammarDirectory, fileName)
            with open(filePath) as f:
                integratedGrammar = integratedGrammar + "\n" + f.read()

        compilerUsingIntegratedGrammar = MtgJsonCompiler.MtgJsonCompiler(
            options={"parser.overrideGrammar": integratedGrammar,
                     "parser.startRule": "cardtext",
                     "parser.ambiguity": "explicit",
                     "parser.larkLexer": "basic",
                     })
        parser = compilerUsingIntegratedGrammar.getParser()

        print("\n-----------------------")
        shouldOutputVerboseDetails = True

        cardsToTest = [
        "sacrifice all blue creatures, black creatures, and white creatures."
        ]

        def getLexerResults(card):
            lexerState = lark.lexer.LexerState(text=cardsToTest[0], line_ctr=lark.lexer.LineCounter(
                b'\n' if isinstance(cardsToTest[0], bytes) else '\n'))
            lexTimeStart = time.time()
            lexerResults = parser.parser.lexer.lex(state=lexerState, parser_state=None)
            lexTimeEnd = time.time()
            print(f"Card ({card}) took {lexTimeEnd - lexTimeStart} to lex.")
            for token in lexerResults:
                print(f"(token type: {token.type}) | {token}")

        for card in cardsToTest:
            cardPrettyPrint = card.replace('\n', ' ')
            try:
                getLexerResults(card)

                fullParseTimeStart = time.time()
                parseTree = parser.parse(card)
                fullParseTimeEnd = time.time()
                ambiguities = list(parseTree.find_data("_ambig"))
                print(
                    f"Card ({cardPrettyPrint}) took {fullParseTimeEnd - fullParseTimeStart} to parse. The input had {len(ambiguities)} ambiguities.")
                if shouldOutputVerboseDetails and len(ambiguities) > 0:
                    print(parseTree.pretty())
            except Exception as exception:
                firstLineOfException = str(exception).split('\n')[0]
                if shouldOutputVerboseDetails:
                    print(f"Card ({cardPrettyPrint}) produced an exception during parsing: {exception}...")
                else:
                    print(
                        f"Card ({cardPrettyPrint}) produced an exception during parsing: {firstLineOfException}...")
        print("-----------------------")





if __name__ == '__main__':
    unittest.main()
