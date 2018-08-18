import mtgcompiler.AST.core as core
import mtgcompiler.AST.expressions as expressions

class MgFlavorText(core.MgNode):
        """This node holds the flavor text for a card."""
        pass

class MgTextBox(core.MgNode):
        """This node represents a text box, the most substantial
        part of most Magic cards."""
        pass

class MgTypeLine(core.MgNode):
        """The type line is the middle part of a Magic card
        that lists the supertypes, types, and subtypes of that card."""
        
        def __init__(self):
                """Default constructor for an empty type line."""
                self._traversable = True
                self._supertypes = expressions.MgTypeExpression()
                self._supertypes.setParent(self)
                self._types = expressions.MgTypeExpression()
                self._types.setParent(self)
                self._subtypes = expressions.MgTypeExpression()
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
        interacting with all aspects of a Magic card."""
        pass