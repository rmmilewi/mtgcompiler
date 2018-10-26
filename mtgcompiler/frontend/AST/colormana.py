import mtgcompiler.AST.core as core
from enum import Enum,Flag,auto

class MgManaSymbol(core.MgNode):
        """This node represents a mana symbol, such as {G\P} or {U/W}."""
        
        class ManaType(Flag):
                """There are six types of mana: white, blue, black, red, green, and colorless.
                A generic mana symbol has None as its mana type. Enum flags can be combined to
                make hybrid mana types."""
                White = auto()
                Blue = auto()
                Black = auto()
                Red = auto()
                Green = auto()
                Colorless = auto()
                
        class ManaModifier(Flag):
                """Mana modifiers include phyrexian mana or snow mana."""
                Phyrexian = auto()
                Snow = auto()
                AlternateTwo = auto()
                Half = auto()
        
        def __init__(self,colorv=None,modifiers=None,cvalue=0):
                """
                colorv: A mana type enum, or None in the case of generic mana.
                modifiers: A modifier enum. Default is None.
                cvalue: The value of the mana symbol. This is only checked in the 
                case of a generic mana symbol. Note that you can supply a string in place
                of an integer value here, such as 'X'."""
                self._traversable = True
                self._colorv = colorv
                self._modifiers = modifiers
                self._cvalue = cvalue
        
        def isChild(self,child):
                """Mana symbols have no children."""
                return False
        
        def getTraversalSuccessors(self):
                """Mana symbols are traversable, but have no successors."""
                return []
                
        def isWhite(self):
                """Checks whether the symbol is considered a white mana symbol."""
                return self._colorv is not None and MgManaSymbol.ManaType.White in self._colorv

        def isBlue(self):
                """Checks whether the symbol is considered a blue mana symbol."""
                return self._colorv is not None and MgManaSymbol.ManaType.Blue in self._colorv
                
        def isBlack(self):
                """Checks whether the symbol is considered a black mana symbol."""
                return self._colorv is not None and MgManaSymbol.ManaType.Black in self._colorv
                
        def isRed(self):
                """Checks whether the symbol is considered a red mana symbol."""
                return self._colorv is not None and MgManaSymbol.ManaType.Red in self._colorv
                
        def isGreen(self):
                """Checks whether the symbol is considered a green mana symbol."""
                return self._colorv is not None and MgManaSymbol.ManaType.Green in self._colorv
        
        def isColorless(self):
                """Checks whether the symbol is considered a green mana symbol."""
                return self._colorv is not None and MgManaSymbol.ManaType.Colorless in self._colorv
                
        def isGeneric(self):
                """Checks whether the symbol is considered a generic mana symbol."""
                return self._colorv is None
        
        def unparseToString(self):
                """Nota bene: a user can create mana symbol nodes that have no in-game equivalent, 
                like half-blue-phyrexian mana. However, this method will make a best effort to
                provide a representation of any kind of mana symbol you specify."""
                output = ""
                if self._colorv is not None:
                        colorSeq = []
                        if MgManaSymbol.ManaType.White in self._colorv:
                                colorSeq.append("W")
                        if MgManaSymbol.ManaType.Blue in self._colorv:
                                colorSeq.append("U")
                        if MgManaSymbol.ManaType.Black in self._colorv:
                                colorSeq.append("B")
                        if MgManaSymbol.ManaType.Red in self._colorv:
                                colorSeq.append("R")
                        if MgManaSymbol.ManaType.Green in self._colorv:
                                colorSeq.append("G")
                        if MgManaSymbol.ManaType.Colorless in self._colorv:
                                colorSeq.append("C")
                        output += '/'.join(colorSeq)
                elif self._colorv is None and self._modifiers is None:
                        output += str(self._cvalue) #For generic mana costs, X values, etc.
                if self._modifiers is not None:
                        if MgManaSymbol.ManaModifier.Phyrexian in self._modifiers:
                                output = output + "/P"
                        if MgManaSymbol.ManaModifier.AlternateTwo in self._modifiers:
                                output = output + "/2"
                        if MgManaSymbol.ManaModifier.Half in self._modifiers:
                                output = "H" + output
                        if MgManaSymbol.ManaModifier.Snow in self._modifiers:
                                output = "S" + output
        
                return "{{{0}}}".format(output)

class MgColorTerm(core.MgNode):
        """This node represents a color term, such as 'green', or 'multicolored'."""
        
        class ColorTermEnum(Enum):
                """
                105.1. There are five colors in the Magic game: white, blue, black, red, and green.
                105.2a A monocolored object is exactly one of the five colors.
                105.2b A multicolored object is two or more of the five colors.
                105.2c A colorless object has no color."""
                White = "white"
                Blue = "blue"
                Black = "black"
                Red = "red"
                Green = "green"
                Monocolored = "monocolored"
                Multicolored = "multicolored"
                Colorless = "colorless"
        
        def __init__(self,value):
                """value: an instance of the ColorTermEnum, or, 
                optionally, a custom-defined color term string (e.g. purple)."""
                self._traversable = True
                self._value = value
                
        def setValue(self, value):
                """Setter method for the value attribute. This is the value held by the color term object. 
                It can either be the pre-defined Enum type, or a string in the case of a custom color term."""
                self._value=value
        
        def getValue(self):
                """Access method for the value attribute. This is the value held by the color term object. 
                It can either be a pre-defined Enum type, or a string in the case of a custom color term."""
                return self._value

        def isCustomTerm(self):
                """Checks whether a color term is user-defined, which must be a string."""
                return type(self._value) is str
                
        def isWhite(self):
                return self._value == MgColorTerm.ColorTermEnum.White
                
        def isBlue(self):
                return self._value == MgColorTerm.ColorTermEnum.Blue
                
        def isBlack(self):
                return self._value == MgColorTerm.ColorTermEnum.Black
                
        def isRed(self):
                return self._value == MgColorTerm.ColorTermEnum.Red

        def isGreen(self):
                return self._value == MgColorTerm.ColorTermEnum.Green
                
        def isMonocolored(self):
                return self._value == MgColorTerm.ColorTermEnum.Monocolored
                
        def isMulticolored(self):
                return self._value == MgColorTerm.ColorTermEnum.Multicolored
                
        def isColorless(self):
                return self._value == MgColorTerm.ColorTermEnum.Colorless
                
        def isChild(self,child):
                """Color terms have no children."""
                return False
        
        def getTraversalSuccessors(self):
                """Color terms are traversable, but have no successors."""
                return []
                
        def unparseToString(self):
                if type(self._value) is str:
                        return self._value
                else:
                        return self._value.value
                
        
                
