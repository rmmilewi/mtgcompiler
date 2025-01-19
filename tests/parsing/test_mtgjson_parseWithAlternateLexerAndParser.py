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
        shouldOutputVerboseDetails = True #Enables printing of lexer results and parse trees.
        useRevisedGrammar = True #Set to False if you want to see how much progress we made over the original grammar
        testAgainstFoundations = True #Set to True if you want to run against all the cards in the Foundations set, False for custom list of strings
        lexerTypeToUse = "basic" #Note: If using the original grammar, lexing will always be done in dynamic mode.
        skipCardsThatPreviouslyPassed = True #When testing against Foundations cards, output a file with a list of cards that previously passed, and skip those that passed before.

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

        if testAgainstFoundations and skipCardsThatPreviouslyPassed:
            if os.path.exists("tests/parsing/foundationsPassedCardList.tmp"):
                passedCardsFile = open("tests/parsing/foundationsPassedCardList.tmp","r+",encoding='utf-8')
                passedCardsList = [cardName.rstrip('\n') for cardName in passedCardsFile.readlines()]
            else:
                passedCardsFile = open("tests/parsing/foundationsPassedCardList.tmp", "w", encoding='utf-8')
                passedCardsList = []

        compilerUsingIntegratedGrammar = MtgJsonCompiler.MtgJsonCompiler(
            options={"parser.overrideGrammar": integratedGrammar,
                     "parser.startRule": "cardtext",
                     "parser.ambiguity": "explicit",
                     "parser.larkLexer": lexerType,
                     })
        parser = compilerUsingIntegratedGrammar.getParser()
        preprocessor = compilerUsingIntegratedGrammar.getPreprocessor()
        cardsToTest = [
            ("Joust Through Snippet", "~ deals 3 damage to target attacking or blocking creature."),
            ("Bant Snippet", "Put a divinity counter on target green, white, or blue creature."),
            ("Luminous Rebuke Snippet", "This spell costs {3} less to cast if it targets a tapped creature. Destroy target creature."),
            ("Math expression test 6", "Draw up to two cards."),
            ("Math expression test 5", "~ deals 2 damage divided as you choose among one or two targets."),
            ("Math expression test 4", "Roll a d20 and subtract the number of cards in your hand."),
            ("Math expression test 3", "It deals that much damage minus 1 to that permanent or player."),
            ("Math expression test 2", "X is 1 plus the number of cards named ~ in your graveyard."),
            ("Math expression test 1","You gain life equal to that creature's toughness."),
            ("Hare Apparent Snippet", "Create a number of 1/1 white Rabbit creature tokens equal to the number of other creatures you control named ~."),
            ("Divine Resilience Snippet","If this spell was kicked, instead any number of target creatures you control gain indestructible until end of turn."),
            ("Crystal Barricade Snippet","Prevent all noncombat damage that would be dealt to other creatures you control."),
            ("Celestial Armor Snippet", "That creature gains hexproof and indestructible until end of turn."),
            ("Claws Out Snippet","This spell costs {1} less to cast."),
            ("Felidar Savior Snippet","Put a +1/+1 counter on each of up to two other target creatures you control.")
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
            print(f"There are {len(unique_cards)} unique cards in the set.")
            for name in unique_cards:
                cardDict = unique_cards[name]
                if "text" in cardDict:
                    preprocessedText = preprocessor.prelex(cardDict['text'], None, name)
                    cardsToTest.append((name,preprocessedText))
        print("Total card texts to test against: {total}".format(total=len(cardsToTest)))
        def getLexerResults(card,name):
            lexerState = lark.lexer.LexerState(text=card, line_ctr=lark.lexer.LineCounter(
                b'\n' if isinstance(card, bytes) else '\n'))
            lexTimeStart = time.time()
            lexerResults = parser.parser.lexer.lex(state=lexerState, parser_state=None)
            lexTimeEnd = time.time()
            print(f"Card {name} ({card}) took {lexTimeEnd - lexTimeStart} to lex.")
            for token in lexerResults:
                print(f"{token} ({token.type}) ",end='')
            print("\n")

        for i in range(len(cardsToTest)):
            cardName,card = cardsToTest[i]
            if testAgainstFoundations and skipCardsThatPreviouslyPassed:
                if cardName in passedCardsList:
                    print(f"Skipping {cardName} ({i}/{len(cardsToTest)})")
                    continue
            print("===================================================================================================")
            print(f"Parsing {cardName} ({i}/{len(cardsToTest)})...")
            cardPrettyPrint = card.replace('\n', ' ')
            try:
                if shouldOutputVerboseDetails and lexerType != "dynamic":
                    getLexerResults(card,cardName)
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
                print(f"Card {cardName} ({cardPrettyPrint}) took {fullParseTimeEnd - fullParseTimeStart} to parse. The input had {len(ambiguities)} ambiguities. {ambiguityTreeSizeStatement}")
                if testAgainstFoundations and skipCardsThatPreviouslyPassed:
                    passedCardsList.append(cardName)
                    passedCardsFile.write(f"{cardName}\n")
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
