import mtgcompiler.AST.core as core
import abc
from enum import Enum

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
        """
        
        class NumberTypeEnum(Enum):
                """Indicates how the number value should be unparsed."""
                Literal = auto() #1, 2, 3
                Quantity = auto() #one, two, three
                Frequency = auto() #once, twice, three times
        
        def __init__(self,value,ntype=MgNumberValue.NumberTypeEnum.Literal):
                self._traversable = True
                self._value = value
                self._ntype = ntype
        
        def isLiteral(self):
                """Checks if the number type is a literal."""
                return self._ntype == MgNumberValue.NumberType.Literal
                
        def setLiteral(self):
                """Makes the number type a literal."""
                self._ntype = MgNumberValue.NumberType.Literal
                
        def isQuantity(self):
                """Checks if the number type is a quantity."""
                return self._ntype == MgNumberValue.NumberType.Quantity
                
        def setQuantity(self):
                """Makes the number type a quantity."""
                self._ntype = MgNumberValue.NumberType.Quantity
                
        def isFrequency(self):
                """Checks if the number type is a frequency."""
                return self._ntype == MgNumberValue.NumberType.Frequency
                
        def setFrequency(self):
                """Makes the number type a frequency."""
                self._ntype = MgNumberValue.NumberType.Frequency
                
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
                if self._ntype == MgNumberValue.NumberType.Literal:
                        return str(self._value)
                
                if self._ntype == MgNumberValue.NumberType.Frequency and self._value == 1:
                        return "once"
                if self._ntype == MgNumberValue.NumberType.Frequency and self._value == 2:
                        return "twice"
                            
                quantity = ""
                
                #Conversion scheme here lovingly borrowed from kamyu104/LeetCode
                
                lookup = {0: "zero", 1:"one", 2: "two", 3: "three", 4: "four", \
                          5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", \
                          10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", \
                          15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", \
                          20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", \
                          70: "seventy", 80: "eighty", 90: "ninety"}
                unit = ["", "thousand", "million", "billion"]
                          
                def threeDigits(self, num, lookup, unit):
                    res = []
                    if num / 100:
                        res = [lookup[num / 100] + " " + "hundred"]
                    if num % 100:
                        res.append(self.twoDigits(num % 100, lookup))
                    if unit != "":
                        res.append(unit)
                    return " ".join(res)

                def twoDigits(self, num, lookup):
                    if num in lookup:
                        return lookup[num]
                    return lookup[(num / 10) * 10] + " " + lookup[num % 10]
                    
                if num == 0:
                        quantity = lookup[0]
                else:
                        res, i = [], 0
                        while num:
                                cur = num % 1000
                                if num % 1000:
                                        res.append(self.threeDigits(cur, lookup, unit[i]))
                                num //= 1000
                                i += 1
                        quantity = " ".join(res[::-1])
                
                if self._ntype == MgNumberValue.NumberType.Quantity:
                        return quantity
                elif self._ntype == MgNumberValue.NumberType.Frequency:
                        return "{0} times".format(quantity)
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
    
class MgPTExpression(MgAbstractExpression):
        """This node represents power/toughness expressions
        such as 5/5, */*, or X/X."""
        def __init__(self,power,toughness):
                self._traversable = True
                self._power = power
                self._toughness = toughness
        
        def getPower(self):
                return self._power
        
        def setPower(self,power):
                self._power = power
        
        def getToughness(self):
                return self._toughness
        
        def setToughness(self,toughness):
                return self._toughness
                
        def isChild(self,child):
                return child in {self._power,self._toughness}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._power,self._toughness} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                return "{0}/{1}".format(self._power.unparseToString(),self._toughness.unparseToString)
    
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
                self._plural = False
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
                
        def isPlural(self):
                """If the plural flag is set, then the type expression will be unparsed as plural
                (e.g. 'artifact creatures' vs. 'artifact creature'). TODO: This may be subject to change."""
                return self._plural
                
        def setPlural(self,plural):
                """Changes the plural flag. TODO: This may be subject to change."""
                self._plural = plural
                
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
                if self._plural is True:
                        return result+'s'
                else:
                        return result
                        
class MgCommaExpression(MgAbstractExpression):
        """This node represents a series of terms/expressions separated by a comma. 
        'one, two, or three target creatures with flying' in Aerial Volley. This expression can
        optionally be terminated with an 'and' or 'or'"""
        pass
        
        
class MgModalExpression(MgAbstractExpression):
        """This node represents a series of modal choices, as is seen in cards like Abzan Charm or
        Citadel Siege"""
        pass
        
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
        """A choice expression is used whenever card text involves the word 'choose'.
        For example, 'choose a color' or 'choose two:[...]'."""

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
        pass
                     
class MgCounterExpression(MgEffectExpression):
        """Represents an counterspell effect, as in 'counter target non-creature spell'."""
        pass

class MgGainLoseExpression(MgEffectExpression):
        """Represents the act of gaining or losing something, like 'target creature gains flying until end of turn'
        or 'you lose three life'."""
        def __init__(self,subject):
                pass
                
        
class MgAddRemoveExpression(MgEffectExpressions):
        """Represents adding or removing something from something else, like 'remove X storage counters from Mage Ring Network'."""
        pass
        
class MgTokenDescriptor(MgAbstractExpression):
        """Represents the description of a token."""
        pass

class MgCreateTokenExpression(MgEffectExpression):
        def __init__(self,descriptor,quantity=None):
                 """quantity: A term/expression denoting how many tokens are made. If quantity is None, it is assumed only one token
                 is made.
                 descriptor: A token descriptor node."""
                 self._quantity =  quantity
                 self._descriptor = descriptor
        
        def getQuantity(self):
                return self._quantity
                
        def setQuantity(self,quantity):
                self._quantity = quantity
        
        def getDescriptor(self):
                return self._descriptor
                
        def setDescriptor(self):
                return 
                 
        def unparseToString(self):
                if self._quantity is None:
                        return "create a {0}".format(self._descriptor.unparseToString())
                else:
                        return "create {0} {1}".format(self._quantity.unparseToString(),self._descriptor.unparseToString())

class MgSearchLibraryExpression(MgEffectExpression):
        pass
        
class MgShuffleLibraryExpression(MgEffectExpression):
        pass
        
                
                
        
        

                
                
        