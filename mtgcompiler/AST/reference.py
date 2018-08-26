import mtgcompiler.AST.core as core
from enum import Enum

class MgSelfReference(core.MgNode):
        """A stand-in used when a card refers to itself in its text."""
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