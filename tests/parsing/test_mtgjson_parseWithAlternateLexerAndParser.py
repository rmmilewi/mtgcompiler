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

    def test_improveExpressionLevelOfGrammar(self):
        revisedExpressionGrammar = """
        
        declaration: "DECLARATION"

        //Expressions make things happen in the game. When spell states "~ *deals* 3 damage to target creature", "nonbasic lands *are* mountains",
        //or "target player *loses* the game", damage is dealt, lands become mountains, and a player loses the game. Expressions take declarations
        //or other expressions (like who deals the damage and to whom is the damage dealt). Meanwhile, statements can contain expressions, like the
        //if statement "if you control a modified creature, draw a card" is equivalent to (if the expression "you control a modified creature" evaluates
        //to true, make the expression "draw a card" happen.
        expression: beingexpression | basickeywordactionexpression
        !expressionordeclaration: expression | declaration

        beingexpression: expressionordeclaration ("is" | "was" | "are" "each"?) ("still"|"not")? expressionordeclaration -> isexpression
        | expressionordeclaration ("has"|"have"|"had") expressionordeclaration -> hasexpression
        | expressionordeclaration "can" "not"? expressionordeclaration -> canexpression
        | expressionordeclaration "become"["s"] expressionordeclaration -> becomesexpression
        | expressionordeclaration "may" expressionordeclaration -> mayexpression
        | expressionordeclaration "would" expressionordeclaration -> wouldexpression
        | expressionordeclaration (expressionordeclaration? ("do"["es"]? | "did") "not"? expressionordeclaration? | "doing" "so" ) -> doesexpression
        | "be" expressionordeclaration -> beexpression //Example(s): "*be* attacked", "*be* sacrificed"
        
        basickeywordactionexpression: expressionordeclaration? BASICKEYWORDACTION expressionordeclaration?
        
        //basickeywordaction: activateexpression
        //| attacksexpression
        //| blocksexpression
        //| attachexpression
        //| castexpression
        //| chooseexpression
        //| controlsexpression
        //| gaincontrolexpression
        //| uncastexpression
        //| createexpression
        //| destroyexpression
        //| drawexpression
        //| discardexpression
        //| doubleexpression
        //| exchangeexpression
        //| exileexpression
        //| fightexpression
        //| playexpression
        //| revealexpression
        //| sacrificeexpression
        //| searchexpression
        //| shuffleexpression
        //| tapuntapexpression
        //| millexpression
        
        BASICKEYWORDACTION: "activate"["s" | "d"]
        | "attack"["s" | "ed"]
        
        DASH: "—"
        MODALCHOICE: "•"
        %import common.UCASE_LETTER -> UCASE_LETTER
        %import common.LCASE_LETTER -> LCASE_LETTER
        //%import common.WORD -> WORD
        %import common.NEWLINE -> NEWLINE
        //%import common.NUMBER -> NUMBER
        %import common.SIGNED_NUMBER -> NUMBER
        %import common.WS -> WS
        %ignore WS
        """

        expressionGrammarOld = """

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

        // dealsdamageexpression:  declarationorreference? ("deal"["s"]|"dealt") valueexpression? DAMAGETYPE ("to" declarationorreference)? (","? quantityrulemodification)* -> dealsdamagevarianta
        // | valueexpression DAMAGETYPE ("to" declarationorreference)?  (","? quantityrulemodification)* -> dealsdamagevariantaimplied //variant a, implied antecedent
        // | declarationorreference ("deal"["s"]|"dealt") DAMAGETYPE valueexpression ("to" declarationorreference)?  (","? quantityrulemodification)* -> dealsdamagevariantb
        // | declarationorreference ("deal"["s"]|"dealt") DAMAGETYPE ("to" declarationorreference)?  valueexpression  (","? quantityrulemodification)* -> dealsdamagevariantc
        dealsdamageexpression: declarationorreference? "deal"["s"] valueexpression? DAMAGETYPE ("to" declarationorreference)? (","? quantityrulemodification)*
        | valueexpression DAMAGETYPE ("to" declarationorreference)?  (","? quantityrulemodification)*
        preventdamageexpression: "prevent" "the" "next" valueexpression DAMAGETYPE "that" "would" "be" "dealt" "to" declarationorreference timeexpression? -> preventdamagevarianta
        | "prevent" "the" "next" valueexpression DAMAGETYPE "that" declarationorreference "would" "deal" "to" declarationorreference timeexpression? -> preventdamagevariantb
        | "prevent" "all" DAMAGETYPE "that" "would" "be" "dealt" ("to" declarationorreference)? timeexpression? -> preventdamagevariantc
        | "prevent" "all" DAMAGETYPE "that" "would" "be" "dealt" "to" "or" "dealt" "by" (declarationorreference)? timeexpression? -> preventdamagevariantd
        | "prevent" "all" DAMAGETYPE "that"? (declarationorreference)? "would" "deal" timeexpression? -> preventdamagevariante
        | "prevent" valueexpression "of" "that" DAMAGETYPE -> preventdamagevariantd
        | "prevent" "that" DAMAGETYPE -> preventdamagevariante
        | DAMAGETYPE "is" "prevented" "this" "way" -> preventdamagevariantf //[TODO: There may be a more general is-statement for stuff like 'damage'.]

        returnexpression: playerdeclref? "return"["s"] declarationorreference atrandomexpression? ("from" zonedeclarationexpression)? "to" zonedeclarationexpression genericdeclarationexpression? zoneplacementmodifier?//[TODO]

        putinzoneexpression: playerdeclref? "put"["s"] (declarationorreference | cardexpression) (locationexpression | "back" | zoneplacementmodifier) (objectdefinition | playerdefinition | zoneplacementmodifier)?
        putcounterexpression: playerdeclref? "put"["s"] ("a"|valueexpression) countertype "counter"["s"] "on" declarationorreference
        removecounterexpression: playerdeclref? "remove"["s"] ("a"|valueexpression) countertype "counter"["s"] "from" declarationorreference
        spendmanaexpression: "spend" "mana" //[TODO: this is just a stub]
        paylifeexpression: playerdeclref? "pay"["s"] valueexpression? "life"
        addmanaexpression: playerdeclref? "add"["s"] manadeclref
        paymanaexpression: playerdeclref? "pay"["s"] manadeclref
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
        changezoneexpression: declarationorreference "enter"["s"] locationexpression? genericdeclarationexpression? zoneplacementmodifier? timeexpression? -> enterzoneexpression
        | declarationorreference "leaves" locationexpression -> leavezoneexpression
        skiptimeexpression: playerdeclref? "skip"["s"] timeexpression
        switchexpression: playerdeclref? "switch"["es"] declarationorreference
        targetsexpression: objectdeclref? "target"["s"] declarationorreference
        shareexpression: declarationorreference "share"["s"] declarationorreference


        keywordactionexpression: basickeywordaction | specialkeywordaction
        basickeywordaction: activateexpression
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

        activateexpression: "activate" declarationorreference
        !attacksexpression: declarationorreference? "only"? "attack"["s"] "only"? (timeexpression? declarationorreference?| declarationorreference? timeexpression?) "alone"?
        | declarationorreference? "attacked" (timeexpression? declarationorreference?| declarationorreference? timeexpression?) "alone"? -> attackedexpression
        | declarationorreference? "attack"["s"] "with" declarationorreference -> attackswithexpression
        //| "be" "attacked" "by" declarationorreference? timeexpression? -> beattackedexpression
        !blocksexpression: declarationorreference? "only"? "block"["s"] "only"? (timeexpression? declarationorreference? | declarationorreference? timeexpression?) "alone"?
        | declarationorreference? "blocked" (timeexpression? declarationorreference? | declarationorreference? timeexpression?) "alone"? -> blockedexpression
        //| "be" "blocked" "by" declarationorreference? timeexpression? -> beattackedexpression

        attachexpression: "attach" declarationorreference "to" declarationorreference
        | "unattach" declarationorreference ("from" declarationorreference)? -> unattachexpression
        | playerdeclref "attaches" declarationorreference "to" declarationorreference -> playerattachesexpression

        castexpression: playerdeclref? "cast"["s"] declarationorreference (castmodifier ("and" castmodifier)?)* timeexpression?
        castmodifier: "without" "paying" "its" "mana" "cost" -> castwithoutpaying //[TODO: We may be able to fold this into the pay-expression]
        | "as" "though" beingexpression -> castasthough
        chooseexpression: playerdeclref? ("choose"["s"]|"chose") declarationorreference ("from" "it")? atrandomexpression? //[TODO]
        controlsexpression: playerdeclref? ("control"["s"] | "controlled") genericdeclarationexpression
        gaincontrolexpression: playerdeclref? ("gain"["s"] | "gained") "control" "of" declarationorreference

        uncastexpression: "counter" declarationorreference
        createexpression: playerdeclref? "create"["s"] declarationorreference
        destroyexpression: "destroy" declarationorreference
        drawexpression: playerdeclref? ("draw"["s"]|"drew") cardexpression //[("a" "card" | valueexpression "card"["s"] | "cards"["s"] valueexpression)]
        discardexpression: playerdeclref? ("discard"["s"] | "discarded") (declarationorreference | "a" "card" | valueexpression "card"["s"] | "card"["s"] valueexpression) "at random"?
        doubleexpression: "double" //[TODO]
        exchangeexpression: "exchange" characteristicexpression //[TODO]
        exileexpression: "exile" declarationorreference
        fightexpression: declarationorreference? "fight"["s"] declarationorreference?
        playexpression: playerdeclref? ("play"["s"] | "played") declarationorreference timeexpression?
        revealexpression: playerdeclref? ("reveal"["s"] | "revealed") (cardexpression | declarationorreference)
        sacrificeexpression: playerdeclref? ("sacrifice"["s"] | "sacrificed") declarationorreference
        searchexpression: playerdeclref? ("search"["es"] | "searched") zonedeclarationexpression? "for" declarationorreference
        // used to be mandatory to specify a zone for shuffling, now default deck shuffling doesn't specify it.
        shuffleexpression: playerdeclref? ("shuffle"["s"] | "shuffled") zonedeclarationexpression?
        tapuntapexpression: "tap" declarationorreference? -> tapexpression
        | "untap" declarationorreference? -> untapexpression
        # millexpression: "mill" valueexpression "card"["s"]
        millexpression: playerdeclref? "mill"["s"] cardexpression

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
        surveilexpression: "surveil" valueexpression
        conniveexpression: "connive" valueexpression
        monstrosityexpression: "monstrosity" valueexpression
        adaptexpression: "adapt" valueexpression
        amassexpression: "amass" typeterm? valueexpression
        learnexpression: "learn"
        ventureexpression: "venture into the dungeon"
        convertexpression: "convert" namereference
        incubateexpression: "incubate" valueexpression
        theringtemptsexpression: "the ring tempts you"
        timetravelexpression: "time travel" valuefrequency?
        discoverexpression: "discover" valueexpression
        # // TODO: not sure this works, e.g. "cloak the top card of your library"
        cloakexpression: "cloak" declarationorreference
        collectevidenceexpression: "collect evidence" valueexpression
        suspectexpression: "suspect" reference
        forageexpression: "forage"
        manifestdreadexpression: "manifest dread"

        """
        

        compilerUsingPartialGrammar = MtgJsonCompiler.MtgJsonCompiler(
            options={"parser.overrideGrammar": revisedExpressionGrammar,
                     "parser.startRule": "expression",
                     "parser.ambiguity": "explicit",
                     "parser.larkLexer": "basic",
                     })
        parser = compilerUsingPartialGrammar.getParser()

        expressionsToTest = [
            "DECLARATION attacks DECLARATION",
            "DECLARATION can not be attacked"
        ]


        shouldOutputVerboseDetails = False

        def getLexerResults(declaration):
            lexerState = lark.lexer.LexerState(text=declaration, line_ctr=lark.lexer.LineCounter(
                b'\n' if isinstance(declaration, bytes) else '\n'))
            lexTimeStart = time.time()
            lexerResults = parser.parser.lexer.lex(state=lexerState, parser_state=None)
            lexTimeEnd = time.time()
            print(f"declaration ({declaration}) took {lexTimeEnd - lexTimeStart} to lex.")
            for token in lexerResults:
                print(f"(token type: {token.type}) | {token}")

        print("\n-----------------------")
        for expression in expressionsToTest:
            try:
                fullParseTimeStart = time.time()
                parseTree = parser.parse(expression)
                fullParseTimeEnd = time.time()
                ambiguities = list(parseTree.find_data("_ambig"))
                expressionPrettyPrint = expression.replace('\n', ' ')
                print(
                    f"Expression ({expressionPrettyPrint}) took {fullParseTimeEnd - fullParseTimeStart} to parse. The input had {len(ambiguities)} ambiguities.")
                if shouldOutputVerboseDetails and len(ambiguities) > 0:
                    print(parseTree.pretty())
            except Exception as exception:
                firstLineOfException = str(exception).split('\n')[0]
                if shouldOutputVerboseDetails:
                    print(f"Expression ({expression}) produced an exception during parsing: {exception}...")
                    print("Outputting lexer interpretation of inputs for reference...")
                    try:
                        getLexerResults(expression)
                    except Exception as lexerException:
                        firstLineOfLexerException = str(lexerException).split('\n')[0]
                        print(f"Lexer failed ({firstLineOfLexerException}...)")
                else:
                    print(
                        f"Expression ({expression}) produced an exception during parsing: {firstLineOfException}...")
        print("-----------------------")

    def test_improveDeclarationLevelOfGrammar(self):
        revisedDeclarationGrammar = """
        abilitysequencestatement: "ABILITYSEQUENCESTATEMENT"
        beingexpression: "BEINGEXPRESSION"
        effectexpression: "EFFECTEXPRESSION"
        statement: "STATEMENT"
        valueexpression: "VALUEEXPRESSION"
        
        //A regular declaration introduces something that the card relates to or acts on.
        //Example(s): "destroy *target nonblack creature*" and "draw *a card*"
        //A reference points to a declaration that was made earlier or that is already assumed to exist.
        //Example(s) : "draw a card if *that creature* had power 3 or greater" or "target creature blocks *this turn* if able"
        declaration: singledeclaration | compounddeclaration
        compounddeclaration:  singledeclaration ("," singledeclaration ",")* "or" singledeclaration -> orcompounddeclaration
        | singledeclaration ("," singledeclaration ",")* "and" singledeclaration -> andcompounddeclaration
        | singledeclaration ("," singledeclaration ",")* "and/or" singledeclaration -> andorcompounddeclaration
        | "neither" singledeclaration "nor" singledeclaration -> neithernorcompounddeclaration
        singledeclaration: regulardeclaration | referencedeclaration | keywordabilitydeclaration
        regulardeclaration: declarationdecorator* declarationdefinition
        referencedeclaration: referencedecorator+ declarationdefinition | personalthirdpersonreferencedefinition | namereferencedefinition
        
        //Reference definition for third-person personal pronoun references.
        //Example(s): "*they* can’t be regenerated." and "Sarkhan the Mad deals damage to *himself*"
        personalthirdpersonreferencedefinition: THIRDPERSONPERSONALREFERENCE | SELFPRONOUNREFERENCE | HERAMBIGUOUSREFERENCE
        HERAMBIGUOUSREFERENCE.100: "her" //This could be the possessive form or the object of a sentence.
        THIRDPERSONPERSONALREFERENCE.90: ("he" | "him") | ("she") | ("they" | "them") | "it"
        SELFPRONOUNREFERENCE.110:  "itself" | "himself" | "herself" | "themselves"
        
        //Reference form used when when a card makes a reference to itself by name. "~" is a full name reference, "~f" (rarely used) is a first name reference.
        //Example(s): "*Chandra, Fire of Kaladesh (~)* deals 1 damage to target player or planeswalker. If *Chandra (~f)* has dealt 3 or more damage [...]"
        namereferencedefinition: NAMEREFSYMBOL
        NAMEREFSYMBOL: "~" | "~f"
        
        //Reference decorators help clarify what is being talked about. Note that reference decorators can have nested
        //references to other defined things (like "your *opponent's* hand").
        //Example(s): "Destroy target creature. *Its* controller [...]" and "*its owner’s* hand." "*that creature’s* toughness."
        referencedecorator: THIRDPERSONIMPERSONALREFERENCE | POSSESSIVEPRONOUNREFERNCE | HERAMBIGUOUSREFERENCE
        THIRDPERSONIMPERSONALREFERENCE: ("that" | "those") | ("this"|"these")
        POSSESSIVEPRONOUNREFERNCE.100: "its" | "your" | "their" | "his" //Note: "her" is handled separately to capture the ambiguity.
        
        //Declaration decorators. The most popular decorator is "target".
        //Example(s): "destroy *target* nonblack creature", "*any* permanent" 
        declarationdecorator: "each" -> eachdecorator
        | "same" -> samedecorator
        | "all" -> alldecorator
        | ["an"]"other" -> otherdecorator
        | ("a" | "an") -> indefinitearticledecorator
        | "the" -> definitearticledecorator
        | valueterm? "target" -> targetdecorator
        | "any" -> anydecorator
        
        //A declaration definition is made up of a set of descriptive terms like "a *blue permanent*" or "*two 1/1 green elf creature tokens*".
        //There can be limited nesting of declarations inside definitions like with possessives ("its *owner's* hand") and prepositions
        //("a creature *with a +1/+1 counter* *on it*").
        declarationdefinition: "DEFINITION" | (nonnesteddeclarationterm | nesteddeclarationterm)+ //TODO: Remove "DEFINITION" placeholder
        nonnesteddeclarationterm : ("non""-"?)? (valueterm | manaterm | characteristicterm 
        | typeterm | colorterm | modifierterm | qualifierterm | timeterm | damageterm | playerterm 
        | powertoughnessterm | loyaltycostterm | counterterm | nameterm | variableterm | zoneterm | anytargetterm )
        nesteddeclarationterm: possessiveclarationreference | prepositionalattacheddeclaration
        
        //Declaration definitions can have prepositional phrases and possessives that can contain declarations of their own.
        //We need a special rule for embedded declarations which shouldn't have any further recursive declarations. Instead,
        //we treat the declaration as flat and it's the job of a semantic analyzer to determine how they are really nested.
        //For example, we parse "the owner of the creature with a +1/+1 counter on it" as 
        //"the owner (of the creature) (with a +1/+1 counter) (on it)" rather than
        //"the owner (of the creature (with a +1/+1 counter (on it)))", if that makes sense.
        embeddedsingledeclaration: embeddedregulardeclaration | embeddedreferencedeclaration
        embeddedregulardeclaration: declarationdecorator* embeddeddeclarationdefinition
        embeddedreferencedeclaration: referencedecorator+ embeddeddeclarationdefinition | personalthirdpersonreferencedefinition | namereferencedefinition
        embeddeddeclarationdefinition: nonnesteddeclarationterm+
        prepositionalattacheddeclaration: DECLARATIONPREPOSITION embeddedsingledeclaration
        DECLARATIONPREPOSITION: "of" | ("on" | "onto") | "who" | "in" | "under" | "with"
        possessiveclarationreference: (embeddeddeclarationdefinition | namereferencedefinition) ("'s"|"'")
        
        
        
        typeterm: (TYPE ["s"] | SUBTYPESPELL ["s"] | SUBTYPELAND ["s"] | SUBTYPEARTIFACT ["s"] | SUBTYPEENCHANTMENT ["s"] | SUBTYPEPLANESWALKER | SUBTYPECREATUREA ["s"] | SUBTYPECREATUREB ["s"] | SUBTYPEPLANAR | SUPERTYPE)
        modifierterm: ABILITYMODIFIER | COMBATSTATUSMODIFIER | KEYWORDSTATUSMODIFIER | TAPPEDSTATUSMODIFIER | EFFECTSTATUSMODIFIER | RELATIVEMODIFIER
        qualifierterm: QUALIFIER["s"]
        timeterm: PHASE | STEP | TURN | GAME
        playerterm: PLAYER["s"]
        zoneterm: ZONE
        powertoughnessterm: valueterm "/" valueterm
        loyaltycostterm: "[" (PLUS | PWMINUS)? valueterm "]"
        counterterm: (COUNTERTYPE | powertoughnessterm)  "counter"["s"]
        characteristicterm: OBJECTCHARACTERISTIC | PLAYERCHARACTERISTIC
        nameterm: "OBJECTNAME" | NAMEREFSYMBOL //TODO: fix objectname vs. basic lexer
        damageterm: DAMAGETYPE
        colorterm: COLOR
        variableterm: "choice"["s"] //Example(s): "their choice", "of your choice"
        | ("copy" | "copies") //Example(s): "You may have Shapeshifters you control become *copies* of that creature", "choose new targets for the *copy*"
        | "vote"["s"] //Example(s): "each *vote* they receive"
        | NUMBERPROPERTY? "number"["s"] //Example(s): "the *number* of cards you drew this term", "a *prime number* of lands"
        | "time"["s"] //Example(s): "the number of *times* ~ was kicked", "the first time this turn"
        anytargetterm: "any target" //Special nullary variant like "~ deals three damage to *any target*"

        
        //Keyworded ability declaration
        //Regular keyworded abilities are those that are of the form "keyword (cost/description"?.
        //Note that the parser will allow for illegal keyworded ability definitions like "flying 3", and it's the
        //job of the semantic analyzer to check for things like this. Special keyworded abilities, meanwhile, are
        //those that have very particular syntax around them and its easier to spell them out in a special rule.
        keywordabilitydeclaration: regularkeywordedabilitydefinition | specialkeywordedabilitydefinition
        
        regularkeywordedabilitydefinition: REGULARKEYWORDEDABILITY declaration? //Example(s): "Flying", "Bushido 3", "Champion a Kithkin"
        | REGULARKEYWORDEDABILITY declaration DASH declaration //Example(s): "Impending 4—{2}{R}{R}"
        
        specialkeywordedabilitydefinition: "specialkeywordedabilitydefinition" //TODO
        
        //need to handle past tense of keyworded actions like "kicked" or "plotted" as part of declarations
        //special cases include...
        //landwalk, hexproof from X and from Y, [typeexpression] "cycling" cost, "splice" "onto" typeexpression cost, typeexpression "offering"
        //"forecast" activationstatement, "suspend" valuenumber cost, "aura swap" (if we wanted to generalize to TYPE swap)
        //partner with objectname, kwcompanion: "companion", "craft" "with" declarationorreference cost, spree (Choose one or more additional costs.)
        
        REGULARKEYWORDEDABILITY: "deathtouch" | "defender" | "double strike" | "enchant" | "equip" | "first strike" | "flash" | "flying"
        | "haste" | "indestructible" | "intimidate" | "lifelink" | "reach" | "shroud" | "trample" | "vigilance" | "ward" | "rampage"
        | "cumulative upkeep" | "flanking" | "phasing" | "buyback" | "shadow" | "echo" | "horsemanship" | "fading" | "multi"? "kicker"
        | "flashback" | "madness" | "fear" | "mega"? "morph" | "amplify" | "provoke" | "storm" | "affinity" "for"? | "entwine" | "modular"
        | "sunburst" | "bushido" | "soulshift" | "ninjutsu" | "epic" | "convoke" | "dredge" | "transmute" | "bloodthirst" | "haunt"
        | "graft" | "recover" | "ripple" | "split second" | "suspend" | "vanishing" | "absorb" | "aura swap" | "delve" | "delve"
        | "fortify" | "frenzy" | "gravestorm" | "poisonous" | "transfigure" | "champion" | "changeling" | "evoke" | "hideaway" | "prowl"
        | "reinforce" | "conspire" | "persist" | "wither" | "retrace" | "devour" | "exalted" | "unearth" | "cascade" | "annihilator"
        | "level up" | "rebound" | "totem armor" | "infect" | "battle cry" | "living weapon" | "undying" | "miracle" | "soulbond"
        | "overload" | "scavenge" | "unleash" | "cipher" | "evolve" | "extort" | "fuse" | "bestow" | "tribute" | "dethrone"
        | "hidden agenda" | "outlast" | "prowess" | "dash" | "exploit" | "menace" | "renown" | "awaken" | "devoid" | "ingest"
        | "myriad" | "surge" | "skulk" | "emerge" | "escalate" | "melee" | "crew" | "fabricate" | "undaunted" | "improvise" | "aftermath"
        | "embalm" | "eternalize" | "afflict" | "ascend" | "assist" | "jump-start" | "mentor" | "afterlife" | "riot" | "spectacle"
        | "escape" | "mutate" | "oncore" | "boast" | "foretell" | "demonstrate" | ("day" | "night") "bound" | "disturb" | "decayed"
        | "cleave" | "training" | " compleated" | "reconfigure" | "blitz" | "casualty" | "enlist" | "read ahead" | "ravenous" | "squad"
        | "prototype" | "living metal" | "for mirrodin!" | "toxic" | "backup" | "bargain" | "disguise" | "plot" | "saddle"
        | "gift" | "offspring" | "impending"

        
        //Below are hardcoded game terms used in declarations.
        PLAYER: "player" | "opponent" | "you" |  "teammate" | "team" | "controller" | "owner"
        PLAYERCHARACTERISTIC: "maximum hand size" | "life total"["s"] | "life" | "cards in hand"
        OBJECTCHARACTERISTIC: "card"? "name" | "mana value" | "color"["s"] | "color indicator" | "type"["s"] | "card type"["s"] | "subtype"["s"] | "supertype"["s"]
        | "rules text" | ("ability" | "abilities" ) | "power" | "toughness" | "base power" | "base toughness" | "loyalty" | "hand modifier" | "life modifier"
        ZONE: "battlefield" | "graveyard"["s"] | ("library"|"libraries") | "hand"["s"] | "stack" | "exile" | "command zone" | "outside the game" | "anywhere"
        TYPE.100: "planeswalker" | "conspiracy" | "creature" | "enchantment" | "instant" | "land" | "phenomenon" | "plane" | "artifact" | "scheme" | "sorcery" | "tribal" | "vanguard"
        SUBTYPESPELL : "arcane" | "trap" | "adventure"
        SUBTYPELAND: "desert" | "forest" | "gate" | "island" | "lair" | "locus"
        | "mine" | "mountain" | "plains" | "power-plant" | "swamp" | "tower" | "urza's"
        SUBTYPEARTIFACT: "clue" | "contraption" | "equipment" | "fortification" | "treasure" | "vehicle" | "food"
        SUBTYPEENCHANTMENT: "aura" | "cartouche" | "curse" | "saga" | "shrine" | "rune" | "shard" | "case" | "room"
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
        | "crocodile" | "cyclops" | "dauthi" | "demon" | "deserter" | "detective" | "devil" | "dinosaur" | "djinn" | "dragon"
        | "drake" | "dreadnought" | "drone" | "druid" | "dryad" | ("dwarf"|"dwarves") | "efreet" | "egg" | "elder" | "eldrazi"
        | "elemental" | "elephant" | ("elf"|"elves") | "elk" | "eye" | "faerie" | "ferret" | "fish" | "flagbearer" | "fox"
        SUBTYPECREATUREB: "frog" | "fungus" | "gargoyle" | "germ" | "giant" | "gnome" | "goat" | "goblin" | "god" | "golem" | "gorgon"
        | "graveborn" | "gremlin" | "griffin" | "hag" | "harpy" | "hellion" | "hippo" | "hippogriff" | "homarid" | "homunculus"
        | "horror" | "horse" | "hound" | "human" | "hydra" | "hyena" | "illusion" | "imp" | "incarnation" | "insect"
        | "jackal" | "jellyfish" | "juggernaut" | "kavu" | "kirin" | "kithkin" | "knight" | "kobold" | "kor" | "kraken"
        | "lamia" | "lammasu" | "leech" | "leviathan" | "lhurgoyf" | "licid" | "lizard" | "manticore" | "masticore"
        | ("mercenary"|"mercenaries") | "merfolk" | "metathran" | "minion" | "minotaur" | "mole" | "monger" | "mongoose" | "monk"
        | "monkey" | "moonfolk" | "mouse" | "mutant" | "myr" | "mystic" | "naga" | "nautilus" | "nephilim" | "nightmare"
        | "nightstalker" | "ninja" | "noggle" | "nomad" | "nymph" | ("octopus"|"octopuses") | "ogre" | "ooze" | "orb" | "orc"
        | "orgg" | "ouphe" | "ox" | "oyster" | "pangolin" | "pegasus" | "pentavite" | "pest" | "phelddagrif" | "phoenix"
        | "pilot" | "pincher" | "pirate" | "plant" | "praetor" | "prism" | "processor" | "rabbit" | "rat" | "rebel"
        | "reflection" | "rhino" | "rigger" | "rogue" | "sable" | "salamander" | "samurai" | "sand" | "saproling" | "satyr"
        | "scarecrow" | "scion" | "scorpion" | "scout" | "serf" | "serpent" | "servo" | "shade" | "shaman" | "shapeshifter"
        | "sheep" | "siren" | "skeleton" | "slith" | "sliver" | "slug" | "snake" | "soldier" | "soltari" | "spawn" | "specter"
        | "spellshaper" | "sphinx" | "spider" | "spike" | "spirit" | "splinter" | "sponge" | "squid" | "squirrel" | "starfish"
        | "surrakar" | "survivor" | "tetravite" | "thalakos" | "thopter" | "thrull" | "treefolk" | "trilobite" | "triskelavite"
        | "troll" | "turtle" | "unicorn" | "vampire" | "vedalken" | "viashino" | "volver" | "wall" | "warrior" | "warlock" | "weird"
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
        DAMAGETYPE: "damage" | "combat damage" | "excess damage"
        ABILITYMODIFIER: "triggered" | "activated" | "mana" | "loyalty"
        RELATIVEMODIFIER: "next" | "additional" | "extra" //Example(s): "an *additional* +1/+1 counter", "take an *extra* turn"
        COMBATSTATUSMODIFIER: "attacking" | "defending" | "attacked" | "blocking" | "blocked" | "active" //Example(s): "the *active* player", "*attacking* creatures you control"
        KEYWORDSTATUSMODIFIER: "paired" | "kicked" | "face-up" | "face-down" | "transformed" | "enchanted" | "equipped" //TODO: This will need to be generalized more.
        | "fortified" | "monstrous" | "regenerated" | "suspended" | "flipped" | "suspected" // TODO: ensure 'suspected' works properly
        TAPPEDSTATUSMODIFIER: ["un"]"tapped"
        EFFECTSTATUSMODIFIER: "named" | "chosen" | "chosen at random" | "revealed" | "returned" | "destroyed" | "exiled" | "died" | "countered" | "sacrificed"
        | "prevented" | "created"
        QUALIFIER: "card" | "permanent" | "source" | "spell" | "token" | "effect"
        COLOR: "white" | "blue" | "black" | "red" | "green" | "monocolored" | "multicolored" | "colorless"
        PHASE: "beginning phase" | ("precombat" | "postcombat")? "main phase" | ("combat" | "combat phase") | "ending phase"
        STEP: "untap step" | ("upkeep step" | "upkeep") | "draw step" | "beginning of combat" | "declare attackers step"
        | "declare blockers step" | "combat damage step" | "end of combat" | "end step" | "cleanup step" | "step"
        TURN: "turn"
        GAME: "game"
        
        //TODO: counter types aren't formally defined in the game (like the "oil" counters doesn't have a specific rules meaning, but until we
        //can have arbitrary names that don't confuse the basic lexer, we might spell out counter types here based on the list
        //provided here: https://mtg.fandom.com/wiki/Counter_(marker)/Full_List.
        COUNTERTYPE: "COUNTERTYPE" //TODO
        
        //COUNTERTYPE: "aegis" | "age" | "aim" | "arrow" | "arrowhead" | "awakening" | "bait" | "blaze" | "blessing" | "blight" | "blood" | "bloodline"
        //| "bloodstain" | "book" | "bounty" | "brain" | "bribery" | "brick" | "burden" | "cage" | "carrion" | "charge" | "coin" | "collection" | "component"
        //| "contested" | "corruption" | "crank!" | "credit" | "croak" | "corpse" | "crystal" | "cube" | "currency" | "death" | "defense" | "delay"
        //| "depletion" | "descent" | "despair" | "devotion" | "discovery" | "divinity" | "doom" | "dream" | "echo
        
        //Rules for mana symbols
        //TODO: Add in text mana descriptions here
        manaterm: manasymbol
        manasymbol: "{" manamarkerseq "}"
        manamarkerseq: manamarker_color -> regularmanasymbol
        | NUMBER -> genericmanasymbol
        | manamarker_halfmana manamarker_color -> halfmanasymbol
        | manamarker_color "/" manamarker_phyrexian -> phyrexianmanasymbol
        | manamarker_color "/" manamarker_color -> hybridmanasymbol
        | NUMBER "/" manamarker_color -> alternate2manasymbol
        | manamarker_snow -> snowmanasymbol
        | manamarker_colorless -> colorlessmanasymbol
        | manamarker_x -> xmanasymbol
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
        
        //Rules for representing numeric values and math operations
        valueterm: NUMBER  | CARDINAL ("time"["s"])?| ORDINAL | FREQUENCY | VARIABLEVALUE | valueoperation
        FREQUENCY: "once" | "twice"
        CARDINAL: "one" | "two" | "three" | "four" | "five" | "six" | "seven" | "eight" | "nine" | "ten"
        | "eleven" | "twelve" | "thirteen" | "fourteen" | "fifteen" | "sixteen" | "seventeen" | "eighteen" | "nineteen" | "twenty" //[TODO]
        ORDINAL: "first" | "second" | "third" | "fourth" | "fifth" | "sixth" | "seventh" | "eighth" | "ninth" | "tenth" //[TODO]
        VARIABLEVALUE: "x" | "*"
        NUMBERPROPERTY: "odd" | "even" | "prime"
        
        //[NOTE: Both Scryfall and Mtgjson use a long dash, not a short dash, to indicate a minus on a planeswalker ability]
        PWMINUS: "−"
        PLUS: "+"
        MINUS: "-"

        tapuntapsymbol: TAPSYMBOL | UNTAPSYMBOL
        TAPSYMBOL: "{T}"i
        UNTAPSYMBOL: "{Q}"i
        
        valueoperation: valuecomparisonoperation | valuemathoperation
        valuecomparisonoperation: "equal to" valueterm // ==
            | "less than" "or equal to"? valueterm // < ; <=
            | "greater than" "or equal to"? valueterm // > ; >=
            | "up to" valueterm // <=
            | valueterm "or" ("less" | "fewer") // <=
            | valueterm "or" ("greater" | "more") // >=
        valuemathoperation: ("that much" | "that many") //Example: "create *that many* treasure tokens", "draw twice *that many* cards"
        | valueterm "rounded" ("up" | "down")
        | valueterm "divided" ("evenly" | "as you choose")
        | valueterm "plus" valueterm //Example: "the number of Elves you control *plus* the number of Elf cards in your graveyard."
        | valueterm "minus" valueterm //Example: "the number of cards in your hand *minus* the number of cards in that player’s hand."
        
        DASH: "—"
        MODALCHOICE: "•"
        %import common.UCASE_LETTER -> UCASE_LETTER
        %import common.LCASE_LETTER -> LCASE_LETTER
        //%import common.WORD -> WORD
        %import common.NEWLINE -> NEWLINE
        //%import common.NUMBER -> NUMBER
        %import common.SIGNED_NUMBER -> NUMBER
        %import common.WS -> WS
        %ignore WS
        """

        compilerUsingPartialGrammar = MtgJsonCompiler.MtgJsonCompiler(
            options={"parser.overrideGrammar": revisedDeclarationGrammar,
                     "parser.startRule": "declaration",
                     "parser.ambiguity": "explicit",
                     "parser.larkLexer": "basic",
                     })
        parser = compilerUsingPartialGrammar.getParser()


        declarationsToTest = [
            "the target of a spell or ability",
            "a creature",
            "a land",
            "an artifact",
            "haste or flying",
            "bushido 3",
            "{R}{R}{2}",
            "{2}{R}{R}",
            "impending 4 — {2}{R}{R}",
            "champion a kithkin",
            "a creature with a +1/+1 counter",
            "a creature with a +1/+1 counter on it",
            "the owner of the creature with a +1/+1 counter on it",
            "that teammate's life total",
            "hands",
            "their hand",
            "their owner",
            "its owner",
            "its owner's hand",
            "that hand",
            "that player",
            "{W}{W}{1}",
            "{G} or {U}",
            "all blue creatures, black creatures, and white creatures",
            "two 1/1 green elf creature tokens",
            "the exiled card",
            "five life",
            "outside the game",
            "a teammate's life total",
            "abilities",
            "permanents",
            "abilities of permanents",
            "this turn",
            "combat damage",
            "each draw step",
            "the battlefield",
            "seven cards in hand",
            "a spell on the stack",
            "multicolored enchantments",
            "the name of the player",
            "they",
            "his hand",
            "himself",
            "him",
            "herself",
            "her",
            "her enchantment",
            "five",
            "three or greater",
            "a cat, a scarecrow, and a construct",
            "a detective and a case",
            "one or two",
            "a creature on the battlefield of your teammate's game",
            "one of three",
            "one with two",
            "the first time",
            "a prime number",
            "creatures you control",
            "an artifact under their control",
            "abilities of permanents you control",
            "each card drawn"
        ]


        shouldOutputVerboseDetails = False

        def getLexerResults(declaration):
            lexerState = lark.lexer.LexerState(text=declaration, line_ctr=lark.lexer.LineCounter(
                b'\n' if isinstance(declaration, bytes) else '\n'))
            lexTimeStart = time.time()
            lexerResults = parser.parser.lexer.lex(state=lexerState, parser_state=None)
            lexTimeEnd = time.time()
            print(f"declaration ({declaration}) took {lexTimeEnd - lexTimeStart} to lex.")
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
                    print("Outputting lexer interpretation of inputs for reference...")
                    try:
                        getLexerResults(declaration)
                    except Exception as lexerException:
                        firstLineOfLexerException = str(lexerException).split('\n')[0]
                        print(f"Lexer failed ({firstLineOfLexerException}...)")
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
