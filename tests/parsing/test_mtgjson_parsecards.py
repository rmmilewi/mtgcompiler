import unittest
from mtgcompiler.parsers.JsonParser import JsonParser
from lark.tree import pydot__tree_to_png #For rendering the parse tree.
import mtgcompiler.support.inspection as inspection
import mtgcompiler.support.binding as binding

class TestParseCards(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                cls._parser = JsonParser()
                
        def test_parseSailorOfMeans(self):
                sailor =  {
                "artist": "Ryan Pancoast",
                "cmc": 3,
                "colorIdentity": [
                "U"
                ],
                "colors": [
                "Blue"
                ],
                "flavor": "In the Brazen Coalition, the wheels of business are greased with plunder.",
                "id": "3df51b5a6b42b34f836a533677dd22977208ec3d",
                "imageName": "sailor of means",
                "layout": "normal",
                "manaCost": "{2}{U}",
                "mciNumber": "73",
                "multiverseid": 435225,
                "name": "Sailor of Means",
                "number": "73",
                "power": "1",
                "rarity": "Common",
                "subtypes": [
                "Human",
                "Pirate"
                ],
                "text": "When Sailor of Means enters the battlefield, create a colorless Treasure artifact token with \"{T}, Sacrifice this artifact: Add one mana of any color.\"",
                "toughness": "4",
                "type": "Creature — Human Pirate",
                "types": [
                "Creature"
                ]
                }
                card = self._parser.parse(sailor)
                print(card.unparseToString())
                
        def test_parseRodOfRuin(self):
                return None
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
                return None
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
                return None
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
        
                
        
        