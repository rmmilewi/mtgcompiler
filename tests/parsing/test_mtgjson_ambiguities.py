import unittest
import time
import mtgcompiler.midend.support.inspection as inspection
import mtgcompiler.midend.support.binding as binding
import mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonCompiler as MtgJsonCompiler
import pytest
import lark.lexer

class SlayingAmbiguities(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        compiler = MtgJsonCompiler.MtgJsonCompiler(options={"parser.startRule": "cardtext",
                                                            "parser.larkDebug": True,
                                                            "parser.larkParser" : "earley",
                                                            "parser.strict" : True,
                                                            "parser.ambiguity" : "explicit"
                                                            })
        parser = compiler.getParser()
        preprocessor = compiler.getPreprocessor()
        cls._parser = parser
        cls._preprocessor = preprocessor

    def test_ambiguities_permanentsWithIrregularNames(self):
        cardData = {
            "object": "card",
            "name": "Target's Demise",
            "manaCost": "{B}{B}",
            "type": "Instant",
            "oracle_text": "Sacrifice a permanent named Target Creature",
            "flavor" : "Who would name their child Target Creature?"
        }
        preprocessedText = self._preprocessor.prelex(cardData['oracle_text'], None, cardData['name'])
        parseTree = self._parser.parse(preprocessedText)
        ambiguities = list(parseTree.find_data("_ambig"))
        print(f"test_permanentsWithIrregularNames: {cardData['name']} has {len(ambiguities)} ambiguities.")
        self.assertEqual(len(ambiguities), 0)

    def test_ambiguities_CounterCounters(self):
        cardData = {
            "object": "card",
            "name": "",
            "manaCost": "{U}{U}{U}",
            "type": "Creature — Beast",
            "oracle_text": "{U}{U}{2}, {T}: Counter target spell. If a spell is countered this way, put a spell counter on this creature.\nIf this creature has three or more spell counters on it, spells you cast can't be countered.",
        }
        preprocessedText = self._preprocessor.prelex(cardData['oracle_text'], None, cardData['name'])
        parseTree = self._parser.parse(preprocessedText)
        ambiguities = list(parseTree.find_data("_ambig"))
        print(f"test_CounterCounters: {cardData['name']} has {len(ambiguities)} ambiguities.")
        self.assertEqual(len(ambiguities), 0)



if __name__ == '__main__':
    unittest.main()
