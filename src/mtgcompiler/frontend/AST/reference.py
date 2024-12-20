import mtgcompiler.frontend.AST.core as core
from enum import Enum

class MgAbstractReference(core.MgNode):
        """The abstract parent class for all reference classes. A reference is a term that is connected back,
        in some way, to a previously defined game entity. All references have one thing in common, an antecedent
        attribute, a node that the reference ultimately refers to. This attribute is typically None when the
        reference is instantiated because resolving its identity happens in a subsequent pass (with the exception of
        card name references, which can be determined during the first pass).
        """
        
        def __init__(self,antecedent=None):
                """antecedent: The thing that the that-reference refers to."""
                self._traversable = True
                self._antecedent = antecedent
                
        def hasAntecedent(self):
                """Checks whether the that-reference has an identified antecedent."""
                return self._antecedent is not None
                
        def getAntecedent(self):
                """Gets the antecedent of the that-reference, assuming it has been resolved."""
                return self._antecedent
                
        def setAntecedent(self,antecedent):
                """Assigns an antecedent to the that-reference."""
                self._antecedent = antecedent
                
                
class MgAbilityReference(MgAbstractReference):
        """An ability reference is a generic reference to an ability, like Cairn Wanderer referring to
        protection in the abstract. TODO: I haven't decided if this is the best way forward or not."""
        pass

class MgNameReference(MgAbstractReference):
        """A stand-in used when a card refers to its own name in its text."""
        def __init__(self,nameref,firstNameOnly=False):
                """
                nameref: The MgName node to which this node refers.
                firstNameOnly: A flag that indicates that a name reference only uses the first
                name of a card. This can happen when you have multiple name references of a
                legendary creature. This flag is False by default. An example would be
                'Arashi, the Sky Asunder' vs. 'discard Arashi'. 
                """
                super().__init__(nameref)
                self._firstonly = firstNameOnly
                
        def isFirstNameOnly(self):
                """Checks whether this name reference only exposes the first name of a card."""
                return self._firstonly
                
        def setFirstNameOnly(self,firstNameOnly):
                """Sets whether this name reference only exposes the first name of a card."""
                self._firstonly = firstNameOnly
                
        def getNameReference(self):
                return self._antecedent
                
        def setNameReference(self,nameref):
                self._antecedent = nameref
                
        def isChild(self,child):
                """A name reference node links to another node, but that node is not
                its child."""
                return False
        
        def getTraversalSuccessors(self):
                """A name reference node links to another node, but that node is not
                its child."""
                return []
                
        def unparseToString(self):
                if self._antecedent == None:
                        #This can happen prior to binding.
                        if self._firstonly == True:
                                return "~f"
                        else:
                                return "~"
                if self._firstonly == True:
                        splitstr = self._antecedent.unparseToString().split(', ')
                        return splitstr[0]
                else:
                        return self._antecedent.unparseToString()
                
class MgSelfReference(MgAbstractReference):
        """This node is used when a card refers to itself as 'itself', 'himself', or 'herself'.
        Supporting this distinction would normally fall into the realm of grammatical features
        that should be handled by the unparser, but because Magic cards lack any inherent gender,
        we have to be able to specify the gender of the self-reference to handle cards like
        Sarkhan the Mad correctly.
        """
        class SelfEnum(Enum):
                Neutral = "itself"
                Male = "himself" #Note: As of 27 Aug 2018, 'himself' has only appeared on Sarkhan the Mad.
                Female = "herself" #Note: As of 27 Aug 2018, 'herself' has never appeared on a Magic card.
                
        def __init__(self,reftype=None,antecedent=None):
                """reftype: A SelfEnum, or None. If the default None is supplied, 'itself' is assumed."""
                super().__init__(antecedent)
                if reftype is None:
                        self._reftype = MgSelfReference.SelfEnum.Neutral
                else:
                        self._reftype = reftype
                        
        def isNeutral(self):
                """Checks whether the self-reference is gender neutral."""
                return self._reftype == MgSelfReference.SelfEnum.Neutral
                
        def setNeutral(self):
                self._reftype = MgSelfReference.SelfEnum.Neutral
                
        def isMale(self):
                """Checks whether the self-reference is gendered male."""
                return self._reftype == MgSelfReference.SelfEnum.Male
                
        def setMale(self):
                self._reftype = MgSelfReference.SelfEnum.Male

        def isFemale(self):
                """Checks whether the self-reference is gendered Female."""
                return self._reftype == MgSelfReference.SelfEnum.Female
                
        def setFemale(self):
                self._reftype = MgSelfReference.SelfEnum.Female
                
        def isChild(self,child):
                """This node has no children."""
                return False
        
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return self._reftype.value
                

class MgThatReference(MgAbstractReference):
        """A reference to a game entity that was previously defined in a card.
        
        A that-reference can expose parts of the previously declared player/object, in order
        to clarify to what thing the reference applies:
        
        'a green or white creature' -> 'that creature'
        'each player' -> 'that player'
        'target land' -> 'that land'
        
        A that-reference can also refer indirectly to some other player or object via the
        thing that it is referencing:
        
        'a creature' -> 'that creature's controller'
        
        A that-reference may also refer to an antecedent more generically:
        
        'exile target creature' -> 'return that card to the battlefield'
        'choose an opponent' -> 'that player'
        
        Finally, a that-reference can also refer to the anonymous result of a previous 'computation':
        
        'name a non-land card' -> 'all cards with that name'.
        
        The antecedents of that-references are not resolved during the first parsing step but during
        a subsequent pass.
         
        """
        def __init__(self,descriptor,antecedent=None):
                """
                descriptor: An expression that describes the antecedent.
                antecedent: The thing that the that-reference refers to. By default, this attribute is None
                to start, because the compiler makes a second pass after parsing and AST construction in order
                to resolve the identity of the antecedent. This is not necessary for parsing or unparsing, but it
                is relevant to analyzers.
                """
                super().__init__(antecedent)
                self._descriptor = descriptor
                self._descriptor.setParent(self)
                
        def getDescriptor(self):
                """Get the descriptor for the that-reference."""
                return self._descriptor
                
        def setDescriptor(self,descriptor):
                """Set the descriptor for the that-reference."""
                self._descriptor = descriptor
                if self._descriptor is not None:
                        self._descriptor.setParent(self)
                
        def isChild(self,child):
                """This node has one child, the descriptor expression."""
                return self._descriptor is not None and child == self._descriptor
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its descriptor."""
                return [node for node in {self._descriptor} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                return "that {0}".format(self._descriptor.unparseToString())
                
                
class MgItReference(MgAbstractReference):
        """Used when a card refers to a previously defined object as 'it'.
        Unlike a that-reference, an it-reference has no descriptor. It does,
        however, have an antecedent.
        """
        
        def __init__(self,antecedent=None):
                """
                antecedent: The thing that the it-reference refers to. By default, this attribute is None
                to start, because the compiler makes a second pass after parsing and AST construction in order
                to resolve the identity of the antecedent. This is not necessary for parsing or unparsing, but it
                is relevant to analyzers.
                """
                super().__init__(antecedent)
                
        def isChild(self,child):
                """A name reference node links to another node, but that node is not
                its child."""
                return False
        
        def getTraversalSuccessors(self):
                """A name reference node links to another node, but that node is not
                its child."""
                return []
                
        def unparseToString(self):
                return "it"
                
                
class MgThisReference(MgAbstractReference):
        """
        
        'Whenever this creature transforms [...]'
        'Until end of turn, creatures you control gain "Whenever this creature [...]"'
        """
        def __init__(self,descriptor,antecedent=None):
                """
                descriptor: An expression that describes the antecedent.
                antecedent: The thing that the that-reference refers to. By default, this attribute is None
                to start, because the compiler makes a second pass after parsing and AST construction in order
                to resolve the identity of the antecedent. This is not necessary for parsing or unparsing, but it
                is relevant to analyzers.
                """
                super().__init__(antecedent)
                self._descriptor = descriptor
                self._descriptor.setParent(self)
                
        def getDescriptor(self):
                """Get the descriptor for the that-reference."""
                return self._descriptor
                
        def setDescriptor(self,descriptor):
                """Set the descriptor for the that-reference."""
                self._descriptor = descriptor
                if self._descriptor is not None:
                        self._descriptor.setParent(self)
                
        def isChild(self,child):
                """This node has one child, the descriptor expression."""
                return self._child is not None and child == self._descriptor
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its descriptor."""
                return [node for node in {self._descriptor} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                return "this {0}".format(self._descriptor.unparseToString())

        

class MgPlayerTerm(core.MgNode):
        """This node represents a description of a player. From the rules:
        
        102.1. A player is one of the people in the game. The active player is the player whose turn it is.
        The other players are nonactive players.

        102.2. In a two-player game, a player’s opponent is the other player.

        102.3. In a multiplayer game between teams, a player’s teammates are the other players on their team,
        and the player’s opponents are all players not on their team.

        102.4. A spell or ability may use the term “your team” as shorthand for “you and/or your teammates.”
        In a game that isn’t a multiplayer game between teams, “your team” means the same thing as “you.”
        """
        
        #Note: The possessives are only used by possessive expressions.
        class PlayerTermEnum(Enum):
                You = {"nominative_singular": "you", "nominative_plural": "NOTUSED","possessive_singular": "your","possessive_plural" : "NOTUSED"}
                Opponent = {"nominative_singular": "opponent", "nominative_plural": "opponents","possessive_singular": "opponent's","possessive_plural" : "opponents'"}
                Teammate = {"nominative_singular": "teammate", "nominative_plural": "teammates","possessive_singular": "teammate's","possessive_plural" : "teammates'"}
                Team =  {"nominative_singular": "team", "nominative_plural": "teams","possessive_singular": "team's","possessive_plural" : "teams'"}
                Owner =  {"nominative_singular": "owner", "nominative_plural": "owners","possessive_singular": "owner's","possessive_plural" : "owners'"}
                Controller = {"nominative_singular": "controller", "nominative_plural": "controllers","possessive_singular": "controller's","possessive_plural" : "controllers'"}
                Player = {"nominative_singular": "player", "nominative_plural": "players","possessive_singular": "player's","possessive_plural" : "players'"}
        
        def __init__(self,playerEnum,isPlural=False):
                """
                playerEnum: An instance of PlayerTermEnum
                isPlural: A flag indicating whether the player term should be interpreted as plural.
                ##isPossessive: A flag indicating whether the player term should be interpreted as possessive.
                """
                self._playerEnum = playerEnum
                self._isPlural = isPlural
                
        def isPlural(self):
                """Checks whether this player term is plural."""
                return self._isPlural == True
                
        def setIsPlural(self,isPlural):
                """Sets whether this player term is plural."""
                self._isPlural = isPlural
                
        def isYou(self):
                """Checks whether the player term refers to you."""
                return self._playerEnum == MgPlayerTerm.PlayerTermEnum.You
        
        def setYou(self):
                """Sets the player term to refer to you."""
                self._playerEnum = MgPlayerTerm.PlayerTermEnum.You
        
        def isOpponent(self):
                """Checks whether the player term refers to one or more opponents."""
                return self._playerEnum == MgPlayerTerm.PlayerTermEnum.Opponent
        
        def setOpponent(self):
                """Sets the player term to refer to one or more opponents."""
                self._playerEnum = MgPlayerTerm.PlayerTermEnum.Opponent
                
        def isTeammate(self):
                """Checks whether the player term refers to one or more teammates."""
                return self._playerEnum == MgPlayerTerm.PlayerTermEnum.Teammate
        
        def setTeammate(self):
                """Sets the player term to refer to one or more teammates."""
                self._playerEnum = MgPlayerTerm.PlayerTermEnum.Teammate
                
        def isTeam(self):
                """Checks whether the player term refers to a team. Note this is not the same as
                the plural of teammate."""
                return self._playerEnum == MgPlayerTerm.PlayerTermEnum.Team
        
        def setTeam(self):
                """Sets the player term to refer to a team. Note this is not the same as
                the plural of teammate."""
                self._playerEnum = MgPlayerTerm.PlayerTermEnum.Team
                
        def isOwner(self):
                """Checks whether the player term refers to one or more owners."""
                return self._playerEnum == MgPlayerTerm.PlayerTermEnum.Owner
        
        def setOwner(self):
                """Sets the player term to refer to one or more owners."""
                self._playerEnum = MgPlayerTerm.PlayerTermEnum.Owner
        
        def isController(self):
                """Checks whether the player term refers to one or more controllers."""
                return self._playerEnum == MgPlayerTerm.PlayerTermEnum.Controller
        
        def setController(self):
                """Sets the player term to refer to one or more controllers."""
                self._playerEnum = MgPlayerTerm.PlayerTermEnum.Controller
                
        def isPlayer(self):
                """Checks whether the player term refers to one or more players."""
                return self._playerEnum == MgPlayerTerm.PlayerTermEnum.Player
        
        def setPlayer(self):
                """Sets the player term to refer to one or more players."""
                self._playerEnum = MgPlayerTerm.PlayerTermEnum.Player
                
        def getPossessive(self):
                if self._isPlural == True:
                        return self._playerEnum.value["possessive_plural"]
                else:
                        return self._playerEnum.value["possessive_singular"]
        
        def unparseToString(self):
                #By default, unparseToString provides the nominative.
                if self._isPlural == True:
                        return self._playerEnum.value["nominative_plural"]
                else:
                        return self._playerEnum.value["nominative_singular"]
        

class MgName(core.MgNode):
        """This node represents a name, such as the name of a card."""
        def __init__(self,name=""):
                """name: a string containing a name."""
                self._traversable = True
                self._name = name
        
        def getName(self):
                return self._name
                
        def setName(self,name):
                self._name = name
        
        def isChild(self,child):
                return False
                
        def getTraversalSuccessors(self):
                return []
                
        def unparseToString(self):
                return self._name
                
                
                
class MgDamageType(core.MgNode):
        """Used to describe a type of damage in a deals-damage expression."""
        class DamageTypeEnum(Enum):
                RegularDamage = "damage"
                NoncombatDamage = "noncombat damage"
                CombatDamage = "combat damage"
                
        def __init__(self,damageType):
                """
                damageType: A damage type enum.
                """
                self._damagetype = damageType
                self._traversable = True
        
        def isRegularDamage(self):
                """Checks whether this damage type is regular, plain old damage."""
                return self._damagetype == MgDamageType.DamageTypeEnum.RegularDamage
                
        def setRegularDamage(self):
                """Sets this damage type as regular, plain old damage."""
                self._damagetype = MgDamageType.DamageTypeEnum.RegularDamage
                
        def isNoncombatDamage(self):
                """Checks whether this damage type is specifically non-combat damage."""
                return self._damagetype == MgDamageType.DamageTypeEnum.NoncombatDamage
                
        def setNoncombatDamage(self):
                """Sets this damage type as non-combat damage specifically."""
                self._damagetype = MgDamageType.DamageTypeEnum.NoncombatDamage
                
        def isNoncombatDamage(self):
                """Checks whether this damage type is specifically non-combat damage."""
                return self._damagetype == MgDamageType.DamageTypeEnum.NoncombatDamage
                
        def setNoncombatDamage(self):
                """Sets this damage type as non-combat damage specifically."""
                self._damagetype = MgDamageType.DamageTypeEnum.NoncombatDamage
                
        def isCombatDamage(self):
                """Checks whether this damage type is specifically combat damage."""
                return self._damagetype == MgDamageType.DamageTypeEnum.CombatDamage
                
        def setCombatDamage(self):
                """Sets this damage type as combat damage specifically."""
                self._damagetype = MgDamageType.DamageTypeEnum.CombatDamage
                
        def isChild(self,child):
                """Damage type nodes have no children."""
                return False
                
        def getTraversalSuccessors(self):
                """Damage type nodes have no successors."""
                return []
                
        def unparseToString(self):
                return self._damagetype.value
                
class MgDeclarationModifier(core.MgNode):
        """A parent class for modifiers to players/objects"""
        def __init__(self,modifier):
                """
                modifier: aA appropriate modifier enum object.
                """
                self._modifier = modifier
                self._traversable = True
                
        def getModifier(self):
                return self._modifier
                
        def setModifier(self,modifier):
                self._modifier = modifier
                
        def isChild(self,child):
                """Declaration modifiers have no children."""
                return False
                
        def getTraversalSuccessors(self):
                """Declaration modifiers have no successors."""
                return []
                
        def unparseToString(self):
                return self._modifier.value
        
class MgAbilityModifier(MgDeclarationModifier):
        """Used when describing what kind an ability is."""
        class AbilityModifierEnum(Enum):
                Triggered = "triggered"
                Activated = "activated"
                Mana = "mana"
                Loyalty = "loyalty"
                
        def __init__(self,modifier):
                assert(type(modifier) == MgAbilityModifier.AbilityModifierEnum)
                super().__init__(modifier)
                
                
class MgCombatStatusModifier(MgDeclarationModifier):
        class CombatStatusEnum(Enum):
                Attacking = "attacking"
                Defending = "defending"
                Attacked = "attacked"
                Blocking = "blocking"
                Blocked = "blocked"
                Active = "active"
                
        def __init__(self,modifier):
                assert(type(modifier) == MgCombatStatusModifier.CombatStatusEnum)
                super().__init__(modifier)

class MgKeywordStatusModifier(MgDeclarationModifier):
        """Keyword-status modifiers indicate that a player/object is affected by a keyword ability in some way,
        like a creature with soulbond can be paired, or a spell with kicker can be kicked."""
        class KeywordStatusEnum(Enum):
                Paired = "paired"
                Kicked = "kicked"
                FaceUp = "face-up"
                FaceDown = "face-down"
                Transformed = "transformed"
                Enchanted = "enchanted"
                Equipped = "equipped"
                Fortified = "fortified"
                Monstrous = "monstrous"
                Suspended = "suspended"
                
        def __init__(self,modifier):
                assert(type(modifier) == MgKeywordStatusModifier.KeywordStatusEnum)
                super().__init__(modifier)
        
class MgTapStatusModifier(MgDeclarationModifier):
        class TapStatusEnum(Enum):
                Tapped = "tapped"
                Untapped = "untapped"

        def __init__(self,modifier):
                assert(type(modifier) == MgTapStatusModifier.TapStatusEnum)
                super().__init__(modifier)
                
class MgEffectStatusModifier(MgDeclarationModifier):
        class EffectStatusEnum(Enum):
                Named = "named"
                Chosen = "chosen"
                Revealed = "revealed"
                Returned = "returned"
                Destroyed = "destroyed"
                Exiled = "exiled"
                Died = "died"
                Countered = "countered"
                Sacrificed = "sacrificed"
                Targeted = "the target of a spell or ability"
                Prevented = "prevented"
        def __init__(self,modifier):
                assert(type(modifier) == MgEffectStatusModifier.EffectStatusEnum)
                super().__init__(modifier)
                
                

class MgCharacteristicTerm(core.MgNode):
        """A term used to refer to the characteristic of some previously defined object. From the rules
        
        109.3. An object’s characteristics are name, mana cost, color, color indicator, card type, subtype,
        supertype, rules text, abilities, power, toughness, loyalty, hand modifier, and life modifier.
        Objects can have some or all of these characteristics. Any other information about an object
        isn’t a characteristic.
        """
        class CharacteristicEnum(Enum):
                Name = "name"
                ManaCost = "mana cost"
                ColorIndicator = "color indicator" #Has never been used.
                CardType = "card type"
                Subtype = "subtype"
                Supertype = "supertype"
                RulesText = "rules text" #Only used in un-cards so far.
                Abilities = "abilities"
                Power = "power"
                Toughness = "toughness"
                Loyalty = "loyalty"
                HandModifier = "hand modifier" #Has never been used.
                LifeModifier = "life modifier" #Has never been used.
                
        def __init__(self,value):
                """value: a CharacteristicEnum."""
                self._traversable = True
                self._value = value
                
        def getValue(self):
                """Access method for the value attribute. This is the value held by the characteristic object. 
                This must be a pre-defined Enum type."""
                return self._value
                
        def setValue(self, value):
                """Setter method for the value attribute. This is the value held by the characteristic object. 
                This must be a pre-defined Enum type."""
                self._value=value

class MgQualifier(core.MgNode):
        """A qualifier is a term that specifies the state of an object (see comp rule 109 for objects).
        For example, 'Elf spell','Elf permanent','Elf token', or 'Elf source'.
        """
        class QualifierEnum(Enum):
                Ability = "ability"
                Card = "card"
                Permanent = "permanent"
                Source = "source"
                Spell = "spell"
                Token = "token"
                
        def __init__(self,value):
                """value: a QualifierEnum."""
                self._traversable = True
                self._value = value
                
        def getValue(self):
                """Access method for the value attribute. This is the value held by the qualifier object. 
                This must be a pre-defined Enum type."""
                return self._value
                
        def setValue(self, value):
                """Setter method for the value attribute. This is the value held by the qualifier object. 
                This must be a pre-defined Enum type."""
                self._value=value
                
        def isChild(self,child):
                """This class is a leaf node. It has no children."""
                return False
                
        def getTraversalSuccessors(self):
                """This class is a leaf node. It has no children."""
                return []
                
        def unparseToString(self):
                return self._value.value
    
class MgTimeTerm(core.MgNode):
        """This class is the parent class for nodes that represent a point in time in a turn, such as 
        the precombat Main phase or the cleanup step."""
        
        def __init__(self):
                self._traversable = True 
        
        def isChild(self,child):
                """Time terms have no children."""
                return False
                
        def getTraversalSuccessors(self):
                """Time terms have no successors."""
                return []
        
        
class MgPhaseTerm(MgTimeTerm):
        """Represents a phase in a turn, such as the precombat Main phase."""
        class PhaseEnum(Enum):
                Beginning = "beginning phase"
                PrecombatMain = "precombat main phase"
                Combat = "combat phase"
                PostcombatMain = "postcombat main phase"
                Ending = "ending phase"
                
        def __init__(self,phaseEnum):
                """
                phaseEnum: A PhaseEnum instance.
                """
                super().__init__()
                self._phase = phaseEnum
                
        def getPhaseValue(self):
                """Get the value for this phase (the Enum instance)."""
                return self._phase
                
        def setPhaseValue(self,phaseEnum):
                """Set the value for this phase (the Enum instance)."""
                self._phase = phaseEnum
                
        def isBeginning(self):
                """Checks whether this phase is the beginning phase."""
                return self._phase == MgPhaseTerm.PhaseEnum.Beginning
                
        def setBeginning(self):
                """Sets this phase to be the beginning phase."""
                self._phase = MgPhaseTerm.PhaseEnum.Beginning
                
        def isPrecombatMain(self):
                """Checks whether this phase is the precombat main phase."""
                return self._phase == MgPhaseTerm.PhaseEnum.PrecombatMain
                
        def setPrecombatMain(self):
                """Sets this phase to be the precombat main phase."""
                self._phase = MgPhaseTerm.PhaseEnum.PrecombatMain
                
        def isCombat(self):
                """Checks whether this phase is the combat phase."""
                return self._phase == MgPhaseTerm.PhaseEnum.Combat
                
        def setCombat(self):
                """Sets this phase to be the combat phase."""
                self._phase = MgPhaseTerm.PhaseEnum.Combat
                
        def isPostcombatMain(self):
                """Checks whether this phase is the postcombat main phase."""
                return self._phase == MgPhaseTerm.PhaseEnum.PostcombatMain
                
        def setPostcombatMain(self):
                """Sets this phase to be the postcombat main phase."""
                self._phase = MgPhaseTerm.PhaseEnum.PostcombatMain
                
        def isEnding(self):
                """Checks whether this phase is the ending phase."""
                return self._phase == MgPhaseTerm.PhaseEnum.Ending
                
        def setEnding(self):
                """Sets this phase to be the ending phase."""
                self._phase = MgPhaseTerm.PhaseEnum.Ending
                
        def unparseToString(self):
                return self._phase.value
                
        
                
class MgStepTerm(MgTimeTerm):
        """Represents a step in a phase, such as the draw step in the beginning phase."""
        class StepEnum(Enum):
                #BEGINNING STEPS
                Untap = "untap step"
                Upkeep = "upkeep step" #Usually shortened to just 'upkeep'
                Draw = "draw step"
                #COMBAT STEPS
                BeginningOfCombat = "beginning of combat"
                DeclareAttackers = "declare attackers step"
                DeclareBlockers = "declare blockers step"
                CombatDamage = "combat damage step"
                EndOfCombat = "end of combat"
                #ENDING STEPS
                EndStep = "end step"
                CleanupStep = "cleanup step"
        
        def __init__(self,stepEnum):
                """
                stepEnum: a StepEnum instance.
                """
                self._step = stepEnum
                
        def getStepValue(self):
                """Get the value for this step (the StepEnum instance)."""
                return self._step
                
        def setStepValue(self,stepEnum):
                """Set the value for this step (the StepEnum instance)."""
                self._step = stepEnum
                
        def isUntap(self):
                """Checks whether this step is an untap step"""
                return self._step == MgStepTerm.StepEnum.Untap
                
        def setUntap(self):
                """Sets this step as an untap step."""
                self._step = MgStepTerm.StepEnum.Untap
                
        def isUpkeep(self):
                """Checks whether this step is an upkeep step"""
                return self._step == MgStepTerm.StepEnum.Upkeep
                
        def setUpkeep(self):
                """Sets this step as an upkeep step."""
                self._step = MgStepTerm.StepEnum.Upkeep
                
        def isDraw(self):
                """Checks whether this step is a draw step"""
                return self._step == MgStepTerm.StepEnum.Draw
                
        def setDraw(self):
                """Sets this step as a draw step."""
                self._step = MgStepTerm.StepEnum.Draw
                
        def isBeginningOfCombat(self):
                """Checks whether this step is a beginning-of-combat step"""
                return self._step == MgStepTerm.StepEnum.BeginningOfCombat
                
        def setBeginningOfCombat(self):
                """Sets this step as a beginning-of-combat step."""
                self._step = MgStepTerm.StepEnum.BeginningOfCombat
                
        def isDeclareAttackers(self):
                """Checks whether this step is a declare-attackers step"""
                return self._step == MgStepTerm.StepEnum.DeclareAttackers
                
        def setDeclareAttackers(self):
                """Sets this step as a declare-attackers step."""
                self._step = MgStepTerm.StepEnum.DeclareAttackers
                
        def isDeclareBlockers(self):
                """Checks whether this step is a declare-blockers step"""
                return self._step == MgStepTerm.StepEnum.DeclareBlockers
                
        def setDeclareBlockers(self):
                """Sets this step as a declare-blockers step."""
                self._step = MgStepTerm.StepEnum.DeclareBlockers
                
        def isCombatDamage(self):
                """Checks whether this step is a combat-damage step"""
                return self._step == MgStepTerm.StepEnum.CombatDamage
                
        def setCombatDamage(self):
                """Sets this step as an combat-damage step."""
                self._step = MgStepTerm.StepEnum.CombatDamage
                
        def isEndOfCombat(self):
                """Checks whether this step is an end-of-combat step"""
                return self._step == MgStepTerm.StepEnum.EndOfCombat
                
        def setEndOfCombat(self):
                """Sets this step as an end-of-combat step."""
                self._step = MgStepTerm.StepEnum.EndOfCombat
                
        def isEnd(self):
                """Checks whether this step is an end step"""
                return self._step == MgStepTerm.StepEnum.End
                
        def setEnd(self):
                """Sets this step as an end step."""
                self._step = MgStepTerm.StepEnum.End
                
        def isCleanup(self):
                """Checks whether this step is a cleanup step"""
                return self._step == MgStepTerm.StepEnum.Cleanup
                
        def setCleanup(self):
                """Sets this step as a cleanup step."""
                self._step = MgStepTerm.StepEnum.Cleanup
                
        def unparseToString(self):
                return self._step.value
                
class MgTurnTerm(MgTimeTerm):
        """Represents a turn, such as your turn, the next turn, or an extra turn."""
        
        def __init__(self):
                super().__init__()
        
        def unparseToString(self):
                return "turn"
                
                
    
class MgZone(core.MgNode):
        """This node represents a zone in the game. From the rules:
        
        400. A zone is a place where objects can be during a game. 
        There are normally seven zones: library, hand, battlefield, graveyard, stack, exile, and command. 
        Some older cards also use the ante zone. Each player has their own library, hand, and graveyard. 
        The other zones are shared by all players.
        """
        
        class ZoneEnum(Enum):
                Battlefield = "the battlefield"
                Graveyard = "graveyard"
                Library = "library"
                Hand = "hand"
                Stack = "stack"
                Exile = "exile"
                Command = "command zone"
                Outside = "outside the game"
                Anywhere = "anywhere"

        def __init__(self,value):
                """value: a ZoneEnum."""
                self._traversable = True
                self._value = value
                
        def getValue(self):
                """Access method for the value attribute. This is the value held by the zone object. 
                This must be a pre-defined Enum type."""
                return self._value
                
        def setValue(self, value):
                """Setter method for the value attribute. This is the value held by the zone object. 
                This must be a pre-defined Enum type."""
                self._value=value
                
        def isChild(self,child):
                """This class is a leaf node. It has no children."""
                return False
                
        def getTraversalSuccessors(self):
                """This class is a leaf node. It has no children."""
                return []
                
        def unparseToString(self):
                return self._value.value
                

class MgTapUntapSymbol(core.MgNode):
        """Represents a tap or untap symbol, used in costs that require something to be tapped."""
        def __init__(self,isTap):
                """
                isTap: A flag indicating that the symbol is a tap symbol. False is an untap symbol.
                """
                self._traversable = True
                self._isTap = isTap
                
        def isTap(self):
                """Checks whether the symbol is a tap symbol."""
                return self._isTap == True
                
        def setTap(self):
                """Sets this symbol to be a tap symbol."""
                self._isTap = True
                
        def isUntap(self):
                """Checks whether the symbol is an untap symbol."""
                return self._isTap == False
        
        def setUntap(self):
                """Sets this symbol to be an untap symbol."""
                self._isUntap = False
        
        def isChild(self,child):
                """This class is a leaf node. It has no children."""
                return False
                
        def getTraversalSuccessors(self):
                """This class is a leaf node. It has no children."""
                return []
                
        def unparseToString(self):
                if self._isTap == True:
                        return "{T}"
                else:
                        return "{Q}"
                
        
