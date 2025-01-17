import unittest
from mtgcompiler.frontend.JsonParser import JsonParser
from lark.tree import pydot__tree_to_png #For rendering the parse tree.
import mtgcompiler.midend.support.inspection as inspection
import mtgcompiler.midend.support.binding as binding
import mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonCompiler as MtgJsonCompiler

class TestParseCards(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                # options = {"rulestextonly": True}
                # cls._parser = JsonParser(options)
                compiler = MtgJsonCompiler.MtgJsonCompiler(options={"parser.startRule": "cardtext", "parser.larkDebug": True})
                parser = compiler.getParser()
                preprocessor = compiler.getPreprocessor()
                cls._parser = parser
                cls._preprocessor = preprocessor


        def test_IxalansBinding(self):
                data = {
                  "object": "card",
                  "id": "5f3c8c31-ceb8-4a2c-beb6-0ff5f7b6ae07",
                  "name": "Ixalan's Binding",
                  "mana_cost": "{3}{W}",
                  "cmc": 4.0,
                  "type_line": "Enchantment",
                  "oracle_text": "When Ixalan's Binding enters, exile target nonland permanent an opponent controls until Ixalan's Binding leaves the battlefield.\nYour opponents can't cast spells with the same name as the exiled card.",
                  "colors": [
                    "W"
                  ],
                  "color_identity": [
                    "W"
                  ]}
                preprocessed = self._preprocessor.prelex(data['oracle_text'], None, data['name'])
                # print(preprocessed)
                card = self._parser.parse(preprocessed)
        
        
        def test_parseCard(self):
                data = {
                "artist": "Jesper Ejsing",
                "cmc": 2,
                "colorIdentity": [
                "G"
                ],
                "colors": [
                "Green"
                ],
                "flavor": "Bulgo paused, puzzled. What was that rustling sound, and why did he feel so stiff? And how could his feet be so thirsty?",
                "id": "014d5a7aeac4a85cfee4e3811969d0de6118a5cf",
                "imageName": "lignify",
                "layout": "normal",
                "manaCost": "{1}{G}",
                "mciNumber": "16",
                "multiverseid": 201837,
                "name": "Lignify",
                "number": "16",
                "rarity": "Common",
                "subtypes": [
                "Treefolk",
                "Aura"
                ],
                "text": "Enchant creature\nEnchanted creature is a Treefolk with base power and toughness 0/4 and loses all abilities.",
                "type": "Tribal Enchantment — Treefolk Aura",
                "types": [
                "Tribal",
                "Enchantment"
                ]
                }
                card = self._parser.parse(data)
                
        def test_parseFireball(self):
                data = {
                "artist": "Dave Dorman",
                "cmc": 1,
                "colorIdentity": [
                "R"
                ],
                "colors": [
                "Red"
                ],
                "id": "f7150866ae484cdcea299da715e6c5ae0612c7cf",
                "imageName": "fireball",
                "layout": "normal",
                "manaCost": "{X}{R}",
                "mciNumber": "136",
                "multiverseid": 191076,
                "name": "Fireball",
                "number": "136",
                "rarity": "Uncommon",
                "text": "This spell costs {1} more to cast for each target beyond the first.\nFireball deals X damage divided evenly, rounded down, among any number of targets.",
                "type": "Sorcery",
                "types": [
                "Sorcery"
                ]
                }
                card = self._parser.parse(data)
                
                
        def test_parseJaceBeleren(self):
                jace = {
                "artist": "Aleksi Briclot",
                "cmc": 3,
                "colorIdentity": [
                "U"
                ],
                "colors": [
                "Blue"
                ],
                "id": "5e898f919d238471eb26b8b740890324b15402b1",
                "imageName": "jace beleren",
                "layout": "normal",
                "loyalty": 3,
                "manaCost": "{1}{U}{U}",
                "mciNumber": "15",
                "name": "Jace Beleren",
                "number": "15",
                "rarity": "Special",
                "releaseDate": "2009-01-27",
                "subtypes": [
                "Jace"
                ],
                "supertypes": [
                "Legendary"
                ],
                "text": "+2: Each player draws a card.\n−1: Target player draws a card.\n−10: Target player puts the top twenty cards of his or her library into his or her graveyard.",
                "type": "Legendary Planeswalker — Jace",
                "types": [
                "Planeswalker"
                ]
                }
                card = self._parser.parse(jace)
                
                
        def test_parseMerfolkLooter(self):
                looter = {
                "artist": "Austin Hsu",
                "cmc": 2,
                "colorIdentity": [
                "U"
                ],
                "colors": [
                "Blue"
                ],
                "flavor": "Merfolk don't always know what they're looking for, but they're certain once they find it.",
                "id": "ca32a0384ba4357a9f792d0388fd0a02e61034d4",
                "imageName": "merfolk looter",
                "layout": "normal",
                "manaCost": "{1}{U}",
                "mciNumber": "61",
                "multiverseid": 413603,
                "name": "Merfolk Looter",
                "number": "61",
                "power": "1",
                "rarity": "Uncommon",
                "subtypes": [
                "Merfolk",
                "Rogue"
                ],
                "text": "{T}: Draw a card, then discard a card.",
                "toughness": "1",
                "type": "Creature — Merfolk Rogue",
                "types": [
                "Creature"
                ]
                }
                card = self._parser.parse(looter)
                print(card)
                
        def test_parseBabyJace(self):
                baby = {
                "manaCost": "{U}",
                "name": "Jace, Baby",
                "rarity": "Rare",
                "text": "+2: Each player draws a card.\n−1: Target player draws a card.",
                "type": "Planeswalker",
                "loyalty": 1,
                "types": [
                  "Planeswalker"
                ]
                }
                card = self._parser.parse(baby)
                
                
        def test_parseAncestralIteration(self):
                # return None
                iteration = {
                "manaCost": "{U}",
                "name": "Ancestral Iteration",
                "rarity": "Rare",
                "text": "Draw a card.\nDraw a card.\nDraw a card.",
                "type": "Instant",
                "types": [
                  "Instant"
                ]
                }
                card = self._parser.parse(iteration)
                
                
        def test_parseBountifulHarvest(self):
                return None
                harvest = {
                "artist": "Jason Chan",
                "cmc": 5,
                "colorIdentity": [
                  "G"
                ],
                "colors": [
                  "Green"
                ],
                "flavor": "\"When we fail to see the beauty in every tree, we are no better than humans.\"\n—Saelia, elvish scout",
                "id": "2d1a1ad709cdef0059708e2f5ef592554e98a538",
                "imageName": "bountiful harvest",
                "layout": "normal",
                "manaCost": "{4}{G}",
                "mciNumber": "163",
                "multiverseid": 278074,
                "name": "Bountiful Harvest",
                "number": "163",
                "rarity": "Common",
                #"text": "You gain 1 life for each land you control.",
                "text": "For each land you control, you gain 1 life.",
                "type": "Sorcery",
                "types": [
                  "Sorcery"
                ]
                }
                card = self._parser.parse(harvest)
                
                
        def test_parseBlackLotus(self):
                # return None
                lotus = {
                "artist": "Chris Rahn",
                "cmc": 0,
                "id": "6ad6463d56da447ab490a1a2b2b8a18759befc5f",
                "imageName": "black lotus",
                "layout": "normal",
                "manaCost": "{0}",
                "mciNumber": "4",
                "multiverseid": 382866,
                "name": "Black Lotus",
                "number": "4",
                "rarity": "Special",
                "reserved": True,
                "text": "{T}, Sacrifice Black Lotus: Add three mana of any one color.",
                "type": "Artifact",
                "types": [
                  "Artifact"
                ]
                }
                card = self._parser.parse(lotus)
                print(card.unparseToString())
                visitor = inspection.SimpleGraphingVisitor(path="blacklotus.dot")
                visitor.traverse(card)
                
        def test_parseSailorOfMeans(self):
                return None
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
                visitor = inspection.SimpleGraphingVisitor(path="sailorOfMeans.dot")
                visitor.traverse(card)
                
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
        
                
        
        
