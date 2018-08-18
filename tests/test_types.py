import unittest
import mtgcompiler.AST.mtypes

class TestMagicTypes(unittest.TestCase):
        
        def test_CustomTypes(self):
                t0 = mtgcompiler.AST.mtypes.MgSupertype("Planetouched")
                t1 = mtgcompiler.AST.mtypes.MgType("Origami")
                t2 = mtgcompiler.AST.mtypes.MgSubtype("Crane")
                
                #They must be recognized as custom types.
                self.assertTrue(t0.isCustomType())
                self.assertTrue(t1.isCustomType())
                self.assertTrue(t2.isCustomType())
                
                #They are stored as strings, just as they are provided.
                self.assertEqual(t0.getValue(),"Planetouched")
                self.assertEqual(type(t0.getValue()),str)
                self.assertEqual(t1.getValue(),"Origami")
                self.assertEqual(type(t1.getValue()),str)
                self.assertEqual(t2.getValue(),"Crane")
                self.assertEqual(type(t2.getValue()),str)
                
                #They are unparsed as-is.
                self.assertEqual(t0.unparseToString(),"Planetouched")
                self.assertEqual(t1.unparseToString(),"Origami")
                self.assertEqual(t2.unparseToString(),"Crane")
                
        def test_MgTypeEnums(self):
                t_creature = mtgcompiler.AST.mtypes.MgType(mtgcompiler.AST.mtypes.MgType.TypeEnum.Creature)
                t_instant = mtgcompiler.AST.mtypes.MgType(mtgcompiler.AST.mtypes.MgType.TypeEnum.Instant)
                
                self.assertTrue(t_creature.isPermanentType())
                self.assertTrue(t_instant.isInstantOrSorceryType())
                self.assertFalse(t_creature.isInstantOrSorceryType())
                self.assertFalse(t_instant.isPermanentType())
                
                #Internally, they are represented by an enum.
                self.assertEqual(t_creature.getValue(),mtgcompiler.AST.mtypes.MgType.TypeEnum.Creature)
                self.assertEqual(type(t_creature.getValue()),mtgcompiler.AST.mtypes.MgType.TypeEnum)
                self.assertEqual(t_instant.getValue(),mtgcompiler.AST.mtypes.MgType.TypeEnum.Instant)
                self.assertEqual(type(t_instant.getValue()),mtgcompiler.AST.mtypes.MgType.TypeEnum)
                
                #During unparsing, they are converted into an equivalent String representation.
                self.assertEqual(t_creature.unparseToString(),"Creature")
                self.assertEqual(t_instant.unparseToString(),"Instant")
                
        def test_MgSupertypeEnums(self):
                t_legendary = mtgcompiler.AST.mtypes.MgSupertype(mtgcompiler.AST.mtypes.MgSupertype.SupertypeEnum.Legendary)
                self.assertEqual(t_legendary.getValue(),mtgcompiler.AST.mtypes.MgSupertype.SupertypeEnum.Legendary)
                self.assertEqual(t_legendary.unparseToString(),"Legendary")
                
        def test_MgSubtypeEnums(self):
                t_ferret = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Ferret)
                t_aura = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.EnchantmentSubtypeEnum.Aura)
                t_vehicle = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.ArtifactSubtypeEnum.Vehicle)
                t_arcane = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.SpellSubtypeEnum.Arcane)
                t_forest = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.LandSubtypeEnum.Forest)
                t_gideon = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.PlaneswalkerSubtypeEnum.Gideon)
                t_zendikar = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.PlanarSubtypeEnum.Zendikar)
                 
                self.assertTrue(t_ferret.isCreatureSubtype())
                self.assertTrue(t_aura.isEnchantmentSubtype())
                self.assertTrue(t_vehicle.isArtifactSubtype())
                self.assertTrue(t_arcane.isSpellSubtype())
                self.assertTrue(t_forest.isLandSubtype())
                self.assertTrue(t_gideon.isPlaneswalkerSubtype())
                self.assertTrue(t_zendikar.isPlanarSubtype())

        def test_ReplaceValue(self):
                #Originally t0 holds the creature type.
                t0 = mtgcompiler.AST.mtypes.MgType(mtgcompiler.AST.mtypes.MgType.TypeEnum.Creature)
                
                self.assertEqual(t0.getValue(),mtgcompiler.AST.mtypes.MgType.TypeEnum.Creature)
                self.assertTrue(t0.isPermanentType())
                self.assertFalse(t0.isInstantOrSorceryType())
                
                #We then swap creature for instant.
                t0.setValue(mtgcompiler.AST.mtypes.MgType.TypeEnum.Instant)

                self.assertEqual(t0.getValue(),mtgcompiler.AST.mtypes.MgType.TypeEnum.Instant)
                self.assertFalse(t0.isPermanentType())
                self.assertTrue(t0.isInstantOrSorceryType())
                
        def test_traversability(self):
                #Type nodes can be visited by a visitor, but they have no children.
                t_legendary = mtgcompiler.AST.mtypes.MgSupertype(mtgcompiler.AST.mtypes.MgSupertype.SupertypeEnum.Legendary)
                t_creature = mtgcompiler.AST.mtypes.MgType(mtgcompiler.AST.mtypes.MgType.TypeEnum.Creature)
                t_ferret = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Ferret)
                
                self.assertTrue(t_legendary.isTraversable())
                self.assertTrue(t_creature.isTraversable())
                self.assertTrue(t_ferret.isTraversable())
                
                self.assertEqual(len(t_legendary.getTraversalSuccessors()),0)
                self.assertEqual(len(t_creature.getTraversalSuccessors()),0)
                self.assertEqual(len(t_ferret.getTraversalSuccessors()),0)
                
                
        
if __name__ == '__main__':
    unittest.main()