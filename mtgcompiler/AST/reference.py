import mtgcompiler.AST.core as core

class MgName(core.MgNode):
    """This node represents a name, such as the name of a card."""
    pass
    
class MgTurnStep(core.MgNode):
    """This node represents a point in time in a turn, such as 
    the first Main phase or the cleanup step."""
    pass
    
class MgZone(core.MgNode):
    """This node represents a zone in the game, such as
    the battlefield, graveyard, or the command zone."""
    pass