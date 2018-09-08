import unittest
from mtgcompiler.parsers.JsonParser import JsonParser

class TestFeatureParsingAndTransformation(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                #Because apparently we can't easily change the starting point of the parser after we
                #instantiate it, I'm putting specialized parsers here to save on setup time for these
                #unit tests.
                cls._keywordSequenceParser = JsonParser(startText="keywordsequence")
        
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
                
                
                
        def test_parseKeywordAbility(self):
                lp = self._keywordSequenceParser.getLarkParser()
                tf = self._keywordSequenceParser.getLarkTransformer()
                
                kw_ability = "hexproof from black"
                tree_ability = lp.parse(kw_ability)
                print(tree_ability)
                ast_ability = tf.transform(tree_ability)
                print(ast_ability.unparseToString())
                

                
                
        # @unittest.expectedFailure
        # def test_parseKeywordAbilities(self):
        #         jsonParser = JsonParser(startText="keywordsequence")
        #         lp = jsonParser.getLarkParser()
        #         tf = jsonParser.getLarkTransformer()
        #
        #         kw_defender = "defender"
        #         tree_defender = lp.parse(kw_defender)
        #         ast_defender = tf.transform(tree_defender)
        #
        #         kw_doublestrike = "double strike"
        #         tree_doublestrike = lp.parse(kw_doublestrike)
        #         ast_doublestrike = tf.transform(tree_doublestrike)
        #
        #         kw_enchant = "enchant artifact creature"
        #         tree_enchant = lp.parse(kw_enchant)
        #         ast_enchant = tf.transform(tree_enchant)
        #
        #         kw_equip = "equip {3}"
        #         tree_equip = lp.parse(kw_equip)
        #         ast_equip = tf.transform(tree_equip)
        #
        #         kw_equipquality = "equip legendary creature {3}"
        #         tree_equipquality = lp.parse(kw_equipquality)
        #         ast_equipquality = tf.transform(tree_equipquality)
        #
        #         kw_firststrike = "first strike"
        #         tree_firststrike = lp.parse(kw_firststrike)
        #         ast_firststrike = tf.transform(tree_firststrike)
        #
        #         kw_flash = "flash"
        #         tree_flash = lp.parse(kw_flash)
        #         ast_flash = tf.transform(tree_flash)
        #
        #         kw_flying = "flying"
        #         tree_flying = lp.parse(kw_flying)
        #         ast_flying = tf.transform(tree_flying)
        #
        #         kw_haste = "haste"
        #         tree_haste = lp.parse(kw_haste)
        #         ast_haste = tf.transform(tree_haste)
        #
        #         kw_hexproof = "hexproof"
        #         tree_hexproof = lp.parse(kw_hexproof)
        #         ast_hexproof = tf.transform(tree_hexproof)
        #
        #         #kw_hexprooffromblack = "hexproof from black"
        #         #tree_hexprooffromblack = lp.parse(kw_hexprooffromblack)
        #         #ast_hexprooffromblack = tf.transform(tree_hexprooffromblack)
        #
        #         kw_indestructible = "indestructible"
        #         tree_indestructible = lp.parse(kw_indestructible)
        #         ast_indestructible = tf.transform(tree_indestructible)
        #
        #         kw_intimidate = "intimidate"
        #         tree_intimidate = lp.parse(kw_intimidate)
        #         ast_intimidate = tf.transform(tree_intimidate)
        #
        #         kw_landwalk = "landwalk"
        #         tree_landwalk = lp.parse(kw_landwalk)
        #         ast_landwalk = tf.transform(tree_landwalk)
        #
        #         kw_lifelink = "lifelink"
        #         tree_lifelink = lp.parse(kw_lifelink)
        #         ast_lifelink = tf.transform(tree_lifelink)
        #
        #         kw_protection = "protection"
        #         tree_protection = lp.parse(kw_protection)
        #         ast_protection = tf.transform(tree_protection)
        #
        #         kw_reach = "reach"
        #         tree_reach = lp.parse(kw_reach)
        #         ast_reach = tf.transform(tree_reach)
        #
        #         kw_shroud = "shroud"
        #         tree_shroud = lp.parse(kw_shroud)
        #         ast_shroud = tf.transform(tree_shroud)
        #
        #         kw_trample = "trample"
        #         tree_trample = lp.parse(kw_trample)
        #         ast_trample = tf.transform(tree_trample)
        #
        #         kw_vigilance = "vigilance"
        #         tree_vigilance = lp.parse(kw_vigilance)
        #         ast_vigilance = tf.transform(tree_vigilance)
        #
        #         kw_banding = "banding"
        #         tree_banding = lp.parse(kw_banding)
        #         ast_banding = tf.transform(tree_banding)
        #
        #         kw_rampage = "rampage"
        #         tree_rampage = lp.parse(kw_rampage)
        #         ast_rampage = tf.transform(tree_rampage)
        #
        #         kw_cumulativeupkeep = "cumulative upkeep"
        #         tree_cumulativeupkeep = lp.parse(kw_cumulativeupkeep)
        #         ast_cumulativeupkeep = tf.transform(tree_cumulativeupkeep)
        #
        #         kw_flanking = "flanking"
        #         tree_flanking = lp.parse(kw_flanking)
        #         ast_flanking = tf.transform(tree_flanking)
        #
        #         kw_phasing = "phasing"
        #         tree_phasing = lp.parse(kw_phasing)
        #         ast_phasing = tf.transform(tree_phasing)
        #
        #         kw_buyback = "buyback"
        #         tree_buyback = lp.parse(kw_buyback)
        #         ast_buyback = tf.transform(tree_buyback)
        #
        #         kw_shadow = "shadow"
        #         tree_shadow = lp.parse(kw_shadow)
        #         ast_shadow = tf.transform(tree_shadow)
        #
        #         kw_cycling = "cycling"
        #         tree_cycling = lp.parse(kw_cycling)
        #         ast_cycling = tf.transform(tree_cycling)
        #
        #         kw_echo = "echo"
        #         tree_echo = lp.parse(kw_echo)
        #         ast_echo = tf.transform(tree_echo)
        #
        #         kw_horsemanship = "horsemanship"
        #         tree_horsemanship = lp.parse(kw_horsemanship)
        #         ast_horsemanship = tf.transform(tree_horsemanship)
        #
        #         kw_fading = "fading"
        #         tree_fading = lp.parse(kw_fading)
        #         ast_fading = tf.transform(tree_fading)
        #
        #         kw_kicker = "kicker"
        #         tree_kicker = lp.parse(kw_kicker)
        #         ast_kicker = tf.transform(tree_kicker)
        #
        #         kw_flashback = "flashback"
        #         tree_flashback = lp.parse(kw_flashback)
        #         ast_flashback = tf.transform(tree_flashback)
        #
        #         kw_madness = "madness"
        #         tree_madness = lp.parse(kw_madness)
        #         ast_madness = tf.transform(tree_madness)
        #
        #         kw_fear = "fear"
        #         tree_fear = lp.parse(kw_fear)
        #         ast_fear = tf.transform(tree_fear)
        #
        #         kw_morph = "morph"
        #         tree_morph = lp.parse(kw_morph)
        #         ast_morph = tf.transform(tree_morph)
        #
        #         kw_amplify = "amplify"
        #         tree_amplify = lp.parse(kw_amplify)
        #         ast_amplify = tf.transform(tree_amplify)
        #
        #         kw_provoke = "provoke"
        #         tree_provoke = lp.parse(kw_provoke)
        #         ast_provoke = tf.transform(tree_provoke)
        #
        #         kw_storm = "storm"
        #         tree_storm = lp.parse(kw_storm)
        #         ast_storm = tf.transform(tree_storm)
        #
        #         kw_affinity = "affinity"
        #         tree_affinity = lp.parse(kw_affinity)
        #         ast_affinity = tf.transform(tree_affinity)
        #
        #         kw_entwine = "entwine"
        #         tree_entwine = lp.parse(kw_entwine)
        #         ast_entwine = tf.transform(tree_entwine)
        #
        #         kw_modular = "modular"
        #         tree_modular = lp.parse(kw_modular)
        #         ast_modular = tf.transform(tree_modular)
        #
        #         kw_sunburst = "sunburst"
        #         tree_sunburst = lp.parse(kw_sunburst)
        #         ast_sunburst = tf.transform(tree_sunburst)
        #
        #         kw_bushido = "bushido"
        #         tree_bushido = lp.parse(kw_bushido)
        #         ast_bushido = tf.transform(tree_bushido)
        #
        #         kw_soulshift = "soulshift"
        #         tree_soulshift = lp.parse(kw_soulshift)
        #         ast_soulshift = tf.transform(tree_soulshift)
        #
        #         kw_splice = "splice"
        #         tree_splice = lp.parse(kw_splice)
        #         ast_splice = tf.transform(tree_splice)
        #
        #         kw_offering = "offering"
        #         tree_offering = lp.parse(kw_offering)
        #         ast_offering = tf.transform(tree_offering)
        #
        #         kw_ninjutsu = "ninjutsu"
        #         tree_ninjutsu = lp.parse(kw_ninjutsu)
        #         ast_ninjutsu = tf.transform(tree_ninjutsu)
        #
        #         kw_epic = "epic"
        #         tree_epic = lp.parse(kw_epic)
        #         ast_epic = tf.transform(tree_epic)
        #
        #         kw_convoke = "convoke"
        #         tree_convoke = lp.parse(kw_convoke)
        #         ast_convoke = tf.transform(tree_convoke)
        #
        #         kw_dredge = "dredge"
        #         tree_dredge = lp.parse(kw_dredge)
        #         ast_dredge = tf.transform(tree_dredge)
        #
        #         kw_transmute = "transmute"
        #         tree_transmute = lp.parse(kw_transmute)
        #         ast_transmute = tf.transform(tree_transmute)
        #
        #         kw_bloodthirst = "bloodthirst"
        #         tree_bloodthirst = lp.parse(kw_bloodthirst)
        #         ast_bloodthirst = tf.transform(tree_bloodthirst)
        #
        #         kw_haunt = "haunt"
        #         tree_haunt = lp.parse(kw_haunt)
        #         ast_haunt = tf.transform(tree_haunt)
        #
        #         kw_replicate = "replicate"
        #         tree_replicate = lp.parse(kw_replicate)
        #         ast_replicate = tf.transform(tree_replicate)
        #
        #         kw_forecast = "forecast"
        #         tree_forecast = lp.parse(kw_forecast)
        #         ast_forecast = tf.transform(tree_forecast)
        #
        #         kw_graft = "graft"
        #         tree_graft = lp.parse(kw_graft)
        #         ast_graft = tf.transform(tree_graft)
        #
        #         kw_recover = "recover"
        #         tree_recover = lp.parse(kw_recover)
        #         ast_recover = tf.transform(tree_recover)
        #
        #         kw_ripple = "ripple"
        #         tree_ripple = lp.parse(kw_ripple)
        #         ast_ripple = tf.transform(tree_ripple)
        #
        #         kw_splitsecond = "splitsecond"
        #         tree_splitsecond = lp.parse(kw_splitsecond)
        #         ast_splitsecond = tf.transform(tree_splitsecond)
        #
        #         kw_suspend = "suspend"
        #         tree_suspend = lp.parse(kw_suspend)
        #         ast_suspend = tf.transform(tree_suspend)
        #
        #         kw_vanishing = "vanishing"
        #         tree_vanishing = lp.parse(kw_vanishing)
        #         ast_vanishing = tf.transform(tree_vanishing)
        #
        #         kw_absorb = "absorb"
        #         tree_absorb = lp.parse(kw_absorb)
        #         ast_absorb = tf.transform(tree_absorb)
        #
        #         kw_auraswap = "auraswap"
        #         tree_auraswap = lp.parse(kw_auraswap)
        #         ast_auraswap = tf.transform(tree_auraswap)
        #
        #         kw_delve = "delve"
        #         tree_delve = lp.parse(kw_delve)
        #         ast_delve = tf.transform(tree_delve)
        #
        #         kw_fortify = "fortify"
        #         tree_fortify = lp.parse(kw_fortify)
        #         ast_fortify = tf.transform(tree_fortify)
        #
        #         kw_frenzy = "frenzy"
        #         tree_frenzy = lp.parse(kw_frenzy)
        #         ast_frenzy = tf.transform(tree_frenzy)
        #
        #         kw_gravestorm = "gravestorm"
        #         tree_gravestorm = lp.parse(kw_gravestorm)
        #         ast_gravestorm = tf.transform(tree_gravestorm)
        #
        #         kw_poisonous = "poisonous"
        #         tree_poisonous = lp.parse(kw_poisonous)
        #         ast_poisonous = tf.transform(tree_poisonous)
        #
        #         kw_transfigure = "transfigure"
        #         tree_transfigure = lp.parse(kw_transfigure)
        #         ast_transfigure = tf.transform(tree_transfigure)
        #
        #         kw_champion = "champion"
        #         tree_champion = lp.parse(kw_champion)
        #         ast_champion = tf.transform(tree_champion)
        #
        #         kw_changeling = "changeling"
        #         tree_changeling = lp.parse(kw_changeling)
        #         ast_changeling = tf.transform(tree_changeling)
        #
        #         kw_evoke = "evoke"
        #         tree_evoke = lp.parse(kw_evoke)
        #         ast_evoke = tf.transform(tree_evoke)
        #
        #         kw_hideaway = "hideaway"
        #         tree_hideaway = lp.parse(kw_hideaway)
        #         ast_hideaway = tf.transform(tree_hideaway)
        #
        #         kw_prowl = "prowl"
        #         tree_prowl = lp.parse(kw_prowl)
        #         ast_prowl = tf.transform(tree_prowl)
        #
        #         kw_reinforce = "reinforce"
        #         tree_reinforce = lp.parse(kw_reinforce)
        #         ast_reinforce = tf.transform(tree_reinforce)
        #
        #         kw_conspire = "conspire"
        #         tree_conspire = lp.parse(kw_conspire)
        #         ast_conspire = tf.transform(tree_conspire)
        #
        #         kw_persist = "persist"
        #         tree_persist = lp.parse(kw_persist)
        #         ast_persist = tf.transform(tree_persist)
        #
        #         kw_wither = "wither"
        #         tree_wither = lp.parse(kw_wither)
        #         ast_wither = tf.transform(tree_wither)
        #
        #         kw_retrace = "retrace"
        #         tree_retrace = lp.parse(kw_retrace)
        #         ast_retrace = tf.transform(tree_retrace)
        #
        #         kw_devour = "devour"
        #         tree_devour = lp.parse(kw_devour)
        #         ast_devour = tf.transform(tree_devour)
        #
        #         kw_exalted = "exalted"
        #         tree_exalted = lp.parse(kw_exalted)
        #         ast_exalted = tf.transform(tree_exalted)
        #
        #         kw_unearth = "unearth"
        #         tree_unearth = lp.parse(kw_unearth)
        #         ast_unearth = tf.transform(tree_unearth)
        #
        #         kw_cascade = "cascade"
        #         tree_cascade = lp.parse(kw_cascade)
        #         ast_cascade = tf.transform(tree_cascade)
        #
        #         kw_annihilator = "annihilator"
        #         tree_annihilator = lp.parse(kw_annihilator)
        #         ast_annihilator = tf.transform(tree_annihilator)
        #
        #         kw_levelup = "levelup"
        #         tree_levelup = lp.parse(kw_levelup)
        #         ast_levelup = tf.transform(tree_levelup)
        #
        #         kw_rebound = "rebound"
        #         tree_rebound = lp.parse(kw_rebound)
        #         ast_rebound = tf.transform(tree_rebound)
        #
        #         kw_totemarmor = "totem armor"
        #         tree_totemarmor = lp.parse(kw_totemarmor)
        #         ast_totemarmor = tf.transform(tree_totemarmor)
        #
        #         kw_infect = "infect"
        #         tree_infect = lp.parse(kw_infect)
        #         ast_infect = tf.transform(tree_infect)
        #
        #         kw_battlecry = "battlecry"
        #         tree_battlecry = lp.parse(kw_battlecry)
        #         ast_battlecry = tf.transform(tree_battlecry)
        #
        #         kw_livingweapon = "living weapon"
        #         tree_livingweapon = lp.parse(kw_livingweapon)
        #         ast_livingweapon = tf.transform(tree_livingweapon)
        #
        #         kw_undying = "undying"
        #         tree_undying = lp.parse(kw_undying)
        #         ast_undying = tf.transform(tree_undying)
        #
        #         kw_miracle = "miracle"
        #         tree_miracle = lp.parse(kw_miracle)
        #         ast_miracle = tf.transform(tree_miracle)
        #
        #         kw_soulbond = "soulbond"
        #         tree_soulbond = lp.parse(kw_soulbond)
        #         ast_soulbond = tf.transform(tree_soulbond)
        #
        #         kw_overload = "overload"
        #         tree_overload = lp.parse(kw_overload)
        #         ast_overload = tf.transform(tree_overload)
        #
        #         kw_scavenge = "scavenge"
        #         tree_scavenge = lp.parse(kw_scavenge)
        #         ast_scavenge = tf.transform(tree_scavenge)
        #
        #         kw_unleash = "unleash"
        #         tree_unleash = lp.parse(kw_unleash)
        #         ast_unleash = tf.transform(tree_unleash)
        #
        #         kw_cipher = "cipher"
        #         tree_cipher = lp.parse(kw_cipher)
        #         ast_cipher = tf.transform(tree_cipher)
        #
        #         kw_evolve = "evolve"
        #         tree_evolve = lp.parse(kw_evolve)
        #         ast_evolve = tf.transform(tree_evolve)
        #
        #         kw_extort = "extort"
        #         tree_extort = lp.parse(kw_extort)
        #         ast_extort = tf.transform(tree_extort)
        #
        #         kw_fuse = "fuse"
        #         tree_fuse = lp.parse(kw_fuse)
        #         ast_fuse = tf.transform(tree_fuse)
        #
        #         kw_bestow = "bestow"
        #         tree_bestow = lp.parse(kw_bestow)
        #         ast_bestow = tf.transform(tree_bestow)
        #
        #         kw_tribute = "tribute"
        #         tree_tribute = lp.parse(kw_tribute)
        #         ast_tribute = tf.transform(tree_tribute)
        #
        #         kw_dethrone = "dethrone"
        #         tree_dethrone = lp.parse(kw_dethrone)
        #         ast_dethrone = tf.transform(tree_dethrone)
        #
        #         kw_hiddenagenda = "hidden agenda"
        #         tree_hiddenagenda = lp.parse(kw_hiddenagenda)
        #         ast_hiddenagenda = tf.transform(tree_hiddenagenda)
        #
        #         kw_doubleagenda = "double agenda"
        #         tree_doubleagenda = lp.parse(kw_doubleagenda)
        #         ast_doubleagenda = tf.transform(tree_doubleagenda)
        #
        #         kw_outlast = "outlast"
        #         tree_outlast = lp.parse(kw_outlast)
        #         ast_outlast = tf.transform(tree_outlast)
        #
        #         kw_prowess = "prowess"
        #         tree_prowess = lp.parse(kw_prowess)
        #         ast_prowess = tf.transform(tree_prowess)
        #
        #         kw_dash = "dash"
        #         tree_dash = lp.parse(kw_dash)
        #         ast_dash = tf.transform(tree_dash)
        #
        #         kw_exploit = "exploit"
        #         tree_exploit = lp.parse(kw_exploit)
        #         ast_exploit = tf.transform(tree_exploit)
        #
        #         kw_menace = "menace"
        #         tree_menace = lp.parse(kw_menace)
        #         ast_menace = tf.transform(tree_menace)
        #
        #         kw_renown = "renown"
        #         tree_renown = lp.parse(kw_renown)
        #         ast_renown = tf.transform(tree_renown)
        #
        #         kw_awaken = "awaken"
        #         tree_awaken = lp.parse(kw_awaken)
        #         ast_awaken = tf.transform(tree_awaken)
        #
        #         kw_devoid = "devoid"
        #         tree_devoid = lp.parse(kw_devoid)
        #         ast_devoid = tf.transform(tree_devoid)
        #
        #         kw_ingest = "ingest"
        #         tree_ingest = lp.parse(kw_ingest)
        #         ast_ingest = tf.transform(tree_ingest)
        #
        #         kw_myriad = "myriad"
        #         tree_myriad = lp.parse(kw_myriad)
        #         ast_myriad = tf.transform(tree_myriad)
        #
        #         kw_surge = "surge"
        #         tree_surge = lp.parse(kw_surge)
        #         ast_surge = tf.transform(tree_surge)
        #
        #         kw_skulk = "skulk"
        #         tree_skulk = lp.parse(kw_skulk)
        #         ast_skulk = tf.transform(tree_skulk)
        #
        #         kw_emerge = "emerge"
        #         tree_emerge = lp.parse(kw_emerge)
        #         ast_emerge = tf.transform(tree_emerge)
        #
        #         kw_escalate = "escalate"
        #         tree_escalate = lp.parse(kw_escalate)
        #         ast_escalate = tf.transform(tree_escalate)
        #
        #         kw_melee = "melee"
        #         tree_melee = lp.parse(kw_melee)
        #         ast_melee = tf.transform(tree_melee)
        #
        #         kw_crew = "crew"
        #         tree_crew = lp.parse(kw_crew)
        #         ast_crew = tf.transform(tree_crew)
        #
        #         kw_fabricate = "fabricate"
        #         tree_fabricate = lp.parse(kw_fabricate)
        #         ast_fabricate = tf.transform(tree_fabricate)
        #
        #         kw_partner = "partner"
        #         tree_partner = lp.parse(kw_partner)
        #         ast_partner = tf.transform(tree_partner)
        #
        #         kw_undaunted = "undaunted"
        #         tree_undaunted = lp.parse(kw_undaunted)
        #         ast_undaunted = tf.transform(tree_undaunted)
        #
        #         kw_improvise = "improvise"
        #         tree_improvise = lp.parse(kw_improvise)
        #         ast_improvise = tf.transform(tree_improvise)
        #
        #         kw_aftermath = "aftermath"
        #         tree_aftermath = lp.parse(kw_aftermath)
        #         ast_aftermath = tf.transform(tree_aftermath)
        #
        #         kw_embalm = "embalm"
        #         tree_embalm = lp.parse(kw_embalm)
        #         ast_embalm = tf.transform(tree_embalm)
        #
        #         kw_eternalize = "eternalize"
        #         tree_eternalize = lp.parse(kw_eternalize)
        #         ast_eternalize = tf.transform(tree_eternalize)
        #
        #         kw_afflict = "afflict"
        #         tree_afflict = lp.parse(kw_afflict)
        #         ast_afflict = tf.transform(tree_afflict)
        #
        #         kw_ascend = "ascend"
        #         tree_ascend = lp.parse(kw_ascend)
        #         ast_ascend = tf.transform(tree_ascend)
        #
        #         kw_assist = "assist"
        #         tree_assist = lp.parse(kw_assist)
        #         ast_assist = tf.transform(tree_assist)

                
        
if __name__ == '__main__':
    unittest.main()