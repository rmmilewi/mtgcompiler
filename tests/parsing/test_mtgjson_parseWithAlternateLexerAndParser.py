import unittest
import time,os
import mtgcompiler.midend.support.inspection as inspection
import mtgcompiler.midend.support.binding as binding
import mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonCompiler as MtgJsonCompiler
import pytest
import lark.lexer
import lark
import json
import mtgcompiler.frontend.compilers.LarkMtgJson.grammar as oldGrammar

class TestGrammarAndParser(unittest.TestCase):

    def test_integratingChangesToGrammar(self):
        shouldOutputVerboseDetails = False #Enables printing of lexer results and parse trees.
        useRevisedGrammar = True #Set to False if you want to see how much progress we made over the original grammar
        testAgainstFoundations = True #Set to True if you want to run against all the cards in the Foundations set, False for custom list of strings
        lexerTypeToUse = "basic" #Note: If using the original grammar, lexing will always be done in dynamic mode.

        integratedGrammar = """"""
        if useRevisedGrammar:
            revisedGrammarDirectory = "tests/parsing/revisedgrammar/"
            for fileName in os.listdir(revisedGrammarDirectory):
                filePath = os.path.join(revisedGrammarDirectory, fileName)
                if fileName == "remainder.lark":
                    continue
                with open(filePath,encoding='utf-8') as f:
                    integratedGrammar = integratedGrammar + "\n" + f.read()
            lexerType = lexerTypeToUse
        else:
            integratedGrammar = oldGrammar.getGrammar()
            lexerType = "dynamic"

        compilerUsingIntegratedGrammar = MtgJsonCompiler.MtgJsonCompiler(
            options={"parser.overrideGrammar": integratedGrammar,
                     "parser.startRule": "cardtext",
                     "parser.ambiguity": "explicit",
                     "parser.larkLexer": lexerType,
                     })
        parser = compilerUsingIntegratedGrammar.getParser()
        preprocessor = compilerUsingIntegratedGrammar.getPreprocessor()
        print("\n===================================================================================================")
        cardsToTest = [
            "Clues you control are equipment in addition to their other types.",  # Armed with Proof
            "If two cards that share all their card types were milled this way, sacrifice ~.", #Demonic Covenant
            "During your next turn, you may draw a card.",
            "For each artifact and/or enchantment you control, that creature gets +1/+1.",
            "For each artifact you control, draw a card.",
            "For each artifact and/or enchantment you control, enchanted creature gets +1/+1.",
            "Enchanted creature gets +1/+1 for each artifact and/or enchantment you control.", #All That Glitters
            "As ~ enters, it becomes your choice of a 3/3 artifact creature, a 2/2 artifact creature with flying, or a 1/6 Wall artifact creature with defender.",
            "As ~ enters, it becomes your choice of a 3/3 artifact creature, a 2/2 artifact creature with flying, or a 1/6 Wall artifact creature with defender in addition to its other types.", #Primal Clay
            "Exile target nonland permanent you control.",
            "Exile target nonland permanent an opponent controls until ~ leaves the battlefield.",
            "when ~ enters, exile target nonland permanent an opponent controls until ~ leaves the battlefield.\nyour opponents can not cast spells with the same name as the exiled card.",  # Ixalan's binding
            "booksmarts — draw a card. if you control a wizard, draw an additional card. (aren't you clever!)", #This has an ambiguity.
            "flash\nward {2}\nprobing telepathy — whenever a creature entering under an opponent's control causes a triggered ability of that creature to trigger, you may copy that ability. You may choose new targets for the copy.",# Aboleth Spawn
            "−1: Target player draws a card.\n+10: Target player draws a card.\n−X: Target player draws a card.\n0: Target player draws a card.",
            "They can not be attacked.",  # There's an ambiguity here that I need to figure out.
            "Each creature has trample. Creatures can not gain flying. Creatures become enchantments. You may draw a card.",
            "If you would lose the game, you win the game instead.",
            "Roll a d6, a d8, and a d12.",  # coins and dice
            "Roll a d6 and flip a coin.",  # coins and dice
            "Choose an elf, goblin, and merfolk.",
            "Roll a d6 and a d8.",
            "Create a 1/1 red Mercenary creature token with \"{T}: Target creature you control gets +1/+0 until end of turn. Activate only as a sorcery.\".", #Quoted ability test.
            "Sacrifice all blue creatures and black creatures, then draw a card.",
            "Planeswalkers' loyalty abilities you activate cost an additional [+1] to activate.", #Carth the Lion
            "{t}: put a +1/+1 counter on each artifact creature you control.", #Steel Overseer
            "unless its controller pays {2}, counter target spell.",  # Quench (inverted)
            "counter target spell unless its controller pays {2}.",  # Quench
            "{t}: draw a card, then discard a card.",  # Merfolk Looter
            "haste (haste is an ability)",
            "Create a 1/1 green elf creature token under your control. Gain control of all elves.",# control as noun test
            "destroy each bird on the battlefield.",
            "draw a card for each bird on the battlefield.", #Airborne Aid
            "reveal the player you chose.",
            "when ~ enters, secretly choose an opponent.", #Stalking Leonin part 1
            "reveal the player you chose: exile target creature that is attacking you if it is controlled by the chosen player. activate only once.", #Stalking Leonin part 2
            "destroy target nonattacking creature.",
            "when this creature dies, create a 1/1 black and green insect creature token with flying.", #Infestation Sage
            "{T}: add {C}.\n{G/W}, {T}: add {G}{G}, {G}{W}, or {W}{W}.", #Wooded Bastion
            "~ deals 4 damage to target creature and each other creature with the same name as that creature.", #Homing Lightning
            "discard your hand.", #One With Nothing
            "at the beginning of your upkeep, each opponent chooses money, friends, or secrets. for each player who chose money, you and that player each create a treasure token. for each player who chose friends, you and that player each create a 1/1 green and white citizen creature token. for each player who chose secrets, you and that player each draw a card.", #Master of Ceremonies
            "~ can not be the target of white spells or abilities from white sources.\n{3}: put target nontoken rebel on the bottom of its owner's library.", #Rebel Informer
            "return target creature card from your graveyard to the battlefield. if {G} was spent to cast this spell, that creature enters with an additional +1/+1 counter on it.", #Vigor Mortis
            "{T}: add {G}.\n{T}: target 1/1 creature gets +1/+2 until end of turn.", #Pendlehaven
            "reach\nwhenever ~ or another cat you control enters, you may destroy target artifact or enchantment.", #Qasali Slingers
            "target nonattacking creature gains reach and deathtouch until end of turn. untap it.", #Ruthless Instincts
            "destroy target nonblack creature.",  # Doom Blade
            "draw two cards.",  # Divination
            "{t}, sacrifice ~: add three mana of any one color.",  # Black Lotus
            "+2: each player draws a card.\n+1: target player draws a card.\n+10: target player puts the top twenty cards of their library into their graveyard.", # Jace Beleren
            "for each land you control, you gain 1 life.", #Bountiful Harvest
            "{1}{u}{r}: return ~ to its owner's hand.\ncascade (when you cast this spell, exile cards from the top of your library until you exile a nonland card that costs less. You may cast it without paying its mana cost. Put the exiled cards on the bottom in a random order.)", #Etherium-Horn Sorcerer
            "when ~ enters, mill three cards.\nwhen ~ dies, you may exile it. when you do, return target creature card from your graveyard to your hand.",
            "flying, vigilance, lifelink", #Aerial Responder
            "enchant creature\nenchanted creature is a treefolk with base power and toughness 0/4 and loses all abilities.", #Lignify,
            "when ~ enters, tap target creature.",
            "if a player would draw a card except the first one they draw in each of their draw steps, that player discards a card instead.", #Chains of Mephistopheles
            "at the beginning of your end step, choose one — • you gain 1 life.\n• return target creature card with mana value 1 from your graveyard to the battlefield.", #Abiding Grace
            "create a 2/2 white cat soldier creature token named OBJECTNAME with \“whenever you gain life, put a +1/+1 counter on OBJECTNAME.\”" #Ajani, Strength of the Pride
        ]
        if testAgainstFoundations:
            with open("tests/parsing/FDN.json", encoding='utf-8') as f:
                foundationsSet = json.load(f)
            cardsToTest = []
            def get_unique_name(card):
                if 'faceName' in card:
                    return card['faceName']
                return card['name']
            unique_cards = {get_unique_name(card): card for card in foundationsSet['data']['cards'] if
                            not get_unique_name(card).startswith("A-")}
            print(len(unique_cards))
            for name in unique_cards:
                cardDict = unique_cards[name]
                if "text" in cardDict:
                    preprocessedText = preprocessor.prelex(cardDict['text'], None, name)
                    cardsToTest.append((name,preprocessedText))
        print("Total card texts to test against: {total}".format(total=len(cardsToTest)))
        def getLexerResults(card):
            lexerState = lark.lexer.LexerState(text=card, line_ctr=lark.lexer.LineCounter(
                b'\n' if isinstance(card, bytes) else '\n'))
            lexTimeStart = time.time()
            lexerResults = parser.parser.lexer.lex(state=lexerState, parser_state=None)
            lexTimeEnd = time.time()
            print(f"Card ({card}) took {lexTimeEnd - lexTimeStart} to lex.")
            for token in lexerResults:
                print(f"{token} ({token.type}) ",end='')
            print("\n")

        for cardName,card in cardsToTest:
            cardPrettyPrint = card.replace('\n', ' ')
            try:
                if shouldOutputVerboseDetails and lexerType != "dynamic":
                    getLexerResults(card)
            except Exception as lexingException:
                lexingException = str(lexingException)[0:200]
                print(f"Card ({cardPrettyPrint}) produced an exception during lexing: {lexingException}...")
                continue
            try:
                fullParseTimeStart = time.time()
                parseTree = parser.parse(card)
                fullParseTimeEnd = time.time()
                ambiguities = list(parseTree.find_data("_ambig"))
                if len(ambiguities) > 0:
                    nodesInTree = parseTree.pretty().count('\n')
                    ambiguityTreeSizeStatement = f"Number of lines in pretty printed tree is {nodesInTree}."
                else:
                    ambiguityTreeSizeStatement = ""
                if shouldOutputVerboseDetails:
                    print(parseTree.pretty())
                print(
                    f"Card {cardName} ({cardPrettyPrint}) took {fullParseTimeEnd - fullParseTimeStart} to parse. The input had {len(ambiguities)} ambiguities. {ambiguityTreeSizeStatement}")
            except Exception as exception:
                firstLineOfException = str(exception).split('\n')[0]
                if shouldOutputVerboseDetails:
                    exception = str(exception)[0:200]
                    print(f"Card {cardName} ({cardPrettyPrint}) produced an exception during parsing: {exception}...")
                else:
                    print(
                        f"Card {cardName} ({cardPrettyPrint}) produced an exception during parsing: {firstLineOfException}...")
            if shouldOutputVerboseDetails:
                print("===================================================================================================")

    def test_MorseCodeTest(self):
        morseCodeGrammar = """
        start: (DOT | dash)+
        DOT: ("." | "•")
        dash: HYPHENMINUSDASH | MINUSDASH | FIGUREDASH | EMDASH
        HYPHENMINUSDASH: "-"
        MINUSDASH: "−"
        FIGUREDASH: "‒"
        EMDASH: "—"
        
        %import common.UCASE_LETTER -> UCASE_LETTER
        %import common.LCASE_LETTER -> LCASE_LETTER
        %import common.WORD -> WORD
        %import common.NEWLINE -> NEWLINE
        //%import common.NUMBER -> NUMBER
        %import common.SIGNED_NUMBER -> NUMBER
        %import common.WS -> WS
        %ignore WS
        """
        parser = lark.Lark(morseCodeGrammar, parser='earley', lexer='basic')
        messageA = ".-...-.-.-.-"
        messageB = "•—•••—•—•—•—"
        messageC = "•−•••−•−•−•−"
        print("Message parsed: {message}".format(message=parser.parse(messageA)))
        print("Message parsed: {message}".format(message=parser.parse(messageB)))
        print("Message parsed: {message}".format(message=parser.parse(messageC)))







if __name__ == '__main__':
    unittest.main()
