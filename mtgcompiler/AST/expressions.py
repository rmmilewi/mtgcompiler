import mtgcompiler.AST.core as core
import abc
from enum import Enum,auto
from num2words import num2words

class MgAbstractExpression(core.MgNode):
        """This is the parent class for all expressions such as power/toughness, 
        types, and mana costs. This class is not instantiated, but provides common
        functionalities for all of these kinds of expressions."""
        def __init__(self):
                self._traversable = True
        
        
class MgValueExpression(MgAbstractExpression):
        """An uninstantiated parent class for value expressions, such as... 
                - '1+*' in '1+*/1+*'
                - 'six' in 'destroy six target creatures'
                - 'twice X' in 'you gain twice X life'
                - 'greater than' in 'power greater than 4'
        """
        def __init__(self):
                super().__init__()
        
class MgValueComparisonExpression(MgValueExpression):
        """A value-comparison expression is a phrase in plain English comparing
        quantities, such as 'equal to' or 'greater than or equal to'.
        
        In some cases, the comparison expression only has a right-hand side. 
        The left-hand side is assumed to be present but bound to some other node. 
        For example, in 'deals damage equal to [...]', 'deals damage' is part 
        of a deals-damage expression, and the value comparison is underneath that
        expression in the tree.
        """
        def __init__(self,lhs,rhs):
                """
                lhs: (optional) the left-hand side of the expression.
                rhs: the right-hand side of the expression.
                """
                super().__init__()
                self._lhs = lhs
                if self._lhs is not None:
                        lhs.setParent(self)
                self._rhs = rhs
                rhs.setParent(self)
                
        def hasImplicitLhs(self):
                """If lhs is None, it is because the left-hand side is implicit."""
                return self._lhs is not None
        
        def getLhs(self):
                """Get the left-hand side."""
                return self._lhs
                
        def setLhs(self,lhs):
                """Set the left-hand side."""
                self._lhs = lhs
                if self._lhs is not None:
                        lhs.setParent(self)
        
        def getRhs(self):
                """Get the right-hand side."""
                return self._lhs
                
        def setRhs(self,rhs):
                """Set the right-hand side."""
                self._right = rhs
                rhs.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in {self._lhs,self._rhs}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._lhs,self._rhs} if node is not None and node.isTraversable()]
        
class MgValueGtExpression(MgValueComparisonExpression):
        """This is the 'greater than' value comparison expression."""
        def __init__(self,lhs,rhs):
                super().__init__(lhs,rhs)
                
        def unparseToString(self):
                if self._lhs is not None:
                        return "{0} greater than {1}".format(self._lhs.unparseToString(),self._rhs.unparseToString())
                else:
                        return "greater than {0}".format(self._rhs.unparseToString())
                        
class MgValueGtEqExpression(MgValueComparisonExpression):
        """This is the 'greater than or equal to' value comparison expression."""
        def __init__(self,lhs,rhs,shortVariant=False):
                """shortVariant: This flag sets whether the wording used is a variant of the following form:
                'destroy target creature with power greater than or equal to 4'
                vs. 'destroy target creature with power 4 or greater.'
                """
                super().__init__(lhs,rhs)
                self._shortVariant = shortVariant
                
        def isShortVariant(self):
                """Checks whether this should be unparsed as the short variant of greater-than-or-equal-to."""
                return self._shortVariant
                
        def setShortVariant(self,shortVariant):
                """Sets whether this should be unparsed as the short variant of greater-than-or-equal-to."""
                self._shortVariant = shortVariant
                
        def unparseToString(self):
                if shortVariant == True:
                        if self._lhs is not None:
                                return "{0} {1} or greater".format(self._lhs.unparseToString(),self._rhs.unparseToString())
                        else:
                                return "{0} or greater".format(self._rhs.unparseToString())
                else:
                        if self._lhs is not None:
                                return "{0} greater than or equal to {1}".format(self._lhs.unparseToString(),self._rhs.unparseToString())
                        else:
                                return "greater than or equal to {0}".format(self._rhs.unparseToString())
                        
class MgValueLtExpression(MgValueComparisonExpression):
        """This is the 'less than' value comparison expression."""
        def __init__(self,lhs,rhs):
                super().__init__(lhs,rhs)
                
        def unparseToString(self):
                if self._lhs is not None:
                        return "{0} less than {1}".format(self._lhs.unparseToString(),self._rhs.unparseToString())
                else:
                        return "less than {0}".format(self._rhs.unparseToString())
                        
class MgValueLtEqExpression(MgValueComparisonExpression):
        """This is the 'less than or equal to' value comparison expression."""
        def __init__(self,lhs,rhs,shortVariant):
                super().__init__(lhs,rhs)
                self._shortVariant = shortVariant
                
        def isShortVariant(self):
                """Checks whether this should be unparsed as the short variant of greater-than-or-equal-to."""
                return self._shortVariant
                
        def setShortVariant(self,shortVariant):
                """Sets whether this should be unparsed as the short variant of greater-than-or-equal-to."""
                self._shortVariant = shortVariant
                
        def unparseToString(self):
                if shortVariant == True:
                        if self._lhs is not None:
                                return "{0} {1} or less".format(self._lhs.unparseToString(),self._rhs.unparseToString())
                        else:
                                return "{0} or less".format(self._rhs.unparseToString())
                else:
                        if self._lhs is not None:
                                return "{0} less than or equal to {1}".format(self._lhs.unparseToString(),self._rhs.unparseToString())
                        else:
                                return "less than or equal to {0}".format(self._rhs.unparseToString())
        
class MgValueEqExpression(MgValueComparisonExpression):
        """This is the 'equals to' value comparison expression."""
        def __init__(self,lhs,rhs):
                super().__init__(lhs,rhs)
                
        def unparseToString(self):
                if self._lhs is not None:
                        return "{0} equal to {1}".format(self._lhs.unparseToString(),self._rhs.unparseToString())
                else:
                        return "equal to {0}".format(self._rhs.unparseToString())
                        

class MgNumberOfExpression(MgValueExpression):
        """A verbal formula for referring to the result of an underlying expression, like
        'the number of creatures that you control' means 'count the number of creatures you control,
        then use that number'.
        """

        def __init__(self,expression):
                """
                expression: The underlying expression that is decorated by this expression.
                """
                super().__init__()
                self._expression = expression
                expression.setParent(self)
                
        def getExpression(self):
                """Get the underlying expression decorated by this expression."""
                return self._expression
                
        def setExpression(self,expression):
                """Set the underlying expression decorated by this expression."""
                self._expression = expression
                expression.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in {self._expression}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._expression} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                return "the number of {0}".format(self._expression.unparseToString())
                
         

class MgNumberValue(MgValueExpression):
        """Represents a number value, which can be unparsed in one of three ways,
        depending on which flag is selected:
                - Literal value: 1,2,3...
                - Magic English quantity - one, two, three...
                - Magic English frequency - once, twice, three times...
                - Custom values: *, 1+*, etc.
        """
        
        class NumberTypeEnum(Enum):
                """Indicates how the number value should be unparsed."""
                Literal = auto() #1, 2, 3
                Cardinal = auto() #one, two, three
                Frequency = auto() #once, twice, three times
                Ordinal = auto() #first, second, third
                Custom = auto() #*,1+*
        
        def __init__(self,value,ntype):
                super().__init__()
                self._value = value
                self._ntype = ntype
        
        def isLiteral(self):
                """Checks if the number type is a literal."""
                return self._ntype == MgNumberValue.NumberTypeEnum.Literal
                
        def setLiteral(self):
                """Makes the number type a literal."""
                self._ntype = MgNumberValue.NumberTypeEnum.Literal
                
        def isCardinal(self):
                """Checks if the number type is a quantity."""
                return self._ntype == MgNumberValue.NumberTypeEnum.Cardinal
                
        def setCardinal(self):
                """Makes the number type a quantity."""
                self._ntype = MgNumberValue.NumberTypeEnum.Cardinal
                
        def isFrequency(self):
                """Checks if the number type is a frequency."""
                return self._ntype == MgNumberValue.NumberTypeEnum.Frequency
                
        def setFrequency(self):
                """Makes the number type a frequency."""
                self._ntype = MgNumberValue.NumberTypeEnum.Frequency
                
        def isOrdinal(self):
                """Checks if the number type is a frequency."""
                return self._ntype == MgNumberValue.NumberTypeEnum.Ordinal
                
        def setOrdinal(self):
                """Makes the number type a frequency."""
                self._ntype = MgNumberValue.NumberTypeEnum.Ordinal
                
        def isCustom(self):
                """Checks if the number type is a frequency."""
                return self._ntype == MgNumberValue.NumberTypeEnum.Ordinal
                
        def setCustom(self):
                """Makes the number type a frequency."""
                self._ntype = MgNumberValue.NumberTypeEnum.Ordinal
                
        def getValue(self):
                """Gets the underlying integer value."""
                return self._value
                
        def setValue(self,value):
                """Sets the underlying integer value."""
                self._value = value
                
        def isChild(self,child):
                """A number value node has no children."""
                return False
        
        def getTraversalSuccessors(self):
                """A number value node has no traversal successors."""
                return []
        
        def unparseToString(self):
                if self._ntype == MgNumberValue.NumberTypeEnum.Custom:
                        return self._value
                if self._ntype == MgNumberValue.NumberTypeEnum.Literal:
                        return str(self._value)
                
                if self._ntype == MgNumberValue.NumberTypeEnum.Frequency and self._value == 1:
                        return "once"
                if self._ntype == MgNumberValue.NumberTypeEnum.Frequency and self._value == 2:
                        return "twice"
                            
                if self._ntype == MgNumberValue.NumberTypeEnum.Cardinal or self._ntype == MgNumberValue.NumberTypeEnum.Frequency:
                        quantityRepresentation = num2words(self._value)
                        if self._ntype == MgNumberValue.NumberTypeEnum.Cardinal:
                                return quantityRepresentation
                        else: #ntype is frequency
                                return "{0} times".format(quantityRepresentation)
                elif self._ntype == MgNumberValue.NumberTypeEnum.Ordinal:
                        ordinalRepresentation = num2words(self._value, to='ordinal')
                        return ordinalRepresentation
                else:
                        raise ValueError("Number type is unspecified or unrecognizable.")
                
    
class MgManaExpression(MgAbstractExpression):
        """This node represents mana expressions, sequences of 
        mana symbols."""

        def __init__(self,*args):
                """The constructor accepts a list of mana symbols in any order."""
                super().__init__()
                self._symlist = args
                for sym in self._symlist:
                        sym.setParent(self)
                        
        def isChild(self,child):
                return child is not None and child in self._symlist
        
        def getTraversalSuccessors(self):
                return [sym for sym in self._symlist if sym.isTraversable()]
                
        def unparseToString(self):
                """This method unparses the mana symbols in the order given by the list, which
                may or may not be the canonical order."""
                return ''.join(sym.unparseToString() for sym in self._symlist)

        def addManaSymbol(self,sym):
                self._symlist.append(sym)
                sym.setParent(self)
                

class MgManaSpecificationExpression(MgAbstractExpression):
        """This node represents a description of the kind of mana produced by an add-mana-expression.
        Examples include (relevant portions enclosed by tildes):
        
        * Add ~one mana of any color~.
        * Add ~three mana of any one color~.
        * Add ~two mana of any combination of colors~.
        * Add ~one mana in any combination of {R} and/or {G}.~
        * Add ~{R} for each creature you control.~
        * Add ~one mana of any type a land an opponent controls could produce~.
        * Add ~one mana of any color in your commander's color identity~.
        
        Normally an add-mana-expression just uses a plain mana expression (e.g. 'add {G}'), but otherwise
        it uses a mana description expression. This can be a combination of value expressions, mana specifiers,
        and/or conditional statements.
        """
        def __init__(self,quantity,*args):
                """"
                quantity: A value expression indicating the amount of mana produced.
                args: The constructor accepts a list of mana specifications in any order.
                """
                super().__init__()
                self._quantity = quantity
                self._speclist = list(args)
                self._quantity.setParent(self)
                for s in self._speclist:
                        s.setParent(self)
                        
        def isChild(self,child):
                return child is not None and child in [self._quantity]+self._speclist
        
        def getTraversalSuccessors(self):
                return [s for s in [self._quantity]+self._speclist if s.isTraversable()]
                
        def unparseToString(self):
                return '{0} '.format(self._quantity.unparseToString())+' '.join(s.unparseToString() for s in self._speclist)
                
class MgManaSpecifier(MgAbstractExpression):
        """This is the abstract parent class for all mana specifications."""
        def __init__(self):
                super().__init__()
        
class MgAnyColorSpecifier(MgManaSpecifier):
        def __init__(self,anyOneColor=False):
                """
                anyOneColor: A flag indicating that the phrase is 'of any one color'. Otherwise it's just 'of any color'.
                """
                super().__init__()
                self._anyOneColor = anyOneColor
        
        def isAnyOneColor(self):
                """Check whether the phrasing is 'of any one color'."""
                return self._anyOneColor
                
        def setAnyOneColor(self,anyOneColor):
                """Set whether the phrasing is 'of any one color'."""
                self._anyOneColor = anyOneColor
                
        def isChild(self,child):
                """This node has no children."""
                return False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                if self._anyOneColor == True:
                        return "mana of any one color"
                else:
                        return "mana of any color"
                 
        
                
class MgCostSequenceExpression(MgAbstractExpression):
        """This node represents a series of terms/expressions separated by a comma used in a series of
        costs, such as those associated with an activated ability."""
        def __init__(self,*args):
                """args: Cost expressions in the cost sequence (e.g. a mana expression)"""
                super().__init__()
                self._arguments = args
                for arg in self._arguments:
                        arg.setParent(self)
                        
        def getArguments(self):
                """Get the list of cost arguments."""
                return self._arguments
                
        def setArguments(self,*args):
                """Set the list of cost arguments."""
                self._arguments = args
                for arg in self._arguments:
                        arg.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in self._arguments
        
        def getTraversalSuccessors(self):
                return [node for node in self._arguments if node.isTraversable()]
        
        def unparseToString(self):
                return ', '.join([arg.unparseToString() for arg in self._arguments])
                
class MgDashCostExpression(MgAbstractExpression):
        """Sometimes a cost of a keyword ability is more than, say, just a simple mana expression.
        For example, in Braid of Fire, we see 'Cumulative upkeep—Add {R}.' In these situations,
        we use a dash cost expression that decorates the underlying expression.
        """
        def __init__(self,cost):
                """
                cost: The expression defining the cost of the keyword ability 
                associated with the dash-cost expresssion.
                """
                super().__init__()
                self._cost = cost
                self._cost.setParent(self)
                
        def getCost(self):
                """Get the cost associated with this expression."""
                return self._cost
        
        def setCost(self,cost):
                """Set the cost associated with this expression."""
                self._cost = cost
                self._cost.setParent(self)
                
        def isChild(self,child):
                return child is not None and child == cost
                
        def getTraversalSuccessors(self):
                return [node for node in {self._cost} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                return "—{0}".format(self._cost.unparseToString())
                
                
class MgDeclarationExpression(MgAbstractExpression):
        """Declaration expressions are anonymous definitions of game entities (such as players and
        game objects. Declarations are composed of one or more MgDescriptionExpression objects (see below),
        possibly joined together with logical operators. Declaration expressions can either stand on their
        own or be decorated by other expressions such as target-expressions or each-expressions.
        
        Example: In "target enchantment or artifact", "target enchantment or artifact" is the whole declaration,
        and it is composed of an OR joining two different description expressions and decorated by a 
        target-expression.
        """
        
        def __init__(self,definition):
                """definition: The root node of the definition contained by this declaration."""
                self._definition = definition
                self._definition.setParent(self)
                
        def getDefinition(self):
                """Returns the definition for this declaration."""
                return self._definition
                
        def setDefinition(self,definition):
                """Sets the definition for this declaration."""
                self._definition = definition
                self._definition.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in {self._definition}
        
        def getTraversalSuccessors(self):
                return [node for node in {self._definition} if node.isTraversable()]
                
        def unparseToString(self):
                return "{0}".format(self._definition.unparseToString())


class MgDescriptionExpression(MgAbstractExpression):
        """A description expression is a sequence of sub-expressions/terms that describe some object.
        For example, in 'destroy target non-black creature', 'non-black' is in a MgColorExpression
        and 'creature' is in an MgTypeExpression. The description expression strings these together.
        The entire description expression itself is a child of an anonymous declaration.
        """
        def __init__(self,*args):
                """The constructor accepts a list of descriptors in any order."""
                super().__init__()
                self._dlist = args
                for d in self._dlist:
                        d.setParent(self)
                        
        def isChild(self,child):
                return child in self._dlist
        
        def getTraversalSuccessors(self):
                return [d for d in self._dlist if d.isTraversable()]
                
        def unparseToString(self):
                return ' '.join(d.unparseToString() for d in self._dlist)


    
class MgPTExpression(MgAbstractExpression):
        """This node represents power/toughness expressions
        such as 5/5, */*, or X/X."""
        def __init__(self,power,toughness):
                super().__init__()
                self._power = power
                self._toughness = toughness
                self._power.setParent(self)
                self._toughness.setParent(self)
        
        def getPower(self):
                return self._power
        
        def setPower(self,power):
                self._power = power
                self._power.setParent(self)
        
        def getToughness(self):
                return self._toughness
        
        def setToughness(self,toughness):
                self._toughness = toughness
                self._toughness.setParent(self)
                
        def isChild(self,child):
                return child in {self._power,self._toughness}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._power,self._toughness} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                return "{0}/{1}".format(self._power.unparseToString(),self._toughness.unparseToString())
    
class MgColorExpression(MgAbstractExpression):
        """This node represents color expressions, such as
        'White' or 'Red and Green'."""
        
        def __init__(self,termOrExpr):
                """Unlike MgTypeExpression, the constructor for MgColorExpression accepts a single child
                that can be a composite (e.g. an 'and' expression or a comma-separated series. You have to say
                'red and white and green', you can't say 'red white green'.)"""
                super().__init__()
                self._value = termOrExpr
                self._value.setParent(self)
                
        def isChild(self,child):
                return child is self._value
                
        def getTraversalSuccessors(self):
                """By default, the value held by the node should be traversable, unless
                traversal was disabled for that child node."""
                return [v for v in {self._value} if v.isTraversable()]
                
        def getValue(self):
                """Returns the term or expression held by the MgColorExpression node."""
                return self._value
                
        def setValue(self,value):
                """Sets the term or expression held by the MgColorExpression node."""
                self._value = value
                self._value.setParent(self)
                
        def unparseToString(self):
                return self._value.unparseToString()
                

class MgTypeExpression(MgAbstractExpression):
        """A type expression is a sequence of subtypes,types, or
        supertypes. For example, Snow Artifact or Human Cleric."""
        
        def __init__(self,*args):
                """The constructor accepts a list of (sub|super)*types in any order."""
                super().__init__()
                self._tlist = args
                #self._plural = False
                self._commaDelimited = False
                for t in self._tlist:
                        t.setParent(self)

        def isChild(self,child):
                return child in self._tlist
        
        def getTraversalSuccessors(self):
                return [t for t in self._tlist if t.isTraversable()]
                
        def addType(self,t):
                self._tlist.append(t)
                t.setParent(self)
                
        def getLength(self):
                """Gets the length of the type of the type expression."""
                return len(self._tlist)
                
        def isCommaDelimited(self):
                """If the comma delimited flag is set, then the type expression will have its terms
                separated by commas, as in 'non-vampire, non-werewolf, non-zombie creature' in Victim of Night."""
                return self._commaDelimited
                
        def setCommaDelimited(self,commaDelimited):
                self._commaDelimited = commaDelimited
                
        def unparseToString(self):
                """This method unparses the (sub|super)*types in the order given by the list, which
                may or may not be the canonical order of supertypes -> types -> subtypes."""
                
                """TODO: The plural solution here is just a hacky workaround until we can come up with something
                more robust. For example, the plural of sorcery is sorceries, not sorcerys (though that word
                has yet to occur in Magic English.).
                However, I do think that the decision for the final entry in a type expression
                to be plural should be decided at the level of the expression as we have it. We may specify
                singular and plural variants for each element in the enums, and force users to supply both
                variants for custom-defined types."""
                
                if self._commaDelimited is True:
                        result = ', '.join(t.unparseToString() for t in self._tlist[0:len(self._tlist)-1]) + ' ' + self._tlist[len(self._tlist)-1].unparseToString()
                else:
                        result = ' '.join(t.unparseToString() for t in self._tlist)
                return result
                #if self._plural is True:
                #        return result+'s'
                #else:
                #        return result

class MgControlExpression(MgAbstractExpression):
        """An expression that indicates control, like 'all creatures your opponents control' or 'target enchantment you control'.
        TODO: This implementation is not final. Still working this and the possessive expressions out. Need an abstract for players,
        then we can come back and change this."""
        def __init__(self,controller):
                """
                controller: The party that has the control.
                """
                super().__init__()
                self._controller = controller
                
        def getController(self):
                """Get the controller."""
                return self._controller
                
        def setController(self,controller):
                """Set the controller."""
                self._controller = controller
                
        def isChild(self,child):
                return False
                
        def getTraversalSuccessors(self):
                """This class is a leaf node. It has no children."""
                return []
                
        def unparseToString(self):
                return "{0} control".format(self._controller)
                        
class MgPossessiveExpression(MgAbstractExpression):
        """Represents a phrase that indicates who owns something, such as 'your graveyard' or 'its owner's hand'"""
        class PossessiveEnum(Enum):
                """TODO: What if possessives are plural? We haven't decided whose responsibility it is to get that right.
                I might end up re-doing this later to refer to a MgPlayer object of some kind."""
                Your = "Your"
                Owner = "Owner's"
                Opponent = "Opponent's"
                Player = "Player's"
                HisOrHer = "His or Her"

        def __init__(self,possessive,owned):
                """
                possessive: a PossessiveEnum.
                owned: An expression describing the thing that is owned.
                """
                super().__init__()
                self._possessive = possessive
                self._owned = owned
                self._owned.setParent(owned)
                
        def getOwned(self):
                """Access method for the owned attribute."""
                return self._owned
                
        def setOwned(self, value):
                """Setter method for the owned attribute."""
                self._owned=owned
                self._owned.setParent(owned)
                
        def isChild(self,child):
                return child is self._owned
                
        def getTraversalSuccessors(self):
                """This class is a leaf node. It has no children."""
                return [node for node in {self._owned} if node.isTraversable()]
                
        def unparseToString(self):
                return "{0} {1}".format(self._possessive.value,self._owned.unparseToString()) 
        
        
class MgModalExpression(MgAbstractExpression):
        """This node represents a series of modal choices, as is seen in cards like Abzan Charm or
        Citadel Siege. TODO: numberOfChoices is going to be replaced a by a 'choose' subexpression."""
        def __init__(self,numberOfChoices,*options):
                """
                numberOfChoices: The number of times that the caster can choose different modes for the spell/ability.
                options: A list containing the different modes of the spell/ability.
                """
                super().__init__()
                self._options = list(options)
                self._numberOfChoices = numberOfChoices
                for option in self._options:
                        option.setParent(self)
                        
        def getNumberOfChoices(self):
                """Get the number of choices."""
                return self._numberOfChoices
                
        def setNumberOfChoices(self,numberOfChoices):
                """Set the number of choices."""
                self._numberOfChoices = numberOfChoices
                
        def getOptions(self):
                return self._options
                
        def setOptions(self,options):
                options = self._options
                for option in self._options:
                        option.setParent(self)

        def isChild(self,child):
                return child in self._options
        
        def getTraversalSuccessors(self):
                return [node for node in self._options+[self._numberOfChoices] if node.isTraversable()]
                
        def unparseToString(self):
                output = "Choose {0} —\n".format(self._numberOfChoices.unparseToString())
                for option in self._options:
                        output += "• {0}\n".format(option.unparseToString())
                return output
                

class MgChangeZoneExpression(MgAbstractExpression):
        """Represents the notion of entering or leaving the battlefield.
        Takes the form of '____ enters the battlefield' or '____ leaves a graveyard.'
        """
        
        def __init__(self,subject,zone,entering=True):
                """
                subject: The thing that is entering or leaving a zone.
                zone: An expression describing the zone being entered or left.
                entering: A flag indicating whether the subject entering the zone?
                """
                super().__init__()
                self._subject = subject
                self._zone = zone
                self._entering = entering
                self._subject.setParent(self)
                self._zone.setParent(self)
                
        def isEntering(self):
                """Check whether the subject is entering the zone."""
                return self._entering == True
                
        def setEntering(self):
                """Make it so that the subject is entering the zone."""
                self._entering = True
                
        def isLeaving(self):
                """Check whether the subject is leaving the zone."""
                return self._entering == False
                
        def setLeaving(self):
                """Make it so that the subject is leaving the zone."""
                self._entering = False
                
        def getSubject(self):
                """Get the subject that is entering/leaving the zone."""
                return self._subject
                
        def setSubject(self,subject):
                """Set the subject that is entering/leaving the zone."""
                subject = self._subject
                self._subject.setParent(self)
                
        def getZone(self):
                """Get the zone that is being entered/left."""
                return self._zone
                
        def setZone(self,Zone):
                """Set the zone that is being entered/left."""
                Zone = self._zone
                self._zone.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in {self._subject,self._zone}
        
        def getTraversalSuccessors(self):
                return [node for node in {self._subject,self._zone} if node.isTraversable()]
                
        def unparseToString(self):
                if self._entering is True:
                        return "{0} enters {1}".format(self._subject.unparseToString(),self._zone.unparseToString())
                else:
                        return "{0} leaves {1}".format(self._subject.unparseToString(),self._zone.unparseToString())
                 
        
        
class MgBinaryOp(MgAbstractExpression):
        """An uninstantiated parent class for all binary operators, namely logical operators like 'and', 'or', etc."""
        def __init__(self,lhs,rhs):
                """
                lhs: left-hand side of the operator.
                rhs: right-hand side of the operator.
                """
                super().__init__() #All binary operators are traversable by default.
                self._lhs = lhs
                self._rhs = rhs
                self._lhs.setParent(self)
                self._rhs.setParent(self)
                
        def getLhs(self):
                """Gets the left-hand side."""
                return self._lhs
                
        def setLhs(self,lhs):
                """Sets the left-hand side."""
                self._lhs = lhs
                self._lhs.setParent(self)
        
        def getRhs(self):
                """Gets the left-hand side."""
                return self._rhs
                
        def setRhs(self,rhs):
                """Sets the left-hand side."""
                self._rhs = rhs
                self._rhs.setParent(self)
                
        def isChild(self,child):
                return child in {self._lhs,self._rhs}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._lhs,self._rhs} if node.isTraversable()]
                
class MgAndExpression(MgBinaryOp):
        """Represents an 'and', such as 'red and green' or 'target creature and target enchantment'"""
        def __init__(self,lhs,rhs):
                super().__init__(lhs,rhs)
                
        def unparseToString(self):
                return "{0} and {1}".format(self._lhs.unparseToString(),self._rhs.unparseToString())
                
class MgOrExpression(MgBinaryOp):
        """Represents an 'or', such as 'white or black' or 'target creature or player'"""
        def __init__(self,lhs,rhs):
                super().__init__(lhs,rhs)
                
        def unparseToString(self):
                return "{0} or {1}".format(self._lhs.unparseToString(),self._rhs.unparseToString())
                
class MgAndOrExpression(MgBinaryOp):
        """Represents an 'and/or', such as 'library and/or graveyard'."""
        def __init__(self,lhs,rhs):
                super().__init__(lhs,rhs)
                
        def unparseToString(self):
                return "{0} and/or {1}".format(self._lhs.unparseToString(),self._rhs.unparseToString())

class MgUnaryOp(MgAbstractExpression):
        """An uninstantiated parent class for all unary operators, like 'target X' or 'non-Y'."""
        def __init__(self,operand):
                super().__init__() #All unary operators are traversable by default.
                self._operand = operand
                self._operand.setParent(self)
                
        def getOperand(self):
                return self._operand
                
        def setOperand(self,operand):
                self._operand = operand
                operand.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in {self._operand}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._operand} if node is not None and node.isTraversable()]
                
class MgTargetExpression(MgUnaryOp):
        """A target expression is used whenever card text involves the word 'target'.
        For example, 'destroy target creature' or 'target player gains 5 life.'"""
        
        def __init__(self,operand=None,isAny=False):
                """isAny: A flag indicating that this target expression refers to 'any target'. If
                this flag is set, the operand is allowed to be None."""
                super().__init__()
                if not isAny:
                        super().__init__(operand)
                        self._isAny = isAny
                else:
                        self._operand = None
                        self._isAny = isAny
                        
        def isAnyTarget(self):
                """Checks whether this target expression refers to 'any target'"""
                return self._isAny
                
        def setIsAnyTarget(self,isAny):
                """Sets the flag indicating whether this target expression refers to 'any target'."""
                self._isAny = isAny
                        
        
        def unparseToString(self):
                if self._isAny == True:
                        return "any target"
                else:
                        return "target {0}".format(self._operand.unparseToString())
                
                
class MgAllExpression(MgUnaryOp):
        """An each expression is used whenever card text involves the word 'all'.
        For example, 'destroy all creatures'."""
        
        def __init__(self,operand):
                super().__init__(operand)
                
        def unparseToString(self):
                return "all {0}".format(self._operand.unparseToString())  

class MgEachExpression(MgUnaryOp):
        """An each expression is used whenever card text involves the word 'each'.
        For example, 'each player draws a card'."""
        
        def __init__(self,operand):
                super().__init__(operand)
                
        def unparseToString(self):
                return "each {0}".format(self._operand.unparseToString())
                
class MgIndefiniteSingularExpression(MgUnaryOp):
        """Uses 'a'/'an' to refer to a player/object in the singular."""
        def __init__(self,operand):
                super().__init__(operand)
                
        def unparseToString(self):
                return "a(n) {0}".format(self._operand.unparseToString())
        
class MgChoiceExpression(MgUnaryOp):
        """A choice expression is used whenever card text involve a non-modal choice.
        For example, 'choose a color'. TODO: This is really more like an effect of the card."""
        def __init__(self,operand):
                super().__init__(operand)
        
        def unparseToString(self):
                """TODO: 'choose a color' vs 'choose three colors' will require knowing the
                plurality of the operand."""
                return "choose {0}".format(self._operand.unparseToString())
        
class MgNonExpression(MgUnaryOp):
        """Adds 'non-' to an underlying term/expression, such as 'non-vampire creatures'
        or 'non-green'."""
        def __init__(self,operand):
                super().__init__(operand)
        
        def unparseToString(self):
                return "non-{0}".format(self._operand.unparseToString())
        
class MgWithExpression(MgUnaryOp):
        """This node represents a 'with' clause, as in 'target creature with power greater than 4'."""
        
        def __init__(self,operand):
                super().__init__(operand)
        
        def unparseToString(self):
                return "with {0}".format(self._operand.unparseToString())
                

class MgNamedExpression(MgUnaryOp):
        """This node represents a 'named' clause, as in 'creature token named 'Cloud Sprite''."""
        
        def __init__(self,operand):
                super().__init__(operand)
        
        def unparseToString(self):
                return "named {0}".format(self._operand.unparseToString())
        
class MgEffectExpression(MgAbstractExpression):
        """This is the parent class for all effect expressions, such as destroying things, creating tokens, or gaining life.
        It is not instantiated directly, but instead provides common functionalities for effects."""
        def __init__(self):
                super().__init__() #All effects are traversable by default.
                
                
class MgAddManaExpression(MgEffectExpression):
        """Represents an effect that adds mana."""
        def __init__(self,manaexpr,playerexpr=None):
                """
                manaexpr: Either a mana expression, value expression containing a mana expression, or a mana specification expression.
                playerexpr: An expression describing a player. Used in the case that the effect instructs a player to add mana.
                """
                super().__init__()
                self._manaexpr = manaexpr
                self._manaexpr.setParent(self)
                self._playerexpr = playerexpr
                if self._playerexpr is not None:
                        self._playerexpr.setParent(self)
        
        def isChild(self,child):
                return child is not None and child in {self._manaexpr,self._playerexpr}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._manaexpr,self._playerexpr} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._playerexpr is not None:
                        return "{0} adds {1}".format(self._playerexpr.unparseToString(),self._manaexpr.unparseToString())
                else:
                        return "add {0}".format(self._manaexpr.unparseToString())
        
        
                
                
class MgDealsDamageExpression(MgEffectExpression):
        """Represents an effect that deals damage, such as
        'Shock deals 2 damage to any target'
        'When this creature deals combat damage to a player'
        'Target creature you control deals damage equal to its power to each other creature and each opponent.'
        """
        
        class DealsDamageVariantEnum(Enum):
                VariantA = auto() #<origin> deals <damageExpression>? damage to <subject>?
                VariantB = auto() #<origin> deals damage <damageExpression> to <subject>
                VariantC = auto() #<origin> deals damage to <subject> <damageExpression>
        
        def __init__(self,origin,damageExpression=None,subject=None,variant=None):
                """
                origin: The entity dealing the damage
                damageExpression: An expression representing the amount of damage. Optional.
                subject: The entity receiving the damage. Optional.
                variant: An enum that indicates the order in which the card should be unparsed.
                By default it is variantA.
                """
                super().__init__()
                self._origin = origin
                self._origin.setParent(self)
                
                self._damageExpression = damageExpression
                if self._damageExpression is not None:
                        self._damageExpression.setParent(self)
                
                self._subject = subject
                if self._subject is not None:
                        self._subject.setParent(self)
                if variant is None:
                        self._variant = MgDealsDamageExpression.DealsDamageVariantEnum.VariantA
                else:
                        self._variant = variant
                
        def getOrigin(self):
                """Get the origin associated with this deals-damage expression."""
                return self._origin
                
        def setOrigin(self,origin):
                """Set the origin associated with this deals-damage expression."""
                self._origin = origin
                if self._origin is not None:
                        self._origin.setParent(self)
                
        def hasDamageExpression(self):
                """Checks whether this deals-damage expression has a damage expression."""
                return self._damageExpression is not None
                
        def getDamageExpression(self):
                """Get the damage expression associated with this deals-damage expression, if it exists."""
                return self._damageExpression
                
        def setDamageExpression(self,damageExpression):
                """Set the damage expression associated with this deals-damage expression"""
                self._damageExpression = damageExpression
                if self._damageExpression is not None:
                        self._damageExpression.setParent(self)
                        
        def hasSubject(self):
                """Checks whether this deals-damage expression has a subject."""
                return self._subject is not None
                
        def getSubject(self):
                """Get the subject associated with this deals-damage expression, if it exists."""
                return self._subject
                
        def setSubject(self,damageExpression):
                """Set the subject associated with this deals-damage expression"""
                self._subject = damageExpression
                if self._subject is not None:
                        self._subject.setParent(self)
                        
        def getVariant(self):
                """Gets the variant of damage dealing expression that this instance is."""
                return self._variant
                
        def setVariant(self,variant):
                """Sets the variant of damage dealing expression that this instance is."""
                self._variant = variant
                        
        def isChild(self,child):
                return child is not None and child in {self._origin,self._damageExpression,self._subject}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._origin,self._damageExpression,self._subject} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                output = "{0} deals".format(self._origin.unparseToString())
                if self._variant == MgDealsDamageExpression.DealsDamageVariantEnum.VariantA:
                        #<origin> deals <damageExpression>? damage to <subject>?
                        if self._damageExpression is not None:
                                output = output + " {0} damage".format(self._damageExpression.unparseToString())
                        if self._subject is not None:
                                output = output + " to {0}".format(self._subject.unparseToString())
                elif self._variant == MgDealsDamageExpression.DealsDamageVariantEnum.VariantB:
                        #<origin> deals damage <damageExpression> to <subject>
                        output = output + "damage {0} to {1}".format(self._damageExpression.unparseToString(),self._subject.unparseToString())
                else:
                        #<origin> deals damage to <subject> <damageExpression>
                        output = output + "damage to {1} {0}".format(self._damageExpression.unparseToString(),self._subject.unparseToString())
                return output
                                
                #if self._damageExpression is not None and self._damageQuantityAfter == True:
                #        output = output + " damage {0}".format(self._damageExpression.unparseToString())
                #elif self._damageExpression is not None:
                #        output = output + " {0} damage".format(self._damageExpression.unparseToString())
                #else:
                #        output = output + " damage"
                #if self._subject is not None:
                #        output = output + " to {0}".format(self._subject.unparseToString())
        
        
class MgDestroyExpression(MgEffectExpression):
        """Represents a destroy effect, as in 'destroy target non-white creature.'."""
        def __init__(self,subject):
                super().__init__()
                self._subject = subject
                self._subject.setParent(self)
                
        def getSubject(self):
                """Get the subject of the destroy effect."""
                return self._subject
                
        def setSubject(self,subject):
                """Set the subject of the destroy effect."""
                self._subject = subject
                self._subject.setParent(self)
                
        def isChild(self,child):
                return child is self._subject
                
        def getTraversalSuccessors(self):
                return [node for node in {self._subject} if node.isTraversable()]
                
        def unparseToString(self):
                return "destroy {0}".format(self._subject.unparseToString())
                
                
class MgSacrificeExpression(MgEffectExpression):
        """Represents a sacrifice effect, as in 'target player sacrifices a creature' or 'sacrifice a Goblin'."""
        def __init__(self,subject,controller=None):
                """
                subject: The thing being sacrificed.
                controller: (optional) An expression describing the person being forced to sacrifice something.
                """
                super().__init__()
                self._subject = subject
                self._subject.setParent(self)
                self._controller = controller
                if self._controller is not None:
                        self._controller.setParent(self)
                
        def getSubject(self):
                """Get the subject of the sacrifice effect."""
                return self._subject
                
        def setSubject(self,subject):
                """Set the subject of the sacrifice effect."""
                self._subject = subject
                self._subject.setParent(self)
                
        def getController(self):
                """Get the (optional) controller of the sacrifice effect."""
                return self._controller
                
        def setController(self,controller):
                """Set the (optional) controller of the sacrifice effect."""
                self._controller = controller
                if self._controller is not None:
                        self._controller.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in {self._subject,self._controller}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._subject,self._controller} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._controller is None:
                        return "sacrifice {0}".format(self._subject.unparseToString())
                else:
                        return "{0} sacrifices {1}".format(self._controller.unparseToString(),self._subject.unparseToString())

class MgExileExpression(MgEffectExpression):
        """Represents an exile effect, as in 'exile all enchantments'."""
        def __init__(self,subject):
                super().__init__()
                self._subject = subject
                self._subject.setParent(self)
                
        def getSubject(self):
                """Get the subject of the exile effect."""
                return self._subject
                
        def setSubject(self,subject):
                """Set the subject of the exile effect."""
                self._subject = subject
                self._subject.setParent(self)
                
        def isChild(self,child):
                return child is self._subject
                
        def getTraversalSuccessors(self):
                return [node for node in {self._subject} if node.isTraversable()]
                
        def unparseToString(self):
                return "exile {0}".format(self._subject.unparseToString())
                

class MgTapUntapExpression(MgEffectExpression):
        """Represents a tap or an untap effect, as in 'untap target permanent'.
        Note that if both flags for tap and untap or set, the effect reads as
        'tap or untap'"""
        def __init__(self,subject,tap=True,untap=False):
                super().__init__()
                self._subject = subject
                self._tap = tap
                self._untap = untap
                self._subject.setParent(self)
                
        def getSubject(self):
                """Get the subject of the tap/untap effect."""
                return self._subject
                
        def setSubject(self,subject):
                """Set the subject of the tap/untap effect."""
                self._subject = subject
                self._subject.setParent(self)
                
        def isTap(self):
                """Checks whether this effect taps the subject."""
                return self._tap
                
        def setTap(self,tap):
                """Changes whether this effect untaps the subject."""
                self._tap = tap
                
        def isUntap(self):
                """Checks whether this effect taps the subject."""
                return self._untap
                
        def setUntap(self,untap):
                """Changes whether this effect taps the subject."""
                self._untap = untap
                
        def isChild(self,child):
                return child is self._subject
                
        def getTraversalSuccessors(self):
                return [node for node in {self._subject} if node.isTraversable()]
                
        def unparseToString(self):
                if self._tap is True and self._untap is True:
                        return "tap or untap {0}".format(self._subject.unparseToString())
                elif self._untap is True:
                        return "untap {0}".format(self._subject.unparseToString())
                else:
                        #self._tap is True, or someone forgot to set a flag.
                        return "tap {0}".format(self._subject.unparseToString())
                        
class MgReturnExpression(MgEffectExpression):
        """Represents a return effect, as in 'return target creature to its owners hand'."""
        def __init__(self,subject,destination,origin=None):
                """
                subject: The recipient of the return effect.
                origin: An optional expression detailing where the subject is coming from.
                destination: An expression detailing where the subject is going.
                """
                super().__init__()
                self._subject = subject
                self._destination = destination
                self._origin = origin
                if self._origin is not None:
                        self._origin.setParent(self)
                self._subject.setParent(self)
                self._destination.setParent(self)
                
        def getSubject(self):
                """Get the subject of the return effect."""
                return self._subject
                
        def setSubject(self,subject):
                """Set the subject of the return effect."""
                self._subject = subject
                self._subject.setParent(self)
                
        def getDestination(self):
                """Get the subject of the return effect."""
                return self._destination
                
        def setDestination(self,subject):
                """Set the subject of the return effect."""
                self._destination = destination
                self._destination.setParent(self)
                
        def isChild(self,child):
                return child is self._subject
                
        def getTraversalSuccessors(self):
                return [node for node in {self._subject,self._destination} if node.isTraversable()]
                
        def unparseToString(self):
                return "return {0} to {1}".format(self._subject.unparseToString(),self._destination.unparseToString())
                     
class MgUncastExpression(MgEffectExpression):
        """Represents an counterspell effect, as in 'counter target non-creature spell'.
        Internally we call this an 'uncast' effect so as to avoid confusion with counters
        in the sense of +1/+1 counters.
        """
        def __init__(self,subject):
                super().__init__()
                self._subject = subject
                self._subject.setParent(self)
                
        def getSubject(self):
                """Get the subject of the uncast effect."""
                return self._subject
                
        def setSubject(self,subject):
                """Set the subject of the uncast effect."""
                self._subject = subject
                self._subject.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in {self._subject}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._subject} if node.isTraversable()]
                
        def unparseToString(self):
                return "counter {0}".format(self._subject.unparseToString())

class MgGainLoseExpression(MgEffectExpression):
        """Represents the act of gaining or losing something, like 'target creature gains flying until end of turn'
        or 'you lose three life'."""
        def __init__(self,subject):
                pass
                
        
class MgAddRemoveExpression(MgEffectExpression):
        """Represents adding or removing something from something else, like 'remove X storage counters from Mage Ring Network'."""
        pass
        
class MgCreateTokenExpression(MgEffectExpression):
        def __init__(self,descriptor,quantity=None):
                 """quantity: A term/expression denoting how many tokens are made. If quantity is None, it is assumed only one token
                 is made.
                 descriptor: A description expression node."""
                 super().__init__()
                 self._quantity =  quantity
                 self._descriptor = descriptor
                 if self._quantity is not None:
                         self._quantity.setParent(self)
                 self._descriptor.setParent(self)
        
        def getQuantity(self):
                return self._quantity
                
        def setQuantity(self,quantity):
                self._quantity = quantity
                if self._quantity is not None:
                        self._quantity.setParent(self)
        
        def getDescriptor(self):
                return self._descriptor
                
        def setDescriptor(self,descriptor):
                self._descriptor = descriptor 
                self._descriptor.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in {self._descriptor,self._quantity}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._descriptor,self._quantity} if node is not None and node.isTraversable()] 
                 
        def unparseToString(self):
                if self._quantity is None:
                        return "create {0}".format(self._descriptor.unparseToString())
                else:
                        return "create {0} {1}".format(self._quantity.unparseToString(),self._descriptor.unparseToString())
                        
class MgCardDrawExpression(MgEffectExpression):
        """Represents a card draw effect, like 'draw a card', 'draw three cards', or
        'draw a card for each creature your opponents control'."""
        def __init__(self,quantity):
                """
                quantity: A term or expression indicating how many cards to draw.
                """
                super().__init__()
                self._quantity = quantity
                self._quantity.setParent(self)
        
        def getQuantity(self):
                """Get the expression for the number of cards to draw."""
                return self._quantity
                
        def setQuantity(self,quantity):
                """Set the expression for the number of cards to draw."""
                self._quantity = quantity
                self._quantity.setParent(self)
              
        def isChild(self,child):
                return child is not None and child in {self._quantity}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._quantity} if node.isTraversable()]
                
        def unparseToString(self):
                if isinstance(self._quantity,MgNumberValue) and self._quantity.getValue() == 1:
                        return "draw a card"
                elif isinstance(self._quantity,MgValueExpression):
                        return "draw {0} cards".format(self._quantity.unparseToString())
                else:
                        return "draw a card for {0}".format(self._quantity.unparseToString())
        

class MgSearchLibraryExpression(MgEffectExpression):
        def __init__(self,owner,subject):
                """
                owner: A possessive expression referencing the person who owns the library.
                subject: An expression describing the thing(s) being searched for.
                """
                super().__init__()
                self._owner = owner
                self._subject = subject
                self._owner.setParent(self)
                self._subject.setParent(self)
                
        def getLibraryOwner(self):
                """Get the reference to the owner of the library."""
                return self._owner
                
        def setLibraryOwner(self,owner):
                """Set the reference to the owner of the library."""
                self._owner = owner
                self._owner.setParent(self)
                
        def getSubject(self):
                """Get the subject, the expression that describes the thing(s) being searched for."""
                return self._subject
                
        def setSubject(self,subject):
                """Set the subject, the expression that describes the thing(s) being searched for."""
                self._subject = subject
                self._subject.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in {self._owner,self._subject}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._owner,self._subject} if node.isTraversable()]
                
        def unparseToString(self):
                return "search {0} library for {1}".format(self._owner.unparseToString(),self._subject.unparseToString())
                
        
class MgShuffleLibraryExpression(MgEffectExpression):
        def __init__(self,owner):
                """
                owner: A possessive expression referencing the person who owns the library.
                """
                super().__init__()
                self._owner = owner
                self._owner.setParent(self)
                
        def getLibraryOwner(self):
                """Get the reference to the owner of the library."""
                return self._owner
                
        def setLibraryOwner(self,owner):
                """Set the reference to the owner of the library."""
                self._owner = owner
                self._owner.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in {self._owner}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._owner} if node.isTraversable()]
                
        def unparseToString(self):
                return "shuffle {0} library"
                
                
def MgPutInZoneExpression(MgEffectExpression):
        def __init__(self,subject,zone,conditions=None):
                """
                subject: An expression describing the thing that is being put somewhere.
                zone: An expression describing the zone where the object is being placed. 
                conditions: An expresssion that describes conditions under which the object
                is placed in the zone, such as 'tapped and attacking'.
                
                Examples:
                'put that card onto the battlefield tapped'
                'put all other cards revealed this way into your graveyard'
                """
                self._subject = subject
                self._zone = zone
                self._conditions = conditions
                self._subject.setParent(self)
                self._zone.setParent(self)
                if self._conditions is not None:
                        self._conditions.setParent(self)
                        
                def getSubject(self):
                        """Get the subject, the expression that describes the thing(s) being put somewhere."""
                        return self._subject
                
                def setSubject(self,subject):
                        """Set the subject, the expression that describes the thing(s) being put somewhere."""
                        self._subject = subject
                        self._subject.setParent(self)
                        
                def getZone(self):
                        """Get the zone where the subject is going."""
                        return self._zone
                
                def setZone(self,zone):
                        """Set the zone where the subject is going."""
                        self._zone = zone
                        self._zone.setParent(self)
                
                def getConditions(self):
                        """Get the conditions expression, if one exists, that describes the circumstances under which
                        the subject is being placed in the zone."""
                        return self._conditions
                
                def setConditions(self,conditions):
                        """Get the conditions expression that describes the circumstances under which
                        the subject is being placed in the zone."""
                        self._conditions = conditions
                        self._conditions.setParent(self)
                        
                def isChild(self,child):
                        return child is not None and child in {self._subject,self._zone,self._conditions}
                
                def getTraversalSuccessors(self):
                        return [node for node in {self._subject,self._zone,self._conditions} if node.isTraversable()]
                
                def unparseToString(self):
                        #Note: the unparser will have to use into for zones like the hand and onto for zones like the battlefield.
                        if self._conditions is not None:
                                return "put {0} into {1} {2}".format(self._subject.unparseToString(),self._zone.unparseToString(),self._conditions.unparseToString())
                        else:
                                return "put {0} into {1}".format(self._subject.unparseToString(),self._zone.unparseToString())
                
        
        
class MgRevealExpression(MgEffectExpression):
        pass
        
                
                
        
        

                
                
        