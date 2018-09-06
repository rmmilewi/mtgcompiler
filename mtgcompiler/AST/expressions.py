import mtgcompiler.AST.core as core
import abc
from enum import Enum,auto
from num2words import num2words

class MgAbstractExpression(core.MgNode):
        """This is the parent class for all expressions such as power/toughness, 
        types, and mana costs. This class is not instantiated, but provides common
        functionalities for all of these kinds of expressions."""
        pass
        
        
class MgValueExpression(MgAbstractExpression):
        """An uninstantiated parent class for value expressions, such as... 
                - '1+*' in '1+*/1+*'
                - 'six' in 'destroy six target creatures'
                - 'twice X' in 'you gain twice X life'
        """
        pass

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
                Quantity = auto() #one, two, three
                Frequency = auto() #once, twice, three times
                Ordinal = auto() #first, second, third
                Custom = auto() #*,1+*
        
        def __init__(self,value,ntype):
                self._traversable = True
                self._value = value
                self._ntype = ntype
        
        def isLiteral(self):
                """Checks if the number type is a literal."""
                return self._ntype == MgNumberValue.NumberTypeEnum.Literal
                
        def setLiteral(self):
                """Makes the number type a literal."""
                self._ntype = MgNumberValue.NumberTypeEnum.Literal
                
        def isQuantity(self):
                """Checks if the number type is a quantity."""
                return self._ntype == MgNumberValue.NumberTypeEnum.Quantity
                
        def setQuantity(self):
                """Makes the number type a quantity."""
                self._ntype = MgNumberValue.NumberTypeEnum.Quantity
                
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
                            
                if self._ntype == MgNumberValue.NumberTypeEnum.Quantity or self._ntype == MgNumberValue.NumberTypeEnum.Frequency:
                        quantityRepresentation = num2words(self._value)
                        if self._ntype == MgNumberValue.NumberTypeEnum.Quantity:
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
                self._traversable = True
                self._symlist = args
                for sym in self._symlist:
                        sym.setParent(self)
                        
        def isChild(self,child):
                return child in self._symlist
        
        def getTraversalSuccessors(self):
                return [sym for sym in self._symlist if sym.isTraversable()]
                
        def unparseToString(self):
                """This method unparses the mana symbols in the order given by the list, which
                may or may not be the canonical order."""
                return ''.join(sym.unparseToString() for sym in self._symlist)

        def addManaSymbol(self,sym):
                self._symlist.append(sym)
                sym.setParent(self)
                
                
                
class MgDashCostExpression(core.MgNode):
        """Sometimes a cost of a keyword ability is more than, say, just a simple mana expression.
        For example, in Braid of Fire, we see 'Cumulative upkeep—Add {R}.' In these situations,
        we use a dash cost expression that decorates the underlying expression.
        """
        pass 


class MgDescriptionExpression(core.MgNode):
        """A description expression is a sequence of sub-expressions/terms that describe some object.
        For example, in 'destroy target non-black creature', 'non-black' is in a MgColorExpression
        and 'creature' is in an MgTypeExpression. The description expression strings these together.
        """
        def __init__(self,*args):
                """The constructor accepts a list of descriptors in any order."""
                self._traversable = True
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
                self._traversable = True
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
                self._traversable = True
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
                self._traversable = True
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
                
        #def isPlural(self):
        #        """If the plural flag is set, then the type expression will be unparsed as plural
        #        (e.g. 'artifact creatures' vs. 'artifact creature'). TODO: This may be subject to change."""
        #        return self._plural
                
        #def setPlural(self,plural):
        #        """Changes the plural flag. TODO: This may be subject to change."""
        #        self._plural = plural
                
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
                self._traversable = True
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
                self._traversable = True
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
                
        
                        
class MgCommaExpression(MgAbstractExpression):
        """This node represents a series of terms/expressions separated by a comma. 
        'one, two, or three target creatures with flying' in Aerial Volley. This expression can
        optionally be terminated with an 'and' or 'or'"""
        pass
        
        
class MgModalExpression(MgAbstractExpression):
        """This node represents a series of modal choices, as is seen in cards like Abzan Charm or
        Citadel Siege. TODO: numberOfChoices is going to be replaced a by a 'choose' subexpression."""
        def __init__(self,numberOfChoices,*options):
                """
                numberOfChoices: The number of times that the caster can choose different modes for the spell/ability.
                options: A list containing the different modes of the spell/ability.
                """
                self._traversable = True
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
                
def MgEntersLeavesBattlefieldExpression(MgAbstractExpression):
        """Represents the notion of entering or leaving the battlefield.
        Takes the form of '____ enters the battlefield' or '____ leaves the battlefield.'
        """
        
        def __init__(self,subject,entering=True):
                """
                subject: The thing that is entering or leaving the battlefield.
                entering: is the subject entering the battlefield?
                """
                self._subject = subject
                self._entering = entering
                self._subject.setParent(this)
                
        def isEntering(self):
                """Check whether the subject is entering the battlefield."""
                return self._entering == True
                
        def setEntering(self):
                """Make it so that the subject is entering the battlefield."""
                self._entering = True
                
        def isLeaving(self):
                """Check whether the subject is leaving the battlefield."""
                return self._entering == False
                
        def setLeaving(self):
                """Make it so that the subject is leaving the battlefield."""
                self._entering = False
                
        def isChild(self,child):
                return child in self._subject
        
        def getTraversalSuccessors(self):
                return [node for node in {self._subject} if node.isTraversable()]
                
        def unparseToString(self):
                if self._entering is True:
                        return "{0} enters the battlefield".format(self._subject.unparseToString())
                else:
                        return "{0} leaves the battlefield".format(self._subject.unparseToString())
                 
        
        
class MgBinaryOp(MgAbstractExpression):
        """An uninstantiated parent class for all binary operators, namely logical operators like 'and', 'or', etc."""
        def __init__(self,lhs,rhs):
                """
                lhs: left-hand side of the operator.
                rhs: right-hand side of the operator.
                """
                self._traversable = True #All binary operators are traversable by default.
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

class MgUnaryOp(MgAbstractExpression):
        """An uninstantiated parent class for all unary operators, like 'target X' or 'non-Y'."""
        def __init__(self,operand):
                self._traversable = True #All unary operators are traversable by default.
                self._operand = operand
                self._operand.setParent(self)
                
        def getOperand(self):
                return self._operand
                
        def setOperand(self,operand):
                self._operand = operand
                operand.setParent(self)
                
        def isChild(self,child):
                return child is self._operand
                
        def getTraversalSuccessors(self):
                return [node for node in {self._operand} if node.isTraversable()]
                
class MgTargetExpression(MgUnaryOp):
        """A target expression is used whenever card text involves the word 'target'.
        For example, 'destroy target creature' or 'target player gains 5 life.'"""
        
        def __init__(self,operand):
                super().__init__(operand)
        
        def unparseToString(self):
                return "target {0}".format(self._operand.unparseToString())
                
                
class MgUntilExpression(MgUnaryOp):
        """An until expression is used whenever card text says that an effect happens until
        a condition is met, like 'until end of turn' or 'until THIS leaves the battlefield'"""
        def __init__(self,operand):
                super().__init__(operand)
                
        def unparseToString(self):
                return "until {0}".format(self._operand.unparseToString())
                        
                
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
        
class MgChoiceExpression(MgUnaryOp):
        """A choice expression is used whenever card text involve a non-modal choice.
        For example, 'choose a color'."""

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
                self._traversable = True #All effects are traversable by default.
                
        
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
                return child is self._subject
                
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
                 self._quantity.setParent(self)
                 self._descriptor.setParent(self)
        
        def getQuantity(self):
                return self._quantity
                
        def setQuantity(self,quantity):
                self._quantity = quantity
                self._quantity.setParent(self)
        
        def getDescriptor(self):
                return self._descriptor
                
        def setDescriptor(self,descriptor):
                self._descriptor = descriptor 
                self._descriptor.setParent(self)
                 
        def unparseToString(self):
                if self._quantity is None:
                        return "create a {0}".format(self._descriptor.unparseToString())
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
                return child is self._quantity
                
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
        pass
        
class MgShuffleLibraryExpression(MgEffectExpression):
        pass
        
class MgRevealExpression(MgEffectExpression):
        pass
        
                
                
        
        

                
                
        