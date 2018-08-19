import abc
import mtgcompiler.AST.core as core
from enum import Enum

#@functools.total_ordering
class MgAbstractType(core.MgNode):
        """MgAbstractType is an uninstantiable parent class for types, subtypes, and supertypes. 
        It provides the functionalities common to all (sub|super)*type objects."""
        
        def setValue(self, value):
                """Setter method for the value attribute. This is the value held by the type object. 
                It can either be a pre-defined Enum type, or a string in the case of a custom (sub|super)*type."""
                self._value=value
        
        def getValue(self):
                """Access method for the value attribute. This is the value held by the type object. 
                It can either be a pre-defined Enum type, or a string in the case of a custom (sub|super)*type."""
                return self._value
                
        def isEquivalentType(self,otherType):
                """Type equivalence method. Two types are considered equivalent if they
                share the same class and have have equal values."""
                return type(self) == type(otherType) and self._value == otherType.getValue()
                
        def isCustomType(self):
                """Checks whether a type is a user-defined custom type, which must be a string."""
                return type(self._value) is str
                
        def isChild(self,child):
                """This class is a leaf node. It has no children."""
                return False
                
        def getTraversalSuccessors(self):
                """This class is a leaf node. It has no children."""
                return []
        
        def unparseToString(self):
                if type(self._value) is str:
                        return self._value
                else:
                        return self._value.value

class MgType(MgAbstractType):
        """This node represents Magic types, such as Creature or Sorcery."""
        class TypeEnum(Enum):
                Artifact = "Artifact"
                Conspiracy = "Conspiracy"
                Creature = "Creature"
                Enchantment = "Enchantment"
                Instant = "Instant"
                Land = "Land"
                Phenomenon = "Phenomenon"
                Plane = "Plane"
                Planeswalker = "Planeswalker"
                Scheme = "Scheme"
                Sorcery = "Sorcery"
                Tribal = "Tribal"
                Vanguard = "Vanguard"

        def __init__(self,value):
                #super(MgAbstractType,self).__init__()
                self._traversable = True
                self._value = value
                
        def isPermanentType(self):
                """Checks whether the given type is a recognized permanent type."""
                return self._value in {MgType.TypeEnum.Artifact, MgType.TypeEnum.Creature, MgType.TypeEnum.Enchantment, MgType.TypeEnum.Land, MgType.TypeEnum.Planeswalker}
                
        def isSupplementaryType(self):
                """Checks whether a type is one used in supplemental products like Planechase or Conspiracy."""
                return self._value in {MgType.TypeEnum.Conspiracy,MgType.TypeEnum.Phenomenon,MgType.TypeEnum.Plane,MgType.TypeEnum.Scheme,MgType.TypeEnum.Vanguard}
                
        def isInstantOrSorceryType(self):
                """Checks whether a type is an instant or sorcery."""
                return self._value in {MgType.TypeEnum.Instant,MgType.TypeEnum.Sorcery}
    
class MgSubtype(MgAbstractType):
        """This class represents Magic subtypes, such as Arcane or Elephant."""
        class SpellSubtypeEnum(Enum):
                """Instants and sorceries share their lists of subtypes; these subtypes are called spell types."""
                Arcane = "Arcane"
                Trap = "Trap"
        
        class LandSubtypeEnum(Enum):
                """Lands have their own unique set of subtypes; these subtypes are called land types."""
                Desert = "Desert"
                Forest = "Forest"
                Gate = "Gate"
                Island = "Island"
                Lair = "Lair"
                Locus = "Locus"
                Mine = "Mine"
                Mountain = "Mountain"
                Plains = "Plains"
                PowerPlant = "Power-Plant"
                Swamp = "Swamp"
                Tower = "Tower"
                Urzas = "Urza's"
                
        class ArtifactSubtypeEnum(Enum):
                """Artifacts have their own unique set of subtypes; these subtypes are called artifact types."""
                Clue = "Clue"
                Contraption = "Contraption"
                Equipment = "Equipment"
                Fortification = "Fortification"
                Treasure = "Treasure"
                Vehicle = "Vehicle"
                
        class EnchantmentSubtypeEnum(Enum):
                """Enchantments have their own unique set of subtypes; these subtypes are called enchantment types."""
                Aura = "Aura"
                Cartouche = "Cartouche"
                Curse = "Curse"
                Saga = "Saga"
                Shrine = "Shrine"
        
        class PlaneswalkerSubtypeEnum(Enum):
                """Planeswalkers have their own unique set of subtypes; these subtypes are called planeswalker types."""
                Ajani = "Ajani"
                Aminatou = "Aminatou"
                Angrath = "Angrath"
                Arlinn = "Arlinn"
                Ashiok = "Ashiok"
                Bolas = "Bolas"
                Chandra = "Chandra"
                Dack = "Dack"
                Daretti = "Daretti"
                Domri = "Domri"
                Dovin = "Dovin"
                Elspeth = "Elspeth"
                Estrid = "Estrid"
                Freyalise = "Freyalise"
                Garruk = "Garruk"
                Gideon = "Gideon"
                Huatli = "Huatli"
                Jace = "Jace"
                Jaya = "Jaya"
                Karn = "Karn"
                Kaya = "Kaya"
                Kiora = "Kiora"
                Koth = "Koth"
                Liliana = "Liliana"
                Nahiri = "Nahiri"
                Narset = "Narset"
                Nissa = "Nissa"
                Nixilis = "Nixilis"
                Ral = "Ral"
                Rowan = "Rowan"
                Saheeli = "Saheeli"
                Samut = "Samut"
                Sarkhan = "Sarkhan"
                Sorin = "Sorin"
                Tamiyo = "Tamiyo"
                Teferi = "Teferi"
                Tezzeret = "Tezzeret"
                Tibalt = "Tibalt"
                Ugin = "Ugin"
                Venser = "Venser"
                Vivien = "Vivien"
                Vraska = "Vraska"
                Will = "Will"
                Windgrace = "Windgrace"
                Xenagos = "Xenagos"
                Yanggu = "Yanggu"
                Yanling = "Yanling"
                
        class CreatureSubtypeEnum(Enum):
                """Creatures and tribals share their lists of subtypes; these subtypes are called creature types."""
                Advisor = "Advisor"
                Aetherborn = "Aetherborn"
                Ally = "Ally"
                Angel = "Angel"
                Antelope = "Antelope"
                Ape = "Ape"
                Archer = "Archer"
                Archon = "Archon"
                Artificer = "Artificer"
                Assassin = "Assassin"
                AssemblyWorker = "Assembly-Worker"
                Atog = "Atog"
                Aurochs = "Aurochs"
                Avatar = "Avatar"
                Azra = "Azra"
                Badger = "Badger"
                Barbarian = "Barbarian"
                Basilisk = "Basilisk"
                Bat = "Bat"
                Bear = "Bear"
                Beast = "Beast"
                Beeble = "Beeble"
                Berserker = "Berserker"
                Bird = "Bird"
                Blinkmoth = "Blinkmoth"
                Boar = "Boar"
                Bringer = "Bringer"
                Brushwagg = "Brushwagg"
                Camarid = "Camarid"
                Camel = "Camel"
                Caribou = "Caribou"
                Carrier = "Carrier"
                Cat = "Cat"
                Centaur = "Centaur"
                Cephalid = "Cephalid"
                Chimera = "Chimera"
                Citizen = "Citizen"
                Cleric = "Cleric"
                Cockatrice = "Cockatrice"
                Construct = "Construct"
                Coward = "Coward"
                Crab = "Crab"
                Crocodile = "Crocodile"
                Cyclops = "Cyclops"
                Dauthi = "Dauthi"
                Demon = "Demon"
                Deserter = "Deserter"
                Devil = "Devil"
                Dinosaur = "Dinosaur"
                Djinn = "Djinn"
                Dragon = "Dragon"
                Drake = "Drake"
                Dreadnought = "Dreadnought"
                Drone = "Drone"
                Druid = "Druid"
                Dryad = "Dryad"
                Dwarf = "Dwarf"
                Efreet = "Efreet"
                Egg = "Egg"
                Elder = "Elder"
                Eldrazi = "Eldrazi"
                Elemental = "Elemental"
                Elephant = "Elephant"
                Elf = "Elf"
                Elk = "Elk"
                Eye = "Eye"
                Faerie = "Faerie"
                Ferret = "Ferret"
                Fish = "Fish"
                Flagbearer = "Flagbearer"
                Fox = "Fox"
                Frog = "Frog"
                Fungus = "Fungus"
                Gargoyle = "Gargoyle"
                Germ = "Germ"
                Giant = "Giant"
                Gnome = "Gnome"
                Goat = "Goat"
                Goblin = "Goblin"
                God = "God"
                Golem = "Golem"
                Gorgon = "Gorgon"
                Graveborn = "Graveborn"
                Gremlin = "Gremlin"
                Griffin = "Griffin"
                Hag = "Hag"
                Harpy = "Harpy"
                Hellion = "Hellion"
                Hippo = "Hippo"
                Hippogriff = "Hippogriff"
                Homarid = "Homarid"
                Homunculus = "Homunculus"
                Horror = "Horror"
                Horse = "Horse"
                Hound = "Hound"
                Human = "Human"
                Hydra = "Hydra"
                Hyena = "Hyena"
                Illusion = "Illusion"
                Imp = "Imp"
                Incarnation = "Incarnation"
                Insect = "Insect"
                Jackal = "Jackal"
                Jellyfish = "Jellyfish"
                Juggernaut = "Juggernaut"
                Kavu = "Kavu"
                Kirin = "Kirin"
                Kithkin = "Kithkin"
                Knight = "Knight"
                Kobold = "Kobold"
                Kor = "Kor"
                Kraken = "Kraken"
                Lamia = "Lamia"
                Lammasu = "Lammasu"
                Leech = "Leech"
                Leviathan = "Leviathan"
                Lhurgoyf = "Lhurgoyf"
                Licid = "Licid"
                Lizard = "Lizard"
                Manticore = "Manticore"
                Masticore = "Masticore"
                Mercenary = "Mercenary"
                Merfolk = "Merfolk"
                Metathran = "Metathran"
                Minion = "Minion"
                Minotaur = "Minotaur"
                Mole = "Mole"
                Monger = "Monger"
                Mongoose = "Mongoose"
                Monk = "Monk"
                Monkey = "Monkey"
                Moonfolk = "Moonfolk"
                Mutant = "Mutant"
                Myr = "Myr"
                Mystic = "Mystic"
                Naga = "Naga"
                Nautilus = "Nautilus"
                Nephilim = "Nephilim"
                Nightmare = "Nightmare"
                Nightstalker = "Nightstalker"
                Ninja = "Ninja"
                Noggle = "Noggle"
                Nomad = "Nomad"
                Nymph = "Nymph"
                Octopus = "Octopus"
                Ogre = "Ogre"
                Ooze = "Ooze"
                Orb = "Orb"
                Orc = "Orc"
                Orgg = "Orgg"
                Ouphe = "Ouphe"
                Ox = "Ox"
                Oyster = "Oyster"
                Pangolin = "Pangolin"
                Pegasus = "Pegasus"
                Pentavite = "Pentavite"
                Pest = "Pest"
                Phelddagrif = "Phelddagrif"
                Phoenix = "Phoenix"
                Pilot = "Pilot"
                Pincher = "Pincher"
                Pirate = "Pirate"
                Plant = "Plant"
                Praetor = "Praetor"
                Prism = "Prism"
                Processor = "Processor"
                Rabbit = "Rabbit"
                Rat = "Rat"
                Rebel = "Rebel"
                Reflection = "Reflection"
                Rhino = "Rhino"
                Rigger = "Rigger"
                Rogue = "Rogue"
                Sable = "Sable"
                Salamander = "Salamander"
                Samurai = "Samurai"
                Sand = "Sand"
                Saproling = "Saproling"
                Satyr = "Satyr"
                Scarecrow = "Scarecrow"
                Scion = "Scion"
                Scorpion = "Scorpion"
                Scout = "Scout"
                Serf = "Serf"
                Serpent = "Serpent"
                Servo = "Servo"
                Shade = "Shade"
                Shaman = "Shaman"
                Shapeshifter = "Shapeshifter"
                Sheep = "Sheep"
                Siren = "Siren"
                Skeleton = "Skeleton"
                Slith = "Slith"
                Sliver = "Sliver"
                Slug = "Slug"
                Snake = "Snake"
                Soldier = "Soldier"
                Soltari = "Soltari"
                Spawn = "Spawn"
                Specter = "Specter"
                Spellshaper = "Spellshaper"
                Sphinx = "Sphinx"
                Spider = "Spider"
                Spike = "Spike"
                Spirit = "Spirit"
                Splinter = "Splinter"
                Sponge = "Sponge"
                Squid = "Squid"
                Squirrel = "Squirrel"
                Starfish = "Starfish"
                Surrakar = "Surrakar"
                Survivor = "Survivor"
                Tetravite = "Tetravite"
                Thalakos = "Thalakos"
                Thopter = "Thopter"
                Thrull = "Thrull"
                Treefolk = "Treefolk"
                Trilobite = "Trilobite"
                Triskelavite = "Triskelavite"
                Troll = "Troll"
                Turtle = "Turtle"
                Unicorn = "Unicorn"
                Vampire = "Vampire"
                Vedalken = "Vedalken"
                Viashino = "Viashino"
                Volver = "Volver"
                Wall = "Wall"
                Warrior = "Warrior"
                Weird = "Weird"
                Werewolf = "Werewolf"
                Whale = "Whale"
                Wizard = "Wizard"
                Wolf = "Wolf"
                Wolverine = "Wolverine"
                Wombat = "Wombat"
                Worm = "Worm"
                Wraith = "Wraith"
                Wurm = "Wurm"
                Yeti = "Yeti"
                Zombie = "Zombie"
                Zubera = "Zubera"
                
        class PlanarSubtypeEnum(Enum):
                """Planes have their own unique set of subtypes; these subtypes are called planar types."""
                Alara = "Alara"
                Arkhos = "Arkhos"
                Azgol = "Azgol"
                Belenon = "Belenon"
                BolassMeditationRealm = "Bolas’s Meditation Realm"
                Dominaria = "Dominaria"
                Equilor = "Equilor"
                Ergamon = "Ergamon"
                Fabacin = "Fabacin"
                Innistrad = "Innistrad"
                Iquatana = "Iquatana"
                Ir = "Ir"
                Kaldheim = "Kaldheim"
                Kamigawa = "Kamigawa"
                Karsus = "Karsus"
                Kephalai = "Kephalai"
                Kinshala = "Kinshala"
                Kolbahan = "Kolbahan"
                Kyneth = "Kyneth"
                Lorwyn = "Lorwyn"
                Luvion = "Luvion"
                Mercadia = "Mercadia"
                Mirrodin = "Mirrodin"
                Moag = "Moag"
                Mongseng = "Mongseng"
                Muraganda = "Muraganda"
                NewPhyrexia = "New Phyrexia"
                Phyrexia = "Phyrexia"
                Pyrulea = "Pyrulea"
                Rabiah = "Rabiah"
                Rath = "Rath"
                Ravnica = "Ravnica"
                Regatha = "Regatha"
                Segovia = "Segovia"
                SerrasRealm = "Serra’s Realm"
                Shadowmoor = "Shadowmoor"
                Shandalar = "Shandalar"
                Ulgrotha = "Ulgrotha"
                Valla = "Valla"
                Vryn = "Vryn"
                Wildfire = "Wildfire"
                Xerex = "Xerex"
                Zendikar = "Zendikar"
        
        def __init__(self,value):
                self._traversable = True
                self._value = value

        def isSpellSubtype(self):
                return type(self._value) is MgSubtype.SpellSubtypeEnum

        def isArtifactSubtype(self):
                return type(self._value) is MgSubtype.ArtifactSubtypeEnum

        def isLandSubtype(self):
                return type(self._value) is MgSubtype.LandSubtypeEnum

        def isEnchantmentSubtype(self):
                return type(self._value) is MgSubtype.EnchantmentSubtypeEnum

        def isPlaneswalkerSubtype(self):
                return type(self._value) is MgSubtype.PlaneswalkerSubtypeEnum

        def isCreatureSubtype(self):
                return type(self._value) is MgSubtype.CreatureSubtypeEnum

        def isPlanarSubtype(self):
                return type(self._value) is MgSubtype.PlanarSubtypeEnum

class MgSupertype(MgAbstractType):
        """This class represents Magic supertypes, such as Snow or World."""
        class SupertypeEnum(Enum):
                Basic = "Basic"
                Legendary = "Legendary"
                Ongoing = "Ongoing"
                Snow = "Snow"
                World = "World"

        def __init__(self,value):
                #super(MgAbstractType,self).__init__()
                self._traversable = True
                self._value = value