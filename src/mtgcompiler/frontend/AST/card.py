import mtgcompiler.frontend.AST.core as core
from mtgcompiler.frontend.AST.expressions import MgTypeExpression,MgManaExpression
from mtgcompiler.frontend.AST.reference import MgName


class MgFlavorText(core.MgNode):
        """This node holds the flavor text for a card."""
        def __init__(self,flavor):
                """Flavor: a string containing flavor text."""
                self._traversable = True
                self._flavor = flavor
        
        def getFlavor(self):
                return self._flavor
                
        def setFlavor(self,flavor):
                self._flavor = flavor
        
        def isChild(self,child):
                return False
                
        def getTraversalSuccessors(self):
                return []
                
        def unparseToString(self):
                return self._flavor

class MgTextBox(core.MgNode):
        """This node represents a text box, the most substantial
        part of most Magic cards."""
        
        def __init__(self,*lines):
                """The constructor accepts a list of MgAbility nodes (or decorators around such nodes)
                in the order that they appear on the card."""
                self._traversable = True
                self._lines = lines
                for line in self._lines:
                        line.setParent(self)
                        
        def getNumberOfLines(self):
                """Returns the number of lines in the textbox."""
                return len(self._lines)
        
        def appendLine(self,line):
                """Append a line to the end of the textbox."""
                self._lines.append(line)
                line.setParent(self)
                
        def removeLine(self,line):
                """Remove a line from the textbox."""
                self._lines.remove(line)
                line.setParent(None)
                
        def getLineIndex(self,line):
                """Get the index of a line in the textbox.
                Note: This will return an exception if the line is not found
                in the textbox."""
                return self._lines.index(line)
                
        def getLine(self,index):
                """Returns the line at the given index.
                Note: This will return an exception if the index is invalid."""
                return self._lines[index]
                
        def isChild(self,child):
                return child in self._lines
                
        def getTraversalSuccessors(self):
                return [line for line in self._lines if line.isTraversable()]
                
        def unparseToString(self):
                return "\n".join(["{0}".format(line.unparseToString()) for line in self._lines])

class MgTypeLine(core.MgNode):
        """The type line is the middle part of a Magic card
        that lists the supertypes, types, and subtypes of that card."""
        
        def __init__(self):
                """Default constructor for an empty type line."""
                self._traversable = True
                self._supertypes = MgTypeExpression()
                self._supertypes.setParent(self)
                self._types = MgTypeExpression()
                self._types.setParent(self)
                self._subtypes = MgTypeExpression()
                self._subtypes.setParent(self)
        
        def __init__(self,supertypes=None,types=None,subtypes=None):
                """Constructor that allows you to supply MgTypeExpression objects."""
                self._traversable = True
                if supertypes is not None:
                        self._supertypes = supertypes
                else:
                        self._supertypes = MgTypeExpression()
                self._supertypes.setParent(self)
                if types is not None:
                        self._types = types
                else:
                        self._types = MgTypeExpression()
                self._types.setParent(self)
                if subtypes is not None:
                        self._subtypes = subtypes
                else:
                        self._subtypes = MgTypeExpression()
                self._subtypes.setParent(self)
                
                
        def getSupertypes(self):
                """Gets the type expression for supertypes."""
                return self._supertypes
                
        def getTypes(self):
                """Gets the type expression for types."""
                return self._types
                
        def getSubtypes(self):
                """Gets the type expression for subtypes."""
                return self._subtypes

        def hasSupertype(self,t):
            """Checks whether a supertype is on the type line."""
            return self._supertypes.isChild(t)
                  
        def hasType(self,t):
            """Checks whether a type is on the type line."""
            return self._types.isChild(t)
        
        def hasSubtype(self,t):
            """Checks whether a subtype is on the type line."""
            return self._subtypes.isChild(t)
            
        def isChild(self,child):
                return child in {self._supertypes,self._types,self._subtypes}
            
        def getTraversalSuccessors(self):
                return [ts for ts in {self._supertypes,self._types,self._subtypes} if ts.isTraversable()]
        
        def unparseToString(self):
                if self._subtypes.getLength() == 0:
                        return "{0} {1}".format(self._supertypes.unparseToString(),self._types.unparseToString())
                else:
                        return "{0} {1} — {2}".format(self._supertypes.unparseToString(),self._types.unparseToString(),self._subtypes.unparseToString())

class MgCard(core.MgNode):
        """This node represents a Magic card. When a card is parsed,
        one of these objects is produced. It contains features for
        interacting with all aspects of a Magic card. 
        
        From the rules... The parts of a card are name, mana cost, illustration, 
        color indicator, type line, expansion symbol, text box, power and toughness, loyalty, 
        hand modifier, life modifier, illustration credit, legal text, and collector number. 
        Some cards may have more than one of any or all of these parts.
        """
        
        def __init__(self,**kwargs):
                """kwargs: A keyword argument dictionary, because there are so many damn fields in this card,
                most of which are optional."""
                
                if "name" in kwargs:
                        self._name = kwargs["name"]
                        if self._name is not None:
                                self._name.setParent(self)
                else:
                        self._name = MgName()
                        self._name.setParent(self)
                        
                if "manaCost" in kwargs:
                        self._manaCost = kwargs["manaCost"]
                        if self._manaCost is not None:
                                self._manaCost.setParent(self)
                else:
                        self._manaCost = MgManaExpression()
                        self._manaCost.setParent(self)
                        
                if "colorIndicator" in kwargs:
                        self._colorIndicator = kwargs["colorIndicator"]
                        if self._colorIndicator is not None:
                                self._colorIndicator.setParent(self)
                else:
                        self._colorIndicator = None
                        
                if "typeLine" in kwargs:
                        self._typeLine = kwargs["typeLine"]
                        if self._typeLine is not None:
                                self._typeLine.setParent(self)
                else:
                        self._typeLine = MgTypeLine()
                        
                if "loyalty" in kwargs:
                        self._loyalty = kwargs["loyalty"]
                        if self._loyalty is not None:
                                self._loyalty.setParent(self)
                else:
                        self._loyalty = None
                 
                #TODO: The expansion symbol is going into some kind of 'card details' data structure,
                #along with info like artist name.
                if "expansionSymbol" in kwargs:
                        self._expansionSymbol = kwargs["expansionSymbol"]
                else:
                        self._expansionSymbol = None
                        
                if "textBox" in kwargs:
                        self._textBox = kwargs["textBox"]
                        if self._textBox is not None:
                                self._textBox.setParent(self)
                else:
                        self._textBox = MgTextBox()
                        self._textBox.setParent(self)
                        
                if "powerToughness" in kwargs:
                        self._powerToughness = kwargs["powerToughness"]
                        if self._powerToughness is not None:
                                self._powerToughness.setParent(self)
                else:
                        self._powerToughness = None
                        
                if "handModifier" in kwargs:
                        self._handModifier = kwargs["handModifier"]
                        if self._handModifier is not None:
                                self._handModifier.setParent(self)
                else:
                        self._handModifier = None
                        
                if "lifeModifier" in kwargs:
                        self._lifeModifier = kwargs["lifeModifier"]
                        if self._lifeModifier is not None:
                                self._lifeModifier.setParent(self)
                else:
                        self._lifeModifier = None
                        
                if "flavor" in kwargs:
                        self._flavor = kwargs["flavor"]
                        if self._flavor is not None:
                                self._flavor.setParent(self)
                else:
                        self._flavor = None
        
        def getName(self):
                return self._name
                
        def hasName(self):
                return self._name is not None
                
        def setName(self,name):
                self._name = name
                self._name.setParent(self)
                
        def getManaCost(self):
                return self._manaCost
                
        def hasManaCost(self):
                return self._manaCost is not None
                
        def setManaCost(self,manaCost):
                self._manaCost = manaCost
                self._manaCost.setParent(self)
                
        def getColorIndicator(self):
                return self._colorIndicator
                
        def hasColorIndicator(self):
                return self._colorIndicator is not None

        def setColorIndicator(self,colorIndicator):
                self._colorIndicator = colorIndicator
        
        def getTypeLine(self):
                return self._typeLine
                
        def hasTypeLine(self):
                return self._typeLine is not None
                
        def setTypeLine(self):
                return self._typeLine
                self._typeline.setParent(self)
                
        def getLoyalty(self):
                return self._loyalty
                
        def hasLoyalty(self):
                return self._loyalty is not None
        
        def setLoyalty(self,loyalty):
                self._loyalty = loyalty
                self._loyalty.setParent(self)
                
        def getExpansionSymbol(self):
                return self._expansionSymbol
                
        def hasExpansionSymbol(self):
                return self._expansionSymbol is not None
                
        def setExpansionSymbol(self,expansionSymbol):
                self._expansionSymbol = expansionSymbol
                
        def getTextBox(self):
                return self._textBox
                
        def hasTextBox(self):
                return self._textBox is not None
                
        def setTextBox(self,textBox):
                self._textBox = textBox
                self._textBox.setParent(self)
                
        def getPowerToughness(self):
                return self._powerToughness
                
        def hasPowerToughness(self):
                return self._powerToughness is not None
                
        def setPowerToughness(self,powerToughness):
                self._powerToughness = powerToughness
                self._powerToughness.setParent(self)
                
        def getHandModifier(self):
                """Note: This only matters for Vanguard cards."""
                return self._handModifier
                
        def hasHandModifier(self):
                """Note: This only matters for Vanguard cards."""
                return self._handModifier is not None
                
        def setHandModifier(self,handModifier):
                """Note: This only matters for Vanguard cards."""
                self._handModifier = handModifier
                self._handModifier.setParent(self)
                
        def getLifeModifier(self):
                """Note: This only matters for Vanguard cards."""
                return self._lifeModifier
                
        def hasLifeModifier(self):
                """Note: This only matters for Vanguard cards."""
                return self._lifeModifier is not None
                
        def setLifeModifier(self,lifeModifier):
                """Note: This only matters for Vanguard cards."""
                self._lifeModifier = lifeModifier
                self._lifeModifier.setParent(self)
                
        def getFlavor(self):
                return self._flavor
        
        def hasFlavor(self):
                return self._flavor is not None
        
        def setFlavor(self,flavor):
                self._flavor = flavor
                self._flavor.setParent(self)
                
        def isChild(self,child):
                return child in {self._name,self._manaCost,self._colorIndicator,self._typeLine,self._loyalty,self._expansionSymbol,self._textBox,self._powerToughness,self._handModifier,self._lifeModifier}
                
        def getTraversalSuccessors(self):
                return [ts for ts in {self._name,self._manaCost,self._colorIndicator,self._typeLine,self._loyalty,self._expansionSymbol,self._textBox,self._powerToughness,self._handModifier,self._lifeModifier} if ts is not None and ts.isTraversable()]               
        
        def unparseToString(self):
                output = ""
                if self._name is not None:
                        output += "{0}".format(self._name.unparseToString())
                if self._manaCost is not None:
                        output += " {0}\n".format(self._manaCost.unparseToString())
                else:
                        output += "\n"
                if self._colorIndicator is not None:
                        output += "Color Indicator: {0}\n".format(self._colorIndicator)
                if self._typeLine is not None:
                        output += "{0}".format(self._typeLine.unparseToString())
                if self._expansionSymbol is not None:
                        output += "     {0}\n".format(self._typeline.unparseToString())
                else:
                        output += "\n"
                if self._textBox is not None:
                        output += "{0}\n".format(self._textBox.unparseToString())
                if self._loyalty is not None:
                        output += "{0}\n".format(self._loyalty.unparseToString())
                if self._powerToughness is not None:
                        output += "{0}\n".format(self._powerToughness.unparseToString())
                if self._handModifier is not None:
                        output += "{0}\n".format(self._lifeModifier.unparseToString())
                if self._lifeModifier is not None:
                        output += "{0}\n".format(self._lifeModifier.unparseToString())
                return output
                
                
