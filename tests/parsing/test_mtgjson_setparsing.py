import unittest,json, os
from tqdm import tqdm
import mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonCompiler as MtgJsonCompiler
from multiprocessing import Pool
import zipfile, time
from datetime import datetime
import pandas as pd

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
                        name = cardDict['faceName']
        else:
                name = None

        start_time = time.perf_counter()  # Record the start time
        try:
                # print(cardDict['text'])
                preprocessed = workerPreprocessor.prelex(cardDict['text'], None, name)
                # print(preprocessed)
                card = workerParser.parse(preprocessed)
                duration = time.perf_counter() - start_time
                print("SUCCESS:",name)
                return name, True, preprocessed, duration, None
        except Exception as e:
                duration = time.perf_counter() - start_time
                print("FAILURE:",name)
                print(preprocessed)
                print(e)
                # traceback.print_exc()
                return name,False, preprocessed, duration, str(e)


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
                results = []
                with Pool(processes=8) as pool:
                        for res in tqdm(pool.imap_unordered(parseWorker,uniqueCards)):
                                name, parsed, cardText, duration, error = res
                                if parsed == True:
                                        if name not in self._parsednames:
                                                self._parsednames.add(name)
                                        cardsParsed += 1
                                        totalCardsParsed += 1
                                        totalCardsAttempted += 1
                                else:
                                        totalCardsAttempted += 1

                                # save the results so they can go to a csv file.
                                results.append({"name": name, "duration": duration,
                                                "parsed": parsed, "error": error, "text": cardText})
                return cardsParsed, numberOfCards, results

        def test_set(self, set_key, set_name):
                mset = self._sets[set_key]
                cardsParsed, numberOfCards, results = self.parseCards(mset)
                print(f"MtgJsonCompiler support for {set_name}: {cardsParsed} / {numberOfCards} cards")
                df = pd.DataFrame(results)
                csvName = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}-{set_key}.csv"
                outdir = 'tests/results'
                if not os.path.exists(outdir):
                        os.makedirs(outdir, exist_ok=True)
                fullname = os.path.join(outdir, csvName)
                df.to_csv(fullname)

        def test_KHM(self):
                self.test_set("KHM", "Kaldheim")

        def test_ELD(self):
                self.test_set("ELD", "Throne of Eldraine")

        def test_10E(self):
                self.test_set("10E", "Tenth Edition")

        def test_2ED(self):
                self.test_set("2ED", "Unlimited Edition")

        def test_3ED(self):
                self.test_set("3ED", "Revised Edition")

        def test_4ED(self):
                self.test_set("4ED", "Fourth Edition")

        def test_5DN(self):
                self.test_set("5DN", "Fifth Dawn")

        def test_5ED(self):
                self.test_set("5ED", "Fifth Edition")

        def test_6ED(self):
                self.test_set("6ED", "Classic Sixth Edition")

        def test_7ED(self):
                self.test_set("7ED", "Seventh Edition")

        def test_8ED(self):
                self.test_set("8ED", "Eighth Edition")

        def test_9ED(self):
                self.test_set("9ED", "Ninth Edition")

        def test_A25(self):
                self.test_set("A25", "Masters 25")

        def test_AER(self):
                self.test_set("AER", "Aether Revolt")

        def test_AKH(self):
                self.test_set("AKH", "Amonkhet")

        def test_ALA(self):
                self.test_set("ALA", "Shards of Alara")

        def test_ALL(self):
                self.test_set("ALL", "Alliances")

        def test_APC(self):
                self.test_set("APC", "Apocalypse")

        def test_ARB(self):
                self.test_set("ARB", "Alara Reborn")

        def test_ARN(self):
                self.test_set("ARN", "Arabian Nights")

        def test_ARC(self):
                self.test_set("ARC", "Archenemy")

        def test_ATH(self):
                self.test_set("ATH", "Anthologies")

        def test_ATQ(self):
                self.test_set("ATQ", "Antiquities")

        def test_AVR(self):
                self.test_set("AVR", "Avacyn Restored")

        def test_BBD(self):
                self.test_set("BBD", "Battlebond")

        def test_BFZ(self):
                self.test_set("BFZ", "Battle for Zendikar")

        def test_BNG(self):
                self.test_set("BNG", "Born of the Gods")

        def test_BOK(self):
                self.test_set("BOK", "Betrayers of Kamigawa")

        def test_BRB(self):
                self.test_set("BRB", "Battle Royale Box Set")

        def test_BTD(self):
                self.test_set("BTD", "Beatdown Box Set")

        def test_C13(self):
                self.test_set("C13", "Commander 2013 Edition")

        def test_C14(self):
                self.test_set("C14", "Commander 2014")

        def test_C15(self):
                self.test_set("C15", "Commander 2015")

        def test_C16(self):
                self.test_set("C16", "Commander 2016")

        def test_C17(self):
                self.test_set("C17", "Commander 2017")

        def test_C18(self):
                self.test_set("C18", "Commander 2018")

        def test_CED(self):
                self.test_set("CED", "Collector's Edition")

        def test_CEI(self):
                self.test_set("CEI", "International Collector's Edition")

        def test_CMA(self):
                self.test_set("CMA", "Commander Anthology")

        def test_CM1(self):
                self.test_set("CM1", "Commander's Arsenal")

        def test_CM2(self):
                self.test_set("CM2", "Commander Anthology 2018")

        def test_CMD(self):
                self.test_set("CMD", "Magic: The Gathering-Commander")

        def test_CNS(self):
                self.test_set("CNS", "Magic: The Gathering—Conspiracy")

        def test_CN2(self):
                self.test_set("CN2", "Conspiracy: Take the Crown")

        def test_CSP(self):
                self.test_set("CSP", "Coldsnap")

        def test_CST(self):
                self.test_set("CST", "Coldsnap Theme Decks")

        def test_DGM(self):
                self.test_set("DGM", "Dragon's Maze")

        def test_DIS(self):
                self.test_set("DIS", "Dissension")

        def test_DKA(self):
                self.test_set("DKA", "Dark Ascension")

        def test_DKM(self):
                self.test_set("DKM", "Deckmasters")

        def test_DOM(self):
                self.test_set("DOM", "Dominaria")

        def test_DPA(self):
                self.test_set("DPA", "Duels of the Planeswalkers")

        def test_DRK(self):
                self.test_set("DRK", "The Dark")

        def test_DST(self):
                self.test_set("DST", "Darksteel")

        def test_DTK(self):
                self.test_set("DTK", "Dragons of Tarkir")

        def test_EMA(self):
                self.test_set("EMA", "Eternal Masters")

        def test_EMN(self):
                self.test_set("EMN", "Eldritch Moon")

        def test_EVE(self):
                self.test_set("EVE", "Eventide")

        def test_EXO(self):
                self.test_set("EXO", "Exodus")

        def test_EXP(self):
                self.test_set("EXP", "Zendikar Expeditions")

        def test_FEM(self):
                self.test_set("FEM", "Fallen Empires")

        def test_FRF(self):
                self.test_set("FRF", "Fate Reforged")

        def test_FUT(self):
                self.test_set("FUT", "Future Sight")

        def test_GS1(self):
                self.test_set("GS1", "Global Series: Jiang Yanggu and Mu Yanling")

        def test_GTC(self):
                self.test_set("GTC", "Gatecrash")

        def test_GPT(self):
                self.test_set("GPT", "Guildpact")

        def test_HML(self):
                self.test_set("HML", "Homelands")

        def test_HOP(self):
                self.test_set("HOP", "Planechase")

        def test_HOU(self):
                self.test_set("HOU", "Hour of Devastation")

        def test_ICE(self):
                self.test_set("ICE", "Ice Age")

        def test_IMA(self):
                self.test_set("IMA", "Iconic Masters")

        def test_INV(self):
                self.test_set("INV", "Invasion")

        def test_ISD(self):
                self.test_set("ISD", "Innistrad")

        def test_ITP(self):
                self.test_set("ITP", "Introductory Two-Player Set")

        def test_JOU(self):
                self.test_set("JOU", "Journey into Nyx")

        def test_JUD(self):
                self.test_set("JUD", "Judgment")

        def test_KLD(self):
                self.test_set("KLD", "Kaladesh")

        def test_KTK(self):
                self.test_set("KTK", "Khans of Tarkir")

        def test_LEA(self):
                self.test_set("LEA", "Limited Edition Alpha")

        def test_LEB(self):
                self.test_set("LEB", "Limited Edition Beta")

        def test_LGN(self):
                self.test_set("LGN", "Legions")

        def test_LRW(self):
                self.test_set("LRW", "Lorwyn")

        def test_M10(self):
                self.test_set("M10", "Magic 2010")

        def test_M11(self):
                self.test_set("M11", "Magic 2011")

        def test_M12(self):
                self.test_set("M12", "Magic 2012")

        def test_M13(self):
                self.test_set("M13", "Magic 2013")

        def test_M14(self):
                self.test_set("M14", "Magic 2014 Core Set")

        def test_M15(self):
                self.test_set("M15", "Magic 2015 Core Set")

        def test_M19(self):
                self.test_set("M19", "Core Set 2019")

        def test_MMA(self):
                self.test_set("MMA", "Modern Masters")

        def test_MOR(self):
                self.test_set("MOR", "Morningtide")

        def test_MPS(self):
                self.test_set("MPS", "Masterpiece Series: Kaladesh Inventions")

        def test_MPS_AKH(self):
                self.test_set("MPS_AKH", "Masterpiece Series: Amonkhet Invocations")

        def test_MRD(self):
                self.test_set("MRD", "Mirrodin")

        def test_MGB(self):
                self.test_set("MGB", "Multiverse Gift Box")

        def test_ME2(self):
                self.test_set("ME2", "Masters Edition II")

        def test_ME3(self):
                self.test_set("ME3", "Masters Edition III")

        def test_ME4(self):
                self.test_set("ME4", "Masters Edition IV")

        def test_MED(self):
                self.test_set("MED", "Masters Edition")

        def test_MM2(self):
                self.test_set("MM2", "Modern Masters 2015 Edition")

        def test_MM3(self):
                self.test_set("MM3", "Modern Masters 2017 Edition")

        def test_NMS(self):
                self.test_set("NMS", "Nemesis")

        def test_NPH(self):
                self.test_set("NPH", "New Phyrexia")

        def test_ODY(self):
                self.test_set("ODY", "Odyssey")

        def test_OGW(self):
                self.test_set("OGW", "Oath of the Gatewatch")

        def test_ONS(self):
                self.test_set("ONS", "Onslaught")

        def test_ORI(self):
                self.test_set("ORI", "Magic Origins")

        def test_PC2(self):
                self.test_set("PC2", "Planechase 2012 Edition")

        def test_PCA(self):
                self.test_set("PCA", "Planechase Anthology")

        def test_PCY(self):
                self.test_set("PCY", "Prophecy")

        def test_PLC(self):
                self.test_set("PLC", "Planar Chaos")

        def test_PLS(self):
                self.test_set("PLS", "Planeshift")

        def test_PO2(self):
                self.test_set("PO2", "Portal Second Age")

        def test_POR(self):
                self.test_set("POR", "Portal")

        def test_PTK(self):
                self.test_set("PTK", "Portal Three Kingdoms")

        def test_RAV(self):
                self.test_set("RAV", "Ravnica: City of Guilds")

        def test_RIX(self):
                self.test_set("RIX", "Rivals of Ixalan")

        def test_ROE(self):
                self.test_set("ROE", "Rise of the Eldrazi")

        def test_RTR(self):
                self.test_set("RTR", "Return to Ravnica")

        def test_SHM(self):
                self.test_set("SHM", "Shadowmoor")

        def test_SOK(self):
                self.test_set("SOK", "Saviors of Kamigawa")

        def test_SOI(self):
                self.test_set("SOI", "Shadows over Innistrad")

        def test_SOM(self):
                self.test_set("SOM", "Scars of Mirrodin")

        def test_STH(self):
                self.test_set("STH", "Stronghold")

        def test_TMP(self):
                self.test_set("TMP", "Tempest")

        def test_TOR(self):
                self.test_set("TOR", "Torment")

        def test_TPR(self):
                self.test_set("TPR", "Tempest Remastered")

        def test_TSB(self):
                self.test_set("TSB", "Time Spiral \"Timeshifted\"")

        def test_TSP(self):
                self.test_set("TSP", "Time Spiral")

        def test_USG(self):
                self.test_set("USG", "Urza's Saga")

        def test_VIS(self):
                self.test_set("VIS", "Visions")

        def test_W17(self):
                self.test_set("W17", "Welcome Deck 2017")

        def test_W16(self):
                self.test_set("W16", "Welcome Deck 2016")

        def test_WTH(self):
                self.test_set("WTH", "Weatherlight")

        def test_WWK(self):
                self.test_set("WWK", "Worldwake")

        def test_XLN(self):
                self.test_set("XLN", "Ixalan")

        def test_ZEN(self):
                self.test_set("ZEN", "Zendikar")

        def test_MMQ(self):
                self.test_set("MMQ", "Mercadian Masques")

        def test_MIR(self):
                self.test_set("MIR", "Mirage")

        def test_MD1(self):
                self.test_set("MD1", "Modern Event Deck 2014")

        def test_MBS(self):
                self.test_set("MBS", "Mirrodin Besieged")

        def test_LEG(self):
                self.test_set("LEG", "Legends")

        def test_CON(self):
                self.test_set("CON", "Conflux")

        def test_CHR(self):
                self.test_set("CHR", "Chronicles")

        def test_CHK(self):
                self.test_set("CHK", "Champions of Kamigawa")

        def test_VMA(self):
                self.test_set("VMA", "Vintage Masters")

        def test_E02(self):
                self.test_set("E02", "Explorers of Ixalan")

        def test_E01(self):
                self.test_set("E01", "Archenemy: Nicol Bolas")

        def test_VAN(self):
                self.test_set("VAN", "Vanguard")

        def test_ULG(self):
                self.test_set("ULG", "Urza's Legacy")

        def test_UDS(self):
                self.test_set("UDS", "Urza's Destiny")

        def test_THS(self):
                self.test_set("THS", "Theros")

        def test_SCG(self):
                self.test_set("SCG", "Scourge")

        def test_S99(self):
                self.test_set("S99", "Starter 1999")

        def test_S00(self):
                self.test_set("S00", "Starter 2000")


if __name__ == '__main__':
        unittest.main()
