import mtgcompiler.AST.core as core

class MgName(core.MgNode):
        """This node represents a name, such as the name of a card."""
        def __init__(self,name=""):
                """name: a string containing a name."""
                self._traversable = True
                self._name = name
        
        def getName(self):
                return self._name
                
        def setName(self,name):
                self._name = name
        
        def isChild(self,child):
                return False
                
        def getTraversalSuccessors(self):
                return []
                
        def unparseToString(self):
                return self._name
    
class MgTurnStep(core.MgNode):
    """This node represents a point in time in a turn, such as 
    the first Main phase or the cleanup step."""
    pass
    
class MgZone(core.MgNode):
    """This node represents a zone in the game, such as
    the battlefield, graveyard, or the command zone."""
    pass