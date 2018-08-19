import mtgcompiler.AST.core as core
import abc

class MgAbstractExpression(core.MgNode):
        """This is the parent class for all expressions such as power/toughness, 
        types, and mana costs. This class is not instantiated, but provides common
        functionalities for all of these kinds of expressions."""
        pass
    
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
        pass
    
class MgColorExpression(MgAbstractExpression):
        """This node represents color expressions, such as
        'White' or 'Red and Green'."""
        pass
         
class MgTypeExpression(MgAbstractExpression):
        """A type expression is a sequence of subtypes,types, or
        supertypes. For example, Snow Artifact or Human Cleric."""
        
        def __init__(self,*args):
                """The constructor accepts a list of (sub|super)*types in any order."""
                self._traversable = True
                self._tlist = args
                for t in self._tlist:
                        t.setParent(self)

        def isChild(self,child):
                return child in self._tlist
        
        def getTraversalSuccessors(self):
                return [t for t in self._tlist if t.isTraversable()]
                
        def addType(self,t):
                self._tlist.append(t)
                t.setParent(self)
                
        def unparseToString(self):
                """This method unparses the (sub|super)*types in the order given by the list, which
                may or may not be the canonical order of supertypes -> types -> subtypes."""
                return ' '.join(t.unparseToString() for t in self._tlist)
                
                
class MgTargetExpression(MgAbstractExpression):
        """A target expression is used whenever card text involves the word 'target'.
        For example, 'destroy target creature' or 'target player gains 5 life.'"""
        pass
        
class MgEachExpression(MgAbstractExpression):
        """An each expression is used whenever card text involves the word 'each'.
        For example, 'each player draws a card'."""
        pass
        
class MgChoiceExpression(MgAbstractExpression):
        """A choice expression is used whenever card text involves the word 'choose'.
        For example, 'choose a color' or 'choose two:[...]'."""
        pass
                
                
        