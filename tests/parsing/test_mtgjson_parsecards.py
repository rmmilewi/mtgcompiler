import unittest
from mtgcompiler.parsers.JsonParser import JsonParser
from lark.tree import pydot__tree_to_png #For rendering the parse tree.
import mtgcompiler.support.inspection as inspection
import mtgcompiler.support.binding as binding

class TestParseCards(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                cls._parser = JsonParser()
        
        def test_parseDiligentFarmhand(self):
                return None
                farmhand = {
                "artist": "Gary Ruddell",
                "cmc": 1,
                "colorIdentity": [
                "G"
                ],
                "colors": [
                "Green"
                ],
                "id": "f8f6dcec4ee1e8192183f0c6ec30f6376e97e8ec",
                "imageName": "diligent farmhand",
                "layout": "normal",
                "manaCost": "{G}",
                "mciNumber": "237",
                "multiverseid": 29773,
                "name": "Diligent Farmhand",
                "number": "237",
                "power": "1",
                "rarity": "Common",
                "subtypes": [
                "Human",
                "Druid"
                ],
                "text": "{1}{G}, Sacrifice Diligent Farmhand: Search your library for a basic land card and put that card onto the battlefield tapped. Then shuffle your library.\nIf Diligent Farmhand is in a graveyard, effects from spells named 'Muscle Burst' count it as a card named 'Muscle Burst'.",
                "toughness": "1",
                "type": "Creature — Human Druid",
                "types": [
                "Creature"
                ]
                }
                card = self._parser.parse(farmhand)
                print(card.unparseToString())
                #tree = larkparser.parse("first strike, double strike, bushido 5 (this is reminder text)")
                #print(tree)
                #pydot__tree_to_png(tree, "lark_test.png")
                #out = transformer.transform(tree)
                #print(out)
                #quit()
                
        def test_parseRodOfRuin(self):
                rod = {
                "artist": "Christopher Rush",
                "cmc": 4,
                "id": "5d8d4a22f3bf86232a1984a3ea978b88cd8faa4e",
                "imageName": "rod of ruin",
                "layout": "normal",
                "manaCost": "{4}",
                "mciNumber": "268",
                "multiverseid": 39,
                "name": "Rod of Ruin",
                "rarity": "Uncommon",
                "text": "{3}, {T}: Rod of Ruin deals 1 damage to any target.",
                "type": "Artifact",
                "types": [
                  "Artifact"
                ]
                }
                card = self._parser.parse(rod)
                card.unparseToString()
                
                #binding.bindNameReferences(card)
                #visitor = inspection.SimpleGraphingVisitor(path="rodOfRuin.dot")
                #visitor.traverse(card)
                
        def test_parseWeightOfSpires(self):
                
                weightOfSpires = {
                "artist": "Michael Sutfin",
                "cmc": 1,
                "colorIdentity": [
                "R"
                ],
                "colors": [
                "Red"
                ],
                "flavor": "\"Finally, a good use for an Azorius courthouse.\"\n—Ghut Rak, Gruul guildmage",
                "id": "bd55a199f44b3b36355944abe920cfe67185ac18",
                "imageName": "weight of spires",
                "layout": "normal",
                "manaCost": "{R}",
                "mciNumber": "78",
                "multiverseid": 107551,
                "name": "Weight of Spires",
                "number": "78",
                "rarity": "Uncommon",
                "text": "Weight of Spires deals damage to target creature equal to the number of nonbasic lands that creature's controller controls.",
                "type": "Instant",
                "types": [
                "Instant"
                ]
                }
                card = self._parser.parse(weightOfSpires)
                print(card.unparseToString())
                
                
        def test_parseForest(self):
                return None
                forest = {
                "artist": "Christopher Rush",
                "cmc": 0,
                "colorIdentity": [
                  "G"
                ],
                "id": "f26c7fce5324a8906f28e05728dd1209e39e1979",
                "imageName": "forest2",
                "layout": "normal",
                "multiverseid": 586,
                "name": "Forest",
                "rarity": "Basic Land",
                "subtypes": [
                  "Forest"
                ],
                "supertypes": [
                  "Basic"
                ],
                "type": "Basic Land — Forest",
                "types": [
                  "Land"
                ],
                "variations": [
                  588,
                  587
                ]
                }
                card = self._parser.parse(forest)
                card.unparseToString()
                
        def test_parseLance(self):
                lance = {
                "artist": "Rob Alexander",
                "cmc": 1,
                "colorIdentity": [
                "W"
                ],
                "colors": [
                "White"
                ],
                "id": "7171f2d311b9726693a7c8c9d18cfedd8635bb83",
                "imageName": "lance",
                "layout": "normal",
                "manaCost": "{W}",
                "mciNumber": "213",
                "multiverseid": 554,
                "name": "Lance",
                "rarity": "Uncommon",
                "subtypes": [
                "Aura"
                ],
                "text": "Enchant creature\nEnchanted creature has first strike.",
                "type": "Enchantment — Aura",
                "types": [
                "Enchantment"
                ]
                }
                card = self._parser.parse(lance)
                card.unparseToString()
                
        
        def test_parseMurder(self):
                return None
                murder =  {
                "artist": "Allen Williams",
                "cmc": 3,
                "colorIdentity": [
                "B"
                ],
                "colors": [
                "Black"
                ],
                "flavor": "\"No matter how busy my schedule gets, I always try to take time for that personal touch.\"\n—Queen Marchesa",
                "id": "abd79ed74b15bee1f7197289ebfc505dc71a7afd",
                "imageName": "murder",
                "layout": "normal",
                "manaCost": "{1}{B}{B}",
                "mciNumber": "98",
                "multiverseid": 442087,
                "name": "Murder",
                "number": "98",
                "rarity": "Common",
                "text": "Destroy target creature.",
                "type": "Instant",
                "types": [
                "Instant"
                ],
                "watermark": "Magic 2013"
                }
                card = self._parser.parse(murder)
                card.unparseToString()
                
                
        def test_parseAncientSpider(self):
                return None
                ancientSpider = {
                  "artist": "Greg Staples",
                  "cmc": 4,
                  "colorIdentity": [
                    "W",
                    "G"
                  ],
                  "colors": [
                    "White",
                    "Green"
                  ],
                  "flavor": "It outlived both king and castle.",
                  "id": "e71d05b4f58a17873379ac0e5ba5fc879b9dbd07",
                  "imageName": "ancient spider",
                  "layout": "normal",
                  "manaCost": "{2}{G}{W}",
                  "mciNumber": "96",
                  "multiverseid": 19149,
                  "name": "Ancient Spider",
                  "number": "96",
                  "power": "2",
                  "rarity": "Rare",
                  "subtypes": [
                    "Spider"
                  ],
                  "text": "First strike; reach (This creature can block creatures with flying.)",
                  "toughness": "5",
                  "type": "Creature — Spider",
                  "types": [
                    "Creature"
                  ]
                }
                
                card = self._parser.parse(ancientSpider)
                card.unparseToString()
                
if __name__ == '__main__':
        unittest.main()
        
                
        
        