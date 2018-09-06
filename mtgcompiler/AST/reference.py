import mtgcompiler.AST.core as core
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

class MgNameReference(MgAbstractReference):
        """A stand-in used when a card refers to its own name in its text."""
        def __init__(self,nameref):
                """
                nameref: The MgName node to which this node refers.
                """
                super().__init__(nameref)
                
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

        

class MgPlayer(core.MgNode):
        """This node represents a player. This can be 'you', an opponent, a teammate, etc."""
        class PlayerEnum(Enum):
                You = "you"
                Opponent = "opponent"
                Teammate = "teammate"
        pass
                
                
                

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
                
                
class MgDeclarationModifier(core.MgNode):
        """A parent class for modifiers to players/objects"""
        pass
                

class MgQualifier(core.MgNode):
        """A qualifier is a term that specifies the state of an object (see comp rule 109 for objects).
        For example, 'Elf spell','Elf permanent','Elf token', or 'Elf source'.
        """
        class QualifierEnum(Enum):
                Ability = "Ability"
                Card = "Card"
                Permanent = "Permanent"
                Source = "Source"
                Spell = "Spell"
                Token = "Token"
                
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
    
class MgTurnStep(core.MgNode):
        """This node represents a point in time in a turn, such as 
        the first Main phase or the cleanup step."""
        pass
    
class MgZone(core.MgNode):
        """This node represents a zone in the game. From the rules:
        
        400. A zone is a place where objects can be during a game. 
        There are normally seven zones: library, hand, battlefield, graveyard, stack, exile, and command. 
        Some older cards also use the ante zone. Each player has their own library, hand, and graveyard. 
        The other zones are shared by all players.
        """
        
        class ZoneEnum(Enum):
                Battlefield = "The Battlefield"
                Graveyard = "Graveyard"
                Library = "Library"
                Hand = "Hand"
                Stack = "Stack"
                Exile = "Exile"
                Command = "Command Zone"

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
                
        

    

#class MgPossessiveModifier(core.MgNode):
#        """A decorator for possessives like 'your' and 'its owner's'... maybe"""
#        pass