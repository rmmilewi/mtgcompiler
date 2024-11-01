import unittest
import mtgcompiler.frontend.AST.mtypes

class TestMagicTypes(unittest.TestCase):
        
        def test_CustomTypes(self):
                t0 = mtgcompiler.frontend.AST.mtypes.MgSupertype("Planetouched")
                t1 = mtgcompiler.frontend.AST.mtypes.MgType("Origami")
                t2 = mtgcompiler.frontend.AST.mtypes.MgSubtype("Crane")
                
                #They must be recognized as custom types.
                self.assertTrue(t0.isCustomType())
                self.assertTrue(t1.isCustomType())
                self.assertTrue(t2.isCustomType())
                
                #They are stored as strings, just as they are provided.
                self.assertEqual(t0.getValue().lower(),"planetouched")
                self.assertEqual(type(t0.getValue()),str)
                self.assertEqual(t1.getValue().lower(),"origami")
                self.assertEqual(type(t1.getValue()),str)
                self.assertEqual(t2.getValue().lower(),"crane")
                self.assertEqual(type(t2.getValue()),str)
                
                #They are unparsed as-is.
                self.assertEqual(t0.unparseToString().lower(),"planetouched")
                self.assertEqual(t1.unparseToString().lower(),"origami")
                self.assertEqual(t2.unparseToString().lower(),"crane")
                
        def test_MgTypeEnums(self):
                t_creature = mtgcompiler.frontend.AST.mtypes.MgType(mtgcompiler.frontend.AST.mtypes.MgType.TypeEnum.Creature)
                t_instant = mtgcompiler.frontend.AST.mtypes.MgType(mtgcompiler.frontend.AST.mtypes.MgType.TypeEnum.Instant)
                
                self.assertTrue(t_creature.isPermanentType())
                self.assertTrue(t_instant.isInstantOrSorceryType())
                self.assertFalse(t_creature.isInstantOrSorceryType())
                self.assertFalse(t_instant.isPermanentType())
                
                #Internally, they are represented by an enum.
                self.assertEqual(t_creature.getValue(),mtgcompiler.frontend.AST.mtypes.MgType.TypeEnum.Creature)
                self.assertEqual(type(t_creature.getValue()),mtgcompiler.frontend.AST.mtypes.MgType.TypeEnum)
                self.assertEqual(t_instant.getValue(),mtgcompiler.frontend.AST.mtypes.MgType.TypeEnum.Instant)
                self.assertEqual(type(t_instant.getValue()),mtgcompiler.frontend.AST.mtypes.MgType.TypeEnum)
                
                #During unparsing, they are converted into an equivalent String representation.
                self.assertEqual(t_creature.unparseToString().lower(),"creature")
                self.assertEqual(t_instant.unparseToString().lower(),"instant")
                
        def test_MgSupertypeEnums(self):
                t_legendary = mtgcompiler.frontend.AST.mtypes.MgSupertype(mtgcompiler.frontend.AST.mtypes.MgSupertype.SupertypeEnum.Legendary)
                self.assertEqual(t_legendary.getValue(),mtgcompiler.frontend.AST.mtypes.MgSupertype.SupertypeEnum.Legendary)
                self.assertEqual(t_legendary.unparseToString().lower(),"legendary")
                
        def test_MgSubtypeEnums(self):
                t_ferret = mtgcompiler.frontend.AST.mtypes.MgSubtype(mtgcompiler.frontend.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Ferret)
                t_aura = mtgcompiler.frontend.AST.mtypes.MgSubtype(mtgcompiler.frontend.AST.mtypes.MgSubtype.EnchantmentSubtypeEnum.Aura)
                t_vehicle = mtgcompiler.frontend.AST.mtypes.MgSubtype(mtgcompiler.frontend.AST.mtypes.MgSubtype.ArtifactSubtypeEnum.Vehicle)
                t_arcane = mtgcompiler.frontend.AST.mtypes.MgSubtype(mtgcompiler.frontend.AST.mtypes.MgSubtype.SpellSubtypeEnum.Arcane)
                t_forest = mtgcompiler.frontend.AST.mtypes.MgSubtype(mtgcompiler.frontend.AST.mtypes.MgSubtype.LandSubtypeEnum.Forest)
                t_gideon = mtgcompiler.frontend.AST.mtypes.MgSubtype(mtgcompiler.frontend.AST.mtypes.MgSubtype.PlaneswalkerSubtypeEnum.Gideon)
                t_zendikar = mtgcompiler.frontend.AST.mtypes.MgSubtype(mtgcompiler.frontend.AST.mtypes.MgSubtype.PlanarSubtypeEnum.Zendikar)
                 
                self.assertTrue(t_ferret.isCreatureSubtype())
                self.assertTrue(t_aura.isEnchantmentSubtype())
                self.assertTrue(t_vehicle.isArtifactSubtype())
                self.assertTrue(t_arcane.isSpellSubtype())
                self.assertTrue(t_forest.isLandSubtype())
                self.assertTrue(t_gideon.isPlaneswalkerSubtype())
                self.assertTrue(t_zendikar.isPlanarSubtype())

        def test_ReplaceValue(self):
                #Originally t0 holds the creature type.
                t0 = mtgcompiler.frontend.AST.mtypes.MgType(mtgcompiler.frontend.AST.mtypes.MgType.TypeEnum.Creature)
                
                self.assertEqual(t0.getValue(),mtgcompiler.frontend.AST.mtypes.MgType.TypeEnum.Creature)
                self.assertTrue(t0.isPermanentType())
                self.assertFalse(t0.isInstantOrSorceryType())
                
                #We then swap creature for instant.
                t0.setValue(mtgcompiler.frontend.AST.mtypes.MgType.TypeEnum.Instant)

                self.assertEqual(t0.getValue(),mtgcompiler.frontend.AST.mtypes.MgType.TypeEnum.Instant)
                self.assertFalse(t0.isPermanentType())
                self.assertTrue(t0.isInstantOrSorceryType())
                
        def test_traversability(self):
                #Type nodes can be visited by a visitor, but they have no children.
                t_legendary = mtgcompiler.frontend.AST.mtypes.MgSupertype(mtgcompiler.frontend.AST.mtypes.MgSupertype.SupertypeEnum.Legendary)
                t_creature = mtgcompiler.frontend.AST.mtypes.MgType(mtgcompiler.frontend.AST.mtypes.MgType.TypeEnum.Creature)
                t_ferret = mtgcompiler.frontend.AST.mtypes.MgSubtype(mtgcompiler.frontend.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Ferret)
                
                self.assertTrue(t_legendary.isTraversable())
                self.assertTrue(t_creature.isTraversable())
                self.assertTrue(t_ferret.isTraversable())
                
                self.assertEqual(len(t_legendary.getTraversalSuccessors()),0)
                self.assertEqual(len(t_creature.getTraversalSuccessors()),0)
                self.assertEqual(len(t_ferret.getTraversalSuccessors()),0)
                
        def test_TypeEquivalence(self):
                
                t_elf_0 = mtgcompiler.frontend.AST.mtypes.MgSubtype(mtgcompiler.frontend.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Elf)
                t_elf_1 = mtgcompiler.frontend.AST.mtypes.MgSubtype(mtgcompiler.frontend.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Elf)
                
                #These two are not the same objects.
                self.assertNotEqual(t_elf_0, t_elf_1)
                #But both are equivalent 'elf' creature types.
                self.assertTrue(t_elf_0.isEquivalentType(t_elf_1))
                self.assertTrue(t_elf_1.isEquivalentType(t_elf_0))
                
                #Custom-defined types are not equivalent to Enum-defined types.
                t_elf_2 = mtgcompiler.frontend.AST.mtypes.MgSubtype("Elf")
                self.assertFalse(t_elf_1.isEquivalentType(t_elf_2))
                
                #Types objects must share both the same class and the same value to be considered equivalent.
                t_cleric = mtgcompiler.frontend.AST.mtypes.MgSubtype(mtgcompiler.frontend.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Cleric)
                self.assertFalse(t_elf_0.isEquivalentType(t_cleric))
                
                #Custom-defined types can, however, be compared to each other.
                t_planetouched_0 = mtgcompiler.frontend.AST.mtypes.MgSupertype("Planetouched")
                t_planetouched_1 = mtgcompiler.frontend.AST.mtypes.MgSupertype("Planetouched")
                self.assertTrue(t_planetouched_0.isEquivalentType(t_planetouched_1))
                
                
        
if __name__ == '__main__':
    unittest.main()