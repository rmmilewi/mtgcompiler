import core,abc

class MgAbstractExpression(core.MgNode):
        """This is the parent class for all expressions such as power/toughness, 
        types, and mana costs. This class is not instantiated, but provides common
        functionalities for all of these kinds of expressions."""
        pass
        #@abc.abstractmethod
        #def getValues():
        #        """Get all the child values"""
        #        raise NotImplemented
    
class MgManaExpression(MgAbstractExpression):
        """This node represents mana expressions, sequences of 
        mana symbols."""
        pass
    
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
                self._tlist = args
                self._traversable = True
        
        def isChild(self,child):
                return child in self._tlist
        
        def getTraversalSuccessors(self):
                return [t for t in self._tlist if t.isTraversable()]
                
        def unparseToString(self):
                """This method unparses the (sub|super)*types in the order given by the list, which
                may or may not be the canonical order of supertypes -> types -> subtypes."""
                return ' '.join(t.unparseToString() for t in self._tlist)
                
                
                
        