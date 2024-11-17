import unittest,json, traceback
from tqdm import tqdm
import mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonCompiler as MtgJsonCompiler
from multiprocessing import Pool
import zipfile

from collections import Counter

def loadAllSets(fname="tests/parsing/AllPrintings.json"):
        with zipfile.ZipFile(fname+".zip", 'r') as zip_ref:
                zip_ref.extractall("tests/parsing/")
        with open(fname, encoding='utf-8') as f:
                data = json.load(f)
                return data["data"] # in latest AllPrintings files, set data is under the 'data' prop

totalCardsParsed = 0
totalCardsAttempted = 0
parsednames = set()

workerParser = None
workerPreprocessor = None
def parseWorker(cardDict):
        global workerParser
        global workerPreprocessor
        preprocessed = None
        if workerParser == None:
                options = {"parseonly": True, "rulestextonly": True}
                # compiler = MtgJsonCompiler.MtgJsonCompiler()
                compiler = MtgJsonCompiler.MtgJsonCompiler(options={"parser.startRule": "cardtext", "parser.larkDebug": True})
                workerParser = compiler.getParser()
                workerPreprocessor = compiler.getPreprocessor()
        if 'name' in cardDict:
                name = cardDict['name']
                if " // " in cardDict['name']:
                        # print('double sided card')
                        # print(name)
                        # double sided card, use faceName
                        name = cardDict['faceName']
        else:
                name = None
        try:
                # print(cardDict['text'])
                preprocessed = workerPreprocessor.prelex(cardDict['text'], None, name)
                # print(preprocessed)
                card = workerParser.parse(preprocessed)
                print("SUCCESS:",name)
                return name, True
        except Exception as e:
                print("FAILURE:",name)
                print(preprocessed)
                print(e)
                # traceback.print_exc()
                return name,False

class TestSetParsing(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
                cls._sets = loadAllSets()
                #cls._parser = MtgJsonCompiler()
                cls._parsednames = set()
        
        @classmethod
        def tearDownClass(cls):
                global totalCardsParsed, totalCardsAttempted, parsednames
                print("Total MtgJsonCompiler parser support for Magic cards: {0} / {1} ({2}%)".format(totalCardsParsed,totalCardsAttempted,totalCardsParsed/totalCardsAttempted))
                print("{0} unique cards parsed.".format(len(parsednames)))
        def parseCards(self,mset):
                global totalCardsParsed, totalCardsAttempted, parsednames
                # Count occurrences of each name
                # Helper function to get unique card names considering 'faceName' for split cards
                def get_unique_name(card):
                        if 'faceName' in card:
                                return card['faceName']
                        return card['name']

                # Count unique cards based on this adjusted logic
                unique_cards = {get_unique_name(card): card for card in mset['cards'] if not get_unique_name(card).startswith("A-")}

                # Ensure the filtered list matches the base set size
                uniqueCards = list(unique_cards.values())
                print("\n".join(sorted([get_unique_name(card) for card in uniqueCards])))
                print(f"Parsing set {mset['name']} with {len(uniqueCards)} cards")
                numberOfCards = len(uniqueCards)
                cardsParsed = 0
                with Pool(processes=8) as pool:
                        for res in tqdm(pool.imap_unordered(parseWorker,uniqueCards)):
                                name,parsed = res
                                if parsed == True:
                                        if name not in self._parsednames:
                                                self._parsednames.add(name)
                                        cardsParsed += 1
                                        totalCardsParsed += 1
                                        totalCardsAttempted += 1
                                else:
                                        totalCardsAttempted += 1
                return cardsParsed,numberOfCards

        def test_KHM(self):
                mset = self._sets["KHM"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Kaldheim: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ELD(self):
                mset = self._sets["ELD"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Throne of Eldraine: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pWOS(self):
                mset = self._sets["pWOS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Wizards of the Coast Online Store: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pWOR(self):
                mset = self._sets["pWOR"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Worlds: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pWCQ(self):
                mset = self._sets["pWCQ"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for World Magic Cup Qualifiers: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pSUS(self):
                mset = self._sets["pSUS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Super Series: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pSUM(self):
                mset = self._sets["pSUM"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Summer of Magic: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pREL(self):
                mset = self._sets["pREL"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Release Events: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pPRO(self):
                mset = self._sets["pPRO"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Pro Tour: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pPRE(self):
                mset = self._sets["pPRE"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Prerelease Events: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pPOD(self):
                mset = self._sets["pPOD"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Portal Demo Game: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pMPR(self):
                mset = self._sets["pMPR"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic Player Rewards: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pMGD(self):
                mset = self._sets["pMGD"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic Game Day: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pMEI(self):
                mset = self._sets["pMEI"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Media Inserts: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pLPA(self):
                mset = self._sets["pLPA"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Launch Parties: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pLGM(self):
                mset = self._sets["pLGM"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Legend Membership: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pJGP(self):
                mset = self._sets["pJGP"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Judge Gift Program: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pHHO(self):
                mset = self._sets["pHHO"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Happy Holidays: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pWPN(self):
                mset = self._sets["pWPN"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Wizards Play Network: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pGTW(self):
                mset = self._sets["pGTW"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Gateway: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pGRU(self):
                mset = self._sets["pGRU"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Guru: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pGPX(self):
                mset = self._sets["pGPX"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Grand Prix: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pFNM(self):
                mset = self._sets["pFNM"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Friday Night Magic: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pELP(self):
                mset = self._sets["pELP"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for European Land Program: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pDRC(self):
                mset = self._sets["pDRC"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Dragon Con: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pCMP(self):
                mset = self._sets["pCMP"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Champs and States: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pCEL(self):
                mset = self._sets["pCEL"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Celebration: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pARL(self):
                mset = self._sets["pARL"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Arena League: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_pALP(self):
                mset = self._sets["pALP"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Asia Pacific Land Program: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_p2HG(self):
                mset = self._sets["p2HG"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Two-Headed Giant Tournament: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_p15A(self):
                mset = self._sets["p15A"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for 15th Anniversary: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_PD3(self):
                mset = self._sets["PD3"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Premium Deck Series: Graveborn: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_PD2(self):
                mset = self._sets["PD2"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Premium Deck Series: Fire and Lightning: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_H09(self):
                mset = self._sets["H09"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Premium Deck Series: Slivers: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_PTK(self):
                mset = self._sets["PTK"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Portal Three Kingdoms: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_POR(self):
                mset = self._sets["POR"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Portal: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_PO2(self):
                mset = self._sets["PO2"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Portal Second Age: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_PCA(self):
                mset = self._sets["PCA"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Planechase Anthology: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_PC2(self):
                mset = self._sets["PC2"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Planechase 2012 Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_HOP(self):
                mset = self._sets["HOP"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Planechase: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_VMA(self):
                mset = self._sets["VMA"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Vintage Masters: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MMA(self):
                mset = self._sets["MMA"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Modern Masters: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MM3(self):
                mset = self._sets["MM3"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Modern Masters 2017 Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MM2(self):
                mset = self._sets["MM2"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Modern Masters 2015 Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MED(self):
                mset = self._sets["MED"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Masters Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ME4(self):
                mset = self._sets["ME4"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Masters Edition IV: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ME3(self):
                mset = self._sets["ME3"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Masters Edition III: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ME2(self):
                mset = self._sets["ME2"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Masters Edition II: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_IMA(self):
                mset = self._sets["IMA"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Iconic Masters: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_EMA(self):
                mset = self._sets["EMA"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Eternal Masters: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_A25(self):
                mset = self._sets["A25"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Masters 25: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MPS_AKH(self):
                mset = self._sets["MPS_AKH"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Masterpiece Series: Amonkhet Invocations: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MPS(self):
                mset = self._sets["MPS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Masterpiece Series: Kaladesh Inventions: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_EXP(self):
                mset = self._sets["EXP"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Zendikar Expeditions: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_GS1(self):
                mset = self._sets["GS1"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Global Series: Jiang Yanggu and Mu Yanling: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_E02(self):
                mset = self._sets["E02"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Explorers of Ixalan: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_V17(self):
                mset = self._sets["V17"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for From the Vault: Transform: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_V16(self):
                mset = self._sets["V16"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for From the Vault: Lore: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_V15(self):
                mset = self._sets["V15"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for From the Vault: Angels: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_V14(self):
                mset = self._sets["V14"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for From the Vault: Annihilation (2014): {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_V13(self):
                mset = self._sets["V13"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for From the Vault: Twenty: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_V12(self):
                mset = self._sets["V12"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for From the Vault: Realms: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_V11(self):
                mset = self._sets["V11"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for From the Vault: Legends: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_V10(self):
                mset = self._sets["V10"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for From the Vault: Relics: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_V09(self):
                mset = self._sets["V09"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for From the Vault: Exiled: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_SS1(self):
                mset = self._sets["SS1"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Signature Spellbook: Jace: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DRB(self):
                mset = self._sets["DRB"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for From the Vault: Dragons: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_EVG(self):
                mset = self._sets["EVG"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Elves vs. Goblins: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDU(self):
                mset = self._sets["DDU"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Elves vs. Inventors: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDT(self):
                mset = self._sets["DDT"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Merfolk vs. Goblins: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDS(self):
                mset = self._sets["DDS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Mind vs. Might: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDR(self):
                mset = self._sets["DDR"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Nissa vs. Ob Nixilis: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDQ(self):
                mset = self._sets["DDQ"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Blessed vs. Cursed: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDP(self):
                mset = self._sets["DDP"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Zendikar vs. Eldrazi: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDO(self):
                mset = self._sets["DDO"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Elspeth vs. Kiora: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDN(self):
                mset = self._sets["DDN"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Speed vs. Cunning: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDM(self):
                mset = self._sets["DDM"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Jace vs. Vraska: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDL(self):
                mset = self._sets["DDL"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Heroes vs. Monsters: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDK(self):
                mset = self._sets["DDK"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Sorin vs. Tibalt: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDJ(self):
                mset = self._sets["DDJ"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Izzet vs. Golgari: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDI(self):
                mset = self._sets["DDI"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Venser vs. Koth: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDH(self):
                mset = self._sets["DDH"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Ajani vs. Nicol Bolas: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDG(self):
                mset = self._sets["DDG"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Knights vs. Dragons: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDF(self):
                mset = self._sets["DDF"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Elspeth vs. Tezzeret: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDE(self):
                mset = self._sets["DDE"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Phyrexia vs. the Coalition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDD(self):
                mset = self._sets["DDD"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Garruk vs. Liliana: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DDC(self):
                mset = self._sets["DDC"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Divine vs. Demonic: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DD3_JVC(self):
                mset = self._sets["DD3_JVC"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks Anthology, Jace vs. Chandra: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DD3_GVL(self):
                mset = self._sets["DD3_GVL"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks Anthology, Garruk vs. Liliana: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DD3_EVG(self):
                mset = self._sets["DD3_EVG"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks Anthology, Elves vs. Goblins: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DD3_DVD(self):
                mset = self._sets["DD3_DVD"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks Anthology, Divine vs. Demonic: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DD2(self):
                mset = self._sets["DD2"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duel Decks: Jace vs. Chandra: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CNS(self):
                mset = self._sets["CNS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic: The Gathering—Conspiracy: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CN2(self):
                mset = self._sets["CN2"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Conspiracy: Take the Crown: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CMD(self):
                mset = self._sets["CMD"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic: The Gathering-Commander: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CMA(self):
                mset = self._sets["CMA"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Commander Anthology: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CM2(self):
                mset = self._sets["CM2"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Commander Anthology 2018: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CM1(self):
                mset = self._sets["CM1"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Commander's Arsenal: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_C18(self):
                mset = self._sets["C18"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Commander 2018: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_C17(self):
                mset = self._sets["C17"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Commander 2017: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_C16(self):
                mset = self._sets["C16"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Commander 2016: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_C15(self):
                mset = self._sets["C15"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Commander 2015: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_C14(self):
                mset = self._sets["C14"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Commander 2014: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_C13(self):
                mset = self._sets["C13"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Commander 2013 Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CEI(self):
                mset = self._sets["CEI"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for International Collector's Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CED(self):
                mset = self._sets["CED"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Collector's Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_E01(self):
                mset = self._sets["E01"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Archenemy: Nicol Bolas: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ARC(self):
                mset = self._sets["ARC"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Archenemy: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ZEN(self):
                mset = self._sets["ZEN"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Zendikar: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_XLN(self):
                mset = self._sets["XLN"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Ixalan: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_WWK(self):
                mset = self._sets["WWK"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Worldwake: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_WTH(self):
                mset = self._sets["WTH"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Weatherlight: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_W17(self):
                mset = self._sets["W17"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Welcome Deck 2017: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_W16(self):
                mset = self._sets["W16"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Welcome Deck 2016: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_VIS(self):
                mset = self._sets["VIS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Visions: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_VAN(self):
                mset = self._sets["VAN"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Vanguard: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_USG(self):
                mset = self._sets["USG"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Urza's Saga: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ULG(self):
                mset = self._sets["ULG"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Urza's Legacy: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_UDS(self):
                mset = self._sets["UDS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Urza's Destiny: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_TSP(self):
                mset = self._sets["TSP"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Time Spiral: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_TSB(self):
                mset = self._sets["TSB"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Time Spiral \"Timeshifted\": {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_TPR(self):
                mset = self._sets["TPR"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Tempest Remastered: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_TOR(self):
                mset = self._sets["TOR"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Torment: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_TMP(self):
                mset = self._sets["TMP"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Tempest: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_THS(self):
                mset = self._sets["THS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Theros: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_STH(self):
                mset = self._sets["STH"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Stronghold: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_SOM(self):
                mset = self._sets["SOM"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Scars of Mirrodin: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_SOK(self):
                mset = self._sets["SOK"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Saviors of Kamigawa: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_SOI(self):
                mset = self._sets["SOI"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Shadows over Innistrad: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_SHM(self):
                mset = self._sets["SHM"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Shadowmoor: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_SCG(self):
                mset = self._sets["SCG"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Scourge: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_S99(self):
                mset = self._sets["S99"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Starter 1999: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_S00(self):
                mset = self._sets["S00"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Starter 2000: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_RTR(self):
                mset = self._sets["RTR"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Return to Ravnica: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_RQS(self):
                mset = self._sets["RQS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Rivals Quick Start Set: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ROE(self):
                mset = self._sets["ROE"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Rise of the Eldrazi: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_RIX(self):
                mset = self._sets["RIX"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Rivals of Ixalan: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_RAV(self):
                mset = self._sets["RAV"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Ravnica: City of Guilds: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_PLS(self):
                mset = self._sets["PLS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Planeshift: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_PLC(self):
                mset = self._sets["PLC"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Planar Chaos: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_PCY(self):
                mset = self._sets["PCY"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Prophecy: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ORI(self):
                mset = self._sets["ORI"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic Origins: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ONS(self):
                mset = self._sets["ONS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Onslaught: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_OGW(self):
                mset = self._sets["OGW"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Oath of the Gatewatch: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ODY(self):
                mset = self._sets["ODY"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Odyssey: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_NPH(self):
                mset = self._sets["NPH"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for New Phyrexia: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_NMS(self):
                mset = self._sets["NMS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Nemesis: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MRD(self):
                mset = self._sets["MRD"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Mirrodin: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MOR(self):
                mset = self._sets["MOR"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Morningtide: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MMQ(self):
                mset = self._sets["MMQ"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Mercadian Masques: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MIR(self):
                mset = self._sets["MIR"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Mirage: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MGB(self):
                mset = self._sets["MGB"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Multiverse Gift Box: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MD1(self):
                mset = self._sets["MD1"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Modern Event Deck 2014: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_MBS(self):
                mset = self._sets["MBS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Mirrodin Besieged: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_M19(self):
                mset = self._sets["M19"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Core Set 2019: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_M15(self):
                mset = self._sets["M15"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic 2015 Core Set: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_M14(self):
                mset = self._sets["M14"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic 2014 Core Set: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_M13(self):
                mset = self._sets["M13"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic 2013: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_M12(self):
                mset = self._sets["M12"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic 2012: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_M11(self):
                mset = self._sets["M11"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic 2011: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_M10(self):
                mset = self._sets["M10"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic 2010: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_LRW(self):
                mset = self._sets["LRW"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Lorwyn: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_LGN(self):
                mset = self._sets["LGN"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Legions: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_LEG(self):
                mset = self._sets["LEG"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Legends: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_LEB(self):
                mset = self._sets["LEB"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Limited Edition Beta: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_LEA(self):
                mset = self._sets["LEA"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Limited Edition Alpha: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_KTK(self):
                mset = self._sets["KTK"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Khans of Tarkir: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_KLD(self):
                mset = self._sets["KLD"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Kaladesh: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_JUD(self):
                mset = self._sets["JUD"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Judgment: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_JOU(self):
                mset = self._sets["JOU"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Journey into Nyx: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ITP(self):
                mset = self._sets["ITP"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Introductory Two-Player Set: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ISD(self):
                mset = self._sets["ISD"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Innistrad: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_INV(self):
                mset = self._sets["INV"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Invasion: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ICE(self):
                mset = self._sets["ICE"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Ice Age: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_HOU(self):
                mset = self._sets["HOU"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Hour of Devastation: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_HML(self):
                mset = self._sets["HML"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Homelands: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_GTC(self):
                mset = self._sets["GTC"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Gatecrash: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_GPT(self):
                mset = self._sets["GPT"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Guildpact: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_FUT(self):
                mset = self._sets["FUT"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Future Sight: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_FRF_UGIN(self):
                mset = self._sets["FRF_UGIN"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Ugin's Fate promos: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_FRF(self):
                mset = self._sets["FRF"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Fate Reforged: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_FEM(self):
                mset = self._sets["FEM"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Fallen Empires: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_EXO(self):
                mset = self._sets["EXO"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Exodus: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_EVE(self):
                mset = self._sets["EVE"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Eventide: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_EMN(self):
                mset = self._sets["EMN"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Eldritch Moon: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DTK(self):
                mset = self._sets["DTK"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Dragons of Tarkir: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DST(self):
                mset = self._sets["DST"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Darksteel: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DRK(self):
                mset = self._sets["DRK"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for The Dark: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DPA(self):
                mset = self._sets["DPA"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Duels of the Planeswalkers: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DOM(self):
                mset = self._sets["DOM"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Dominaria: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DKM(self):
                mset = self._sets["DKM"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Deckmasters: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DKA(self):
                mset = self._sets["DKA"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Dark Ascension: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DIS(self):
                mset = self._sets["DIS"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Dissension: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_DGM(self):
                mset = self._sets["DGM"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Dragon's Maze: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CST(self):
                mset = self._sets["CST"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Coldsnap Theme Decks: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CSP(self):
                mset = self._sets["CSP"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Coldsnap: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CP3(self):
                mset = self._sets["CP3"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic Origins Clash Pack: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CP2(self):
                mset = self._sets["CP2"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Fate Reforged Clash Pack: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CP1(self):
                mset = self._sets["CP1"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Magic 2015 Clash Pack: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CON(self):
                mset = self._sets["CON"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Conflux: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CHR(self):
                mset = self._sets["CHR"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Chronicles: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_CHK(self):
                mset = self._sets["CHK"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Champions of Kamigawa: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_BTD(self):
                mset = self._sets["BTD"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Beatdown Box Set: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_BRB(self):
                mset = self._sets["BRB"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Battle Royale Box Set: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_BOK(self):
                mset = self._sets["BOK"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Betrayers of Kamigawa: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_BNG(self):
                mset = self._sets["BNG"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Born of the Gods: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_BFZ(self):
                mset = self._sets["BFZ"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Battle for Zendikar: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_BBD(self):
                mset = self._sets["BBD"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Battlebond: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_AVR(self):
                mset = self._sets["AVR"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Avacyn Restored: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ATQ(self):
                mset = self._sets["ATQ"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Antiquities: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ATH(self):
                mset = self._sets["ATH"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Anthologies: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ARN(self):
                mset = self._sets["ARN"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Arabian Nights: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ARB(self):
                mset = self._sets["ARB"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Alara Reborn: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_APC(self):
                mset = self._sets["APC"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Apocalypse: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ALL(self):
                mset = self._sets["ALL"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Alliances: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_ALA(self):
                mset = self._sets["ALA"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Shards of Alara: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_AKH(self):
                mset = self._sets["AKH"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Amonkhet: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_AER(self):
                mset = self._sets["AER"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Aether Revolt: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_9ED(self):
                mset = self._sets["9ED"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Ninth Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_8ED(self):
                mset = self._sets["8ED"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Eighth Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_7ED(self):
                mset = self._sets["7ED"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Seventh Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_6ED(self):
                mset = self._sets["6ED"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Classic Sixth Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_5ED(self):
                mset = self._sets["5ED"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Fifth Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_5DN(self):
                mset = self._sets["5DN"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Fifth Dawn: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_4ED(self):
                mset = self._sets["4ED"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Fourth Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_3ED(self):
                mset = self._sets["3ED"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Revised Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_2ED(self):
                mset = self._sets["2ED"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Unlimited Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))
        def test_10E(self):
                mset = self._sets["10E"]
                cardsParsed,numberOfCards = self.parseCards(mset)
                print("MtgJsonCompiler support for Tenth Edition: {0} / {1} cards".format(cardsParsed,numberOfCards))


if __name__ == '__main__':
        unittest.main()
