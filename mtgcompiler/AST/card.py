import mtgcompiler.AST.core as core
from mtgcompiler.AST.expressions import MgTypeExpression,MgManaExpression
from mtgcompiler.AST.reference import MgName


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
        
        def __init__(self,supertypes,types,subtypes):
                """Constructor that allows you to supply MgTypeExpression objects."""
                self._traversable = True
                self._supertypes = supertypes
                self._supertypes.setParent(self)
                self._types = types
                self._types.setParent(self)
                self._subtypes = subtypes
                self._subtypes.setParent(self)

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
                        self._name = name
                else:
                        self._name = MgName()
                        
                if "manaCost" in kwargs:
                        self._manaCost = manaCost
                else:
                        self._manaCost = MgManaExpression()
                        
                if "colorIndicator" in kwargs:
                        self._colorIndicator = colorIndicator
                else:
                        self._colorIndicator = None
                        
                if "typeLine" in kwargs:
                        self._typeLine = typeLine
                else:
                        self._typeLine = MgTypeLine()
                        
                if "loyalty" in kwargs:
                        self._loyalty = loyalty
                else:
                        self._loyalty = None
                        
                if "expansionSymbol" in kwargs:
                        self._expansionSymbol = expansionSymbol
                else:
                        self._expansionSymbol = None
                        
                if "textBox" in kwargs:
                        self._textBox = textBox
                else:
                        self._textBox = MgTextBox()
                        
                if "powerToughness" in kwargs:
                        self._powerToughness = powerToughness
                else:
                        self._powerToughness = None
                        
                if "handModifier" in kwargs:
                        self._handModifier = handModifier
                else:
                        self._handModifier = None
                        
                if "lifeModifier" in kwargs:
                        self._lifeModifier = lifeModifier
                else:
                        self._lifeModifier = None
                        
             
        
        def getName(self):
                return self._name
                
        def setName(self,name):
                self._name = name
                
        def getManaCost(self):
                return self._manacost
                
        def setManaCost(self,manacost):
                self._manacost = manacost
                
        def getColorIndicator(self):
                return self._colorindicator

        def setColorIndicator(self,colorindicator):
                self._colorindicator = colorindicator
        
        def getTypeLine(self):
                return self._typeLine
        
        def setTypeLine(self,typeline):
                self._typeLine = typeLine
                
        def getLoyalty(self):
                return self._loyalty
        
        def setLoyalty(self,loyalty):
                self._loyalty = loyalty
                
        def getExpansionSymbol(self):
                return self._expansionSymbol
                
        def setExpansionSymbol(self,expansionSymbol):
                self._expansionSymbol = expansionSymbol
                
        def getTextBox(self):
                return self._textBox
                
        def setTextBox(self,textBox):
                self._textBox = textBox
                
        def getPowerToughness(self):
                return self._powerToughness
                
        def setPowerToughness(self,powerToughness):
                self._powerToughness = powerToughness
                
        def getHandModifier(self):
                """Note: This only matters for Vanguard cards."""
                return self._handModifier
                
        def setHandModifier(self,handModifier):
                """Note: This only matters for Vanguard cards."""
                self._handModifier = handModifier
                
        def getLifeModifier(self):
                """Note: This only matters for Vanguard cards."""
                return self._lifeModifier
                
        def setLifeModifier(self,lifeModifier):
                """Note: This only matters for Vanguard cards."""
                self._lifeModifier = lifeModifier
                
        def isChild(self,child):
                return child in {self._name,self._manacost,self._colorindicator,self._typeline,self._loyalty,self._expansionSymbol,self._textBox,self._powerToughness,self._handModifier,self._lifeModifier}
                
        def getTraversalSuccessors(self):
                return [ts for ts in {self._name,self._manacost,self._colorindicator,self._typeline,self._loyalty,self._expansionSymbol,self._textBox,self._powerToughness,self._handModifier,self._lifeModifier} if ts is not None and ts.isTraversable()]               
                