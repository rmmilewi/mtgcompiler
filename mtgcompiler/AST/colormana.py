import mtgcompiler.AST.core as core
from enum import Flag,auto

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
        """This node represents a color term, such as 'non-white','green', or 'multicolored'."""
        pass
