import unittest
from mtgcompiler.parsers.JsonParser import JsonParser

class TestFeatureParsingAndTransformation(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                #Because apparently we can't easily change the starting point of the parser after we
                #instantiate it, I'm putting specialized parsers here to save on setup time for these
                #unit tests.
                cls._keywordSequenceParser = JsonParser(startText="ability")
        
        def test_parseManaExpressions(self):
                jsonParser = JsonParser(startText="manaexpression")
                lp = jsonParser.getLarkParser()
                
                tf = jsonParser.getLarkTransformer()
                
                symbols_1 = "{W}{U}{B}{R}{G}"
                tree_1 = lp.parse(symbols_1)
                ast_1 = tf.transform(tree_1)
                
                symbols_2 = "{0}{2}{4}{8}{15}"
                tree_2 = lp.parse(symbols_2)
                ast_2 = tf.transform(tree_2)
                
                symbols_3 = "{2/W}{2/U}{2/B}{2/R}{2/G}"
                tree_3 = lp.parse(symbols_3)
                ast_3 = tf.transform(tree_3)
                
                symbols_4 = "{W/P}{U/P}{B/P}{R/P}{G/P}"
                tree_4 = lp.parse(symbols_4)
                ast_4 = tf.transform(tree_4)
                
                symbols_4 = "{G/W}{W/U}{U/B}{B/R}{R/G}"
                tree_4 = lp.parse(symbols_4)
                ast_4 = tf.transform(tree_4)
                
                symbols_5 = "{W/B}{U/R}{B/G}{G/U}{R/W}"
                tree_5 = lp.parse(symbols_5)
                ast_5 = tf.transform(tree_5)
                
                symbols_6 = "{S}{X}"
                tree_6 = lp.parse(symbols_6)
                ast_6 = tf.transform(tree_6)
                
                symbols_7 = "{HW}{HU}{HB}{HR}{HG}"
                tree_7 = lp.parse(symbols_7)
                ast_7 = tf.transform(tree_7)
                
                symbols_godEmperor = "{2}{U}{U}{B}{B}{R}{R}"
                tree_godEmperor = lp.parse(symbols_godEmperor)
                ast_godEmperor = tf.transform(tree_godEmperor)
                
        def test_parseTypeExpressions(self):
                jsonParser = JsonParser(startText="typeexpression")
                lp = jsonParser.getLarkParser()
                tf = jsonParser.getLarkTransformer()
                
                expr_1 = "creature"
                tree_1 = lp.parse(expr_1)
                ast_1 = tf.transform(tree_1)
                
                expr_2 = "legendary elf power-plant assembly-worker"
                tree_2 = lp.parse(expr_2)
                ast_2 = tf.transform(tree_2)
                
                expr_3 = "ajani planeswalker"
                tree_3 = lp.parse(expr_3)
                ast_3 = tf.transform(tree_3)
                
                expr_4 = "snow dragon artifact creature"
                tree_4 = lp.parse(expr_4)
                ast_4 = tf.transform(tree_4)
                
        def test_parseChampionAbility(self):
                lp = self._keywordSequenceParser.getLarkParser()
                tf = self._keywordSequenceParser.getLarkTransformer()
                kw_ability = "champion an elf"
                tree_ability = lp.parse(kw_ability)
                ast_ability = tf.transform(tree_ability)
                ast_ability.unparseToString()
                
        def test_parseLandwalkAbility(self):
                lp = self._keywordSequenceParser.getLarkParser()
                tf = self._keywordSequenceParser.getLarkTransformer()
                kw_ability = "legendary swampwalk"
                tree_ability = lp.parse(kw_ability)
                ast_ability = tf.transform(tree_ability)
                ast_ability.unparseToString()
        
        @unittest.expectedFailure
        def test_parsePartnerAbility(self):
                lp = self._keywordSequenceParser.getLarkParser()
                tf = self._keywordSequenceParser.getLarkTransformer()
                
                kw_ability_0 = "partner"
                tree_ability_0 = lp.parse(kw_ability_0)
                ast_ability_0 = tf.transform(tree_ability_0)
                ast_ability_0.unparseToString()
                
                kw_ability_1 = "partner with Proud Mentor"
                tree_ability_1 = lp.parse(kw_ability_1)
                ast_ability_1 = tf.transform(tree_ability_1)
                ast_ability_1.unparseToString()
                
                #This fails because the comma is a separator for a
                #keyword ability sequence, so it looks like two abilities.
                kw_ability_2 = "partner with Regna, the Redeemer"
                tree_ability_2 = lp.parse(kw_ability_2)
                ast_ability_2 = tf.transform(tree_ability_2)
                ast_ability_2.unparseToString()
                
        def test_parseAffinityAbility(self):
                lp = self._keywordSequenceParser.getLarkParser()
                tf = self._keywordSequenceParser.getLarkTransformer()
                
                kw_ability = "affinity for artifacts"
                tree_ability = lp.parse(kw_ability)
                ast_ability = tf.transform(tree_ability)
                ast_ability.unparseToString()
                
        def test_parseSpliceAbility(self):
                lp = self._keywordSequenceParser.getLarkParser()
                tf = self._keywordSequenceParser.getLarkTransformer()
                
                kw_ability = "splice onto arcane {1}{R}"
                tree_ability = lp.parse(kw_ability)
                ast_ability = tf.transform(tree_ability)
                ast_ability.unparseToString()
                
        def test_parseBandingAbility(self):
                lp = self._keywordSequenceParser.getLarkParser()
                tf = self._keywordSequenceParser.getLarkTransformer()
                
                kw_ability_0 = "banding"
                tree_ability_0 = lp.parse(kw_ability_0)
                ast_ability_0 = tf.transform(tree_ability_0)
                ast_ability_0.unparseToString()
                
                kw_ability_1 = "bands with other creatures named Wolves of the Hunt"
                tree_ability_1 = lp.parse(kw_ability_1)
                ast_ability_1 = tf.transform(tree_ability_1)
                ast_ability_1.unparseToString()
                
                kw_ability_2 = "bands with other legendary creatures"
                tree_ability_2 = lp.parse(kw_ability_1)
                ast_ability_2 = tf.transform(tree_ability_1)
                ast_ability_2.unparseToString()
                
        def test_parseHexproofAbility(self):
                lp = self._keywordSequenceParser.getLarkParser()
                tf = self._keywordSequenceParser.getLarkTransformer()
                
                kw_ability_0 = "hexproof"
                tree_ability_0 = lp.parse(kw_ability_0)
                ast_ability_0 = tf.transform(tree_ability_0)
                ast_ability_0.unparseToString()
                
                kw_ability_1 = "hexproof from black"
                tree_ability_1 = lp.parse(kw_ability_1)
                ast_ability_1 = tf.transform(tree_ability_1)
                ast_ability_1.unparseToString()
                
                kw_ability = "hexproof from black"
                tree_ability = lp.parse(kw_ability)
                print(tree_ability)
                ast_ability = tf.transform(tree_ability)
                print(ast_ability.unparseToString())
                
        def test_parseProtectionAbility(self):
                lp = self._keywordSequenceParser.getLarkParser()
                tf = self._keywordSequenceParser.getLarkTransformer()
                
                kw_ability_0 = "protection from creatures"
                tree_ability_0 = lp.parse(kw_ability_0)
                ast_ability_0 = tf.transform(tree_ability_0)
                ast_ability_0.unparseToString()
                
                kw_ability_1 = "protection from green and from blue"
                tree_ability_1 = lp.parse(kw_ability_1)
                ast_ability_1 = tf.transform(tree_ability_1)
                ast_ability_1.unparseToString()
                
        def test_parseKeywordList(self):
                lp = self._keywordSequenceParser.getLarkParser()
                tf = self._keywordSequenceParser.getLarkTransformer()
                
                kw_ability_0 = "haste, first strike, trample"
                tree_ability_0 = lp.parse(kw_ability_0)
                ast_ability_0 = tf.transform(tree_ability_0)
                ast_ability_0.unparseToString()
                
                kw_ability_0 = "defender; reach (this creature can block creatures with flying.)"
                tree_ability_0 = lp.parse(kw_ability_0)
                ast_ability_0 = tf.transform(tree_ability_0)
                ast_ability_0.unparseToString()
                
                
                
        def test_parseKeywordAbility(self):
                lp = self._keywordSequenceParser.getLarkParser()
                tf = self._keywordSequenceParser.getLarkTransformer()
                
                kw_ability = "haste, first strike, trample"
                #kw_ability = "haste, first strike"
                tree_ability = lp.parse(kw_ability)
                print(tree_ability)
                ast_ability = tf.transform(tree_ability)
                print(ast_ability.unparseToString())
                

                
        
if __name__ == '__main__':
    unittest.main()